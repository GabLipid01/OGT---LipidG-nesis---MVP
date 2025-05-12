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

    # Exporta para BytesIO com a codificação correta
    buffer = BytesIO()
    pdf_output = pdf.output(dest='S').encode('latin1')
    buffer.write(pdf_output)
    buffer.seek(0)
    return buffer

# === Blend Lipídico ===
with tabs[1]:
    st.header("🧪 Montagem do Blend LG")
    st.sidebar.title("🔬 Monte seu Blend")

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
    st.header("👃 Receita Sensorial")

    if total_pct == 0:
        st.warning("Monte seu blend com ao menos um óleo na aba '🧪 Blend Lipídico'.")
    else:
        oleos_utilizados = [oil for oil, pct in oil_percentages.items() if pct > 0]

        perfils_volateis = {
            "Palm Oil": {
                "2,2,6-Trimethylcyclohexanone": ("Palmeira", 35),
                "3,3,5-Trimethylcyclohex-2-enone": ("Palmeira", 25),
                "Nonanone": ("Doce", 15),
                "Nonanal": ("Doce", 15),
                "Linalol": ("Floral", 5),
                "Trans-allo-ocimene": ("Fresca", 3),
                "β-Cyclocitral": ("Cítrica", 2),
                "Ionol": ("Floral", 5),
            },
            "Palm Olein": {
                "Heptanal": ("Fresca, frutada", 30),
                "Trans-2-heptenal": ("Verde", 20),
                "Decanal": ("Doce", 25),
                "Trans-2-undecenal": ("Doce", 25),
            },
            "Palm Stearin": {
                "Ácido acético": ("Azeda", 30),
                "Ácido butanoico": ("Láctea", 25),
                "1-Hexanol": ("Verde", 20),
                "Metilcetona": ("Frutada", 25),
            },
            "Palm Kernel Oil": {
                "2-Nonanona": ("Doce", 40),
                "Ácido octanoico": ("Gordurosa", 20),
                "Metil octanoato": ("Doce", 20),
                "Pirazinas": ("Tostadas, amadeiradas", 10),
                "Maltol": ("Doce", 5),
            },
            "Palm Kernel Olein": {
                "2-Nonanona": ("Doce", 40),
                "Ácido octanoico": ("Gordurosa", 20),
                "Metil octanoato": ("Doce", 20),
                "Pirazinas": ("Tostadas, amadeiradas", 10),
                "Maltol": ("Doce", 5),
            },
            "Palm Kernel Stearin": {
                "Pirazinas": ("Tostadas, amadeiradas", 40),
                "Maltol": ("Doce", 30),
                "Ácido benzoico etil éster": ("Doce", 20),
                "Ácido octanoico": ("Gordurosa", 10),
            },
        }

        referencias = {
            "Palm Oil": "Kuntum et al. (1989), *Journal of Oil Palm Research*.",
            "Palm Olein": "Omar et al. (2007), *Pakistan Journal of Biological Sciences*.",
            "Palm Stearin": "Omar et al. (2007), *Pakistan Journal of Biological Sciences*.",
            "Palm Kernel Oil": "Zhang et al. (2016), *Food Research International*.",
            "Palm Kernel Olein": "Zhang et al. (2016), *Food Research International*.",
            "Palm Kernel Stearin": "Zhang et al. (2016), *Food Research International*.",
        }

        st.subheader("🔬 Compostos Voláteis Identificados")
        for oleo in oleos_utilizados:
            compostos = perfils_volateis.get(oleo, {})
            st.markdown(f"**{oleo}**:")
            for composto, (nota, pct) in compostos.items():
                st.markdown(f"- {composto}: {nota} — {pct}%")
            st.markdown("---")

        st.subheader("📚 Referências Científicas")
        for oleo in oleos_utilizados:
            ref = referencias.get(oleo)
            if ref:
                st.markdown(f"**{oleo}:** {ref}")


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
sensorial_txt = "Compostos Voláteis Identificados:\n"
for oleo in oil_percentages:
    if oil_percentages[oleo] > 0:
        sensorial_txt += f"\n{oleo}:\n"
        for composto, (nota, pct) in perfils_volateis.get(oleo, {}).items():
            sensorial_txt += f" - {composto}: {nota} — {pct}%\n"

sensorial_txt += "\nReferências Científicas:\n"
for oleo in oil_percentages:
    if oil_percentages[oleo] > 0:
        ref = referencias.get(oleo)
        if ref:
            sensorial_txt += f" - {oleo}: {ref}\n"
        pdf_buffer = gerar_pdf(df_lipidico, sensorial_txt)
        st.download_button(
            label="📥 Baixar Relatório PDF",
            data=pdf_buffer,
            file_name=f"relatorio_lipidgenesis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            mime="application/pdf"
        )
    else:
        st.warning("Você precisa montar um blend com ao menos um óleo para gerar o relatório.")
