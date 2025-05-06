import streamlit as st
st.set_page_config(page_title="LipidGenesis - Blend LG", layout="wide")
import pandas as pd
import plotly.express as px
from fpdf import FPDF

# === Perfis de Ácidos Graxos (Codex Alimentarius) ===
FATTY_ACID_PROFILES = {
    "Palm Oil": {
        "C12:0": 0.2, "C14:0": 1.0, "C16:0": 44.0, "C16:1": 0.2,
        "C18:0": 4.5, "C18:1": 39.0, "C18:2": 10.0, "C18:3": 0.3,
        "C20:0": 0.2, "C20:1": 0.1
    },
    "Palm Olein": {
        "C12:0": 0.1, "C14:0": 1.0, "C16:0": 39.0, "C16:1": 0.2,
        "C18:0": 4.5, "C18:1": 43.5, "C18:2": 11.0, "C18:3": 0.3,
        "C20:0": 0.2, "C20:1": 0.2
    },
    "Palm Stearin": {
        "C14:0": 1.2, "C16:0": 56.0, "C16:1": 0.1, "C18:0": 6.5,
        "C18:1": 30.0, "C18:2": 5.0, "C18:3": 0.1, "C20:0": 0.3
    },
    "Palm Kernel Oil": {
        "C6:0": 0.2, "C8:0": 3.6, "C10:0": 3.5, "C12:0": 48.2,
        "C14:0": 16.2, "C16:0": 8.4, "C16:1": 0.1, "C18:0": 2.0,
        "C18:1": 15.3, "C18:2": 2.3, "C18:3": 0.1, "C20:0": 0.1
    },
    "Palm Kernel Olein": {
        "C6:0": 0.3, "C8:0": 4.0, "C10:0": 3.7, "C12:0": 49.5,
        "C14:0": 15.7, "C16:0": 8.0, "C16:1": 0.1, "C18:0": 1.9,
        "C18:1": 14.5, "C18:2": 2.1, "C18:3": 0.1, "C20:0": 0.1
    },
    "Palm Kernel Stearin": {
        "C8:0": 3.0, "C10:0": 3.0, "C12:0": 47.0, "C14:0": 17.5,
        "C16:0": 9.5, "C16:1": 0.1, "C18:0": 2.5, "C18:1": 14.0,
        "C18:2": 2.0, "C18:3": 0.1, "C20:0": 0.1
    }
}

# === Ícones/emojis sensoriais ===
SENSORY_EMOJIS = {
    "Purificação": "🧼", "Enraizamento": "🌱", "Nutrição": "🥥", "Força": "💪",
    "Renovação": "💧", "Serenidade": "🌿", "Originalidade": "🍑", "Reconstrução": "🔧",
    "Alegria": "😊", "Tranquilidade": "🍃", "Aconchego": "🛏️", "Proteção": "🛡️",
    "Calmaria": "🕊️", "Suavidade": "☁️", "Frescor": "🌬️"
}

