# -*- coding: utf-8 -*-
# LipidGenesis MVP v7.1 — Suporte a perfis reais de ácidos graxos (CSV/XLSX)
# Autor: OGTera (Gabriel) + ChatGPT
#
# Novidades v7.1:
# - Upload (CSV/XLSX) de perfis reais de ácidos graxos
# - Validação dos dados (soma ≈ 100% ±2; colunas obrigatórias)
# - Seleção de óleo por nome/ID e uso direto de II/ISap/PF se existirem no dataset
# - Estimativas de II/ISap a partir do perfil FA caso valores não venham no arquivo (aproximações padrão de literatura)
# - Fallback para heurísticas internas quando não houver dados
#
# Observação: estimativas de II/ISap são aproximações para MVP. Calibre com literatura e dados laboratoriais.

import os
import io
import json
from datetime import datetime
from typing import Dict, List

import numpy as np
import pandas as pd
import streamlit as st

# PDF (ReportLab)
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib import colors

st.set_page_config(page_title="LipidGenesis — MVP v7.1", page_icon="💧", layout="wide")

# =============================
# --------- CONSTANTES --------
# =============================

# Heurísticas internas (fallback)
FATS = {
    "PFAD": {"II": 50, "ISap": 195, "PFusao": 38},
    "RBD (Palma)": {"II": 52, "ISap": 196, "PFusao": 35},
    "PKO (Palm Kernel Oil)": {"II": 17, "ISap": 248, "PFusao": 24},
}

ESSENCIAS = [
        {"emoji": "🌰", "nome": "Cumaru (Tonka)",      "acorde": "baunilha-amêndoa",   "família": "oriental",   "nota": "fundo"},
        {"emoji": "🔥", "nome": "Breu-branco",         "acorde": "resinoso-limpo",     "família": "balsâmico",  "nota": "coração"},
        {"emoji": "🌿", "nome": "Priprioca",           "acorde": "terroso-amadeirado", "família": "amadeirado", "nota": "coração"},
        {"emoji": "🌳", "nome": "Copaíba",             "acorde": "amadeirado-resinoso","família": "amadeirado", "nota": "fundo"},
        {"emoji": "🍂", "nome": "Patchouli Amazônico", "acorde": "terroso-úmido",      "família": "chipre",     "nota": "fundo"},
        {"emoji": "🌸", "nome": "Pau-rosa (Rosewood)", "acorde": "floral-amadeirado",  "família": "floral",     "nota": "coração"},
    ]

# Constantes para estimar II a partir de FA (%), usando fatores aproximados (Wij's)
IV_FACTORS = {
    "FA_C16:1": 0.95, "FA_C18:1": 0.86, "FA_C20:1": 0.785, "FA_C22:1": 0.723,
    "FA_C18:2": 1.732, "FA_C18:3": 2.616
}

# Massas molares aproximadas para SV (g/mol) por classe FA
FA_MW = {
    "FA_C8:0": 144.21, "FA_C10:0": 172.26, "FA_C12:0": 200.32, "FA_C14:0": 228.37,
    "FA_C16:0": 256.42, "FA_C18:0": 284.48, "FA_C20:0": 312.53, "FA_C22:0": 340.58, "FA_C24:0": 368.64,
    "FA_C16:1": 254.41, "FA_C18:1": 282.46, "FA_C20:1": 310.52, "FA_C22:1": 338.57,
    "FA_C18:2": 280.45, "FA_C18:3": 278.43, "FA_C20:2": 308.50, "FA_C20:4": 304.47
}

REQUIRED_FA_COLS = [
    "FA_C12:0","FA_C14:0","FA_C16:0","FA_C18:0","FA_C18:1","FA_C18:2"
]

# =============================
# --------- FUNÇÕES -----------
# =============================

def normaliza_blend(pfad, rbd, pko):
    soma = pfad + rbd + pko
    if soma == 0:
        return 0, 0, 0, soma
    pfad_n = round(100 * pfad / soma, 2)
    rbd_n = round(100 * rbd / soma, 2)
    pko_n = round(100 * pko / soma, 2)
    return pfad_n, rbd_n, pko_n, soma

