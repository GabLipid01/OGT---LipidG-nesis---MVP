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

# ====== PERFIS DE ÁCIDOS GRAXOS ======
perfil_rpko = {
    "C6:0": 0.1751, "C8:0": 2.7990, "C10:0": 2.7349, "C12:0": 40.7681,
    "C14:0": 14.8587, "C16:0": 11.8319, "C18:0": 0.0, "C18:1": 20.8017,
    "C18:2": 3.2454, "C20:0": 0.1446, "C20:1": 0.1049
}
perfil_rbdt = {
    "C10:0": 0.0, "C12:0": 0.4976, "C14:0": 0.8371, "C16:0": 38.1650,
    "C16:1": 0.1286, "C18:0": 5.1485, "C18:1": 45.3823, "C18:2": 9.6964,
    "C18:3": 0.1995, "C20:0": 0.3747, "C20:1": 0.1838
}

def calcular_blend(perfil_a, perfil_b, proporcao_a=0.82, proporcao_b=0.18):
    todos_acidos = set(perfil_a.keys()) | set(perfil_b.keys())
    blend = {}
    for acido in todos_acidos:
        val_a = perfil_a.get(acido, 0)
        val_b = perfil_b.get(acido, 0)
        blend[acido] = round(val_a * proporcao_a + val_b * proporcao_b, 4)
    return dict(sorted(blend.items()))

perfil_blend_8218 = calcular_blend(perfil_rpko, perfil_rbdt)

# ====== SIDEBAR ======
st.sidebar.header("Seleção de Produtos")

produtos_disponiveis = [
    "RPKO",
    "RBDT",
    "Blend 82/18 Palma e Palmiste Natura",
    "Blend LG 82/18 Oleína de Palma e Palmiste",
    "Blend LG 82/18 Palma e Palmiste"
]

selecionados = st.sidebar.multiselect(
    "Selecione um ou mais produtos base",
    produtos_disponiveis,
    default=["Blend 82/18 Palma e Palmiste Natura"]
)

# ====== PAINEL PRINCIPAL ======
st.subheader("Composição de Ácidos Graxos")

if "Blend 82/18 Palma e Palmiste Natura" in selecionados:
    dados = perfil_blend_8218
    df = pd.DataFrame.from_dict(dados, orient="index", columns=["%"])
    st.write("**Blend 82/18 Palma e Palmiste Natura (base: 82% RPKO + 18% RBDT)**")
    st.dataframe(df)
    st.bar_chart(df)

    st.markdown("### Simulação de Parâmetros Físico-Químicos")
    st.markdown("- **Temperatura estimada:** 58 °C")
    st.markdown("- **Índice de Acidez:** 0,2")
    st.markdown("- **Cor Lovibond (R/Y):** máx 4,0")
    st.markdown("- **Umidade estimada:** 0,18%")
    st.markdown("- **Índice de Iodo estimado:** 42,5")
    st.markdown("- **Índice de Saponificação estimado:** 202,5")

    st.markdown("### ESG e Rastreabilidade")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("- **ESG Score Simulado:** Alta sustentabilidade")
        st.markdown("- **Pegada de carbono estimada:** 0,34 kg CO2 eq/kg")
        st.markdown("- **Origem dos ingredientes:** Brasil (PA, AM)")

    with col2:
        st.markdown("#### QR Code de Rastreabilidade")
        qr = qrcode.make("https://example.com/supply-chain")
        buf = BytesIO()
        qr.save(buf)
        img = Image.open(buf)
        st.image(img, caption="https://example.com/supply-chain", width=200)

else:
    st.info("Selecione o blend 82/18 para visualizar a composição baseada em dados reais.")