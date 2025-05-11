import streamlit as st
import pandas as pd
import plotly.express as px
from fpdf import FPDF
from datetime import datetime
from io import BytesIO
from blend_calculator import BlendCalculator

st.set_page_config(
    page_title="LipidGenesis - Blend LG",
    layout="wide"
)

# === Título e Slogan (fora das abas) ===
st.title("🌿 LipidGenesis - Bioengenharia Lipídica Aplicada à Indústrias de Óleos Vegetais")

# === Interface em Abas (logo abaixo do slogan) ===
tabs = st.tabs([
    "🏠 Home",
    "🧪 Blend Lipídico",
    "👃 Receita Sensorial",
    "🌱 ESG e Ambiental",
    "📍 Rastreabilidade",
    "📄 Exportação PDF"
])

# === Home ===
with tabs[0]:
    st.header("🏠 Visão Geral")
    st.markdown("Explore os recursos desta plataforma inovadora para bioengenharia sensorial e funcional.")

# === Dados fixos ===

FATTY_ACID_PROFILES = {
    "Palm Oil": {"C12:0": 0.2, "C14:0": 1.0, "C16:0": 44.0, "C16:1": 0.2, "C18:0": 4.5, "C18:1": 39.0, "C18:2": 10.0, "C18:3": 0.3, "C20:0": 0.2, "C20:1": 0.1},
    "Palm Olein": {"C12:0": 0.1, "C14:0": 1.0, "C16:0": 39.0, "C16:1": 0.2, "C18:0": 4.5, "C18:1": 43.5, "C18:2": 11.0, "C18:3": 0.3, "C20:0": 0.2, "C20:1": 0.2},
    "Palm Stearin": {"C14:0": 1.2, "C16:0": 56.0, "C16:1": 0.1, "C18:0": 6.5, "C18:1": 30.0, "C18:2": 5.0, "C18:3": 0.1, "C20:0": 0.3},
    "Palm Kernel Oil": {"C6:0": 0.2, "C8:0": 3.6, "C10:0": 3.5, "C12:0": 48.2, "C14:0": 16.2, "C16:0": 8.4, "C16:1": 0.1, "C18:0": 2.0, "C18:1": 15.3, "C18:2": 2.3, "C18:3": 0.1, "C20:0": 0.1},
    "Palm Kernel Olein": {"C6:0": 0.3, "C8:0": 4.0, "C10:0": 3.7, "C12:0": 49.5, "C14:0": 15.7, "C16:0": 8.0, "C16:1": 0.1, "C18:0": 1.9, "C18:1": 14.5, "C18:2": 2.1, "C18:3": 0.1, "C20:0": 0.1},
    "Palm Kernel Stearin": {"C8:0": 3.0, "C10:0": 3.0, "C12:0": 47.0, "C14:0": 17.5, "C16:0": 9.5, "C16:1": 0.1, "C18:0": 2.5, "C18:1": 14.0, "C18:2": 2.0, "C18:3": 0.1, "C20:0": 0.1}
}

nomes_acidos = {
    "C6:0": "Ácido Capróico", "C8:0": "Ácido Caprílico", "C10:0": "Ácido Cáprico",
    "C12:0": "Ácido Láurico", "C14:0": "Ácido Mirístico", "C16:0": "Ácido Palmítico",
    "C16:1": "Ácido Palmitoleico", "C18:0": "Ácido Esteárico", "C18:1": "Ácido Oleico",
    "C18:2": "Ácido Linoleico", "C18:3": "Ácido Linolênico", "C20:0": "Ácido Araquídico",
    "C20:1": "Ácido Gadoleico"
}

