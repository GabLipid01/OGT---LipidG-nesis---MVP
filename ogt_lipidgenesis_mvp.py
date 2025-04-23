
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import qrcode
from io import BytesIO
from PIL import Image

st.set_page_config(page_title="OGT LipidGenesis", layout="wide")

# ====== HEADER ======
st.markdown("# LipidGenesis")
st.markdown("### Personalized Lipid Architectures")
st.markdown("##### *The Future of Disruption, On Demand*")
st.markdown("---")

# ====== SIDEBAR ======
st.sidebar.header("Seleção do Produto Base")
produto_base = st.sidebar.selectbox("Selecione o produto", ["RPKO", "RBDT", "RPRO"])

st.sidebar.header("Proporção do Blend")
blend_ratio = st.sidebar.slider("LG-8218 N-Soft (oleína) vs LG-8218 N-Structured (estearina)", 0, 100, 50)

st.sidebar.header("Upload de Dados")
uploaded_file = st.sidebar.file_uploader("Upload de Composição de Ácidos Graxos (.csv / .xlsx)")
gc_placeholder = st.sidebar.file_uploader("Upload de Espectro GC (futuro placeholder)")

if st.sidebar.button("Gerar Blend Personalizado"):
    st.session_state['gerar'] = True

# ====== BLOCO PRINCIPAL ======

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Visualização da Composição Lipídica")
    labels = ["SFA", "MUFA", "PUFA"]
    values = [blend_ratio * 0.5, (100 - blend_ratio) * 0.3, (100 - blend_ratio) * 0.2]
    fig, ax = plt.subplots()
    ax.bar(labels, values, color=["#1f77b4", "#aec7e8", "#98df8a"])
    st.pyplot(fig)

    st.subheader("Camada Sensorial (Temporária)")
    radar_labels = np.array(["Doce", "Herbal", "Ranço", "Cítrico", "Frutado"])
    radar_values = np.random.rand(5) * 5
    radar_values = np.append(radar_values, radar_values[0])  # fechar o gráfico

    fig2, ax2 = plt.subplots(subplot_kw={'projection': 'polar'})
    angles = np.linspace(0, 2 * np.pi, len(radar_labels), endpoint=False).tolist()
    angles += angles[:1]
    ax2.plot(angles, radar_values, 'b-', linewidth=2)
    ax2.fill(angles, radar_values, 'b', alpha=0.25)
    ax2.set_xticks(angles[:-1])
    ax2.set_xticklabels(radar_labels)
    st.pyplot(fig2)

with col2:
    st.subheader("Simulação de Parâmetros Físico-Químicos")
    st.markdown(f"""
    - **Índice de acidez:** {round(blend_ratio * 0.004, 2)}  
    - **Cor Lovibond (R/Y):** {round(blend_ratio * 0.11, 2)}  
    - **Umidade estimada:** {round(0.1 + (100 - blend_ratio) * 0.002, 2)} %  
    - **Ponto de fusão:** {round(24 + blend_ratio * 0.25, 1)} ºC  
    - **Índice de iodo:** {round(40 + (100 - blend_ratio) * 0.3)}  
    - **Índice de saponificação:** {round(190 - blend_ratio * 0.4)}  
    - **Viscosidade estimada:** {round(30 + blend_ratio * 0.25)}  
    """)

# ====== RECEITA FINAL ======
st.markdown("### Receita Final")
st.markdown("**Receita Lipídica Gerada:** baseada no blend selecionado.")
st.markdown("*Receita Sensorial (fictícia): baseada em espectro simulado.*")
colpdf, coljson = st.columns(2)
colpdf.button("Exportar como .pdf")
coljson.button("Exportar como .json")

# ====== ESG + QR CODE ======
st.markdown("---")
col_esg1, col_esg2 = st.columns(2)

with col_esg1:
    st.subheader("ESG + Rastreabilidade")
    st.markdown("- **ESG Score Simulado:** Alta sustentabilidade")
    st.markdown("- **Pegada de carbono estimada:** 0.34 kg CO2 eq/kg")
    st.markdown("- **Origem rastreável dos ingredientes (mock)**")

with col_esg2:
    st.subheader("QR Code de Rastreabilidade")
    qr = qrcode.make("https://example.com/supply-chain")
    buf = BytesIO()
    qr.save(buf)
    img = Image.open(buf)
    st.image(img, caption="https://example.com/supply-chain", width=200)

# ====== FOOTER ======
st.markdown("---")
st.markdown("© 2025 OGT - The Future of Disruption, On Demand")
