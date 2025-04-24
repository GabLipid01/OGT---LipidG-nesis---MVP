
import streamlit as st
import pandas as pd

# Slogan atualizado
st.set_page_config(page_title="LipidGenesis", page_icon="🧪", layout="wide")
st.title("LipidGenesis")
st.caption("Bioengineering Of Oils For Nextgen")

# Banco de assinaturas aromáticas
banco_sensorial = {
    "Ekos": {
        "Rosto": {
            "Ingrediente-chave": "Pitanga",
            "Notas olfativas": "Cítrico fresco, verde, frutado",
            "Emoções evocadas": "Revitalização, leveza, frescor",
            "Etiquetas sensoriais": "revigorante, cítrico, tropical"
        },
        "Banho": {
            "Ingrediente-chave": "Andiroba",
            "Notas olfativas": "Amadeirado, herbal, balsâmico",
            "Emoções evocadas": "Conexão com a natureza, equilíbrio",
            "Etiquetas sensoriais": "calmante, terroso, natural"
        }
    },
    "Chronos": {
        "Rosto": {
            "Ingrediente-chave": "Jambu",
            "Notas olfativas": "Floral fresco, levemente especiado",
            "Emoções evocadas": "Elegância, cuidado, sofisticação",
            "Etiquetas sensoriais": "floral, sofisticado, moderno"
        }
    }
}

# Seleção de linha de produto e ocasião de uso
linha_produto = st.selectbox("Linha de Produto", list(banco_sensorial.keys()))
ocasiao_uso = st.selectbox("Ocasião de Uso", list(banco_sensorial[linha_produto].keys()))

# Botão para gerar receita sensorial
if st.button("Gerar Receita Sensorial"):
    assinatura = banco_sensorial[linha_produto][ocasiao_uso]
    st.subheader("Receita Sensorial Estimada")
    st.markdown(f"**Ingrediente-chave:** {assinatura['Ingrediente-chave']}")
    st.markdown(f"**Notas olfativas:** {assinatura['Notas olfativas']}")
    st.markdown(f"**Emoções evocadas:** {assinatura['Emoções evocadas']}")
    st.markdown(f"**Etiquetas sensoriais:** {assinatura['Etiquetas sensoriais']}")

# Layout e funcionalidades anteriores são mantidos aqui...
# (Suponha que o restante do código do app original permanece abaixo)
