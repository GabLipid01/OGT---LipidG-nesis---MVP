import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from fpdf import FPDF

# === Perfis de Ácidos Graxos Reais (baseados em laudos Eurofins) ===
RPKO_PROFILE = {
    "C6:0": 0.1751,
    "C8:0": 2.7990,
    "C10:0": 2.7349,
    "C12:0": 40.7681,
    "C14:0": 14.8587,
    "C16:0": 11.8319,
    "C18:0": 0.0000,
    "C18:1": 20.8017,
    "C18:2": 3.2454,
    "C20:0": 0.1446,
    "C20:1": 0.1049
}

RBDT_PROFILE = {
    "C12:0": 0.4976,
    "C14:0": 0.8371,
    "C16:0": 38.1650,
    "C16:1": 0.1286,
    "C18:0": 5.1485,
    "C18:1": 45.3823,
    "C18:2": 9.6964,
    "C18:3": 0.1995,
    "C20:0": 0.3747,
    "C20:1": 0.1838,
    "C15:1t": 0.0107,
    "C20:1t": 0.0320
}

# === Parâmetros de Especificação do Blend Natura ===
NATURA_SPECS = {
    "Temperatura (°C)": (55, 60),
    "Índice de Acidez": 0.20,
    "Cor Lovibond (vermelho 5 1/4)": 4.0,
    "Umidade (%)": 0.20,
    "Índice de Iodo": (37, 45),
    "Índice de Saponificação (mgKOH/g)": (193, 213)
}

# CONFIGURAÇÃO
st.set_page_config(page_title="LipidGenesis - Plataforma", layout="wide")
st.title("🌿 LipidGenesis - Bioengineering of Oils for Nextgen")
st.markdown("#### Comparativo entre Blend Natura 82/18 e LG Blend 82/18")

# SIDEBAR
st.sidebar.title("🔬 Configurações")
linha = st.sidebar.selectbox("Escolha a linha de produto Natura:", ["Ekos", "Chronos", "Tododia", "Mamãe e Bebê"])
ocasião = st.sidebar.selectbox("Ocasião de uso:", ["Banho", "Rosto", "Corpo", "Cabelos"])

# PERFIS DE ÁCIDOS GRAXOS (valores hipotéticos)
perfil_rbdt = {'C16:0': 45.2, 'C18:0': 4.8, 'C18:1': 38.5, 'C18:2': 10.1, 'C18:3': 1.4}
perfil_rpko = {'C12:0': 48.0, 'C14:0': 16.0, 'C16:0': 10.5, 'C18:1': 15.3, 'C18:2': 10.2}
blend_natura = {k: 0.82 * perfil_rbdt.get(k, 0) + 0.18 * perfil_rpko.get(k, 0) for k in set(perfil_rbdt) | set(perfil_rpko)}
blend_lg = {k: 0.82 * perfil_rbdt.get(k, 0) + 0.18 * perfil_rpko.get(k, 0) + np.random.normal(0, 0.2) for k in set(perfil_rbdt) | set(perfil_rpko)}

# FUNÇÕES
def gerar_receita_lipidica(blend):
    df = pd.DataFrame.from_dict(blend, orient='index', columns=['%'])
    df.index.name = 'Ácido Graxo'
    return df

