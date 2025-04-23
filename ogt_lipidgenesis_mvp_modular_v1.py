import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="LipidGenesis - Estrutura Modular", layout="wide")

# ====== Dados dos insumos ======
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
referencia_natura = {
    "Temperatura": "55–60 ºC", "Índice de Acidez": 0.2, "Cor Lovibond (R)": "≤ 4.0",
    "Umidade (%)": "≤ 0.20", "Índice de Iodo": "37–45", "Índice de Saponificação": "193–213"
}

def calcular_blend(pA, pB, rA, rB):
    acidos = set(pA.keys()).union(pB.keys())
    return {a: round(pA.get(a,0)*rA + pB.get(a,0)*rB, 4) for a in sorted(acidos)}

def estimar_parametros(blend):
    iodo = round(sum([
        blend.get("C18:1",0)*0.86,
        blend.get("C18:2",0)*1.73,
        blend.get("C18:3",0)*2.62
    ]), 1)
    saponificacao = round(200 + np.random.uniform(-5, 5), 1)
    return {
        "Temperatura estimada": "58 ºC", "Índice de Acidez": 0.2,
        "Cor Lovibond (R)": "≤ 4.0", "Umidade (%)": "0.18",
        "Índice de Iodo": iodo, "Índice de Saponificação": saponificacao
    }

def gerar_perfil_sensorial(blend):
    return {
        "Doce (láurico)": blend.get("C12:0", 0)/10,
        "Verde (oleico)": blend.get("C18:1", 0)/10,
        "Cítrico (linoleico)": blend.get("C18:2", 0)/5,
        "Herbal (linolênico)": blend.get("C18:3", 0)/0.5,
        "Coco (caprílico)": blend.get("C8:0", 0)/3,
        "Frutado (mirístico)": blend.get("C14:0", 0)/5
    }

def estrutura_molecular(blend):
    grupos = {
        "SFA": sum([v for k, v in blend.items() if k in ["C6:0", "C8:0", "C10:0", "C12:0", "C14:0", "C16:0", "C18:0", "C20:0"]]),
        "MUFA": sum([v for k, v in blend.items() if k in ["C16:1", "C18:1", "C20:1"]]),
        "PUFA": sum([v for k, v in blend.items() if k in ["C18:2", "C18:3"]])
    }
    return grupos

# ====== UI Modular ======

st.title("LipidGenesis - MVP Modular")

# CAMADA A – ENTRADA
st.sidebar.header("Selecione a composição do Blend")
proporcao = st.sidebar.radio("Composição", ["82/18", "90/10"])
r_rbdt, r_rpko = (0.82, 0.18) if proporcao == "82/18" else (0.90, 0.10)
blend = calcular_blend(perfil_rbdt, perfil_rpko, r_rbdt, r_rpko)

# CAMADA B – RECEITA LIPÍDICA
if st.button("Gerar Receita Lipídica"):
    df = pd.DataFrame.from_dict(blend, orient="index", columns=["%"])
    st.subheader("Composição Lipídica do Blend")
    st.dataframe(df)
    st.bar_chart(df)

# CAMADA C – COMPARATIVO FÍSICO-QUÍMICO
    st.subheader("Parâmetros Físico-Químicos")
    estimado = estimar_parametros(blend)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Blend Personalizado**")
        for k,v in estimado.items():
            st.write(f"- {k}: {v}")
    with col2:
        st.markdown("**Blend Natura (Referência)**")
        for k,v in referencia_natura.items():
            st.write(f"- {k}: {v}")

# CAMADA D – SENSORIAL
if st.button("Gerar Receita Sensorial"):
    sensorial = gerar_perfil_sensorial(blend)
    st.subheader("Perfil Sensorial (Estimado por literatura)")
    labels = list(sensorial.keys())
    values = list(sensorial.values())
    values += values[:1]
    angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False).tolist() + [0]
    fig2, ax2 = plt.subplots(subplot_kw={'projection': 'polar'})
    ax2.plot(angles, values, 'r-', linewidth=2)
    ax2.fill(angles, values, 'r', alpha=0.25)
    ax2.set_xticks(angles[:-1])
    ax2.set_xticklabels(labels)
    st.pyplot(fig2)

# CAMADA E – VISUALIZAÇÃO MOLECULAR
    st.subheader("Visualização Estrutural Molecular")
    mol = estrutura_molecular(blend)
    df_mol = pd.DataFrame.from_dict(mol, orient="index", columns=["%"])
    st.bar_chart(df_mol)
    st.markdown("*Distribuição entre SFA / MUFA / PUFA. A estrutura controla os parâmetros físico-químicos.*")

# CAMADA F – ESG
st.markdown("---")
st.subheader("Painel ESG e Rastreabilidade")
st.markdown("- **Score ESG Simulado:** Alta sustentabilidade")
st.markdown("- **Origem dos Ingredientes:** Amazônia, Brasil")
st.markdown("- **QR Code:** (simulado)")
st.image("https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=https://example.com/supply-chain")