# === Receita Sensorial ===
def get_sensory_recipe(line, occasion):
    aromatic_profiles = {
        "Vitalis": {
            "Banho": {"ingrediente": "Breu-branco", "notas": "Balsâmico, incensado", "emoções": "Purificação", "etiqueta": "A floresta viva no vapor."},
            "Rosto": {"ingrediente": "Priprioca", "notas": "Terroso, doce", "emoções": "Enraizamento", "etiqueta": "A raiz que ancora a pele."},
            "Corpo": {"ingrediente": "Castanha-do-Pará", "notas": "Cremoso, doce", "emoções": "Nutrição", "etiqueta": "Abundância amazônica."},
            "Cabelos": {"ingrediente": "Andiroba", "notas": "Herbal-amargo", "emoções": "Força", "etiqueta": "Força medicinal."}
        },
        "Essentia": {
            "Banho": {"ingrediente": "Chá-verde", "notas": "Verde, fresco", "emoções": "Renovação", "etiqueta": "Frescor técnico."},
            "Rosto": {"ingrediente": "Copaíba", "notas": "Amadeirado suave", "emoções": "Serenidade", "etiqueta": "Amadeirado calmo."},
            "Corpo": {"ingrediente": "Pequi", "notas": "Frutado-oleoso", "emoções": "Originalidade", "etiqueta": "Verde do cerrado."},
            "Cabelos": {"ingrediente": "Tucumã", "notas": "Vegetal denso", "emoções": "Reconstrução", "etiqueta": "Textura rica."}
        },
        "Ardor": {
            "Banho": {"ingrediente": "Pitanga", "notas": "Frutado, cítrico", "emoções": "Alegria", "etiqueta": "Explosão cítrica."},
            "Rosto": {"ingrediente": "Maracujá", "notas": "Frutado ácido", "emoções": "Tranquilidade", "etiqueta": "Leveza tropical."},
            "Corpo": {"ingrediente": "Cupuaçu", "notas": "Doce, manteigado", "emoções": "Aconchego", "etiqueta": "Tropical amanteigado."},
            "Cabelos": {"ingrediente": "Murumuru", "notas": "Vegetal cremoso", "emoções": "Proteção", "etiqueta": "Densidade vegetal."}
        },
        "Lúmina": {
            "Banho": {"ingrediente": "Lavanda", "notas": "Floral suave", "emoções": "Calmaria", "etiqueta": "Calma floral."},
            "Rosto": {"ingrediente": "Camomila", "notas": "Herbal adocicado", "emoções": "Aconchego", "etiqueta": "Silêncio na pele."},
            "Corpo": {"ingrediente": "Castanha de Caju", "notas": "Doce-leitosa", "emoções": "Suavidade", "etiqueta": "Cuidado natural."},
            "Cabelos": {"ingrediente": "Água de coco", "notas": "Aquático, refrescante", "emoções": "Frescor", "etiqueta": "Aroma que acalma."}
        }
    }
    return aromatic_profiles.get(line, {}).get(occasion, {})

# === Funções auxiliares ===
def gerar_receita_lipidica(blend):
    df = pd.DataFrame.from_dict(blend, orient='index', columns=['%'])
    df.index.name = 'Ácido Graxo'
    df = df.reset_index()
    df['Nome Completo'] = df['Ácido Graxo'].apply(lambda x: f"{nomes_acidos.get(x, x)} ({x})")
    return df

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
    for _, row in df_lipidica.iterrows():
        nome = f"{row['Nome Completo']}"
        pdf.cell(200, 10, txt=f"{nome}: {row['%']:.2f}%", ln=True)

    pdf.ln(10)

    # Receita Sensorial
    pdf.set_font("Arial", 'B', size=14)
    pdf.cell(200, 10, txt="Receita Sensorial", ln=True)
    pdf.set_font("Arial", size=12)
    for linha in sensorial_txt.split("\n"):
        pdf.multi_cell(0, 10, txt=linha)

    # Exporta para BytesIO com a codificação correta
    buffer = BytesIO()
    pdf_output = pdf.output(dest='S').encode('latin1')
    buffer.write(pdf_output)
    buffer.seek(0)
    return buffer