# Banco de assinaturas aromáticas
def get_sensory_recipe(line, occasion):
    aromatic_profiles = {
        "Ekos": {
            "Banho": {"ingrediente": "Breu-branco", "notas": "Balsâmico, incensado, fresco", "emoções": "Purificação, conexão espiritual", "etiqueta": "A floresta viva se dissolve no vapor. O breu sobe como reza ancestral, purificando alma e pele."},
            "Rosto": {"ingrediente": "Priprioca", "notas": "Terroso, amadeirado, levemente doce", "emoções": "Enraizamento, mistério", "etiqueta": "A raiz terrosa e resinosa que ancora a pele na sabedoria da floresta. Um perfume de origem."},
            "Corpo": {"ingrediente": "Castanha-do-Pará", "notas": "Cremoso, doce, oleoso", "emoções": "Nutrição, conforto", "etiqueta": "Textura cremosa, aroma nutritivo. A abundância da Amazônia se faz pele."},
            "Cabelos": {"ingrediente": "Andiroba", "notas": "Herbal-amargo, medicinal", "emoções": "Força, proteção", "etiqueta": "Força medicinal que reveste cada fio. Amargor que cura, perfume que marca."}
        },
        "Chronos": {
            "Banho": {"ingrediente": "Chá-verde amazônico", "notas": "Verde, leve, fresco", "emoções": "Clareza, renovação", "etiqueta": "Frescor técnico e elegante. Um banho de clareza e renovação celular."},
            "Rosto": {"ingrediente": "Copaíba", "notas": "Amadeirado suave, doce-resinoso", "emoções": "Serenidade, equilíbrio", "etiqueta": "Amadeirado sutil, envolto em calma. A pele encontra seu equilíbrio atemporal."},
            "Corpo": {"ingrediente": "Pequi", "notas": "Verde, frutado-oleoso", "emoções": "Originalidade, sofisticação", "etiqueta": "Exótico e refinado. O verde untuoso do cerrado encontra a pele urbana."},
            "Cabelos": {"ingrediente": "Tucumã", "notas": "Vegetal denso, oleoso, levemente doce", "emoções": "Reconstrução, vigor", "etiqueta": "Textura rica e vegetal, com o perfume da reconstrução invisível."}
        },
        "Tododia": {
            "Banho": {"ingrediente": "Pitanga", "notas": "Frutado verde, cítrico", "emoções": "Alegria, vivacidade", "etiqueta": "Explosão frutada e cítrica que convida ao sorriso. Energia fresca para o dia."},
            "Rosto": {"ingrediente": "Maracujá", "notas": "Frutado fresco, ácido suave", "emoções": "Tranquilidade, equilíbrio", "etiqueta": "Ácido-suave que relaxa e equilibra. Um cuidado leve como um fim de tarde calmo."},
            "Corpo": {"ingrediente": "Cupuaçu", "notas": "Doce, manteigado, tropical", "emoções": "Aconchego, prazer", "etiqueta": "Doçura tropical com toque amanteigado. A pele sorri com cada aplicação."},
            "Cabelos": {"ingrediente": "Murumuru", "notas": "Vegetal cremoso, denso", "emoções": "Proteção, maciez", "etiqueta": "Densidade vegetal que amacia e modela. Um bálsamo diário de nutrição sensorial."}
        },
        "Mamãe e Bebê": {
            "Banho": {"ingrediente": "Lavanda brasileira", "notas": "Floral suave, fresca, aromática", "emoções": "Calmaria, proteção", "etiqueta": "Calma floral que embala. Uma nuvem perfumada de proteção e amor."},
            "Rosto": {"ingrediente": "Camomila", "notas": "Herbal adocicado, suave", "emoções": "Serenidade, aconchego", "etiqueta": "Erva doce que silencia a pele. Um carinho invisível no toque mais delicado."},
            "Corpo": {"ingrediente": "Castanha de caju", "notas": "Doce-leitosa, cremosa", "emoções": "Acolhimento, suavidade", "etiqueta": "Doce-leitosa e familiar. A pele se reconhece nesse cuidado natural."},
            "Cabelos": {"ingrediente": "Água de coco", "notas": "Aquático, leve, refrescante", "emoções": "Frescor, leveza", "etiqueta": "Refresco leve e transparente. Umidade que limpa, aroma que acalma."}
        }
    }
    return aromatic_profiles.get(line, {}).get(occasion, {
        "ingrediente": "N/A", "notas": "N/A", "emoções": "N/A", "etiqueta": "Combinação não disponível no banco atual."
    })

# FUNÇÃO DE GERAÇÃO DE RELATÓRIO PDF
def gerar_pdf(df_lipidica, sensorial_txt):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Relatório Técnico - LipidGenesis", ln=True, align='C')
    pdf.ln(10)
    pdf.cell(200, 10, txt="Receita Lipídica:", ln=True)
    for i, row in df_lipidica.iterrows():
        pdf.cell(200, 10, txt=f"{i}: {row['%']:.2f}%", ln=True)
    pdf.ln(10)
    pdf.cell(200, 10, txt="Receita Sensorial:", ln=True)
    pdf.multi_cell(200, 10, txt=sensorial_txt)
    caminho = "/mnt/data/relatorio_lipidgenesis.pdf"
    pdf.output(caminho)
    return caminho

