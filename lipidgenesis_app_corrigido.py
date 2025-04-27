import streamlit as st
import pandas as pd
import plotly.express as px
from fpdf import FPDF

# === Perfis de Ácidos Graxos (Codex Alimentarius) ===
RPKO_PROFILE = {
    "C6:0": 0.5, "C8:0": 4.3, "C10:0": 3.8, "C12:0": 50.0,
    "C14:0": 16.0, "C16:0": 8.3, "C16:1": 0.1, "C18:0": 2.0,
    "C18:1": 15.5, "C18:2": 2.25, "C18:3": 0.1, "C20:0": 0.1, "C20:1": 0.0
}

RBDT_PROFILE = {
    "C12:0": 0.5, "C14:0": 0.75, "C16:0": 43.4, "C16:1": 0.3,
    "C18:0": 5.0, "C18:1": 40.0, "C18:2": 10.5, "C18:3": 0.2,
    "C20:0": 0.3, "C20:1": 0.2
}

blend_lg = {k: 0.18 * RPKO_PROFILE.get(k, 0) + 0.82 * RBDT_PROFILE.get(k, 0) for k in set(RPKO_PROFILE) | set(RBDT_PROFILE)}

st.set_page_config(page_title="LipidGenesis - Blend LG", layout="wide")
st.title("🌿 LipidGenesis")
st.markdown("**Bioengineering Of Oils For Nextgen**")
st.markdown("*Produto: Blend LG 82/18 RBDT:RPKO*")

# Sidebar
st.sidebar.title("🔬 Configurações")
linha = st.sidebar.selectbox("Linha de Produto:", ["Ekos", "Chronos", "Tododia", "Mamãe e Bebê"])
ocasião = st.sidebar.selectbox("Ocasião de Uso:", ["Banho", "Rosto", "Corpo", "Cabelos"])

# Funções

def gerar_receita_lipidica(blend):
    df = pd.DataFrame.from_dict(blend, orient='index', columns=['%'])
    df.index.name = 'Ácido Graxo'
    return df

def get_sensory_recipe(line, occasion):
    aromatic_profiles = {
        "Ekos": {
            "Banho": {"ingrediente": "Breu-branco", "notas": "Balsâmico, incensado", "emoções": "Purificação", "etiqueta": "A floresta viva no vapor."},
            "Rosto": {"ingrediente": "Priprioca", "notas": "Terroso, doce", "emoções": "Enraizamento", "etiqueta": "A raiz que ancora a pele."},
            "Corpo": {"ingrediente": "Castanha-do-Pará", "notas": "Cremoso, doce", "emoções": "Nutrição", "etiqueta": "Abundância amazônica."},
            "Cabelos": {"ingrediente": "Andiroba", "notas": "Herbal-amargo", "emoções": "Força", "etiqueta": "Força medicinal."}
        },
        "Chronos": {
            "Banho": {"ingrediente": "Chá-verde", "notas": "Verde, fresco", "emoções": "Renovação", "etiqueta": "Frescor técnico."},
            "Rosto": {"ingrediente": "Copaíba", "notas": "Amadeirado suave", "emoções": "Serenidade", "etiqueta": "Amadeirado calmo."},
            "Corpo": {"ingrediente": "Pequi", "notas": "Frutado-oleoso", "emoções": "Originalidade", "etiqueta": "Verde do cerrado."},
            "Cabelos": {"ingrediente": "Tucumã", "notas": "Vegetal denso", "emoções": "Reconstrução", "etiqueta": "Textura rica."}
        },
        "Tododia": {
            "Banho": {"ingrediente": "Pitanga", "notas": "Frutado, cítrico", "emoções": "Alegria", "etiqueta": "Explosão cítrica."},
            "Rosto": {"ingrediente": "Maracujá", "notas": "Frutado ácido", "emoções": "Tranquilidade", "etiqueta": "Leveza tropical."},
            "Corpo": {"ingrediente": "Cupuaçu", "notas": "Doce, manteigado", "emoções": "Aconchego", "etiqueta": "Tropical amanteigado."},
            "Cabelos": {"ingrediente": "Murumuru", "notas": "Vegetal cremoso", "emoções": "Proteção", "etiqueta": "Densidade vegetal."}
        },
        "Mamãe e Bebê": {
            "Banho": {"ingrediente": "Lavanda", "notas": "Floral suave", "emoções": "Calmaria", "etiqueta": "Calma floral."},
            "Rosto": {"ingrediente": "Camomila", "notas": "Herbal adocicado", "emoções": "Aconchego", "etiqueta": "Silêncio na pele."},
            "Corpo": {"ingrediente": "Castanha de Caju", "notas": "Doce-leitosa", "emoções": "Suavidade", "etiqueta": "Cuidado natural."},
            "Cabelos": {"ingrediente": "Água de coco", "notas": "Aquático, refrescante", "emoções": "Frescor", "etiqueta": "Aroma que acalma."}
        }
    }
    return aromatic_profiles.get(line, {}).get(occasion, {"ingrediente": "N/A", "notas": "N/A", "emoções": "N/A", "etiqueta": "Não disponível."})