# === Pirâmide olfativa visual ===
def exibir_piramide_olfativa(sensorial_data):
    st.subheader("🔺 Pirâmide Olfativa")
    with st.container():
        st.markdown(f\"\"\"
        <div style='text-align: center; font-size: 18px;'>
            <div><b>🌸 Topo:</b> {sensorial_data['notas'].split(',')[0].strip()}</div>
            <div><b>🌿 Corpo:</b> {sensorial_data['ingrediente']}</div>
            <div><b>🌳 Fundo:</b> {sensorial_data['notas'].split(',')[-1].strip()}</div>
        </div>
        \"\"\", unsafe_allow_html=True)

# === Storytelling de marca ===
def exibir_storytelling(sensorial_data):
    st.subheader("📖 Storytelling Sensorial")
    emoji = SENSORY_EMOJIS.get(sensorial_data['emoções'], "✨")
    st.markdown(f"**{emoji} {sensorial_data['etiqueta']}**")



# Sidebar: Sliders para montagem do blend personalizado
st.sidebar.markdown("### Monte seu Blend Personalizado (%)")

oil_keys = list(FATTY_ACID_PROFILES.keys())

# Captura das porcentagens via sliders
oil_percentages = {}
total_pct = 0
for oil in oil_keys:
    pct = st.sidebar.slider(f"{oil} (%)", 0, 100, 0, 1)
    oil_percentages[oil] = pct
    total_pct += pct

# Cálculo da média ponderada do perfil lipídico
blend_lg = {}
if total_pct == 0:
    st.warning("Defina pelo menos um óleo com percentual maior que 0.")
else:
    normalized = {k: v / total_pct for k, v in oil_percentages.items()}
    all_fatty_acids = set()
    for profile in FATTY_ACID_PROFILES.values():
        all_fatty_acids |= set(profile.keys())

    blend_lg = {
        fa: sum(normalized[oil] * FATTY_ACID_PROFILES[oil].get(fa, 0) for oil in oil_keys)
        for fa in all_fatty_acids
    }

# === Título principal ===
st.title("🌿 LipidGenesis - Bioengineering Of Oils For Nextgen")
st.markdown("<h3 style='text-align: center; color: #4C9B9C;'>PLATAFORMA DE FORMULAÇÃO PERSONALIZADA DE BLENDS DE PALMA E PALMISTE</h3>", unsafe_allow_html=True)
# === Importar BlendCalculator ===
from blend_calculator import BlendCalculator

# === Inicializar cálculo de blends ===
blend_calc = BlendCalculator('Blend_LG_Modelagem.xlsx')


# === Sidebar ===
st.sidebar.title("🔬 Configurações")
linha = st.sidebar.selectbox("Linha de Produto:", ["Vitalis", "Essentia", "Ardor", "Lúmina"], index=0)
ocasião = st.sidebar.selectbox("Ocasião de Uso:", ["Banho", "Rosto", "Corpo", "Cabelos"], index=0)

# Nome completo dos ácidos graxos
nomes_acidos = {
    "C6:0": "Ácido Capróico", "C8:0": "Ácido Caprílico", "C10:0": "Ácido Cáprico",
    "C12:0": "Ácido Láurico", "C14:0": "Ácido Mirístico", "C16:0": "Ácido Palmítico",
    "C16:1": "Ácido Palmitoleico", "C18:0": "Ácido Esteárico", "C18:1": "Ácido Oleico",
    "C18:2": "Ácido Linoleico", "C18:3": "Ácido Linolênico", "C20:0": "Ácido Araquídico",
    "C20:1": "Ácido Gadoleico"

}



# === Funções ===
def gerar_receita_lipidica(blend):
    df = pd.DataFrame.from_dict(blend, orient='index', columns=['%'])
    df.index.name = 'Ácido Graxo'
    df = df.reset_index()
    df['Nome Completo'] = df['Ácido Graxo'].apply(lambda x: f"{nomes_acidos.get(x, x)} ({x})")
    return df



# === Função para obter a receita sensorial ===
def get_sensory_recipe(line, occasion):
    aromatic_profiles = {
        "Vitalis": {  # Linha Vitalis
            "Banho": {"ingrediente": "Breu-branco", "notas": "Balsâmico, incensado", "emoções": "Purificação", "etiqueta": "A floresta viva no vapor."},
            "Rosto": {"ingrediente": "Priprioca", "notas": "Terroso, doce", "emoções": "Enraizamento", "etiqueta": "A raiz que ancora a pele."},
            "Corpo": {"ingrediente": "Castanha-do-Pará", "notas": "Cremoso, doce", "emoções": "Nutrição", "etiqueta": "Abundância amazônica."},
            "Cabelos": {"ingrediente": "Andiroba", "notas": "Herbal-amargo", "emoções": "Força", "etiqueta": "Força medicinal."}
        },
        "Essentia": {  # Linha Essentia
            "Banho": {"ingrediente": "Chá-verde", "notas": "Verde, fresco", "emoções": "Renovação", "etiqueta": "Frescor técnico."},
            "Rosto": {"ingrediente": "Copaíba", "notas": "Amadeirado suave", "emoções": "Serenidade", "etiqueta": "Amadeirado calmo."},
            "Corpo": {"ingrediente": "Pequi", "notas": "Frutado-oleoso", "emoções": "Originalidade", "etiqueta": "Verde do cerrado."},
            "Cabelos": {"ingrediente": "Tucumã", "notas": "Vegetal denso", "emoções": "Reconstrução", "etiqueta": "Textura rica."}
        },
        "Ardor": {  # Linha Ardor
            "Banho": {"ingrediente": "Pitanga", "notas": "Frutado, cítrico", "emoções": "Alegria", "etiqueta": "Explosão cítrica."},
            "Rosto": {"ingrediente": "Maracujá", "notas": "Frutado ácido", "emoções": "Tranquilidade", "etiqueta": "Leveza tropical."},
            "Corpo": {"ingrediente": "Cupuaçu", "notas": "Doce, manteigado", "emoções": "Aconchego", "etiqueta": "Tropical amanteigado."},
            "Cabelos": {"ingrediente": "Murumuru", "notas": "Vegetal cremoso", "emoções": "Proteção", "etiqueta": "Densidade vegetal."}
        },
        "Lúmina": {  # Linha Lúmina
            "Banho": {"ingrediente": "Lavanda", "notas": "Floral suave", "emoções": "Calmaria", "etiqueta": "Calma floral."},
            "Rosto": {"ingrediente": "Camomila", "notas": "Herbal adocicado", "emoções": "Aconchego", "etiqueta": "Silêncio na pele."},
            "Corpo": {"ingrediente": "Castanha de Caju", "notas": "Doce-leitosa", "emoções": "Suavidade", "etiqueta": "Cuidado natural."},
            "Cabelos": {"ingrediente": "Água de coco", "notas": "Aquático, refrescante", "emoções": "Frescor", "etiqueta": "Aroma que acalma."}
        }
    }
    return aromatic_profiles.get(line, {}).get(occasion, {"ingrediente": "N/A", "notas": "N/A", "emoções": "N/A", "etiqueta": "Não disponível."})

from io import BytesIO
from datetime import datetime

def gerar_pdf(df_lipidica, sensorial_txt):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.set_text_color(33, 37, 41)

    # Título
    pdf.set_font("Arial", 'B', size=16)
    pdf.cell(200, 10, txt="Relatório LipidGenesis", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.ln(10)

    # Data
    pdf.cell(200, 10, txt="Data: " + datetime.now().strftime('%d/%m/%Y %H:%M'), ln=True, align='L')
    pdf.ln(10)

    # Receita Lipídica
    pdf.set_font("Arial", 'B', size=14)
    pdf.cell(200, 10, txt="Receita Lipídica", ln=True)
    pdf.set_font("Arial", size=12)
    for index, row in df_lipidica.iterrows():
        nome = f"{nomes_acidos.get(index, index)} ({index})"
        pdf.cell(200, 10, txt=f"{nome}: {row['%']:.2f}%", ln=True)


    pdf.ln(10)

    # Receita Sensorial
    pdf.set_font("Arial", 'B', size=14)
    pdf.cell(200, 10, txt="Receita Sensorial", ln=True)
    pdf.set_font("Arial", size=12)
    for linha in sensorial_txt.split("\n"):
        pdf.multi_cell(0, 10, txt=linha)

    # Salvar para memória (BytesIO)
    buffer = BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    return buffer


# === Interface ===
st.header("🔬 Análise Lipídica e Sensorial Refinada")

# Botões com design refinado
if st.button("🧪 Gerar Receita Lipídica", key="lipidica_btn"):
    df_lipidica = gerar_receita_lipidica(blend_lg)
    st.dataframe(df_lipidica[['Nome Completo', '%']])


    # === Cálculo físico-químico dinâmico com base nas proporções do usuário ===
    valores_iodo = {
        'C18:1': 86, 'C18:2': 173, 'C18:3': 260
    }

    valores_saponificacao = {
        'C6:0': 325.0, 'C8:0': 305.0, 'C10:0': 295.0, 'C12:0': 276.0, 'C14:0': 255.0,
        'C16:0': 241.0, 'C18:0': 222.0, 'C18:1': 198.0, 'C18:2': 195.0, 'C18:3': 190.0
    }

    valores_ponto_fusao = {
        'C6:0': -3.0, 'C8:0': 16.0, 'C10:0': 31.0, 'C12:0': 44.0, 'C14:0': 53.0,
        'C16:0': 63.0, 'C18:0': 70.0, 'C18:1': 13.0, 'C18:2': -5.0, 'C18:3': -11.0
    }

    # Índice de Iodo
    indice_iodo = sum(
        blend_lg.get(fa, 0) * valores_iodo.get(fa, 0) / 100 for fa in blend_lg
    )

    # Índice de Saponificação
    indice_saponificacao = sum(
        blend_lg.get(fa, 0) * valores_saponificacao.get(fa, 0) / 100 for fa in blend_lg
    )

    # Ponto de Fusão estimado (média ponderada simples)
    ponto_fusao = sum(
        blend_lg.get(fa, 0) * valores_ponto_fusao.get(fa, 0) / 100 for fa in blend_lg
    )

    # Exibição
    st.subheader("⚗️ Parâmetros Físico-Químicos do Blend LG (Dinâmico)")
    st.metric("Índice de Iodo (II)", f"{indice_iodo:.2f}")
    st.metric("Índice de Saponificação (IS)", f"{indice_saponificacao:.2f} mg KOH/g")
    st.metric("Ponto de Fusão Estimado", f"{ponto_fusao:.2f} °C")

if st.button("👃 Gerar Receita Sensorial", key="sensorial_btn"):
    sensorial_data = get_sensory_recipe(linha, ocasião)
    sensorial_txt = f"Ingrediente-chave: {sensorial_data['ingrediente']}\nNotas olfativas: {sensorial_data['notas']}\nEmoções evocadas: {sensorial_data['emoções']}\nEtiqueta sensorial: {sensorial_data['etiqueta']}"
    st.success(sensorial_txt)
    exibir_piramide_olfativa(sensorial_data)
    exibir_storytelling(sensorial_data)


# Estilo visual para o gráfico

# Estilo visual para o gráfico
st.subheader("📊 Perfil de Ácidos Graxos no Blend LG")
df_blend_lg = gerar_receita_lipidica(blend_lg)

df_blend_lg = df_blend_lg.reset_index()
df_blend_lg['Nome Completo'] = df_blend_lg['Ácido Graxo'].apply(lambda x: f"{nomes_acidos.get(x, x)} ({x})")

fig = px.bar(
    df_blend_lg,
    x='Nome Completo',
    y='%',
    title='Distribuição dos Ácidos Graxos',
    template="plotly_dark"
)
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
        .css-1d391kg { font-size: 1.2em; font-weight: bold; }
        .stDataFrame { font-size: 1em; padding: 10px; border: 1px solid #ddd; }
    </style>
""", unsafe_allow_html=True)

# Exportação Refinada
# Exportação Refinada
if st.button("📄 Exportar Relatório PDF", key="export_pdf"):
    df_lipidica = gerar_receita_lipidica(blend_lg)
    sensorial_data = get_sensory_recipe(linha, ocasião)
    sensorial_txt = f"Ingrediente-chave: {sensorial_data['ingrediente']}\nNotas olfativas: {sensorial_data['notas']}\nEmoções evocadas: {sensorial_data['emoções']}\nEtiqueta sensorial: {sensorial_data['etiqueta']}"
    pdf_buffer = gerar_pdf(df_lipidica, sensorial_txt)

    st.download_button(
        label="📥 Baixar Relatório PDF",
        data=pdf_buffer,
        file_name=f"relatorio_lipidgenesis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
        mime="application/pdf"
    )

