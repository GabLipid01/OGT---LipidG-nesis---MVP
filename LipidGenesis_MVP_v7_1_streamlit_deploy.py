# -*- coding: utf-8 -*-
# LipidGenesis_MVP_v7_1_streamlit_deploy.py — OGTera / LipidPalma (MVP) — 8 abas

import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json, io, math
from collections import OrderedDict

def _first_existing(paths):
    """
    Retorna o primeiro caminho existente de uma lista de caminhos de arquivo.
    Se nenhum arquivo existir, retorna None.
    """
    for p in paths:
        if os.path.exists(p):
            return p
    return None

# ---------------- Page config ----------------
try:
    st.set_page_config(page_title="LipidPalma – OGTera", layout="wide")
except Exception:
    pass

# ---------------- Session defaults ----------------
_defaults = {
    "blend_mode_radio": "Heurísticas (rápido)",
    "ajuste_method_heur": "Classe B — Ácidos graxos puros",
    "ajuste_method_upload": "Classe B — Ácidos graxos puros",
    "formato_planilha": "Ingredientes (%)",
    "go_to_assistente": False,
}
for k, v in _defaults.items():
    st.session_state.setdefault(k, v)

# ---------------- Global data (essences) ----------------
if "ESSENCIAS" not in st.session_state:
    st.session_state["ESSENCIAS"] = [
        {"emoji": "🌰", "nome": "Cumaru (Tonka)",      "acorde": "baunilha-amêndoa",   "família": "oriental",   "nota": "fundo"},
        {"emoji": "🔥", "nome": "Breu-branco",         "acorde": "resinoso-limpo",     "família": "balsâmico",  "nota": "coração"},
        {"emoji": "🌿", "nome": "Priprioca",           "acorde": "terroso-amadeirado", "família": "amadeirado", "nota": "coração"},
        {"emoji": "🌳", "nome": "Copaíba",             "acorde": "amadeirado-resinoso","família": "amadeirado", "nota": "fundo"},
        {"emoji": "🍂", "nome": "Patchouli Amazônico", "acorde": "terroso-úmido",      "família": "chipre",     "nota": "fundo"},
        {"emoji": "🌸", "nome": "Pau-rosa (Rosewood)", "acorde": "floral-amadeirado",  "família": "floral",     "nota": "coração"},
    ]

# ---------------- Create tabs (8) ----------------
tabs = st.tabs([
    "Home",                         # tabs[0]
    "Proposta Cosmética",           # tabs[1]
    "Blend Enzimático",             # tabs[2]
    "Assistente de Formulação",     # tabs[3]
    "Protocolo de Produção",        # tabs[4]
    "Sustentabilidade / ESG",       # tabs[5]
    "Rastreabilidade",              # tabs[6]
    "Exportação PDF",               # tabs[7]
])

# ======================================================================
# TAB 0 — HOME (institucional consolidado)
# ======================================================================
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
        col1, col2, col3 = st.columns([2,2,1])
        with col2:
            st.image("cosmetico.png.PNG.jpeg", width=400)

    st.markdown("---")

    # --- KPIs institucionais em linha única ---
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.metric("Indústria-alvo", "Cosméticos")
    with k2:
        st.metric("Rota", "Enzimática")
    with k3:
        st.metric("Plataforma", "LipidGenesis")
    with k4:
        st.metric("Módulo", "LipidPalma™")

    st.markdown("---")

    # --- Camadas de confiança (layout estável e responsivo) ---
    st.subheader("Camadas de confiança")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("**♻️ ESG transparente**")
        st.caption("Score 0–100: upcycling, RSPO, orgânico, fair trade, saturados.")
    with c2:
        st.markdown("**📦 Rastreabilidade**")
        st.caption("Ficha de ingredientes (fornecedor, lote, certificações) + exportação CSV.")
    with c3:
        st.markdown("**📜 Licenciamento**")
        st.caption("Modelo B2B: protótipos + patentes + licenças.")

