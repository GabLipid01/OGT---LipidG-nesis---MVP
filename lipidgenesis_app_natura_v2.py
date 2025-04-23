
import streamlit as st
from rdkit import Chem
from rdkit.Chem import Draw
from PIL import Image
import io

st.set_page_config(page_title="LipidGenesis | Natura Edition", layout="centered")

# Estilo CSS inspirado na Natura
st.markdown("""
    <style>
    body {
        background-color: #f5f2ee;
        font-family: 'Helvetica Neue', sans-serif;
        color: #3e3e3e;
    }
    .stButton>button {
        background-color: #8fc38b;
        color: white;
        border-radius: 20px;
        padding: 0.5em 2em;
    }
    .stSelectbox>div>div {
        border-radius: 10px;
        border: 1px solid #ccc;
    }
    </style>
""", unsafe_allow_html=True)

# Título
st.markdown("""
# 🌿 LipidGenesis
### Simulador de Blends Sensorialmente Inteligentes
""")

# Seletor de óleos
col1, col2 = st.columns(2)
with col1:
    base1 = st.selectbox("Óleo Base 1", ["RBDT"], index=0)
with col2:
    base2 = st.selectbox("Óleo Base 2", ["RPKO"], index=0)

# Botão para gerar blend
if st.button("🌱 Gerar Receita Lipídica"):
    st.markdown("""
    #### 🔬 Blend 82/18: TAGs mais prováveis
    > Blend enzimático ideal para formulações sustentáveis e sensoriais.
    """)

    # Exemplo de TAGs com visualização molecular
    tag_smiles = {
        "OPO (Oleic-Palmitic-Oleic)": "CCCCCCCC=CCCCCCCCC(=O)OCC(COC(=O)CCCCCCCCCCCCCCCC)COC(=O)CCCCCCCC=CCCCCC",
        "POP (Palmitic-Oleic-Palmitic)": "CCCCCCCCCCCCCCCC(=O)OCC(COC(=O)CCCCCCCC=CCCCCC)COC(=O)CCCCCCCCCCCCCCCC",
        "POL (Palmitic-Oleic-Linoleic)": "CCCCCCCCCCCCCCCC(=O)OCC(COC(=O)CCCCCCCC=CCCCCC)COC(=O)CCC=CCC=CCCCCCC"
    }

    cols = st.columns(len(tag_smiles))
    for col, (tag, smiles) in zip(cols, tag_smiles.items()):
        mol = Chem.MolFromSmiles(smiles)
        img = Draw.MolToImage(mol, size=(200, 200))
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        col.image(Image.open(buf), caption=tag)

# Botão de receita sensorial
if st.button("🌸 Gerar Receita Sensorial"):
    st.markdown("#### 📊 Comparativo com Blend Natura")
    st.bar_chart({"Blend Natura": [60, 45, 70], "Blend 82/18": [65, 40, 68]})

# Simulações adicionais
st.markdown("""
---
#### 🌍 Simulações Adicionais
""")
col1, col2 = st.columns(2)
with col1:
    linha = st.selectbox("Linha de Produto", ["Ekos", "Chronos", "Mamãe e Bebê"])
with col2:
    uso = st.selectbox("Ocasião de uso", ["Banho", "Corpo", "Rosto"])

st.write("♻️ **Custo estimado**: R$18,40/kg | **Pegada de CO₂**: 1.3 kg eq/kg")

# Exportar relatório
st.download_button("📄 Exportar PDF Técnico e Sensorial", data="Relatório gerado.".encode("utf-8"), file_name="relatorio_blend_natura.pdf")
