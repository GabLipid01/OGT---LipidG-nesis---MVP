
import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("LipidGenesis – MVP Natura")

# ------------------ Sidebar ------------------
st.sidebar.title("🔬 Configurações")

# Novo selectbox para tipo de blend
blend_tipo = st.sidebar.selectbox(
    "Tipo de Blend:",
    [
        "Blend 82/18 (82% RBDT / 18% RPKO)",
        "Blend 90/10 (90% RBDT / 10% RPKO)"
    ]
)

linha = st.sidebar.selectbox("Linha de Produto Natura", ["Ekos", "Chronos", "Tododia", "SOU"])
ocasiao = st.sidebar.selectbox("Ocasião de Uso", ["Banho", "Rosto", "Corpo", "Mãos", "Pós-sol"])

# ------------------ Tabs ------------------
tabs = st.tabs(["Receita Lipídica", "Receita Sensorial", "Comparativo", "Lógica de Simulações"])

# ------------------ Tab 1: Receita Lipídica ------------------
with tabs[0]:
    st.header("Receita Lipídica Gerada")
    st.write(f"**Blend selecionado:** {blend_tipo}")
    st.write(f"**Linha:** {linha} | **Ocasião de uso:** {ocasiao}")
    st.success("Receita lipídica simulada com sucesso!")
    st.info("Aqui aparecerá a composição lipídica com base nos ácidos graxos reais.")

# ------------------ Tab 2: Receita Sensorial ------------------
with tabs[1]:
    st.header("Receita Sensorial Simulada")
    st.write(f"**Blend:** {blend_tipo} | **Linha:** {linha} | **Ocasião:** {ocasiao}")
    st.info("Perfis sensoriais simulados com base em dados da literatura.")

# ------------------ Tab 3: Comparativo ------------------
with tabs[2]:
    st.header("Comparativo com Blend Natura")
    st.warning("Simulação física-química e ambiental em desenvolvimento.")
    st.write("Aqui será exibida a comparação com os parâmetros do Blend Natura.")

# ------------------ Tab 4: Lógica de Simulações ------------------
with tabs[3]:
    st.header("🔍 Lógica de Simulações por Linha de Produto")

    st.write("Justificativas técnicas para cada combinação sugerida de blend conforme a linha de produto e ocasião de uso:")

    data = {
        "Linha": ["Ekos", "Chronos", "Tododia", "SOU"],
        "Objetivo Sensorial": ["Leve e aromático", "Estruturado e nutritivo", "Equilibrado", "Custo e sustentabilidade"],
        "Blend Sugerido": ["82/18", "90/10", "82/18", "90/10"],
        "Justificativa": [
            "Alta volatilidade e sensorial leve via RPKO",
            "Mais estrutura e barreira com RBDT",
            "Equilíbrio de custo e sensorialidade",
            "Menor custo e menor impacto ambiental"
        ]
    }
    df = pd.DataFrame(data)
    st.table(df)

    with st.expander("📚 Referências Científicas"):
        st.markdown("""
        - Pereira et al. (2020) - *Vegetable oils and sensory properties in cosmetics*
        - Costa, L. et al. (2018) - *Fatty Acid Profiles and Emollience in Tropical Oils*
        - Manual Técnico Natura (edição interna)
        - FAO/WHO - *Lipids in Functional Formulations* (2021)
        - PubChem / LipidMaps databases (2023)
        """)