# INTERFACE PRINCIPAL
st.markdown("#### Receita Lipídica e Sensorial Personalizadas")

col1, col2 = st.columns(2)
with col1:
    if st.button("🧪 Gerar Receita Lipídica"):
        df_lipidica = gerar_receita_lipidica(blend_lg)
        st.dataframe(df_lipidica)
with col2:
    if st.button("👃 Gerar Receita Sensorial"):
        sensorial_data = get_sensory_recipe(linha, ocasião)
        sensorial_txt = f"Ingrediente-chave: {sensorial_data['ingrediente']}\nNotas olfativas: {sensorial_data['notas']}\nEmoções evocadas: {sensorial_data['emoções']}\nEtiqueta sensorial: {sensorial_data['etiqueta']}"
        st.success(sensorial_txt)

# COMPARATIVO
# Função para mostrar o comparativo entre os blends Natura e LG
def mostrar_comparativo(blend_natura, blend_lg, titulo):
    # Criando DataFrame para os comparativos
    df_comparativo = pd.DataFrame({
        'Ácido Graxo': list(blend_natura.keys()),
        'Blend Natura (%)': list(blend_natura.values()),
        'Blend LG (%)': list(blend_lg.values())
    })
    
    # Exibindo o comparativo
    st.subheader(titulo)
    st.dataframe(df_comparativo)

mostrar_comparativo(blend_natura, blend_lg, "Comparativo de Ácidos Graxos")
# Função para mostrar o impacto ambiental
def mostrar_impacto_ambiental():
    natura = 1.25  # kg CO₂ eq / kg de produto
    lg = 0.98
    st.metric("🌍 Emissão CO₂ eq/kg", f"{lg:.2f}", delta=f"{(natura-lg)/natura*100:.1f}%", delta_color="inverse")

mostrar_impacto_ambiental()

# Função para mostrar o painel ESG
def painel_esg():
    st.subheader("🌱 Painel ESG - Sustentabilidade e Responsabilidade")
    
    # Seção Ambiental
    st.markdown("#### 🌍 Aspectos Ambientais")
    st.markdown("- **Emissões de CO₂**: A redução de emissões de carbono é uma prioridade em nossos processos produtivos.")
    st.markdown("- **Pegada Hídrica**: Implementação de técnicas de uso eficiente da água.")
    st.markdown("- **Matéria-Prima Sustentável**: Priorizamos o uso de óleos vegetais provenientes de fontes responsáveis.")
    
    # Seção Social
    st.markdown("#### 🤝 Aspectos Sociais")
    st.markdown("- **Desenvolvimento Comunitário**: Trabalhamos com comunidades locais para garantir práticas agrícolas sustentáveis.")
    st.markdown("- **Condições de Trabalho**: Comprometemo-nos com condições de trabalho justas e seguras para todos os colaboradores.")
    st.markdown("- **Responsabilidade Social**: Investimos em programas sociais e educacionais nas regiões onde atuamos.")
    
    # Seção Governança
    st.markdown("#### 📊 Aspectos de Governança")
    st.markdown("- **Transparência**: Mantemos a transparência nas nossas práticas de negócios e relatórios financeiros.")
    st.markdown("- **Ética Empresarial**: Cumprimos rigorosamente as normas e leis locais e internacionais.")
    st.markdown("- **Anti-Corrupção**: Implementação de políticas rigorosas de combate à corrupção em todos os níveis da empresa.")


# EXPORTAR
if st.button("📄 Exportar Relatório PDF"):
    df_lipidica = gerar_receita_lipidica(blend_lg)
    sensorial_data = get_sensory_recipe(linha, ocasião)
    sensorial_txt = f"Ingrediente-chave: {sensorial_data['ingrediente']}\nNotas olfativas: {sensorial_data['notas']}\nEmoções evocadas: {sensorial_data['emoções']}\nEtiqueta sensorial: {sensorial_data['etiqueta']}"
    caminho_pdf = gerar_pdf(df_lipidica, sensorial_txt)
    st.markdown(f"**[Baixar Relatório PDF]**({caminho_pdf})")

# Mostrar o painel ESG
painel_esg()