def props_blend(pfad_pct, rbd_pct, pko_pct, props_map: Dict[str, Dict[str, float]]):
    # média ponderada de II/ISap/PFusao usando mapa de propriedades atual (dataset real se existir, senão heurística)
    def val(f, key):
        return f.get(key) if f and f.get(key) is not None else np.nan

    oils = ["PFAD", "RBD (Palma)", "PKO (Palm Kernel Oil)"]
    pcts = [pfad_pct, rbd_pct, pko_pct]
    II_vals, ISap_vals, PF_vals, weights = [], [], [], []
    for oil, pct in zip(oils, pcts):
        f = props_map.get(oil, {})
        II_vals.append(val(f, "II"))
        ISap_vals.append(val(f, "ISap"))
        PF_vals.append(val(f, "PFusao"))
        weights.append(pct)

    # Se algum valor faltar, usa fallback FATS
    for i, oil in enumerate(oils):
        if np.isnan(II_vals[i]): II_vals[i] = FATS.get(oil, {}).get("II", np.nan)
        if np.isnan(ISap_vals[i]): ISap_vals[i] = FATS.get(oil, {}).get("ISap", np.nan)
        if np.isnan(PF_vals[i]): PF_vals[i] = FATS.get(oil, {}).get("PFusao", np.nan)

    II = round(np.nansum(np.array(II_vals)*np.array(weights)) / 100, 2)
    ISap = round(np.nansum(np.array(ISap_vals)*np.array(weights)) / 100, 2)
    PFusao = round(np.nansum(np.array(PF_vals)*np.array(weights)) / 100, 2)
    return II, ISap, PFusao

def heuristica_por_ocasião(ocasião):
    base = {"toque":5, "hidr":5, "estab":5, "brilho":5}
    blend = {"PFAD": 30, "RBD (Palma)": 40, "PKO (Palm Kernel Oil)": 30}
    if ocasião == "Mãos":
        base = {"toque":8, "hidr":6, "estab":7, "brilho":4}
        blend = {"PFAD": 20, "RBD (Palma)": 45, "PKO (Palm Kernel Oil)": 35}
    elif ocasião == "Corpo":
        base = {"toque":6, "hidr":8, "estab":7, "brilho":5}
        blend = {"PFAD": 35, "RBD (Palma)": 45, "PKO (Palm Kernel Oil)": 20}
    elif ocasião == "Rosto":
        base = {"toque":8, "hidr":7, "estab":7, "brilho":3}
        blend = {"PFAD": 25, "RBD (Palma)": 55, "PKO (Palm Kernel Oil)": 20}
    elif ocasião == "Cabelos":
        base = {"toque":6, "hidr":7, "estab":6, "brilho":8}
        blend = {"PFAD": 15, "RBD (Palma)": 35, "PKO (Palm Kernel Oil)": 50}
    return base, blend

def estimate_iv_from_fa(row: pd.Series) -> float:
    iv = 0.0
    for col, k in IV_FACTORS.items():
        iv += float(row.get(col, 0) or 0) * k
    return round(iv, 2)

def estimate_sv_from_fa(row: pd.Series) -> float:
    # SV ≈ 560 / MW_médio, onde MW_médio é a média ponderada pelos % dos FA presentes
    total = 0.0
    denom = 0.0
    for col, mw in FA_MW.items():
        pct = float(row.get(col, 0) or 0)
        total += pct
        denom += pct / mw if mw else 0
    if denom <= 0:
        return np.nan
    avg_mw = total / denom
    return round(560.0 / avg_mw, 2)

def load_dataset(file) -> pd.DataFrame:
    if file.name.lower().endswith(".csv"):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)
    # Normaliza nomes de colunas
    df.columns = [c.strip() for c in df.columns]
    return df

def validate_dataset(df: pd.DataFrame) -> List[str]:
    msgs = []
    # Verifica colunas essenciais (pelo menos algumas FA)
    missing = [c for c in REQUIRED_FA_COLS if c not in df.columns]
    if missing:
        msgs.append(f"Colunas de FA ausentes: {missing}")
    # Verifica soma de FA quando possível
    fa_cols = [c for c in df.columns if c.startswith("FA_")]
    if fa_cols:
        fa_sum = df[fa_cols].fillna(0).sum(axis=1)
        out = df.index[(fa_sum < 98) | (fa_sum > 102)].tolist()
        if len(out):
            msgs.append(f"Soma FA fora do intervalo 100%±2 em {len(out)} amostras (linhas: {out[:5]}{'...' if len(out)>5 else ''})")
    # Verifica identificação
    if ("Oil_Name" not in df.columns) and ("Oil_ID" not in df.columns):
        msgs.append("Inclua ao menos uma coluna identificadora: 'Oil_Name' ou 'Oil_ID'.")
    return msgs