# === Blend Lipídico ===
with tabs[1]:
    st.header("🧪 Montagem do Blend LG")
    st.sidebar.title("🔬 Configurações")
    linha = st.sidebar.selectbox("Linha de Produto:", ["Vitalis", "Essentia", "Ardor", "Lúmina"])
    ocasião = st.sidebar.selectbox("Ocasião de Uso:", ["Banho", "Rosto", "Corpo", "Cabelos"])

    oil_keys = list(FATTY_ACID_PROFILES.keys())
    oil_percentages = {oil: st.sidebar.slider(f"{oil} (%)", 0, 100, 0, 1) for oil in oil_keys}
    total_pct = sum(oil_percentages.values())

    if total_pct == 0:
        st.warning("Defina pelo menos um óleo com percentual maior que 0.")
    else:
        normalized = {k: v / total_pct for k, v in oil_percentages.items()}
        all_fatty_acids = set().union(*FATTY_ACID_PROFILES.values())
        blend_lg = {
            fa: sum(normalized[oil] * FATTY_ACID_PROFILES[oil].get(fa, 0) for oil in oil_keys)
            for fa in all_fatty_acids
        }

        df_lipidico = gerar_receita_lipidica(blend_lg)
        st.dataframe(df_lipidico)

        st.subheader("📊 Perfil de Ácidos Graxos")
        fig = px.bar(df_lipidico, x='Nome Completo', y='%', template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

        # Parâmetros físico-químicos
        valores_iodo = {'C18:1': 86, 'C18:2': 173, 'C18:3': 260}
        valores_saponificacao = {'C6:0': 325, 'C8:0': 305, 'C10:0': 295, 'C12:0': 276, 'C14:0': 255, 'C16:0': 241, 'C18:0': 222, 'C18:1': 198, 'C18:2': 195, 'C18:3': 190}
        valores_ponto_fusao = {'C6:0': -3, 'C8:0': 16, 'C10:0': 31, 'C12:0': 44, 'C14:0': 53, 'C16:0': 63, 'C18:0': 70, 'C18:1': 13, 'C18:2': -5, 'C18:3': -11}

        ii = sum(blend_lg.get(fa, 0) * valores_iodo.get(fa, 0) / 100 for fa in blend_lg)
        isap = sum(blend_lg.get(fa, 0) * valores_saponificacao.get(fa, 0) / 100 for fa in blend_lg)
        pfusao = sum(blend_lg.get(fa, 0) * valores_ponto_fusao.get(fa, 0) / 100 for fa in blend_lg)

        st.metric("Índice de Iodo", f"{ii:.2f}")
        st.metric("Índice de Saponificação", f"{isap:.2f} mg KOH/g")
        st.metric("Ponto de Fusão Estimado", f"{pfusao:.2f} °C")

# === Receita Sensorial ===
with tabs[2]:
    st.header("👃 Receita Sensorial e Storytelling")

    sensorial_data = get_sensory_recipe(linha, ocasião)
    notas = sensorial_data['notas'].split(',')
    proporcoes = {'Topo': 15, 'Corpo': 50, 'Fundo': 35}

    # Ajuste para garantir 3 notas
    if len(notas) == 1:
        nota_topo = notas[0].strip()
        nota_corpo = "Cremoso, doce"
        nota_fundo = "Amadeirado suave"
    elif len(notas) == 2:
        nota_topo = notas[0].strip()
        nota_corpo = notas[1].strip()
        nota_fundo = "Amadeirado suave"
    else:
        nota_topo, nota_corpo, nota_fundo = [n.strip() for n in notas[:3]]

    df_piramide = pd.DataFrame({
        'Nota': [nota_topo, nota_corpo, nota_fundo],
        'Camada': ['Topo', 'Corpo', 'Fundo'],
        'Proporção (%)': [proporcoes['Topo'], proporcoes['Corpo'], proporcoes['Fundo']]
    })
    camada_ordem = {'Fundo': 0, 'Corpo': 1, 'Topo': 2}
    df_piramide['ordem'] = df_piramide['Camada'].map(camada_ordem)
    df_piramide = df_piramide.sort_values('ordem', ascending=False)

    fig = px.bar(
        df_piramide,
        x="Proporção (%)",
        y="Camada",
        orientation="h",
        color="Camada",
        text="Nota",
        color_discrete_map={"Topo": "#FFC1E3", "Corpo": "#B2E4B2", "Fundo": "#A0C4FF"},
        height=400
    )
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(f"""
    <div style='text-align: center; font-size: 16px;'>
        🌸 <b>{nota_topo}</b> (Topo) — {proporcoes['Topo']}%<br>
        🌿 <b>{nota_corpo}</b> (Corpo) — {proporcoes['Corpo']}%<br>
        🌳 <b>{nota_fundo}</b> (Fundo) — {proporcoes['Fundo']}%
    </div>
    """, unsafe_allow_html=True)

    st.subheader("📖 Storytelling Sensorial")
    emocao = sensorial_data['emoções']
    emoji = SENSORY_EMOJIS.get(emocao, "")
    ingrediente = sensorial_data['ingrediente']
    etiqueta = sensorial_data['etiqueta']

    narrativa = f"""
    <div style="font-size: 16px; line-height: 1.6; text-align: justify; padding: 1rem; border-radius: 12px;
                background-color: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1);">
        Imagine a primeira impressão: <b>{nota_topo}</b> — uma nota que desperta os sentidos com leveza e frescor. 
        Logo depois, o coração da criação revela <b>{ingrediente}</b>, alma desta composição, conectando profundamente com o propósito da sua ocasião. 
        Por fim, a base se firma em <b>{nota_fundo}</b>, sustentando a memória aromática com elegância e permanência.
        <br><br>
        Essa jornada sensorial evoca <b>{emocao}</b> {emoji}, alinhando-se com a etiqueta <b>{etiqueta}</b> e transmitindo valor olfativo com propósito e emoção.
    </div>
    """
    st.markdown(narrativa, unsafe_allow_html=True)

# === ESG e Ambiental ===
with tabs[3]:
    st.header("🌎 Análise ESG e Ambiental")

    benchmark_co2 = {
        "Natura": 1.25,
        "Unilever": 1.20,
        "Johnson & Johnson": 1.15,
        "LipidGenesis": 0.98
    }

    for company, value in benchmark_co2.items():
        delta = (value - benchmark_co2["LipidGenesis"]) / value * 100
        st.metric(f"Emissão de CO₂ eq/kg ({company})", f"{value:.2f}", delta=f"{delta:.1f}%", delta_color="inverse" if delta > 0 else "normal")

    impacto_ambiental = {
        "Água Consumida (L/kg)": {
            "LipidGenesis": 5.0,
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

    for indicador, dados in impacto_ambiental.items():
        st.subheader(f"{indicador}")
        st.dataframe(pd.DataFrame.from_dict(dados, orient='index', columns=[indicador]))

# === Rastreabilidade (Placeholder) ===
with tabs[4]:
    st.header("📍 Rastreabilidade do Blend")
    st.info("Esta seção será dedicada à origem dos ingredientes, lotes e fornecedores — em breve.")

# === Exportação PDF ===
with tabs[5]:
    st.header("📄 Exportar Relatório PDF")

    if total_pct > 0:
        sensorial_txt = f"""
Ingrediente-chave: {sensorial_data['ingrediente']}
Notas olfativas: {sensorial_data['notas']}
Emoções evocadas: {sensorial_data['emoções']}
Etiqueta sensorial: {sensorial_data['etiqueta']}
"""
        pdf_buffer = gerar_pdf(df_lipidico, sensorial_txt)
        st.download_button(
            label="📥 Baixar Relatório PDF",
            data=pdf_buffer,
            file_name=f"relatorio_lipidgenesis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            mime="application/pdf"
        )
    else:
        st.warning("Você precisa montar um blend com ao menos um óleo para gerar o relatório.")
