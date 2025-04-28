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

# === Título principal ===
st.title("🌿 LipidGenesis - Bioengineering Of Oils For Nextgen")
st.markdown("<h3 style='text-align: center; color: #4C9B9C;'>Produto: Blend LG 82/18 RBDT:RPKO</h3>", unsafe_allow_html=True)

# === Sidebar ===
st.sidebar.title("🔬 Configurações")
linha = st.sidebar.selectbox("Linha de Produto:", ["Ekos", "Chronos", "Tododia", "Mamãe e Bebê"], index=0)
ocasião = st.sidebar.selectbox("Ocasião de Uso:", ["Banho", "Rosto", "Corpo", "Cabelos"], index=0)

# === Funções ===
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

    # Título + Slogan (Ajustado para estilo refinado)
    pdf.set_font("Arial", 'B', 18)
    pdf.cell(200, 10, "LipidGenesis - Bioengineering Of Oils For Nextgen", ln=True, align='C')
    pdf.ln(10)

    # Produto centralizado
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "Produto: Blend LG 82/18 RBDT:RPKO", ln=True, align='C')
    pdf.ln(20)

    # Receita Lipídica - Tabela Bonita
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Receita Lipídica:", ln=True)
    pdf.set_font("Arial", '', 12)
    for i, row in df_lipidica.iterrows():
        pdf.cell(0, 10, f"{i}: {row['%']:.2f}%", ln=True)

    # Receita Sensorial
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Receita Sensorial:", ln=True)
    pdf.set_font("Arial", '', 12)
    pdf.multi_cell(0, 10, sensorial_txt)

    # Seção Gráficos
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Gráfico de Ácidos Graxos", ln=True)

    # Aqui você pode adicionar um gráfico (em PNG) gerado no Streamlit, se necessário

    caminho = "/mnt/data/relatorio_refinado_blendlg.pdf"
    pdf.output(caminho)
    return caminho

# === Interface ===
st.header("🔬 Análise Lipídica e Sensorial Refinada")

# Botões com design refinado
if st.button("🧪 Gerar Receita Lipídica", key="lipidica_btn"):
    df_lipidica = gerar_receita_lipidica(blend_lg)
    st.dataframe(df_lipidica)

if st.button("👃 Gerar Receita Sensorial", key="sensorial_btn"):
    sensorial_data = get_sensory_recipe(linha, ocasião)
    sensorial_txt = f"Ingrediente-chave: {sensorial_data['ingrediente']}\nNotas olfativas: {sensorial_data['notas']}\nEmoções evocadas: {sensorial_data['emoções']}\nEtiqueta sensorial: {sensorial_data['etiqueta']}"
    st.success(sensorial_txt)

# Estilo visual para o gráfico
st.subheader("📊 Perfil de Ácidos Graxos no Blend LG")
df_blend_lg = gerar_receita_lipidica(blend_lg)
fig = px.bar(df_blend_lg.reset_index(), x='Ácido Graxo', y='%', title='Distribuição dos Ácidos Graxos', template="plotly_dark")
st.plotly_chart(fig, use_container_width=True)

# === Indicadores Ambientais e ESG ===
st.subheader("🌎 Indicadores Ambientais e ESG")

# Benchmark de CO₂ eq/kg de algumas empresas do setor
benchmark_co2 = {
    "Natura": 1.25,  # Emissões do blend da Natura
    "Unilever": 1.20,  # Benchmark do setor (valores hipotéticos)
    "Johnson & Johnson": 1.15,  # Benchmark de outra empresa do setor (hipotético)
    "LipidGenesis": 0.98  # Sua pegada de CO₂ eq/kg
}

# Cálculo da diferença entre seu produto e os benchmarks
for company, co2_value in benchmark_co2.items():
    delta = (co2_value - benchmark_co2["LipidGenesis"]) / co2_value * 100
    st.metric(f"Emissão de CO₂ eq/kg ({company})", f"{co2_value:.2f}", delta=f"{delta:.1f}%", delta_color="inverse" if delta > 0 else "normal")

# Adicionando outros indicadores ambientais como água, energia, e impacto social
# (Os valores aqui são fictícios e podem ser ajustados conforme necessário)
impacto_ambiental = {
    "Água Consumida (L/kg)": {
        "LipidGenesis": 5.0,  # Exemplo de valor
        "Natura": 6.5,
        "Unilever": 7.0,
        "Johnson & Johnson": 5.5
    },
    "Uso de Energia (kWh/kg)": {
        "LipidGenesis": 0.25,
        "Natura": 0.30,
        "Unilever": 0.28,
        "Johnson & Johnson": 0.35
    }
}

# Exibir os dados de impacto ambiental em tabelas comparativas
for indicator, values in impacto_ambiental.items():
    st.subheader(f"Impacto Ambiental - {indicator}")
    df_impacto = pd.DataFrame.from_dict(values, orient='index', columns=[indicator])
    st.dataframe(df_impacto)

# Estilos refinados para facilitar a leitura e a comparação visual
st.markdown("""
    <style>
        .css-1d391kg { font-size: 1.2em; font-weight: bold; color: #00796B;}
        .css-15zrgfz { font-size: 1.2em; font-weight: bold; color: #388E3C;}
        .css-yyb8g4 { background-color: #F1F8E9; }
    </style>
""", unsafe_allow_html=True)

# === Rodapé ===
st.markdown("""
    <footer style="background-color: #4C9B9C; color: white; padding: 10px; text-align: center; font-size: 12px;">
        <p>&copy; 2025 LipidGenesis | Bioengineering Of Oils For Nextgen</p>
        <p>Todos os direitos reservados. Sustentabilidade e inovação em cada gota.</p>
        <p><a href="https://www.ogt.com" style="color: white; text-decoration: underline;">www.ogt.com</a></p>
    </footer>
""", unsafe_allow_html=True)