def build_props_map(df: pd.DataFrame) -> Dict[str, Dict[str, float]]:
    # Esta função procura por entradas de PFAD, RBD (Palma) e PKO no dataset, usando Oil_Name ou Oil_ID
    props = {}
    def pick(oil_key, candidates):
        # tenta encontrar por Oil_Name que contenha um dos candidates
        mask = pd.Series(False, index=df.index)
        if "Oil_Name" in df.columns:
            for c in candidates:
                mask = mask | df["Oil_Name"].astype(str).str.contains(c, case=False, na=False)
        if not mask.any() and "Oil_ID" in df.columns:
            for c in candidates:
                mask = mask | df["Oil_ID"].astype(str).str.contains(c, case=False, na=False)
        if mask.any():
            row = df[mask].iloc[0]
            II = row.get("IodineValue_Wijs", np.nan)
            ISap = row.get("SaponificationValue_mgKOH_g", np.nan)
            PF = row.get("MeltingPoint_C", np.nan)
            # Estima se ausente
            if pd.isna(II): II = estimate_iv_from_fa(row)
            if pd.isna(ISap): ISap = estimate_sv_from_fa(row)
            props[oil_key] = {"II": float(II) if not pd.isna(II) else None,
                              "ISap": float(ISap) if not pd.isna(ISap) else None,
                              "PFusao": float(PF) if not pd.isna(PF) else None}
        return

    pick("PFAD", ["PFAD", "Palm Fatty Acid Distillate", "Destilado de Ácidos Graxos de Palma"])
    pick("RBD (Palma)", ["RBD", "Palm Oil", "Óleo de Palma"])
    pick("PKO (Palm Kernel Oil)", ["PKO", "Palm Kernel", "Palm Kernel Oil", "Palmiste", "Palm kernel"])
    return props

def score_esg(upcycling=True, rspo=False, organico=False, fair=False, saturados_pct=0.0):
    score = 50
    if upcycling: score += 20
    if rspo: score += 10
    if organico: score += 10
    if fair: score += 5
    if saturados_pct >= 60: score -= 10
    if saturados_pct >= 70: score -= 10
    return int(max(0, min(100, score)))

def gerar_pdf(relato, modo="essencial"):
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, leftMargin=48, rightMargin=48, topMargin=48, bottomMargin=48)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="Just", parent=styles["Normal"], alignment=TA_JUSTIFY, leading=14))
    story = []

    story.append(Paragraph(f"<b>{relato['titulo']}</b>", styles["Title"]))
    story.append(Paragraph(f"Relatório gerado em {datetime.now().strftime('%d/%m/%Y %H:%M')}", styles["Normal"]))
    story.append(Spacer(1, 10))

    b = relato["blend"]
    story.append(Paragraph("<b>Blend Enzimático</b>", styles["Heading2"]))
    story.append(Paragraph(f"PFAD: {b['PFAD']}% • RBD (Palma): {b['RBD (Palma)']}% • PKO: {b['PKO (Palm Kernel Oil)']}%", styles["Normal"]))
    p = relato["props"]
    story.append(Paragraph(f"Índice de Iodo (II): {p['II']} • Índice de Saponificação (ISap): {p['ISap']} • Ponto de Fusão: {p['PFusao']} °C", styles["Normal"]))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>Aplicação Cosmética</b>", styles["Heading2"]))
    story.append(Paragraph(f"Ocaşão: {relato.get('ocasião','—')}", styles["Normal"]))
    if relato.get("essencias"):
        ess_txt = ", ".join([e["nome"] for e in relato["essencias"]])
        story.append(Paragraph(f"Essências Amazônicas: {ess_txt}", styles["Normal"]))
    story.append(Spacer(1, 6))

    esg = relato["esg"]
    story.append(Paragraph("<b>Sustentabilidade (Score ESG)</b>", styles["Heading2"]))
    story.append(Paragraph(f"Score ESG: {esg['score']} / 100", styles["Normal"]))
    story.append(Paragraph(f"Critérios: upcycling={esg['upcycling']}, RSPO={esg['rspo']}, Orgânico={esg['organico']}, Fair Trade={esg['fair']}, Saturados≈{esg['saturados']}%", styles["Normal"]))
    story.append(Spacer(1, 6))

    if modo == "completo" and relato.get("rastreio_df") is not None and not relato["rastreio_df"].empty:
        story.append(Paragraph("<b>Rastreabilidade (resumo)</b>", styles["Heading2"]))
        df = relato["rastreio_df"].copy()
        cols = [c for c in ["Ingrediente","Fornecedor","Lote","Validade","Certificações"] if c in df.columns]
        data = [cols] + df[cols].values.tolist()
        tbl = Table(data, colWidths=[80,120,60,60,120])
        tbl.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0), colors.whitesmoke),
                                 ('GRID',(0,0),(-1,-1), 0.25, colors.grey),
                                 ('FONTSIZE',(0,0),(-1,-1), 9)]))
        story.append(tbl)
        story.append(Spacer(1, 6))

    doc.build(story)
    buf.seek(0)
    return buf

