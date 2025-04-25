import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
import base64
from io import BytesIO

# Título e slogan
st.markdown("## LipidGenesis\n### Bioengineering Of Oils For Nextgen")

# Seleção de óleos-base
oleos_base = ['RPKO', 'RBDT']
oleo1 = st.selectbox('Selecione o primeiro óleo:', oleos_base)
oleo2 = st.selectbox('Selecione o segundo óleo:', oleos_base)

# Composições fixas para simulações
composicoes = {'82/18': [0.82, 0.18], '90/10': [0.90, 0.10]}
composicao_selecionada = st.selectbox('Selecione a composição:', list(composicoes.keys()))

# Dados reais dos perfis de ácidos graxos (% peso)
perfis_acidos_graxos = {
    'RPKO': {
        'C8:0': 3.1, 'C10:0': 3.6, 'C12:0': 48.2, 'C14:0': 15.1, 'C16:0': 8.6,
        'C18:0': 2.5, 'C18:1': 12.5, 'C18:2': 5.3, 'C18:3': 0.4, 'Outros': 0.7
    },
    'RBDT': {
        'C12:0': 0.2, 'C14:0': 0.9, 'C16:0': 38.7, 'C18:0': 4.2, 'C18:1': 42.0,
        'C18:2': 12.4, 'C18:3': 0.2, 'Outros': 1.4
    }
}

# Função para calcular o blend
@st.cache_data
def calcular_blend(oleo1, oleo2, proporcoes):
    perfil1 = perfis_acidos_graxos[oleo1]
    perfil2 = perfis_acidos_graxos[oleo2]
    blend = {}
    acidos = set(perfil1) | set(perfil2)
    for acido in acidos:
        val1 = perfil1.get(acido, 0)
        val2 = perfil2.get(acido, 0)
        blend[acido] = val1 * proporcoes[0] + val2 * proporcoes[1]
    return blend

# Cálculo do blend
blend_resultado = calcular_blend(oleo1, oleo2, composicoes[composicao_selecionada])

# Exibição do resultado
st.markdown("### Receita Lipídica (Perfil de Ácidos Graxos)")
st.dataframe(pd.DataFrame.from_dict(blend_resultado, orient='index', columns=['% Peso']).round(2))

# Comparação com especificação do Blend Natura (exemplo hipotético)
spec_natura = {
    'C12:0': 20.0, 'C14:0': 10.0, 'C16:0': 30.0, 'C18:0': 5.0,
    'C18:1': 25.0, 'C18:2': 8.0, 'Outros': 2.0
}

blend_df = pd.DataFrame.from_dict(blend_resultado, orient='index', columns=['Blend LG'])
spec_df = pd.DataFrame.from_dict(spec_natura, orient='index', columns=['Blend Natura'])
comparacao = blend_df.join(spec_df, how='outer').fillna(0)
st.markdown("### Comparação com Blend Natura")
st.bar_chart(comparacao)

# Banco de assinaturas aromáticas
banco_sensorial = {
    'Ekos': {
        'Banho': {
            'Ingrediente-chave': 'Pitanga',
            'Notas olfativas': 'Frutal verde',
            'Emoções evocadas': 'Frescor e vitalidade',
            'Etiqueta sensorial': 'Dinâmico e energizante'
        },
        'Rosto': {
            'Ingrediente-chave': 'Açaí',
            'Notas olfativas': 'Frutado suave',
            'Emoções evocadas': 'Cuidado e leveza',
            'Etiqueta sensorial': 'Delicado e reconfortante'
        }
    },
    'Chronos': {
        'Corpo': {
            'Ingrediente-chave': 'Jasmim',
            'Notas olfativas': 'Floral branco',
            'Emoções evocadas': 'Elegância e sofisticação',
            'Etiqueta sensorial': 'Envolvente e luxuoso'
        },
        'Cabelos': {
            'Ingrediente-chave': 'Castanha',
            'Notas olfativas': 'Creme suave e nozes',
            'Emoções evocadas': 'Nutrição e proteção',
            'Etiqueta sensorial': 'Conforto nutritivo'
        }
    }
}

# Seleção de linha e ocasião de uso
linha = st.selectbox('Selecione a linha de produto:', list(banco_sensorial.keys()))
ocasiao = st.selectbox('Selecione a ocasião de uso:', list(banco_sensorial[linha].keys()))

# Botão para gerar receita sensorial
if st.button('Gerar Receita Sensorial'):
    assinatura = banco_sensorial[linha][ocasiao]
    st.markdown("### Receita Sensorial")
    st.write(f"**Ingrediente-chave:** {assinatura['Ingrediente-chave']}")
    st.write(f"**Notas olfativas:** {assinatura['Notas olfativas']}")
    st.write(f"**Emoções evocadas:** {assinatura['Emoções evocadas']}")
    st.write(f"**Etiqueta sensorial:** {assinatura['Etiqueta sensorial']}")

# Função para gerar PDF
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Relatório LipidGenesis', ln=True, align='C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, ln=True, align='L')

    def chapter_body(self, body):
        self.set_font('Arial', '', 10)
        self.multi_cell(0, 10, body)

    def add_blend_data(self, data):
        self.chapter_title('Receita Lipídica')
        for k, v in data.items():
            self.cell(0, 10, f'{k}: {v:.2f}%', ln=True)

    def add_sensorial_data(self, data):
        self.chapter_title('Receita Sensorial')
        for k, v in data.items():
            self.cell(0, 10, f'{k}: {v}', ln=True)

# Botão para exportar relatório
if st.button('Exportar Relatório PDF'):
    pdf = PDF()
    pdf.add_page()
    pdf.add_blend_data(blend_resultado)
    pdf.add_sensorial_data(banco_sensorial[linha][ocasiao])

    buffer = BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    b64 = base64.b64encode(buffer.read()).decode()
    href = f'<a href="data:application/pdf;base64,{b64}" download="relatorio_lipidgenesis.pdf">Baixar Relatório PDF</a>'
    st.markdown(href, unsafe_allow_html=True)
