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
with tabs[2]:
    st.header("👃 Receita Sensorial")

    # Perfis de compostos voláteis (mantendo nomes dos óleos em inglês)
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
            "Acetic acid": ("Azeda", 30),
            "Butanoic acid": ("Láctea", 25),
            "1-Hexanol": ("Verde", 20),
            "Methyl ketone": ("Frutada", 25),
        },
        "Palm Kernel Oil": {
            "2-Nonanone": ("Doce", 40),
            "Octanoic acid": ("Gordurosa", 20),
            "Methyl octanoate": ("Doce", 20),
            "Pyrazines": ("Tostadas, amadeiradas", 10),
            "Maltol": ("Doce", 5),
        },
        "Palm Kernel Olein": {
            "2-Nonanone": ("Doce", 40),
            "Octanoic acid": ("Gordurosa", 20),
            "Methyl octanoate": ("Doce", 20),
            "Pyrazines": ("Tostadas, amadeiradas", 10),
            "Maltol": ("Doce", 5),
        },
        "Palm Kernel Stearin": {
            "Pyrazines": ("Tostadas, amadeiradas", 40),
            "Maltol": ("Doce", 30),
            "Ethyl benzoate": ("Doce", 20),
            "Octanoic acid": ("Gordurosa", 10),
        },
    }

    referencias = {
        "Palm Oil": "Kuntum, A., Dirinck, P. J., & Schamp, N. M. (1989). Identification of volatile compounds that contribute to the aroma of fresh palm oil and oxidized oil. *Journal of Oil Palm Research*.",
        "Palm Olein": "Omar, M. N. B., Idris, N. A. M., & Idris, N. A. (2007). Changes of headspace volatile constituents of palm olein and selected oils after frying French fries. *Pakistan Journal of Biological Sciences*.",
        "Palm Stearin": "Omar, M. N. B., Idris, N. A. M., & Idris, N. A. (2007). Changes of headspace volatile constituents of palm olein and selected oils after frying French fries. *Pakistan Journal of Biological Sciences*.",
        "Palm Kernel Oil": "Zhang, Y., et al. (2016). Changes in volatiles of palm kernel oil before and after kernel roasting. *Food Research International*.",
        "Palm Kernel Olein": "Zhang, Y., et al. (2016). Changes in volatiles of palm kernel oil before and after kernel roasting. *Food Research International*.",
        "Palm Kernel Stearin": "Zhang, Y., et al. (2016). Changes in volatiles of palm kernel oil before and after kernel roasting. *Food Research International*.",
    }

    # Detectar óleos com % > 0 no blend
    oleos_utilizados = [oleo for oleo, pct in oil_percentages.items() if pct > 0 and oleo in perfils_volateis]

    def gerar_receita_sensoria(oleos_selecionados):
        receita = []
        for oleo in oleos_selecionados:
            for composto, (nota, porcentagem) in perfils_volateis[oleo].items():
                receita.append(f"{composto}: {nota} - {porcentagem}%")
        return receita

    if oleos_utilizados:
        st.write("**Oils used in lipidic blend:**", ", ".join(oleos_utilizados))
        
        st.subheader("🔬 Sensorial Recipe Generated from Blend:")
        receita = gerar_receita_sensoria(oleos_utilizados)
        for item in receita:
            st.write("-", item)

        st.subheader("📚 Bibliographic References:")
        for oleo in oleos_utilizados:
            st.markdown(f"**{oleo}**: {referencias[oleo]}")
    else:
        st.info("The sensorial recipe will appear here after you configure your lipidic blend in the previous tab.")

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