# =============================
# --------- SIDEBAR -----------
# =============================

with st.sidebar:
    st.markdown("## 💧 LipidGenesis — MVP v7.1")
    st.caption("Perfis reais de ácidos graxos (CSV/XLSX), ESG e sociobioeconomia.")
    st.markdown("---")
    if "rastreio" not in st.session_state:
        st.session_state.rastreio = []
    if "blend" not in st.session_state:
        st.session_state.blend = {"PFAD": 30.0, "RBD (Palma)": 50.0, "PKO (Palm Kernel Oil)": 20.0}
    if "props" not in st.session_state:
        st.session_state.props = {"II": 50.0, "ISap": 200.0, "PFusao": 35.0}
    if "dataset" not in st.session_state:
        st.session_state.dataset = None
    if "props_map" not in st.session_state:
        st.session_state.props_map = {}

# =============================
# ----------- ABAS ------------
# =============================

# === Título e Slogan (fora das abas) 

tabs = st.tabs([
    "🏠 Home",
    "💄 Proposta Cosmética",          # nova aba 2
    "🧪 Blend Enzimático",
    "👩‍🔬 Assistente de Formulação",
    "⚗️ Protocolo de Produção",
    "🌱 Sustentabilidade",
    "📍 Rastreabilidade",
    "📄 Exportação PDF"
])

# ------- HOME — arquitetura visual ajustada (com mockup cosmético) -------

with tabs[0]:
    # HERO em duas colunas: texto (3) + imagem/logo (2)
    col_text, col_img = st.columns([3, 2], gap="large")

    with col_text:
        # Título em 2 linhas (impacto + propósito)
        st.markdown("## 🌴 **LipidPalma — Design de Blends Lipídicos Enzimáticos**")
        st.markdown("### **Com ESG transparente e sociobioeconomia amazônica**")

        st.markdown("---")
        st.markdown("_OGTera – The Future of Oil Disruption_  \n**Apresenta:** **LipidPalma™**")
        st.write(
            "Um app para **simulação e formulação** de blends lipídicos **enzimáticos** aplicados à **cosmética**. "
            "Faz parte da linha **LipidGenesis**, a plataforma modular da **OGTera** para inovação em lipídios."
        )

        st.markdown("---")
        st.subheader("Visão")
        st.write(
            "Unir **biocatálise**, **upcycling** e **rastreabilidade** com **ESG** claro. "
            "A integração com a **sociobioeconomia amazônica** começa pela **assinatura sensorial** (essências) "
            "e evolui para cadeias **rastreáveis**."
        )

        st.subheader("Como usar")
        st.markdown(
            "➡️ **🧪 Blend Enzimático** — defina PFAD / RBD / PKO / DERIVADOS.  \n"
            "➡️ **👩‍🔬 Assistente de Formulação** — escolha ocasião (mãos/corpo/rosto/cabelos) e essências (opcional).  \n"
            "➡️ **⚗️ Protocolo de Produção** — parâmetros e custo/kg.  \n"
            "➡️ **📄 Exportação PDF** — gere o dossiê do blend."
        )

    with col_img:
          # Logo institucional (se existir)
        for fname in ["logo_ogtera.png.PNG", "logo_ogtera.jpg", "logo.png", "ogtera.png"]:
            if os.path.exists(fname):
                st.image(fname, use_container_width=True)
                break

        # Mockup cosmético (troque a URL por um arquivo local se preferir, ex.: 'mockup_cosmetico.png')
        st.image("cosmetico.png.PNG", use_container_width=True)

    st.markdown("---")

    # KPIs em 2x2 (mais responsivo)
    k1, k2 = st.columns(2)
    with k1:
        st.metric("Indústria-alvo", "Cosméticos")
    with k2:
        st.metric("Rota", "Enzimática")
    k3, k4 = st.columns(2)
    with k3:
        st.metric("Plataforma", "LipidGenesis")
    with k4:
        st.metric("Módulo", "LipidPalma™")

    st.markdown("---")

    # Pilares de confiança com ícones (visual mais “beauty”)
    st.subheader("Camadas de confiança")
    p1, p2, p3 = st.columns(3)
    with p1:
        st.markdown("### ♻️ ESG transparente")
        st.write("Score 0–100 com critérios claros: upcycling, RSPO, orgânico, fair trade, saturados.")
    with p2:
        st.markdown("### 📦 Rastreabilidade")
        st.write("Ficha de ingredientes (fornecedor, lote, certificações) com exportação CSV.")
    with p3:
        st.markdown("### 📜 Licenciamento")
        st.write("Modelo: **protótipos + patentes + licenças** (B2B).")

    # (rodapé permanece exatamente como está no seu arquivo)

 # ------- PROPOSTA COSMÉTICA (ajustada com ponte para Home) -------
