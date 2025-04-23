import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from fpdf import FPDF

# CONFIGURAÇÃO
st.set_page_config(page_title="LipidGenesis - Plataforma", layout="wide")
st.title("🌿 LipidGenesis - The Future of Disruption, On Demand")
st.markdown("#### Comparativo entre Blend Natura 82/18 e LG Blend 82/18")

# SIDEBAR
st.sidebar.title("🔬 Configurações")
linha = st.sidebar.selectbox("Escolha a linha de produto Natura:", ["Ekos", "Chronos", "Tododia", "Mamãe e Bebê"])
ocasião = st.sidebar.selectbox("Ocasião de uso:", ["Banho", "Rosto", "Corpo", "Cabelos"])

# PERFIS DE ÁCIDOS GRAXOS (valores hipotéticos)
perfil_rbdt = {'C16:0': 45.2, 'C18:0': 4.8, 'C18:1': 38.5, 'C18:2': 10.1, 'C18:3': 1.4}
perfil_rpko = {'C12:0': 48.0, 'C14:0': 16.0, 'C16:0': 10.5, 'C18:1': 15.3, 'C18:2': 10.2}
blend_natura = {k: 0.82 * perfil_rbdt.get(k, 0) + 0.18 * perfil_rpko.get(k, 0) for k in set(perfil_rbdt) | set(perfil_rpko)}
blend_lg = {k: 0.82 * perfil_rbdt.get(k, 0) + 0.18 * perfil_rpko.get(k, 0) + np.random.normal(0, 0.2) for k in set(perfil_rbdt) | set(perfil_rpko)}

# FUNÇÕES
def gerar_receita_lipidica(blend):
    df = pd.DataFrame.from_dict(blend, orient='index', columns=['%'])
    df.index.name = 'Ácido Graxo'
    return df

def gerar_receita_sensorial(linha, ocasião):
    notas = {
        "Ekos": {"Banho": "refrescante, leve", "Rosto": "suave, hidratante"},
        "Chronos": {"Rosto": "anti-idade, sedosa", "Corpo": "nutritiva, rica"},
        "Tododia": {"Banho": "aveludada, cremosa", "Corpo": "hidratante, reconfortante"},
        "Mamãe e Bebê": {"Banho": "delicada, suave", "Corpo": "protetora, calmante"}
    }
    sensorial = notas.get(linha, {}).get(ocasião, "neutra")
    return f"Perfil sensorial estimado: {sensorial}."

def mostrar_comparativo(blend1, blend2, titulo):
    df = pd.DataFrame({'Blend Natura': blend1, 'LG Blend': blend2})
    fig = px.bar(df, barmode='group', title=titulo, labels={'value': 'Composição (%)', 'index': 'Ácido Graxo'})
    st.plotly_chart(fig, use_container_width=True)

def mostrar_impacto_ambiental():
    natura = 1.25  # kg CO₂ eq / kg de produto
    lg = 0.98
    st.metric("🌍 Emissão CO₂ eq/kg", f"{lg:.2f}", delta=f"{(natura-lg)/natura*100:.1f}%", delta_color="inverse")

def mostrar_módulo_esg():
    st.subheader("📊 Indicadores ESG")
    col1, col2, col3 = st.columns(3)
    col1.metric("Energia renovável", "92%", "+12% vs concorrência")
    col2.metric("Insumos rastreáveis", "100%", "+25%")
    col3.metric("Água reutilizada", "68%", "+18%")

def gerar_pdf(df_lipidica, sensorial_txt):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Relatório Técnico - LipidGenesis", ln=True, align='C')
    pdf.ln(10)
    pdf.cell(200, 10, txt="Receita Lipídica:", ln=True)
    for i, row in df_lipidica.iterrows():
        pdf.cell(200, 10, txt=f"{i}: {row['%']:.2f}%", ln=True)
    pdf.ln(10)
    pdf.cell(200, 10, txt="Receita Sensorial:", ln=True)
    pdf.multi_cell(200, 10, txt=sensorial_txt)
    caminho = "/mnt/data/relatorio_lipidgenesis.pdf"
    pdf.output(caminho)
    return caminho

# INTERFACE PRINCIPAL
st.markdown("#### Receita Lipídica e Sensorial Personalizadas")

col1, col2 = st.columns(2)
with col1:
    if st.button("🧪 Gerar Receita Lipídica"):
        df_lipidica = gerar_receita_lipidica(blend_lg)
        st.dataframe(df_lipidica)
with col2:
    if st.button("👃 Gerar Receita Sensorial"):
        sensorial_txt = gerar_receita_sensorial(linha, ocasião)
        st.success(sensorial_txt)

# COMPARATIVO
mostrar_comparativo(blend_natura, blend_lg, "Comparativo de Ácidos Graxos")
mostrar_impacto_ambiental()
mostrar_módulo_esg()

# EXPORTAR
if st.button("📄 Exportar Relatório PDF"):
    df_lipidica = gerar_receita_lipidica(blend_lg)
    sensorial_txt = gerar_receita_sensorial(linha, ocasião)
    caminho_pdf = gerar_pdf(df_lipidica, sensorial_txt)
    with open(caminho_pdf, "rb") as f:
        st.download_button("⬇️ Baixar Relatório", f, file_name="relatorio_lipidgenesis.pdf")
