
import streamlit as st
import pandas as pd
from fpdf import FPDF

# Função para gerar o PDF
def gerar_pdf(blend_data, assinatura_data, custo_kg, impacto_ambiental):
    pdf = FPDF()
    pdf.add_page()
    
    # Definindo título do relatório
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(200, 10, txt='Relatório Técnico e Sensorial', ln=True, align='C')
    
    # Adicionando informações sobre o Blend
    pdf.set_font('Arial', '', 12)
    pdf.ln(10)
    pdf.cell(200, 10, txt='Informações do Blend:', ln=True)
    for key, value in blend_data.items():
        pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)
    
    # Adicionando informações do banco de assinaturas aromáticas
    pdf.ln(10)
    pdf.cell(200, 10, txt='Assinatura Sensorial:', ln=True)
    for key, value in assinatura_data.items():
        pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)
    
    # Adicionando informações de custo e impacto ambiental
    pdf.ln(10)
    pdf.cell(200, 10, txt=f'Custo por kg: R$ {custo_kg}', ln=True)
    pdf.cell(200, 10, txt=f'Impacto Ambiental (CO2 eq): {impacto_ambiental} kg CO2', ln=True)
    
    # Gerando o arquivo PDF
    pdf_output = '/mnt/data/relatorio_completo.pdf'
    pdf.output(pdf_output)
    return pdf_output

# Função para exibir o conteúdo na interface do Streamlit
def exibir_relatorio():
    st.title('Gerar Relatório Técnico e Sensorial')
    
    # Exemplo de dados de entrada para o Blend, Assinatura e Custo
    blend_data = {
        'Blend': 'RBDT 82% / RPKO 18%',
        'Composição Ácidos Graxos': 'Ácido Palmítico 50%, Ácido Linoleico 20%, etc.',
        'Propriedades Físico-químicas': 'Temperatura de fusão 30°C, Índice de Iodo 50, etc.'
    }
    
    assinatura_data = {
        'Ingrediente-chave': 'Óleo de RPKO',
        'Notas olfativas': 'Frutal, floral, fresco',
        'Emoções evocadas': 'Relaxamento, frescor',
        'Etiqueta sensorial': 'Leve, refrescante'
    }
    
    custo_kg = 15.75
    impacto_ambiental = 0.25
    
    if st.button('Gerar PDF'):
        pdf_gerado = gerar_pdf(blend_data, assinatura_data, custo_kg, impacto_ambiental)
        st.success(f'PDF gerado com sucesso! Baixe aqui: [relatório completo](sandbox:{pdf_gerado})')

# Executando a função de exibição do relatório
if __name__ == "__main__":
    exibir_relatorio()