with tabs[1]:
    st.header("Proposta Cosmética 💄")
    st.write(
        "O **LipidPalma™** é focado em **blends lipídicos enzimáticos** para **cosméticos**, "
        "ajustando **toque**, **hidratação**, **estabilidade** e **brilho** conforme a aplicação e o perfil do blend.\n\n"
        "Como apresentado na **Home**, o LipidPalma™ integra pilares de **ESG**, **rastreabilidade** e **inovação**. "
        "Aqui destacamos **como esses conceitos se traduzem em valor concreto para a indústria cosmética**, "
        "tanto em termos de **benefícios práticos** quanto de **narrativa amazônica**."
    )

    st.markdown("---")
    st.subheader("Benefícios por aplicação ✨")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            "- ✋ **Mãos**: absorção rápida, **toque seco** e hidratação leve.\n"
            "- 🧴 **Corpo**: **nutrição** e maciez com textura uniforme.\n"
        )
    with c2:
        st.markdown(
            "- 🙂 **Rosto**: perfil **balanceado**, adequado a peles sensíveis.\n"
            "- 💇‍♀️ **Cabelos**: **brilho**, emoliência e redução de frizz.\n"
        )
    st.caption("Observação: os efeitos variam conforme a composição do blend (PFAD/RBD/PKO/derivados) e a presença de essências.")

    st.markdown("---")
    st.subheader("Contribuição dos ingredientes-base 🧪")
    st.markdown(
        """
| Ingrediente                 | Contribuição cosmética                                                                 |
|-----------------------------|-----------------------------------------------------------------------------------------|
| 🟠 **RBD(Óleo de Palma)**    | **Estabilidade oxidativa**, textura uniforme, base versátil                             |
| 🧴 **Estearina de Palma**    | Textura **firme**; dá corpo a cremes/manteigas; opacidade em pomadas e sabonetes        |
| ✨ **Oleína de Palma**       | Fração **líquida e leve**; boa espalhabilidade; usada em loções e óleos capilares       |
| 🌰 **RPKO(Óleo de Palmiste)**| **Leveza** e **toque seco**; brilho em cabelos; melhora espalhabilidade                 |
| 🧼 **Estearina de Palmiste** | **Dureza** e espuma; rica em C12–C14; usada em sabonetes e shampoos sólidos              |
| 💧 **Oleína de Palmiste**    | Fração mais fluida; toque leve; alternativa de baixo custo em hidratantes de absorção rápida |
| 🌿 **PFAD**                  | Emoliência e **hidratação profunda**; corpo de fórmula                                  |
| ♻️ **Soapstock**             | Subproduto do refino químico; pode ser refinado/esterificado em blends sustentáveis com apelo ESG |
        """,
        help="Mapa qualitativo ampliado: inclui frações da palma e palmiste, além de PFAD e soapstock (upcycling)."
    )
    st.caption("Nota: **soapstock** requer adequação regulatória (refino/esterificação e dossiê) antes de uso em cosméticos.")

    # ---------- UP AMAZÔNICO 1: Assinatura Sensorial ----------
st.markdown("---")
st.subheader("Assinatura Sensorial Amazônica (opcional) 🍃")
st.caption("Vitrine inspiracional de essências; a seleção efetiva é feita na aba **Assistente de Formulação**.")

# 1) Fonte de dados: usa ESSENCIAS se existir; senão, fallback local (6 itens)
try:
    _ess_raw = ESSENCIAS  # pode NÃO ter 'emoji' em cada item
