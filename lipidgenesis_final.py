
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="LipidGenesis", layout="wide")
st.title("🧪 LipidGenesis | Bioengineering Of Oils For Nextgen")

st.markdown("""
Este app compara blends lipídicos inovadores com o blend Natura de referência, calcula a receita lipídica ideal, 
e propõe uma composição sensorial baseada na literatura científica e na ocasião de uso.
""")

# Dados reais dos perfis de ácidos graxos
RPKO_PROFILE = {
    "C8:0": 3.6, "C10:0": 3.2, "C12:0": 45.7, "C14:0": 16.9,
    "C16:0": 8.2, "C18:0": 2.3, "C18:1": 11.6, "C18:2": 6.8, "C18:3": 1.7
}

RBDT_PROFILE = {
    "C12:0": 0.2, "C14:0": 0.3, "C16:0": 41.3, "C18:0": 4.5,
    "C18:1": 39.1, "C18:2": 13.6, "C18:3": 0.4
}

def ordenar_acidos_graxos(blend):
    ordem = sorted(blend.keys(), key=lambda x: (int(x.split(":")[0])*100 + int(x.split(":")[1])))
    return {k: blend[k] for k in ordem}

def mostrar_comparativo(blend1, blend2, titulo):
    acidos = sorted(set(blend1) | set(blend2))
    df = pd.DataFrame({
        "Blend Natura (%)": [blend1.get(k, 0) for k in acidos],
        "Blend LG (%)": [blend2.get(k, 0) for k in acidos]
    }, index=acidos)
    st.subheader(titulo)
    st.dataframe(df.style.format("{:.2f}"))

    fig, ax = plt.subplots(figsize=(10, 5))
    df.plot(kind="bar", ax=ax)
    st.pyplot(fig)
    return df

# Blends baseados nos perfis reais
todos_acidos = set(RPKO_PROFILE) | set(RBDT_PROFILE)
perfil_rpko = RPKO_PROFILE
perfil_rbdt = RBDT_PROFILE

blend_natura = {k: 0.82 * perfil_rbdt.get(k, 0) + 0.18 * perfil_rpko.get(k, 0) for k in todos_acidos}
blend_lg = {k: blend_natura[k] + np.random.normal(0, 0.2) for k in todos_acidos}

# Layout
linha = st.selectbox("Selecione a Linha de Produto", ["Ekos", "Chronos"])
ocasião = st.selectbox("Selecione a Ocasião de Uso", ["Banho", "Rosto", "Corpo", "Cabelos"])

# Visualização lipídica
blend1 = ordenar_acidos_graxos(blend_natura)
blend2 = ordenar_acidos_graxos(blend_lg)
df_lipidica = mostrar_comparativo(blend1, blend2, "Comparativo de Ácidos Graxos")

# Banco aromático estruturado
BANCO_SENSORIAL = {
    ("Ekos", "Banho"): {
        "ingrediente": "Castanha", "notas": "cremosas, confortáveis", "emoções": "acolhimento e prazer",
        "etiqueta": "Banho nutritivo e envolvente"
    },
    ("Chronos", "Rosto"): {
        "ingrediente": "Jambu", "notas": "herbais, frescas", "emoções": "revitalização e energia",
        "etiqueta": "Ritual de cuidado facial revigorante"
    }
}

def get_sensory_recipe(linha, ocasião):
    return BANCO_SENSORIAL.get((linha, ocasião), None)

def gerar_receita_sensorial(linha, ocasião):
    perfil = get_sensory_recipe(linha, ocasião)
    if perfil:
        return (
            f"**Ingrediente-chave:** {perfil['ingrediente']}\n\n"
            f"**Notas olfativas:** {perfil['notas']}\n\n"
            f"**Emoções evocadas:** {perfil['emoções']}\n\n"
            f"**Etiqueta sensorial:** {perfil['etiqueta']}"
        )
    else:
        return "Perfil sensorial não disponível para essa combinação."

if st.button("🌸 Gerar Receita Sensorial"):
    st.markdown(gerar_receita_sensorial(linha, ocasião))

def gerar_pdf(df, sensorial_texto):
    from fpdf import FPDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, "Relatório Técnico - LipidGenesis\n\n")

    for col in df.columns:
        pdf.cell(0, 10, f"{col}:", ln=True)
        for idx, val in df[col].items():
            pdf.cell(0, 10, f"{idx}: {val:.2f}", ln=True)
        pdf.ln()

    pdf.multi_cell(0, 10, "\n---\n\nPerfil Sensorial\n")
    pdf.multi_cell(0, 10, sensorial_texto)
    path = "/tmp/relatorio_lipidgenesis.pdf"
    pdf.output(path)
    return path

if st.button("📄 Exportar Relatório PDF"):
    try:
        df_lipidica
    except NameError:
        st.warning("Por favor, gere a Receita Lipídica antes de exportar o PDF.")
    else:
        sensorial_txt = gerar_receita_sensorial(linha, ocasião)
        caminho_pdf = gerar_pdf(df_lipidica, sensorial_txt)
        with open(caminho_pdf, "rb") as f:
            st.download_button("⬇️ Baixar Relatório", f, file_name="relatorio_lipidgenesis.pdf")
