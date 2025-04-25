import streamlit as st
import pandas as pd
from fpdf import FPDF

# Perfis de ácidos graxos reais
perfis = {
    "RPKO": {"C12:0": 48.2, "C14:0": 15.1, "C16:0": 8.2, "C18:1": 15.6, "C18:2": 1.5},
    "RBDT": {"C16:0": 44.3, "C18:0": 4.6, "C18:1": 39.2, "C18:2": 10.7},
}

blend_natura = {"C16:0": 35.0, "C18:1": 30.0, "C18:2": 10.0, "C12:0": 10.0, "C14:0": 5.0, "C18:0": 5.0}

# Banco sensorial estruturado
sensorial = {
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

def calcular_blend(p1, p2, prop1, prop2):
    acidos = set(p1) | set(p2)
    return {a: round(p1.get(a, 0)*prop1 + p2.get(a, 0)*prop2, 2) for a in acidos}

# Layout original mantido
st.set_page_config(page_title="LipidGenesis", layout="centered")
st.title("LipidGenesis")
st.markdown("**Bioengineering Of Oils For Nextgen**")

st.header("Receita Lipídica")
blend_8218 = calcular_blend(perfis["RBDT"], perfis["RPKO"], 0.82, 0.18)
blend_9010 = calcular_blend(perfis["RBDT"], perfis["RPKO"], 0.90, 0.10)

df = pd.DataFrame({
    "Blend Natura": pd.Series(blend_natura),
    "Blend LG 82/18": pd.Series(blend_8218),
    "Blend LG 90/10": pd.Series(blend_9010)
}).fillna(0)

st.dataframe(df)

# Linha e ocasião mantidas no corpo principal
st.header("Receita Sensorial")
linha = st.selectbox("Linha de Produto", list(sensorial.keys()))
ocasiao = st.selectbox("Ocasião de Uso", list(sensorial[linha].keys()))

if st.button("Gerar Receita Sensorial"):
    dados = sensorial[linha][ocasiao]
    st.subheader("Resultado Sensorial")
    st.markdown(f"**Ingrediente-chave:** {dados['Ingrediente-chave']}")
    st.markdown(f"**Notas olfativas:** {dados['Notas olfativas']}")
    st.markdown(f"**Emoções evocadas:** {dados['Emoções evocadas']}")
    st.markdown(f"**Etiqueta sensorial:** {dados['Etiqueta sensorial']}")