except NameError:
    _ess_raw = [
        {"emoji": "🌰", "nome": "Cumaru (Tonka)",      "acorde": "baunilha-amêndoa",   "família": "oriental",   "nota": "fundo"},
        {"emoji": "🔥", "nome": "Breu-branco",         "acorde": "resinoso-limpo",     "família": "balsâmico",  "nota": "coração"},
        {"emoji": "🌿", "nome": "Priprioca",           "acorde": "terroso-amadeirado", "família": "amadeirado", "nota": "coração"},
        {"emoji": "🌳", "nome": "Copaíba",             "acorde": "amadeirado-resinoso","família": "amadeirado", "nota": "fundo"},
        {"emoji": "🍂", "nome": "Patchouli Amazônico", "acorde": "terroso-úmido",      "família": "chipre",     "nota": "fundo"},
        {"emoji": "🌸", "nome": "Pau-rosa (Rosewood)", "acorde": "floral-amadeirado",  "família": "floral",     "nota": "coração"},
    ]

# Layout responsivo 3 + 3 colunas
row1 = st.columns(3)
row2 = st.columns(3)
cards = row1 + row2
for col, e in zip(cards, _ess[:6]):
    with col:
        st.markdown(
            f"**{e['emoji']} {e['nome']}**\n\n"
            f"- Acorde: *{e['acorde']}*\n"
            f"- Família: *{e['família']}*\n"
            f"- Nota: *{e['nota']}*\n"
        )


    # ---------- UP AMAZÔNICO 2: Sociobioeconomia ----------
    st.markdown("---")
    st.subheader("Sociobioeconomia (indicadores de origem) 🌎")
    st.caption("Indicadores de narrativa e diligência; não substituem certificações formais.")

    cA, cB, cC, cD = st.columns(4)
    with cA:
        origem = st.checkbox("Origem comunitária/cooperativa", False)
    with cB:
        rastreio = st.checkbox("Rastreabilidade confirmada", False)
    with cC:
        cert = st.checkbox("Certificação socioambiental (ex.: orgânico/fair)", False)
    with cD:
        repart = st.checkbox("Repartição de benefícios documentada", False)

    # 🔹 Índice 0–100 com persistência
    score_amz = 0 + 25*int(origem) + 35*int(rastreio) + 20*int(cert) + 20*int(repart)
    score_amz = max(0, min(100, score_amz))
    st.metric("Índice de Narrativa Amazônica", f"{score_amz} / 100")
    st.session_state["indice_narrativa_amazonia"] = score_amz

    st.markdown("---")
    st.subheader("Proposta de valor para P&D e negócio 🚀")
    st.markdown(
        "- ⚡ **Velocidade de P&D**: triagem digital antes do laboratório.\n"
        "- 🧬 **Precisão**: possibilidade de usar **perfis reais** de ácidos graxos (quando habilitado no Blend).\n"
        "- ♻️ **Sustentabilidade**: upcycling (PFAD/soapstock) e **ESG** transparente.\n"
        "- 🔍 **Rastreabilidade**: ficha de ingredientes e certificações (CSV exportável).\n"
        "- 🛠️ **Customização**: ajuste do blend por **ocasião de uso** e assinatura sensorial (essências amazônicas opcionais).\n"
        "- 📈 **Negócio**: foco em **protótipos + patentes + licenciamento** (modelo B2B)."
    )

    with st.expander("💡 Exemplos de posicionamento/claims (ideias)"):
        st.markdown(
            "- “Toque sedoso com rápida absorção” (mãos/corpo)\n"
            "- “Nutrição e maciez com leveza” (corpo)\n"
            "- “Perfil balanceado para peles delicadas” (rosto)\n"
            "- “Brilho e emoliência com controle de frizz” (cabelos)\n"
        )
        st.caption("Claims dependem de validação de bancada e requisitos regulatórios.")

    st.caption("Esta aba apresenta a **proposta cosmética, assinatura sensorial e narrativa amazônica**, sem repetir instruções já mostradas na Home.")
