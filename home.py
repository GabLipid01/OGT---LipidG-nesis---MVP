# home.py
import os
import streamlit as st

def render_home(st):
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

        # Mockup cosmético
        col1, col2, col3 = st.columns([2,2,1])
        with col2:
            if os.path.exists("cosmetico.png.PNG.jpeg"):
                st.image("cosmetico.png.PNG.jpeg", width=400)

    st.markdown("---")

    # --- KPIs institucionais em linha única ---
    k1, k2, k3, k4 = st.columns(4)
    with k1: st.metric("Indústria-alvo", "Cosméticos")
    with k2: st.metric("Rota", "Enzimática")
    with k3: st.metric("Plataforma", "LipidGenesis")
    with k4: st.metric("Módulo", "LipidPalma™")

    st.markdown("---")

    # --- Camadas de confiança ---
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
