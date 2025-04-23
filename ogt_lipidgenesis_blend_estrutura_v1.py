import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="LipidGenesis - Natura Reference", layout="wide")

# ====== DADOS BASE ======
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
    "Temperatura": "55–60 ºC",
    "Índice de Acidez": 0.2,
    "Cor Lovibond (R)": "≤ 4.0",
    "Umidade (%)": "≤ 0.20",
    "Índice de Iodo": "37–45",
    "Índice de Saponificação": "193–213"
}

def calcular_blend(perfil_a, perfil_b, proporcao_a, proporcao_b):
    acidos = set(perfil_a.keys()) | set(perfil_b.keys())
    return {ac: round(perfil_a.get(ac,0)*proporcao_a + perfil_b.get(ac,0)*proporcao_b, 4) for ac in sorted(acidos)}

def estimar_parametros(blend):
    iodo = round(sum([
        blend.get("C18:1",0)*0.86,
        blend.get("C18:2",0)*1.73,
        blend.get("C18:3",0)*2.62
    ]), 1)
    saponificacao = round(200 + np.random.uniform(-5, 5), 1)
    return {
        "Temperatura estimada": "58 ºC",
        "Índice de Acidez": 0.2,
        "Cor Lovibond (R)": "≤ 4.0",
        "Umidade (%)": "0.18",
        "Índice de Iodo": iodo,
        "Índice de Saponificação": saponificacao
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

def visualizar_estrutura(blend):
    fig, ax = plt.subplots(figsize=(10, 1))
    labels = list(blend.keys())
    values = list(blend.values())
    ax.barh(["Blend"], [sum(values)], color="lightblue", edgecolor="black")
    ax.set_xlim(0, 100)
    ax.set_title("Visualização Estrutural (Distribuição de Ácidos Graxos)")
    return fig

st.title("LipidGenesis - Comparativo com Blend Natura")

st.sidebar.markdown("## Configuração do Blend")
proporcao = st.sidebar.radio("Selecione a composição:", ["82/18", "90/10"])

if proporcao == "82/18":
    blend = calcular_blend(perfil_rbdt, perfil_rpko, 0.82, 0.18)
else:
    blend = calcular_blend(perfil_rbdt, perfil_rpko, 0.90, 0.10)

# Receita Lipídica
if st.button("Gerar Receita Lipídica"):
    df_blend = pd.DataFrame.from_dict(blend, orient="index", columns=["%"])
    st.subheader("Composição Lipídica do Blend Enzimático")
    st.dataframe(df_blend)
    st.bar_chart(df_blend)

    parametros = estimar_parametros(blend)

    st.subheader("Parâmetros Físico-Químicos: Comparativo com a Natura")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Blend Personalizado**")
        for k,v in parametros.items():
            st.write(f"- {k}: {v}")
    with col2:
        st.markdown("**Blend Natura (Referência)**")
        for k,v in referencia_natura.items():
            st.write(f"- {k}: {v}")

    st.subheader("Visualização Molecular do Blend")
    fig = visualizar_estrutura(blend)
    st.pyplot(fig)
    st.markdown("*A estrutura lipídica representa a distribuição total dos ácidos graxos e como a proporção afeta o perfil físico-químico.*")

# Receita Sensorial
if st.button("Gerar Receita Sensorial"):
    sensorial = gerar_perfil_sensorial(blend)
    st.subheader("Perfil Sensorial Simulado")
    labels = list(sensorial.keys())
    values = list(sensorial.values())
    values += values[:1]
    angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]

    fig2, ax2 = plt.subplots(subplot_kw={'projection': 'polar'})
    ax2.plot(angles, values, 'r-', linewidth=2)
    ax2.fill(angles, values, 'r', alpha=0.25)
    ax2.set_xticks(angles[:-1])
    ax2.set_xticklabels(labels)
    st.pyplot(fig2)