# ------- BLEND ENZIMÁTICO -------
with tabs[2]:
    st.header("Blend Enzimático")

    # Painel opcional de perfis reais (upload)
    with st.expander("📥 Perfis Reais (opcional): carregar CSV/XLSX com ácidos graxos e/ou propriedades"):
        file = st.file_uploader("Carregar arquivo CSV/XLSX", type=["csv", "xlsx"])
        if file is not None:
            try:
                df = load_dataset(file)               # sua função existente
                msgs = validate_dataset(df)           # sua função existente
                if msgs:
                    for m in msgs:
                        st.warning(m)
                st.session_state.dataset = df
                st.session_state.props_map = build_props_map(df)   # sua função existente
                st.success("Perfis aplicados. Cálculos de II/ISap/PFusão agora usam os dados carregados (ou estimativa por FA).")
                st.dataframe(df.head(15), use_container_width=True)
                with st.expander("Mapa de propriedades identificado"):
                    st.json(st.session_state.props_map)
            except Exception as e:
                st.error(f"Falha ao carregar arquivo: {e}")

    # --- (seus sliders atuais) ---
    c1, c2, c3 = st.columns(3)
    with c1:
        pfad = st.slider("PFAD (%)", 0.0, 100.0, float(st.session_state.blend["PFAD"]), 1.0)
    with c2:
        rbd  = st.slider("RBD (Palma) (%)", 0.0, 100.0, float(st.session_state.blend["RBD (Palma)"]), 1.0)
    with c3:
        pko  = st.slider("PKO (%)", 0.0, 100.0, float(st.session_state.blend["PKO (Palm Kernel Oil)"]), 1.0)

    pfad_n, rbd_n, pko_n, soma = normaliza_blend(pfad, rbd, pko)   # sua função existente
    st.markdown(f"**Soma antes da normalização:** {soma:.2f}%  →  **Blend final:** PFAD {pfad_n}%, RBD {rbd_n}%, PKO {pko_n}%")
    st.session_state.blend = {"PFAD": pfad_n, "RBD (Palma)": rbd_n, "PKO (Palm Kernel Oil)": pko_n}

    II, ISap, PF = props_blend(                                    # sua função existente
        pfad_n, rbd_n, pko_n, st.session_state.get("props_map", {})
    )
    st.session_state.props = {"II": II, "ISap": ISap, "PFusao": PF}
    st.success(f"II={II} | ISap={ISap} | PFusão≈{PF}°C")
    st.caption("Sem upload, usamos heurísticas internas. Com dataset, os valores seguem o arquivo (ou estimados a partir dos FAs).")

# ------- ASSISTENTE DE FORMULAÇÃO -------
with tabs[3]:
    st.header("Assistente de Formulação")
    ocasião = st.selectbox("Escolha a ocasião de uso", ["Mãos", "Corpo", "Rosto", "Cabelos"])
    base_attr, blend_sug = heuristica_por_ocasião(ocasião)
    st.write("**Blend sugerido (ajustável):**", blend_sug)
    use_sugerido = st.checkbox("Usar blend sugerido", True)
    if use_sugerido:
        st.session_state.blend.update(blend_sug)
        II, ISap, PF = props_blend(
    st.session_state.blend["PFAD"],
    st.session_state.blend["RBD (Palma)"],
    st.session_state.blend["PKO (Palm Kernel Oil)"],
    props_map=st.session_state.get("props_map", {})
)
        st.session_state.props = {"II": II, "ISap": ISap, "PFusao": PF}

    st.subheader("Essências Amazônicas (máx. 2)")
    nomes = [e["nome"] for e in ESSENCIAS]
    escolhidas = st.multiselect("Adicionar essências", nomes, max_selections=2)
    ess_objs = [e for e in ESSENCIAS if e["nome"] in escolhidas]
    st.session_state["essencias_escolhidas"] = ess_objs

    st.subheader("Atributos esperados (heurístico 0–10)")
    colA, colB, colC, colD = st.columns(4)
    colA.metric("Toque seco", base_attr["toque"])
    colB.metric("Hidratação", base_attr["hidr"])
    colC.metric("Estabilidade", base_attr["estab"])
    colD.metric("Brilho (cabelos)", base_attr["brilho"])
    st.info("Heurística inicial. Ajustes virão após dados de bancada.")

# ------- PROTOCOLO DE PRODUÇÃO -------
with tabs[4]:
    st.header("Protocolo de Produção (Esterificação Enzimática)")
    with st.form("protocolo"):
        enz_pct = st.number_input("% enzima (m/m)", 1.0, 15.0, 5.0, 0.5)
        temp = st.number_input("Temperatura (°C)", 30.0, 70.0, 50.0, 1.0)
        ciclos = st.number_input("Nº de ciclos", 1, 10, 3, 1)
        massa_lote = st.number_input("Massa do lote (kg)", 0.1, 100.0, 5.0, 0.1)
        custo_enz = st.number_input("Custo da enzima (R$/kg)", 100.0, 5000.0, 1200.0, 10.0)
        custo_insumos = st.number_input("Custo dos insumos base (R$/kg)", 5.0, 100.0, 18.0, 0.5)
        remover_agua = st.checkbox("Remoção contínua de água (melhora rendimento)", True)
        submitted = st.form_submit_button("Calcular custos")

    if submitted:
        enz_kg = massa_lote * (enz_pct/100.0)
        custo_enz_total = enz_kg * custo_enz / max(1, ciclos)
        custo_base_total = massa_lote * custo_insumos
        custo_kg = (custo_enz_total + custo_base_total) / massa_lote
        agua_formada = 0.05 * massa_lote
        st.success(f"Custo estimado: **R$ {custo_kg:,.2f}/kg** (enzima rateada em {ciclos} ciclos)")
        st.caption(f"Água formada (proxy): {agua_formada:.2f} kg • Remoção de água: {'sim' if remover_agua else 'não'}")

