import streamlit as st
import pandas as pd
from fpdf import FPDF

# Dados de perfis de ácidos graxos (exemplos reais)
perfis_acidos_graxos = {
    "RPKO": {"C12:0": 48.2, "C14:0": 15.1, "C16:0": 8.2, "C18:1": 15.6, "C18:2": 1.5},
    "RBDT": {"C16:0": 44.3, "C18:0": 4.6, "C18:1": 39.2, "C18:2": 10.7},
}

# Dados do Blend Natura (referência)
blend_natura = {"C16:0": 35.0, "C18:1": 30.0, "C18:2": 10.0, "C12:0": 10.0, "C14:0": 5.0, "C18:0": 5.0}

# Banco de assinaturas aromáticas
assinaturas_aromaticas = {
    "Ekos": {
        "Banho": {
            "Ingrediente-chave": "Castanha-do-Brasil",
            "Notas olfativas": "Amadeiradas, cremosas, confortáveis",
            "Emoções evocadas": "Cuidado, nutrição, acolhimento",
            "Etiqueta sensorial": "Cremoso & Nutritivo"
        },
        "Rosto": {
            "Ingrediente-chave": "Açaí",
            "Notas olfativas": "Frutadas, frescas, verdes",
            "Emoções evocadas": "Revitalização, frescor, energia",
            "Etiqueta sensorial": "Fresco & Energizante"
        }
    },
    "Chronos": {
        "Rosto": {
            "Ingrediente-chave": "Jambu",
            "Notas olfativas": "Verdes, florais, suaves",
            "Emoções evocadas": "Sofisticação, equilíbrio, leveza",
            "Etiqueta sensorial": "Floral & Sofisticado"
        },
        "Corpo": {
            "Ingrediente-chave": "Retinol vegetal",
            "Notas olfativas": "Amadeiradas, almiscaradas, limpas",
            "Emoções evocadas": "Confiança, firmeza, autocuidado",
            "Etiqueta sensorial": "Puro & Tecnológico"
        }
    },
    "Lumina": {
        "Cabelos": {
            "Ingrediente-chave": "Pequi",
            "Notas olfativas": "Frutadas, exóticas, intensas",
            "Emoções evocadas": "Força, brilho, personalidade",
            "Etiqueta sensorial": "Frutado & Vibrante"
        }
    }
}

def calcular_blend(p1, p2, proporcao1, proporcao2):
    resultado = {}
    for acido in set(p1.keys()).union(p2.keys()):
        resultado[acido] = round(
            p1.get(acido, 0) * proporcao1 + p2.get(acido, 0) * proporcao2, 2
        )
    return resultado

def gerar_pdf_receita(blend, assinatura_sensorial):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Relatório LipidGenesis", ln=True, align="C")

    pdf.ln(10)
    pdf.cell(200, 10, txt="Composição Lipídica (%)", ln=True)
    for acido, perc in blend.items():
        pdf.cell(200, 10, txt=f"{acido}: {perc}", ln=True)

    pdf.ln(10)
    pdf.cell(200, 10, txt="Receita Sensorial", ln=True)
    for k, v in assinatura_sensorial.items():
        pdf.cell(200, 10, txt=f"{k}: {v}", ln=True)

    path = "/tmp/relatorio_lipidgenesis.pdf"
    pdf.output(path)
    return path

def obter_assinatura_sensorial(linha, ocasiao):
    try:
        return assinaturas_aromaticas[linha][ocasiao]
    except KeyError:
        return {
            "Ingrediente-chave": "Não disponível",
            "Notas olfativas": "Não disponível",
            "Emoções evocadas": "Não disponível",
            "Etiqueta sensorial": "Não disponível"
        }

# Layout
st.set_page_config(page_title="LipidGenesis App", layout="centered")
st.title("LipidGenesis — Bioengineering Of Oils For Nextgen")

st.sidebar.header("Configuração do Blend")
oleo1 = "RBDT"
oleo2 = "RPKO"

blend_8218 = calcular_blend(perfis_acidos_graxos[oleo1], perfis_acidos_graxos[oleo2], 0.82, 0.18)
blend_9010 = calcular_blend(perfis_acidos_graxos[oleo1], perfis_acidos_graxos[oleo2], 0.90, 0.10)

st.subheader("Comparação com Blend Natura")
df = pd.DataFrame({
    "Blend Natura": pd.Series(blend_natura),
    "Blend 82/18": pd.Series(blend_8218),
    "Blend 90/10": pd.Series(blend_9010)
}).fillna(0)
st.dataframe(df)

# Linha e ocasião
st.sidebar.header("Receita Sensorial")
linha = st.sidebar.selectbox("Linha de Produto", list(assinaturas_aromaticas.keys()))
ocasiao = st.sidebar.selectbox("Ocasião de Uso", list(assinaturas_aromaticas[linha].keys()))

# Botão: Receita Sensorial
if st.button("Gerar Receita Sensorial"):
    assinatura = obter_assinatura_sensorial(linha, ocasiao)
    st.subheader("Receita Sensorial")
    for k, v in assinatura.items():
        st.markdown(f"**{k}:** {v}")

# Botão: Exportar PDF
if st.button("Exportar PDF"):
    assinatura = obter_assinatura_sensorial(linha, ocasiao)
    caminho = gerar_pdf_receita(blend_8218, assinatura)
    with open(caminho, "rb") as f:
        st.download_button("📄 Baixar Relatório PDF", f, file_name="relatorio_lipidgenesis.pdf")