def gerar_pdf(df_lipidica, sensorial_txt):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, "Relatório Técnico - Blend LG", ln=True, align='C')
    pdf.ln(10)
    pdf.cell(0, 10, "Receita Lipídica:", ln=True)
    for i, row in df_lipidica.iterrows():
        pdf.cell(0, 10, f"{i}: {row['%']:.2f}%", ln=True)
    pdf.ln(10)
    pdf.cell(0, 10, "Receita Sensorial:", ln=True)
    pdf.multi_cell(0, 10, sensorial_txt)
    caminho = "/mnt/data/relatorio_blendlg.pdf"
    pdf.output(caminho)
    return caminho

# Interface
st.header("🔬 Análise Lipídica e Sensorial")

if st.button("🧪 Gerar Receita Lipídica"):
    df_lipidica = gerar_receita_lipidica(blend_lg)
    st.dataframe(df_lipidica)

if st.button("👃 Gerar Receita Sensorial"):
    sensorial_data = get_sensory_recipe(linha, ocasião)
    sensorial_txt = f"Ingrediente-chave: {sensorial_data['ingrediente']}\nNotas olfativas: {sensorial_data['notas']}\nEmoções evocadas: {sensorial_data['emoções']}\nEtiqueta sensorial: {sensorial_data['etiqueta']}"
    st.success(sensorial_txt)

st.subheader("📊 Perfil de Ácidos Graxos no Blend LG")
df_blend_lg = gerar_receita_lipidica(blend_lg)
fig = px.bar(df_blend_lg.reset_index(), x='Ácido Graxo', y='%', title='Distribuição dos Ácidos Graxos')
st.plotly_chart(fig, use_container_width=True)

st.subheader("🌎 Indicadores Ambientais e ESG")
natura_co2 = 1.25
lg_co2 = 0.98
st.metric("Emissão de CO₂ eq/kg", f"{lg_co2:.2f}", delta=f"{(natura_co2-lg_co2)/natura_co2*100:.1f}%", delta_color="inverse")

st.markdown("- **Redução de emissões**: Produção limpa.")
st.markdown("- **Fontes vegetais sustentáveis**.")
st.markdown("- **Impacto social positivo**.")
st.markdown("- **Governança ética**.")

if st.button("📄 Exportar Relatório PDF"):
    df_lipidica = gerar_receita_lipidica(blend_lg)
    sensorial_data = get_sensory_recipe(linha, ocasião)
    sensorial_txt = f"Ingrediente-chave: {sensorial_data['ingrediente']}\nNotas olfativas: {sensorial_data['notas']}\nEmoções evocadas: {sensorial_data['emoções']}\nEtiqueta sensorial: {sensorial_data['etiqueta']}"
    caminho_pdf = gerar_pdf(df_lipidica, sensorial_txt)
    st.markdown(f"**[Baixar Relatório PDF]({caminho_pdf})**")