# ======================================================================
# TAB 1 — PROPOSTA COSMÉTICA (consolidada)
# ======================================================================
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
| Ingrediente                  | Contribuição cosmética                                                                 |
|------------------------------|-----------------------------------------------------------------------------------------|
| 🟠 **RBD(Óleo de Palma)**     | **Estabilidade oxidativa**, textura uniforme, base versátil                             |
| 🧴 **Estearina de Palma**     | Textura **firme**; dá corpo a cremes/manteigas; opacidade em pomadas e sabonetes        |
| ✨ **Oleína de Palma**        | Fração **líquida e leve**; boa espalhabilidade; usada em loções e óleos capilares       |
| 🌰 **RPKO(Óleo de Palmiste)** | **Leveza** e **toque seco**; brilho em cabelos; melhora espalhabilidade                 |
| 🧼 **Estearina de Palmiste**  | **Dureza** e espuma; rica em C12–C14; usada em sabonetes e shampoos sólidos              |
| 💧 **Oleína de Palmiste**     | Fração mais fluida; toque leve; alternativa de baixo custo em hidratantes de absorção rápida |
| 🌿 **PFAD**                   | Emoliência e **hidratação profunda**; corpo de fórmula                                  |
| ♻️ **Soapstock**              | Subproduto do refino químico; pode ser refinado/esterificado em blends sustentáveis com apelo ESG |
        """,
        help="Mapa qualitativo ampliado: inclui frações da palma e palmiste, além de PFAD e soapstock (upcycling)."
    )
    st.caption("Nota: **soapstock** requer adequação regulatória (refino/esterificação e dossiê) antes de uso em cosméticos.")

    st.markdown("---")
    st.subheader("Assinatura Sensorial Amazônica (opcional) 🍃")
    st.caption("Vitrine inspiracional de essências; a seleção efetiva é feita na aba **Assistente de Formulação**.")
    _ess_raw = st.session_state["ESSENCIAS"]
    _default_emojis = ["🌰","🔥","🌿","🌳","🍂","🌸","🌺","🌲"]
    _ess = []
    for i, e in enumerate(_ess_raw[:6]):
        _ess.append({
            "emoji":   e.get("emoji", _default_emojis[i % len(_default_emojis)]),
            "nome":    e.get("nome", "Essência"),
            "acorde":  e.get("acorde", "—"),
            "família": e.get("família", "—"),
            "nota":    e.get("nota", "—"),
        })
    row1 = st.columns(3)
    row2 = st.columns(3)
    cards = row1 + row2
    for col, e in zip(cards, _ess):
        with col:
            st.markdown(
                f"**{e['emoji']} {e['nome']}**\n\n"
                f"- Acorde: *{e['acorde']}*\n"
                f"- Família: *{e['família']}*\n"
                f"- Nota: *{e['nota']}*\n"
            )

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

# ======================================================================
# TAB 2 — BLEND ENZIMÁTICO (robusta)
# ======================================================================
with tabs[2]:
    st.header("Blend Enzimático ⚗️")
    st.caption(
        "Defina o blend por **Classe A (Ingredientes da palma)** e, se necessário, aplique **ajuste fino** por "
        "**Classe B (Ácidos graxos puros)** ou **Classe C (Ingredientes)**. "
        "No modo Upload real (CSV/XLSX), você também pode aplicar o mesmo ajuste fino. "
        "⚠️ KPIs no modo heurístico são **estimativas** (perfis médios por ingrediente)."
    )

    # Ingredientes (Proposta Cosmética)
    INGREDIENTS = [
        ("rbd_palma",            "🟠 RBD (Óleo de Palma)"),
        ("estearina_palma",      "🧴 Estearina de Palma"),
        ("oleina_palma",         "✨ Oleína de Palma"),
        ("rpko_palmiste",        "🌰 RPKO (Óleo de Palmiste)"),
        ("estearina_palmiste",   "🧼 Estearina de Palmiste"),
        ("oleina_palmiste",      "💧 Oleína de Palmiste"),
        ("pfad",                 "🌿 PFAD"),
        ("soapstock",            "♻️ Soapstock"),
    ]

    # Constantes FA (para proxies de KPIs – abordagem UIGES-like)
    FA_CONST = {
        "C12:0": {"IV": 0.0,   "MW": 200.32},
        "C14:0": {"IV": 0.0,   "MW": 228.37},
        "C16:0": {"IV": 0.0,   "MW": 256.42},
        "C18:0": {"IV": 0.0,   "MW": 284.48},
        "C18:1": {"IV": 90.0,  "MW": 282.47},
        "C18:2": {"IV": 181.0, "MW": 280.45},
        "C18:3": {"IV": 273.0, "MW": 278.43},
    }
    FA_ORDER = list(FA_CONST.keys())

    # Perfis FA por ingrediente (com variabilidade)
    FA_PROFILES_RANGED = {
        "rbd_palma": {
            "mean": {"C16:0": 44, "C18:1": 39, "C18:2": 10, "C18:0": 4, "C14:0": 1, "C12:0": 0},
            "min":  {"C16:0": 41, "C18:1": 36, "C18:2": 8,  "C18:0": 3, "C14:0": 1, "C12:0": 0},
            "max":  {"C16:0": 47, "C18:1": 42, "C18:2": 12, "C18:0": 5, "C14:0": 2, "C12:0": 1},
        },
        "oleina_palma": {
            "mean": {"C16:0": 39, "C18:1": 42, "C18:2": 13, "C18:0": 4, "C14:0": 1, "C12:0": 0},
            "min":  {"C16:0": 36, "C18:1": 39, "C18:2": 11, "C18:0": 3, "C14:0": 1, "C12:0": 0},
            "max":  {"C16:0": 42, "C18:1": 45, "C18:2": 15, "C18:0": 5, "C14:0": 2, "C12:0": 1},
        },
        "estearina_palma": {
            "mean": {"C16:0": 55, "C18:1": 33, "C18:2": 7,  "C18:0": 4, "C14:0": 1, "C12:0": 0},
            "min":  {"C16:0": 52, "C18:1": 30, "C18:2": 6,  "C18:0": 3, "C14:0": 1, "C12:0": 0},
            "max":  {"C16:0": 58, "C18:1": 36, "C18:2": 9,  "C18:0": 5, "C14:0": 2, "C12:0": 1},
        },
        "rpko_palmiste": {
            "mean": {"C12:0": 48, "C14:0": 16, "C16:0": 8,  "C18:1": 15, "C18:2": 2, "C18:0": 2},
            "min":  {"C12:0": 45, "C14:0": 14, "C16:0": 7,  "C18:1": 13, "C18:2": 2, "C18:0": 1},
            "max":  {"C12:0": 51, "C14:0": 18, "C16:0": 9,  "C18:1": 17, "C18:2": 3, "C18:0": 3},
        },
        "oleina_palmiste": {
            "mean": {"C12:0": 42, "C14:0": 15, "C16:0": 10, "C18:1": 20, "C18:2": 4, "C18:0": 2},
            "min":  {"C12:0": 39, "C14:0": 14, "C16:0": 9,  "C18:1": 18, "C18:2": 3, "C18:0": 1},
            "max":  {"C12:0": 45, "C14:0": 17, "C16:0": 11, "C18:1": 22, "C18:2": 5, "C18:0": 3},
        },
        "estearina_palmiste": {
            "mean": {"C12:0": 50, "C14:0": 17, "C16:0": 7,  "C18:1": 12, "C18:2": 3, "C18:0": 3},
            "min":  {"C12:0": 47, "C14:0": 15, "C16:0": 6,  "C18:1": 10, "C18:2": 2, "C18:0": 2},
            "max":  {"C12:0": 53, "C14:0": 19, "C16:0": 8,  "C18:1": 14, "C18:2": 4, "C18:0": 4},
        },
        "pfad": {
            "mean": {"C16:0": 50, "C18:1": 35, "C18:2": 10, "C18:0": 5},
            "min":  {"C16:0": 47, "C18:1": 33, "C18:2": 8,  "C18:0": 4},
            "max":  {"C16:0": 53, "C18:1": 37, "C18:2": 12, "C18:0": 6},
        },
        "soapstock": {
            "mean": {"C16:0": 40, "C18:1": 40, "C18:2": 15, "C18:0": 5},
            "min":  {"C16:0": 37, "C18:1": 38, "C18:2": 13, "C18:0": 4},
            "max":  {"C16:0": 43, "C18:1": 42, "C18:2": 17, "C18:0": 6},
        },
    }

    def _normalize_percentages(d: dict) -> dict:
        total = sum(float(v or 0) for v in d.values())
        if total <= 0:
            return {k: 0.0 for k in d}
        return {k: (float(v or 0) * 100.0 / total) for k, v in d.items()}

    def _badge_total(total: float, prefix="Total"):
        msg = f"**{prefix}: {total:.2f}%**"
        if abs(total - 100.0) < 1e-6:
            st.success(msg)
        elif total < 100:
            st.warning(msg + " • abaixo de 100%")
        else:
            st.error(msg + " • acima de 100%")

    def _download_json_button(obj, label, fname):
        st.download_button(
            label=label,
            data=json.dumps(obj, ensure_ascii=False, indent=2).encode("utf-8"),
            file_name=fname,
            mime="application/json",
            key=f"dl_{fname}",
        )

    def _get_profile(ing_key: str, scenario: str) -> dict:
        profs = FA_PROFILES_RANGED.get(ing_key, {})
        return profs.get(scenario, profs.get("mean", {}))

    # KPIs (proxies derivados do perfil FA – mesma visualização)
    def iodine_index(fa_pct: dict) -> float:
        return sum((fa_pct.get(k, 0.0) / 100.0) * FA_CONST[k]["IV"] for k in FA_CONST.keys())

    def saponification_index(fa_pct: dict) -> float:
        return sum((fa_pct.get(k, 0.0) / 100.0) * (560.0 / FA_CONST[k]["MW"]) for k in FA_CONST.keys())

    def melt_proxy(fa_pct: dict) -> float:
        sat = fa_pct.get("C12:0",0)+fa_pct.get("C14:0",0)+fa_pct.get("C16:0",0)+fa_pct.get("C18:0",0)
        mono = fa_pct.get("C18:1",0)
        poly = fa_pct.get("C18:2",0)+fa_pct.get("C18:3",0)
        score = (0.6*sat + 0.2*(fa_pct.get("C16:0",0)+fa_pct.get("C18:0",0)) - 0.3*poly + 0.05*mono)
        return max(0.0, min(100.0, score))

    # Heurísticas sensoriais (estimativas)
    def spreadability(fa):
        insat = fa.get("C18:1",0) + fa.get("C18:2",0) + fa.get("C18:3",0)
        laur = fa.get("C12:0",0) + fa.get("C14:0",0)
        return max(0, min(100, 0.7*insat + 0.2*laur))

    def hydration_potential(fa):
        lin = fa.get("C18:2",0); ole = fa.get("C18:1",0)
        sat = fa.get("C16:0",0) + fa.get("C18:0",0)
        return max(0, min(100, 0.5*lin + 0.4*ole + 0.1*sat))

    def occlusion(fa):
        sat = fa.get("C12:0",0)+fa.get("C14:0",0)+fa.get("C16:0",0)+fa.get("C18:0",0)
        return max(0, min(100, 0.9*sat))

    def toque_seco(fa, PF):
        return max(0, min(100, 100 - PF))

    def brilho(fa):
        ole = fa.get("C18:1",0); laur = fa.get("C12:0",0)+fa.get("C14:0",0)
        return max(0, min(100, 0.6*ole + 0.3*laur))

    def finalidade_scores(fa, PF, II):
        spread = spreadability(fa); hidr = hydration_potential(fa)
        ocl = occlusion(fa); toque = toque_seco(fa, PF); brilho_v = brilho(fa)
        scores = OrderedDict()
        scores["Mãos"]    = round(0.5*toque + 0.3*spread + 0.2*max(0,100-0.4*II), 1)
        scores["Corpo"]   = round(0.4*hidr  + 0.3*ocl    + 0.3*max(0,100-0.4*II), 1)
        scores["Rosto"]   = round(0.4*fa.get("C18:1",0) + 0.3*max(0,100-0.4*II) + 0.3*toque, 1)
        scores["Cabelos"] = round(0.5*spread + 0.3*fa.get("C18:1",0) + 0.2*max(0,100-0.4*II), 1)
        rad = OrderedDict(
            toque=int(round(toque)), hidr=int(round(hidr)),
            brilho=int(round(brilho_v)), oclusividade=int(round(ocl)),
            absorcao=int(round((toque+spread)/2))
        )
        return scores, rad

    def _fa_from_ingredientes_mix(ing_mix: dict, total_ref: float, get_profile_fn, scenario_key: str):
        fa_tmp = {k: 0.0 for k in FA_ORDER}
        if total_ref <= 0:
            return fa_tmp
        for ing_key, pct in ing_mix.items():
            if pct <= 0:
                continue
            w = pct / total_ref
            prof = get_profile_fn(ing_key, scenario_key)
            for fa_key, fa_pct in prof.items():
                fa_tmp[fa_key] += w * fa_pct
        return _normalize_percentages(fa_tmp)

    def _kpis_from_fa(fa_dict: dict):
        II = iodine_index(fa_dict)
        ISap = saponification_index(fa_dict)
        PF = melt_proxy(fa_dict)
        return II, ISap, PF

    def _plot_tradeoff_bars(title: str, labels: list, deltas: list, ylabel: str):
        fig, ax = plt.subplots()
        ax.bar(range(len(labels)), deltas)
        ax.set_xticks(range(len(labels)))
        ax.set_xticklabels(labels, rotation=45, ha='right')
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        st.pyplot(fig)

    def _compute_tradeoffs_heuristico(A_vals: dict, method: str, B_vals: dict, C_vals: dict,
                                      consider_var: bool, scenario: str):
        total_A = sum(A_vals.values())
        total_adjust = sum(B_vals.values()) if method.startswith("Classe B") else sum(C_vals.values())
        total_all = total_A + total_adjust
        if total_all <= 0:
            return None

        fa_base = {k:0.0 for k in FA_ORDER}
        for ing_key, pct in A_vals.items():
            if pct <= 0: continue
            w = pct / total_all
            prof = _get_profile(ing_key, scenario if consider_var else "mean")
            for fa_key, fa_pct in prof.items():
                fa_base[fa_key] += w * fa_pct
        if method.startswith("Classe B"):
            for fa_key, pct in B_vals.items():
                if pct <= 0: continue
                w = pct / total_all
                fa_base[fa_key] += w * 100.0
        else:
            for ing_key, pct in C_vals.items():
                if pct <= 0: continue
                w = pct / total_all
                prof = _get_profile(ing_key, scenario if consider_var else "mean")
                for fa_key, fa_pct in prof.items():
                    fa_base[fa_key] += w * fa_pct
        fa_base = _normalize_percentages(fa_base)
        II0, IS0, PF0 = _kpis_from_fa(fa_base)

        labels, dII, dIS, dPF = [], [], [], []
        for ing_key, pct in A_vals.items():
            inc = 5.0
            A_new = A_vals.copy()
            A_new[ing_key] = max(0.0, pct + inc)
            new_total_A = sum(A_new.values())
            factor = (total_all) / (new_total_A + total_adjust) if (new_total_A + total_adjust) > 0 else 1.0
            for k in A_new:
                A_new[k] *= factor

            fa_new = {k:0.0 for k in FA_ORDER}
            for k, pv in A_new.items():
                if pv <= 0: continue
                w = pv / total_all
                prof = _get_profile(k, scenario if consider_var else "mean")
                for fk, fp in prof.items():
                    fa_new[fk] += w * fp
            if method.startswith("Classe B"):
                for fk, pv in B_vals.items():
                    if pv <= 0: continue
                    w = pv / total_all
                    fa_new[fk] += w * 100.0
            else:
                for k, pv in C_vals.items():
                    if pv <= 0: continue
                    w = pv / total_all
                    prof2 = _get_profile(k, scenario if consider_var else "mean")
                    for fk, fp in prof2.items():
                        fa_new[fk] += w * fp
            fa_new = _normalize_percentages(fa_new)
            II1, IS1, PF1 = _kpis_from_fa(fa_new)

            label = next(lbl for key,lbl in INGREDIENTS if key==ing_key)
            labels.append(label)
            dII.append(round(II1 - II0, 2))
            dIS.append(round(IS1 - IS0, 2))
            dPF.append(round(PF1 - PF0, 2))

        return labels, dII, dIS, dPF

    def _compute_tradeoffs_upload(fa_start: dict, method_upl: str, B_vals_upload: dict, C_vals_upload: dict,
                                  consider_var: bool, scenario: str):
        fa_base = _normalize_percentages(fa_start.copy())
        II0, IS0, PF0 = _kpis_from_fa(fa_base)

        labels, dII, dIS, dPF = [], [], [], []
        for ing_key, label in INGREDIENTS:
            add_pct = 5.0
            add_fa = {k:0.0 for k in FA_ORDER}
            prof = _get_profile(ing_key, scenario if consider_var else "mean")
            for fk, fp in prof.items():
                add_fa[fk] += (add_pct * fp / 100.0)

            fa_new = fa_base.copy()
            for fk, inc in add_fa.items():
                fa_new[fk] = fa_new.get(fk, 0.0) + inc
            fa_new = _normalize_percentages(fa_new)

            if method_upl.startswith("Classe B"):
                totB = sum(B_vals_upload.values())
                if totB > 0:
                    for fk, pv in B_vals_upload.items():
                        fa_new[fk] = fa_new.get(fk, 0.0) + pv
                    fa_new = _normalize_percentages(fa_new)
            else:
                totC = sum(C_vals_upload.values())
                if totC > 0:
                    add2 = {k:0.0 for k in FA_ORDER}
                    for k, pv in C_vals_upload.items():
                        if pv <= 0: continue
                        prof2 = _get_profile(k, scenario if consider_var else "mean")
                        for fk, fp in prof2.items():
                            add2[fk] += (pv * fp / 100.0)
                    for fk, inc2 in add2.items():
                        fa_new[fk] = fa_new.get(fk, 0.0) + inc2
                    fa_new = _normalize_percentages(fa_new)

            II1, IS1, PF1 = _kpis_from_fa(fa_new)
            labels.append(label); dII.append(round(II1 - II0, 2)); dIS.append(round(IS1 - IS0, 2)); dPF.append(round(PF1 - PF0, 2))

        return labels, dII, dIS, dPF

    def plot_fa_bars(fa_norm):
        data = [fa_norm.get(k, 0.0) for k in FA_ORDER]
        fig, ax = plt.subplots()
        ax.bar(range(len(FA_ORDER)), data)
        ax.set_xticks(range(len(FA_ORDER)))
        ax.set_xticklabels(FA_ORDER, rotation=45, ha='right')
        ax.set_ylabel('%'); ax.set_title('Composição por Ácido Graxo (%)')
        st.pyplot(fig)

    def plot_radar(rad_dict):
        labels = list(rad_dict.keys())
        values = [rad_dict[k] for k in labels]
        N = len(labels)
        angles = [n / float(N) * 2 * math.pi for n in range(N)]
        values += values[:1]; angles += angles[:1]
        fig, ax = plt.subplots(subplot_kw=dict(polar=True))
        ax.plot(angles, values); ax.fill(angles, values, alpha=0.25)
        ax.set_xticks(angles[:-1]); ax.set_xticklabels(labels); ax.set_yticklabels([])
        ax.set_title("Radar Sensorial (0–100)")
        st.pyplot(fig)

    # Variabilidade
    st.markdown("### Variabilidade de lote (opcional)")
    consider_var = st.toggle("Considerar variabilidade de lote", value=False, help="Usa perfis Min/Típico/Max por ingrediente.")
    scenario = "mean"
    if consider_var:
        scen_label = st.radio("Cenário", ["Típico", "Min", "Max"], horizontal=True, index=0, key="var_scenario")
        scenario = {"Típico": "mean", "Min": "min", "Max": "max"}[scen_label]

    # Modo
    mode = st.radio(
        "Modo de entrada",
        ["Heurísticas (rápido)", "Upload de planilha (real)"],
        horizontal=True, key="blend_mode_radio",
    )

    # ---------------- HEURÍSTICAS ----------------
    if mode == "Heurísticas (rápido)":
        st.subheader("Heurísticas com duas camadas: Base (Classe A) + Ajuste fino (B ou C)")
        st.caption("⚠️ **Estimativas**: perfis FA por ingrediente são médios/literatura; cenários Min/Max refletem variação de lote.")

        A_vals = OrderedDict()
        with st.expander("Classe A — Ingredientes da palma (base do blend)", expanded=True):
            colsA = st.columns(4)
            for idx, (k, label) in enumerate(INGREDIENTS):
                with colsA[idx % 4]:
                    A_vals[k] = st.slider(
                        label, min_value=0.0, max_value=100.0, value=0.0, step=1.0,
                        key=f"slider_ing_{k}", help="Percentual no blend (%)",
                    )
            total_A = sum(A_vals.values())
            _badge_total(total_A, "Total Classe A")

        st.markdown("**Ajuste fino** (opcional): escolha o método")
        method = st.radio("Método de ajuste", ["Classe B — Ácidos graxos puros", "Classe C — Ingredientes"],
                          horizontal=True, key="ajuste_method_heur")

        B_vals = OrderedDict((fa, 0.0) for fa in FA_ORDER)
        total_B = 0.0
        if method == "Classe B — Ácidos graxos puros":
            with st.expander("Classe B — Ajuste fino por Ácidos graxos puros", expanded=True):
                colsB = st.columns(4)
                for idx, fa in enumerate(FA_ORDER):
                    with colsB[idx % 4]:
                        B_vals[fa] = st.slider(
                            f"FA {fa}", min_value=0.0, max_value=100.0, value=0.0, step=1.0,
                            key=f"slider_fa_{fa}", help="Percentual no blend (%)"
                        )
                total_B = sum(B_vals.values())
                _badge_total(total_B, "Total Classe B")
                if total_B > 30:
                    st.warning("A Classe B excede 30% do blend — considere reduzir para manter o caráter do óleo base.")

        C_vals = OrderedDict((k, 0.0) for k, _ in INGREDIENTS)
        total_C = 0.0
        if method == "Classe C — Ingredientes":
            with st.expander("Classe C — Ajuste fino por Ingredientes", expanded=True):
                colsC = st.columns(4)
                for idx, (k, label) in enumerate(INGREDIENTS):
                    with colsC[idx % 4]:
                        C_vals[k] = st.slider(
                            f"{label} (ajuste)", min_value=0.0, max_value=100.0, value=0.0, step=1.0,
                            key=f"slider_adj_{k}", help="Percentual no blend (%)"
                        )
                total_C = sum(C_vals.values())
                _badge_total(total_C, "Total Classe C")
                if total_C > 30:
                    st.warning("A Classe C excede 30% do blend — considere reduzir para manter o caráter do óleo base.")

        total_all = total_A + (total_B if method.startswith("Classe B") else total_C)
        st.markdown("---")
        _badge_total(total_all, "Total Global (A + Ajuste)")
        if total_all > 0 and st.button("🔄 Normalizar Global (A + Ajuste) para 100%", key="btn_norm_AB_or_AC"):
            scale = 100.0 / total_all
            for k in A_vals: A_vals[k] *= scale
            if method.startswith("Classe B"):
                for k in B_vals: B_vals[k] *= scale
            else:
                for k in C_vals: C_vals[k] *= scale
            for k, v in A_vals.items(): st.session_state[f"slider_ing_{k}"] = round(v, 2)
            if method.startswith("Classe B"):
                for fa, v in B_vals.items(): st.session_state[f"slider_fa_{fa}"] = round(v, 2)
            else:
                for k, v in C_vals.items(): st.session_state[f"slider_adj_{k}"] = round(v, 2)
            st.experimental_rerun()

        fa_est = {k: 0.0 for k in FA_ORDER}
        if total_all > 0:
            for ing_key, pct in A_vals.items():
                if pct <= 0: continue
                w = pct / total_all
                prof = _get_profile(ing_key, scenario if consider_var else "mean")
                for fa_key, fa_pct in prof.items():
                    fa_est[fa_key] += w * fa_pct
            if method.startswith("Classe B"):
                for fa_key, pct in B_vals.items():
                    if pct <= 0: continue
                    w = pct / total_all
                    fa_est[fa_key] += w * 100.0
            else:
                for ing_key, pct in C_vals.items():
                    if pct <= 0: continue
                    w = pct / total_all
                    prof = _get_profile(ing_key, scenario if consider_var else "mean")
                    for fa_key, fa_pct in prof.items():
                        fa_est[fa_key] += w * fa_pct

        fa_est = _normalize_percentages(fa_est)

        II = iodine_index(fa_est); ISap = saponification_index(fa_est); PF_proxy = melt_proxy(fa_est)
        st.markdown("---")
        st.subheader("KPIs (estimados a partir de perfis médios + ajuste selecionado)")
        c1, c2, c3 = st.columns(3)
        c1.metric("Índice de Iodo (II)", f"{II:.1f}")
        c2.metric("Índice de Saponificação (ISap)", f"{ISap:.1f} mgKOH/g")
        c3.metric("Ponto de Fusão (proxy, 0–100)", f"{PF_proxy:.0f}")
        st.caption("⚠️ Estimativas. Para decisões técnicas, use **Upload de perfil real**.")

        # ——— Expanders com faixas típicas (somente no heurístico) ———
        e1, e2, e3 = st.columns(3)
        with e1:
            with st.expander("ℹ️ Faixas típicas — II (estimativo)"):
                st.markdown(
                    "- **RBD (Palma)**: ~50–55\n"
                    "- **Estearina de Palma**: ~32–42\n"
                    "- **Oleína de Palma**: ~55–65\n"
                    "- **RPKO (Palmiste)**: ~14–22\n"
                    "- **Estearina de Palmiste**: ~8–14\n"
                    "- **Oleína de Palmiste**: ~18–28\n"
                    "- **PFAD**: ~45–55\n"
                    "- **Soapstock**: ~50–65\n"
                    "_Obs.: faixas orientativas com base em literatura/mercado; variam por lote/processo._"
                )
        with e2:
            with st.expander("ℹ️ Faixas típicas — ISap (mgKOH/g, estimativo)"):
                st.markdown(
                    "- **RBD (Palma)**: ~190–205\n"
                    "- **Estearina de Palma**: ~185–200\n"
                    "- **Oleína de Palma**: ~195–205\n"
                    "- **RPKO (Palmiste)**: ~240–255\n"
                    "- **Estearina de Palmiste**: ~235–250\n"
                    "- **Oleína de Palmiste**: ~240–255\n"
                    "- **PFAD**: ~185–205\n"
                    "- **Soapstock**: ~185–210\n"
                    "_Estimativas por perfil FA; confirmar com dados de bancada._"
                )
        with e3:
            with st.expander("ℹ️ Faixas típicas — Ponto de Fusão (proxy 0–100)"):
                st.markdown(
                    "- **Mais saturados/estearinas** → **proxy alto** (textura firme)\n"
                    "- **Mais insaturados/oleínas** → **proxy baixo** (toque fluido)\n"
                    "_O valor é um **índice** (0–100) como **proxy** de MP real._"
                )

        st.info("📄 Após finalizar sua formulação, gere o dossiê completo na aba **Exportação PDF** (perfil FA, KPIs, preview e narrativa).")
        with st.expander("🌱 Integração narrativa (ESG) — recomendações de apresentação do blend"):
            st.markdown(
                "- **Upcycling e origem**: destaque **PFAD** e **soapstock** como rotas de **reaproveitamento**; cite rastreio e fornecedores quando houver.\n"
                "- **Consistência de qualidade**: use **variabilidade de lote (Min/Típico/Max)** para mostrar **faixas de KPI** (robustez do blend).\n"
                "- **Claims alinhados**: conecte KPIs a atributos de uso:\n"
                "  - **II↓ / PF↑** → texturas mais firmes, toque menos oleoso (mãos/rosto).\n"
                "  - **ISap↑** → base interessante para saboaria/shampoo sólido (palmiste/estearina).\n"
                "  - **Insaturados↑ (oleico/linoleico)** → espalhabilidade e nutrição (corpo/cabelos).\n"
                "- **Compliance**: para **soapstock/PFAD**, mencionar **refino/esterificação** e dossiê regulatório antes de claims cosméticos."
            )

        g1, g2 = st.columns(2)
        with g1: plot_fa_bars(fa_est)
        with g2:
            _, radar_vals = finalidade_scores(fa_est, PF_proxy, II)
            plot_radar(radar_vals)

        st.markdown("---")
        st.subheader("Análise de Trade-offs (variação de +5% em cada ingrediente da Classe A)")
        trade = _compute_tradeoffs_heuristico(
            A_vals=A_vals, method=method, B_vals=B_vals, C_vals=C_vals,
            consider_var=consider_var, scenario=scenario
        )
        if trade is None:
            st.caption("Defina a base (Classe A) para visualizar os trade-offs.")
        else:
            labels, dII, dIS, dPF = trade
            cto1, cto2, cto3 = st.columns(3)
            with cto1: _plot_tradeoff_bars("Δ Índice de Iodo (II)", labels, dII, "Δ II")
            with cto2: _plot_tradeoff_bars("Δ Índice de Saponificação (ISap)", labels, dIS, "Δ ISap")
            with cto3: _plot_tradeoff_bars("Δ Ponto de Fusão (proxy)", labels, dPF, "Δ PF")
            st.caption("Leitura: as barras mostram como **cada ingrediente** alteraria os KPIs ao variar **+5%** (renormalizado).")

        st.subheader("Preview de notas por finalidade (0–100) – estimativas")
        scores, _ = finalidade_scores(fa_est, PF_proxy, II)
        p1, p2, p3, p4 = st.columns(4)
        p1.metric("Mãos", f"{scores['Mãos']}"); p2.metric("Corpo", f"{scores['Corpo']}")
        p3.metric("Rosto", f"{scores['Rosto']}"); p4.metric("Cabelos", f"{scores['Cabelos']}")

        st.markdown("---")
        st.subheader("Salvar / Carregar Blend (JSON)")
        heur_blend = {
            "modo": "heuristico",
            "classeA_pct": {k: float(v) for k, v in A_vals.items()},
            "classeB_pct": {k: float(v) for k, v in B_vals.items()},
            "classeC_pct": {k: float(v) for k, v in C_vals.items()},
            "ajuste_method": "B" if method.startswith("Classe B") else "C",
            "fa_profile": _normalize_percentages(fa_est),
            "total_pct": float(total_all),
            "variabilidade": {"ativada": bool(consider_var), "cenario": scenario},
            "nota": "Heurístico com Classe A (base) + ajuste fino (B=FA puros OU C=Ingredientes). KPIs estimados.",
        }
        cjs1, cjs2 = st.columns(2)
        with cjs1:
            st.download_button(
                label="💾 Baixar Blend (JSON)",
                data=json.dumps(heur_blend, ensure_ascii=False, indent=2).encode("utf-8"),
                file_name="blend_heuristico_ajuste.json",
                mime="application/json",
                key="dl_blend_heuristico_ajuste.json",
            )
        with cjs2:
            uploaded_json = st.file_uploader("📂 Carregar Blend (JSON)", type=["json"], key="blend_json_upload_heur")
            if uploaded_json is not None:
                try:
                    loaded = json.load(uploaded_json)
                    if loaded.get("modo") == "heuristico":
                        for k, v in loaded.get("classeA_pct", {}).items():
                            st.session_state[f"slider_ing_{k}"] = float(v)
                        for k, v in loaded.get("classeB_pct", {}).items():
                            st.session_state[f"slider_fa_{k}"] = float(v)
                        for k, v in loaded.get("classeC_pct", {}).items():
                            st.session_state[f"slider_adj_{k}"] = float(v)
                        st.session_state["blend"] = loaded
                        st.success("Blend heurístico (A + ajuste) carregado e sliders atualizados.")
                        st.experimental_rerun()
                    else:
                        st.warning("JSON não parece ser um blend heurístico.")
                except Exception as e:
                    st.error(f"Erro ao carregar JSON: {e}")

        st.markdown("---")
        st.info("Pronto para detalhar por finalidade no **Assistente de Formulação** (estimativa baseada em heurística).")
        assist_payload = {
            "fa_profile": fa_est,
            "kpis": {"II": II, "ISap": ISap, "PF_proxy": PF_proxy},
            "scores_preview": scores,
            "source": "heuristica_estimada_A+" + ("B" if method.startswith("Classe B") else "C"),
            "classes": {"A": dict(A_vals), "B": dict(B_vals), "C": dict(C_vals)},
            "variabilidade": {"ativada": bool(consider_var), "cenario": scenario},
        }

             st.session_state["assist_payload"] = assist_payload
         if st.button("➜ Enviar para Assistente de Formulação", key="btn_handoff_assist_real_adj"):
             st.session_state["go_to_assistente"] = True
             st.success("Perfil enviado (Upload + Ajuste fino). Abra a aba **Assistente de Formulação** para continuar.")
         else:
         st.caption("Carregue um **perfil de ácidos graxos** (ou ingredientes) para habilitar KPIs, gráficos e ajuste fino.")

# ======================================================================
# TAB 3 — ASSISTENTE DE FORMULAÇÃO (placeholder leve)
# ======================================================================
with tabs[3]:
    st.header("Assistente de Formulação 👩‍🔬")
    st.caption("Ajuste por **ocasião de uso** e **essências** a partir do payload recebido da aba **Blend Enzimático**.")
    payload = st.session_state.get("assist_payload")
    if payload:
        st.json(payload, expanded=False)
        st.success("Payload recebido. (Implemente a lógica específica desta aba conforme o escopo.)")
    else:
        st.info("Aguardando payload da aba **Blend Enzimático**.")

# ======================================================================
# TAB 4 — PROTOCOLO DE PRODUÇÃO (placeholder leve)
# ======================================================================
with tabs[4]:
    st.header("Protocolo de Produção ⚗️")
    st.caption("Defina parâmetros de processo, rendimentos e custo/kg.")
    st.info("Placeholder para o MVP. Cole aqui sua lógica original quando quiser.")

# ======================================================================
# TAB 5 — SUSTENTABILIDADE / ESG (placeholder leve)
# ======================================================================
with tabs[5]:
    st.header("Sustentabilidade / ESG 🌱")
    st.caption("Camada de ESG e métricas (RSPO, orgânico, fair trade, upcycling).")
    
    st.markdown("---")
    st.subheader("Sociobioeconomia (indicadores de origem) 🌎")
    st.caption("Indicadores de narrativa e diligência; não substituem certificações formais.")
    
    cA, cB, cC, cD = st.columns(4)
    with cA:
        origem = st.checkbox("Origem comunitária/cooperativa", False, key="pc_soc_origem")
    with cB:
        rastreio = st.checkbox("Rastreabilidade confirmada", False, key="pc_soc_rastreio")
    with cC:
        cert = st.checkbox("Certificação socioambiental (ex.: orgânico/fair)", False, key="pc_soc_cert")
    with cD:
        repart = st.checkbox("Repartição de benefícios documentada", False, key="pc_soc_repart")

    score_amz = 50 + 15*int(origem) + 15*int(rastreio) + 10*int(cert) + 10*int(repart)
    score_amz = max(0, min(100, score_amz))
    st.metric("Índice de Narrativa Amazônica", f"{score_amz} / 100")
    st.caption("Uso interno para comunicação; ampare claims com documentos (contratos, certificações, notas fiscais).")

# ======================================================================
# TAB 6 — RASTREABILIDADE (placeholder leve)
# ======================================================================
with tabs[6]:
    st.header("Rastreabilidade 🔍")
    st.caption("Ficha de ingredientes (fornecedor, lote, certificações) e exportação CSV.")
    st.info("Placeholder para o MVP. Cole aqui sua lógica original quando quiser.")

# ======================================================================
# TAB 7 — EXPORTAÇÃO PDF (placeholder leve)
# ======================================================================
with tabs[7]:
    st.header("Exportação PDF 📄")
    st.caption("Gere o dossiê do blend com perfil FA, KPIs, narrativa ESG e anexos.")
    st.info("Placeholder para o MVP. Cole aqui sua lógica original quando quiser.")

# ============ RODAPÉ ============
st.markdown("---")
st.markdown(
    "<p style='text-align: center; font-size: 14px;'>"
    "🌿 Desenvolvido por <b>OGTera - The Future of Oil Disruption</b>. "
    "Aplicação modular <b>LipidGenesis</b> com o módulo atual: <b>LipidPalma</b>. "
    "<br>Versão MVP demonstrativa. &copy; 2025 OGTera."
    "</p>",
    unsafe_allow_html=True
)
