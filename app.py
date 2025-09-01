# app.py
# App principal do LipidGenesis / LipidPalma com abas modularizadas

import os
import streamlit as st

# ---- Config de página ----
try:
    st.set_page_config(page_title="LipidPalma – OGTera", layout="wide")
except Exception:
    pass

# ---- Defaults de sessão importantes para o MVP ----
_defaults = {
    "blend_mode_radio": "Heurísticas (rápido)",
    "ajuste_method_heur": "Classe B — Ácidos graxos puros",
    "ajuste_method_upload": "Classe B — Ácidos graxos puros",
    "formato_planilha": "Ingredientes (%)",
    "go_to_assistente": False,
}
for k, v in _defaults.items():
    st.session_state.setdefault(k, v)

# ---- Import das abas modularizadas (3 primeiras prontas) ----
# Certifique-se de ter estes arquivos no mesmo diretório:
# - home.py  -> deve expor: render_home(st)
# - proposta_cosmetica.py -> deve expor: render_proposta_cosmetica(st)
# - blend_enzimatico.py   -> deve expor: render_blend_enzimatico(st)

from home import render_home
from proposta_cosmetica import render_proposta_cosmetica
from blend_enzimatico import render_blend_enzimatico

# ---- Placeholders para as demais abas (mantém a ordem original) ----
def render_assistente_formulacao(st):
    st.header("Assistente de Formulação 👩‍🔬")
    st.caption("Ajuste por ocasião de uso e essências a partir do payload recebido da aba **Blend Enzimático**.")
    payload = st.session_state.get("assist_payload")
    if payload:
        st.json(payload, expanded=False)
        st.success("Payload recebido. (Implemente a lógica específica desta aba conforme o escopo.)")
    else:
        st.info("Aguardando payload da aba **Blend Enzimático**.")

def render_protocolo_producao(st):
    st.header("Protocolo de Produção ⚗️")
    st.caption("Defina parâmetros de processo, rendimentos e custo/kg.")
    st.info("Placeholder para o MVP. Cole aqui sua lógica original quando quiser.")

def render_esg(st):
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

def render_rastreabilidade(st):
    st.header("Rastreabilidade 🔍")
    st.caption("Ficha de ingredientes (fornecedor, lote, certificações) e exportação CSV.")
    st.info("Placeholder para o MVP. Cole aqui sua lógica original quando quiser.")

def render_exportacao_pdf(st):
    st.header("Exportação PDF 📄")
    st.caption("Gere o dossiê do blend com perfil FA, KPIs, narrativa ESG e anexos.")
    st.info("Placeholder para o MVP. Cole aqui sua lógica original quando quiser.")

# ---- Tabs (ordem original) ----
tabs = st.tabs([
    "Home",
    "Proposta Cosmética",
    "Blend Enzimático",
    "Assistente de Formulação",
    "Protocolo de Produção",
    "Sustentabilidade / ESG",
    "Rastreabilidade",
    "Exportação PDF",
])

with tabs[0]:
    render_home(st)

with tabs[1]:
    render_proposta_cosmetica(st)

with tabs[2]:
    render_blend_enzimatico()

with tabs[3]:
    render_assistente_formulacao(st)

with tabs[4]:
    render_protocolo_producao(st)

with tabs[5]:
    render_esg(st)

with tabs[6]:
    render_rastreabilidade(st)

with tabs[7]:
    render_exportacao_pdf(st)

# ---- Rodapé ----
st.markdown("---")
st.markdown(
    "<p style='text-align: center; font-size: 14px;'>"
    "🌿 Desenvolvido por <b>OGTera - The Future of Oil Disruption</b>. "
    "Aplicação modular <b>LipidGenesis</b> com o módulo atual: <b>LipidPalma</b>. "
    "<br>Versão MVP demonstrativa. &copy; 2025 OGTera."
    "</p>",
    unsafe_allow_html=True
)
