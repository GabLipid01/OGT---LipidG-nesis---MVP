
import streamlit as st
import pandas as pd
import numpy as np
from fpdf import FPDF

# Função para gerar o relatório PDF
def gerar_relatorio_pdf(ingredientes, notas, emoções, etiquetas, blend_comparacao, receita_lipidica):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Relatório Técnico - LipidGenesis", ln=True, align="C")

    pdf.ln(10)
    pdf.cell(200, 10, txt="Composição do Blend Natura x LipidGenesis", ln=True)
    pdf.ln(5)
    pdf.multi_cell(0, 10, f"Blend Natura: {blend_comparacao['Natura']}
Blend LipidGenesis: {blend_comparacao['LipidGenesis']}")

    pdf.ln(10)
    pdf.cell(200, 10, txt="Receita Lipídica:", ln=True)
    pdf.multi_cell(0, 10, receita_lipidica)

    pdf.ln(10)
    pdf.cell(200, 10, txt="Perfil Sensorial:", ln=True)
    for i in range(len(ingredientes)):
        pdf.cell(200, 10, txt=f"{ingredientes[i]} - {notas[i]} - {emoções[i]} - {etiquetas[i]}", ln=True)

    pdf.output("relatorio_lipidgenesis.pdf")

# Função para gerar a receita lipídica
def gerar_receita_lipidica(rpkp_composicao, rbdt_composicao):
    # Gerar receita lipídica com base nas composições
    receita = f"Composição RPKO: {rpkp_composicao}%
Composição RBDT: {rbdt_composicao}%"
    return receita

# Função para gerar a receita sensorial
def gerar_receita_sensorial(linha, ocasião):
    # Gerar receita sensorial com base na linha de produto e ocasião
    assinatura = banco_assinaturas_oleosas[linha][ocasião]
    ingredientes = assinatura['ingrediente-chave']
    notas = assinatura['notas-olfativas']
    emoções = assinatura['emoções-evocadas']
    etiquetas = assinatura['etiquetas-sensoriais']

    return ingredientes, notas, emoções, etiquetas

# Banco de assinaturas aromáticas (dados de exemplo)
banco_assinaturas_oleosas = {
    'Ekos': {
        'Banho': {
            'ingrediente-chave': ['Óleo de Castanha-do-Pará', 'Óleo de Maracujá'],
            'notas-olfativas': ['Notas amadeiradas', 'Notas tropicais'],
            'emoções-evocadas': ['Aconchego', 'Energia'],
            'etiquetas-sensoriais': ['Acalma', 'Revigorante']
        },
        'Corpo': {
            'ingrediente-chave': ['Óleo de Pequi', 'Óleo de Buriti'],
            'notas-olfativas': ['Notas frutadas', 'Notas herbais'],
            'emoções-evocadas': ['Relaxamento', 'Vitalidade'],
            'etiquetas-sensoriais': ['Calor', 'Refrescante']
        }
    },
    'Chronos': {
        'Rosto': {
            'ingrediente-chave': ['Óleo de Semente de Uva', 'Óleo de Rosa Mosqueta'],
            'notas-olfativas': ['Notas florais', 'Notas de frutas'],
            'emoções-evocadas': ['Rejuvenescimento', 'Suavidade'],
            'etiquetas-sensoriais': ['Acalmante', 'Hidratante']
        },
        'Corpo': {
            'ingrediente-chave': ['Óleo de Argão', 'Óleo de Marula'],
            'notas-olfativas': ['Notas doces', 'Notas de madeira'],
            'emoções-evocadas': ['Luxo', 'Nutrição'],
            'etiquetas-sensoriais': ['Suave', 'Refrescante']
        }
    }
}

# Layout do app
st.title("LipidGenesis - Simulação de Blends Lipídicos e Sensorial")
st.sidebar.header("Configurações")

# Seleção de blend e ocasião de uso
linha = st.sidebar.selectbox("Escolha a linha de produto:", ["Ekos", "Chronos"])
ocasião = st.sidebar.selectbox("Escolha a ocasião de uso:", ["Banho", "Corpo", "Rosto"])

# Exibir dados da receita sensorial
if st.sidebar.button('Gerar Receita Sensorial'):
    ingredientes, notas, emoções, etiquetas = gerar_receita_sensorial(linha, ocasião)
    st.write(f"**Receita Sensorial - {linha} - {ocasião}:**")
    for i in range(len(ingredientes)):
        st.write(f"{ingredientes[i]} - {notas[i]} - {emoções[i]} - {etiquetas[i]}")

# Gerar a receita lipídica
rpkp_composicao = st.sidebar.slider("Composição do RPKO (%)", 0, 100, 82)
rbdt_composicao = 100 - rpkp_composicao
receita_lipidica = gerar_receita_lipidica(rpkp_composicao, rbdt_composicao)
st.write(f"**Receita Lipídica:**")
st.write(receita_lipidica)

# Comparação entre os blends
blend_comparacao = {'Natura': 'RBDT 82% / RPKO 18%', 'LipidGenesis': f'RBDT {rbdt_composicao}% / RPKO {rpkp_composicao}%'}
st.write("**Comparação entre Blend Natura e LipidGenesis:**")
st.write(blend_comparacao)

# Botão para gerar relatório PDF
if st.sidebar.button('Gerar Relatório'):
    gerar_relatorio_pdf(ingredientes, notas, emoções, etiquetas, blend_comparacao, receita_lipidica)
    st.write("Relatório gerado com sucesso!")