# ------- SUSTENTABILIDADE -------
with tabs[5]:
    st.header("Sustentabilidade (ESG)")
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1: upcycling = st.checkbox("Upcycling (PFAD/soapstock)", True)
    with c2: rs = st.checkbox("RSPO", False)
    with c3: org = st.checkbox("Orgânico", False)
    with c4: fair = st.checkbox("Fair Trade", False)
    with c5: sat = st.slider("Saturados (estimado, %)", 0, 100, 55)

    esg_score = score_esg(upcycling=upcycling, rspo=rs, organico=org, fair=fair, saturados_pct=sat)
    st.metric("Score ESG", f"{esg_score} / 100")
    st.caption("Penalização aplicada acima de 60–70% de saturados.")
    st.session_state.esg = {"score": esg_score, "upcycling": upcycling, "rspo": rs, "organico": org, "fair": fair, "saturados": sat}

# ------- RASTREABILIDADE -------
with tabs[6]:
    st.header("Rastreabilidade")
    st.write("Registre, por ingrediente, fornecedor e certificações. Exporte CSV.")
    with st.expander("Adicionar ingrediente", expanded=True):
        ing = st.text_input("Ingrediente", "")
        forn = st.text_input("Fornecedor", "")
        lote = st.text_input("Lote", "")
        validade = st.date_input("Validade")
        cert = st.text_input("Certificações (RSPO, Orgânico, Fair, ISO)", "")
        if st.button("Salvar ingrediente"):
            if ing and forn and lote:
                st.session_state.rastreio.append({
                    "Ingrediente": ing,
                    "Fornecedor": forn,
                    "Lote": lote,
                    "Validade": validade.strftime("%d/%m/%Y"),
                    "Certificações": cert
                })
                st.success("Ingrediente salvo.")
            else:
                st.error("Preencha ao menos Ingrediente, Fornecedor e Lote.")

    if len(st.session_state.rastreio):
        df_r = pd.DataFrame(st.session_state.rastreio)
        st.dataframe(df_r, use_container_width=True)
        buffer = io.StringIO()
        df_r.to_csv(buffer, index=False)
        buffer.seek(0)
        st.download_button("📥 Baixar Ficha de Rastreabilidade (CSV)", data=buffer, file_name="rastreabilidade.csv", mime="text/csv")

# ------- EXPORTAÇÃO PDF -------
with tabs[7]:
    st.header("Exportação PDF")
    modo = st.radio("Modo de relatório", ["Essencial", "Completo"], horizontal=True)

    relato = {
        "titulo": "Relatório — LipidGenesis MVP v7.1",
        "blend": st.session_state.blend,
        "props": st.session_state.props,
        "ocasião": st.session_state.get("ocasião", "—"),
        "essencias": st.session_state.get("essencias_escolhidas", []),
        "esg": st.session_state.get("esg", {"score": 0, "upcycling": False, "rspo": False, "organico": False, "fair": False, "saturados": 0}),
        "rastreio_df": pd.DataFrame(st.session_state.rastreio) if len(st.session_state.rastreio) else None
    }
    pdf_buf = gerar_pdf(relato, modo="completo" if modo == "Completo" else "essencial")
    st.download_button("📄 Baixar PDF", data=pdf_buf, file_name=f"Relatorio_LipidGenesis_{modo}.pdf", mime="application/pdf")

# ------- RODAPÉ -------
st.markdown("---")
st.markdown(
    "<p style='text-align: center; font-size: 14px;'>"
    "🌿 Desenvolvido por <b>OGTera - The Future of Oil Disruption</b>. "
    "Aplicação modular <b>LipidGenesis</b> com o módulo atual: <b>LipidPalma</b>. "
    "<br>Versão MVP demonstrativa. &copy; 2025 OGT."
    "</p>",
    unsafe_allow_html=True
)

# Fim
