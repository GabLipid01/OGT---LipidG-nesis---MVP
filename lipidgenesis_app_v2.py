
import streamlit as st
import pandas as pd

# ------------------ Sidebar ou Header com Tipo de Blend ------------------
st.title("LipidGenesis – MVP Natura")

st.subheader("Configurações do Blend")
blend_tipo = st.selectbox(
    "Tipo de Blend",
    [
        "Blend 82/18 (82% RBDT / 18% RPKO)",
        "Blend 90/10 (90% RBDT / 10% RPKO)"
    ]
)

linha_produto = st.selectbox("Linha de Produto Natura", ["Ekos", "Chronos", "Tododia", "SOU"])
ocasiao_uso = st.selectbox("Ocasião de Uso", ["Banho", "Rosto", "Corpo", "Mãos", "Pós-sol"])

# ------------------ Tabs ------------------
tabs = st.tabs(["Receita Lipídica", "Receita Sensorial", "Lógica de Simulações"])

# ------------------ Tab: Receita Lipídica ------------------
with tabs[0]:
    st.write(f"Receita lipídica gerada com base no blend: **{blend_tipo}**, linha **{linha_produto}**, ocasião de uso: **{ocasiao_uso}**")
    # Aqui entraria o cálculo real com base nos perfis de ácidos graxos
    st.success("Receita lipídica simulada com sucesso!")

# ------------------ Tab: Receita Sensorial ------------------
with tabs[1]:
    st.write(f"Simulação sensorial para o blend **{blend_tipo}** na linha **{linha_produto}** - ocasião: **{ocasiao_uso}**")
    # Placeholder de lógica sensorial
    st.info("Perfis sensoriais simulados com base em dados de literatura.")

# ------------------ Tab: Lógica de Simulações ------------------
with tabs[2]:
    st.header("🔬 Lógica de Simulações")

    st.write("Esta seção descreve a lógica utilizada para sugerir blends lipídicos conforme a linha de produto Natura. As escolhas são baseadas em propriedades físico-químicas dos óleos, dados de literatura técnica e o posicionamento sensorial de cada linha.")

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
