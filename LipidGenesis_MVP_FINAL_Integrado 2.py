import streamlit as st
import pandas as pd
import plotly.express as px
from fpdf import FPDF
from datetime import datetime
from io import BytesIO
from blend_calculator import BlendCalculator

# === Dados fixos ===

FATTY_ACID_PROFILES = {
    "Óleos Refinados": {
        "Palm Oil": {"C12:0": 0.2, "C14:0": 1.0, "C16:0": 44.0, "C16:1": 0.2, "C18:0": 4.5, "C18:1": 39.0, "C18:2": 10.0, "C18:3": 0.3, "C20:0": 0.2, "C20:1": 0.1},
        "Palm Olein": {"C12:0": 0.1, "C14:0": 1.0, "C16:0": 39.0, "C16:1": 0.2, "C18:0": 4.5, "C18:1": 43.5, "C18:2": 11.0, "C18:3": 0.3, "C20:0": 0.2, "C20:1": 0.2},
        "Palm Stearin": {"C14:0": 1.2, "C16:0": 56.0, "C16:1": 0.1, "C18:0": 6.5, "C18:1": 30.0, "C18:2": 5.0, "C18:3": 0.1, "C20:0": 0.3},
        "Palm Kernel Oil": {"C6:0": 0.2, "C8:0": 3.6, "C10:0": 3.5, "C12:0": 48.2, "C14:0": 16.2, "C16:0": 8.4, "C16:1": 0.1, "C18:0": 2.0, "C18:1": 15.3, "C18:2": 2.3, "C18:3": 0.1, "C20:0": 0.1},
        "Palm Kernel Olein": {"C6:0": 0.3, "C8:0": 4.0, "C10:0": 3.7, "C12:0": 49.5, "C14:0": 15.7, "C16:0": 8.0, "C16:1": 0.1, "C18:0": 1.9, "C18:1": 14.5, "C18:2": 2.1, "C18:3": 0.1, "C20:0": 0.1},
        "Palm Kernel Stearin": {"C8:0": 3.0, "C10:0": 3.0, "C12:0": 47.0, "C14:0": 17.5, "C16:0": 9.5, "C16:1": 0.1, "C18:0": 2.5, "C18:1": 14.0, "C18:2": 2.0, "C18:3": 0.1, "C20:0": 0.1}
    },

    "Ácidos Graxos Puros": {
        "Ácido Láurico (C12:0)": {"C12:0": 100.0},
        "Ácido Mirístico (C14:0)": {"C14:0": 100.0},
        "Ácido Palmítico (C16:0)": {"C16:0": 100.0},
        "Ácido Esteárico (C18:0)": {"C18:0": 100.0},
        "Ácido Oleico (C18:1)": {"C18:1": 100.0},
        "Ácido Linoleico (C18:2)": {"C18:2": 100.0},
        "Ácido Linolênico (C18:3)": {"C18:3": 100.0}
    },
    
    "Insumos Industriais": {
        "PFAD (Destilado de Ácidos Graxos de Palma)": {"C16:0": 52.0, "C18:0": 5.0, "C18:1": 34.0, "C18:2": 8.0, "C20:0": 1.0},
        "Soapstock de Palma (Refino Químico)": {"C16:0": 38.0, "C18:0": 3.5, "C18:1": 45.0, "C18:2": 11.0, "C18:3": 1.0}
    }
}

nomes_acidos = {
    "C6:0": "Ácido Capróico", "C8:0": "Ácido Caprílico", "C10:0": "Ácido Cáprico",
    "C12:0": "Ácido Láurico", "C14:0": "Ácido Mirístico", "C16:0": "Ácido Palmítico",
    "C16:1": "Ácido Palmitoleico", "C18:0": "Ácido Esteárico", "C18:1": "Ácido Oleico",
    "C18:2": "Ácido Linoleico", "C18:3": "Ácido Linolênico", "C20:0": "Ácido Araquídico",
    "C20:1": "Ácido Gadoleico"
}

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
    "PFAD": {
        "Ácido palmítico": ("Gorduroso, ceroso", 35),
        "Ácido oleico": ("Oleoso, suave", 20),
        "Ácido linoleico": ("Leve amendoado", 12),
        "Hexanal": ("Notas verdes, herbais", 8),
        "Acetona": ("Notas químicas, solvente", 8),
        "Compostos sulfurados": ("Pungente, característico", 5),
        "Ácido láurico": ("Levemente doce", 5),
    },
    "Soapstock": {
        "Ácido palmítico": ("Oleoso, gorduroso", 23),
        "Ácido oleico": ("Suave, oleoso", 18),
        "Sabões de potássio/sódio": ("Sabão, alcalino", 15),
        "Fosfolipídios oxidados": ("Mineral, rancidez leve", 12),
        "Ácido linoleico": ("Verde, vegetal", 7),
        "Compostos fenólicos": ("Amargo, terroso", 5),
        "Água e traços orgânicos": ("Neutro", 5),
    },
    "Ácido Oleico": {
        "Octanal": ("Cítrico, doce", 30),
        "Nonanal": ("Floral, ceroso", 25),
        "Decanal": ("Alaranjado, doce", 20),
        "Ácido hexanoico": ("Gorduroso, rançoso", 15),
        "1-Octeno-3-ol": ("Terroso, cogumelo", 10),
    },
    "Ácido Linoleico": {
        "Hexanal": ("Verde, herbáceo", 35),
        "2-Pentilfurano": ("Amendoado, torrado", 25),
        "1-Octeno-3-ol": ("Terroso", 15),
        "Nonanal": ("Floral, gorduroso", 15),
        "Ácido 2,4-decadienoico": ("Rancidez característica", 10),
    },
    "Ácido Palmítico": {
        "Ácido hexanoico": ("Gorduroso", 40),
        "Nonanal": ("Cítrico, ceroso", 30),
        "Octanal": ("Cítrico", 20),
        "Compostos alifáticos": ("Neutro", 10),
    },
    "Ácido Esteárico": {
        "Nonanal": ("Ceroso", 35),
        "Octanal": ("Cítrico", 25),
        "Decanal": ("Doce, frutado", 20),
        "Ácido butanoico": ("Lácteo", 10),
        "Ácido hexanoico": ("Rancidez leve", 10),
    },
    "Ácido Láurico": {
        "Ácido butanoico": ("Lácteo", 30),
        "Decanal": ("Doce", 25),
        "Dodecanol": ("Gorduroso", 25),
        "Octanal": ("Fresco, cítrico", 20),
    },
    "Ácido Mirístico": {
        "Tetradecanol": ("Gorduroso", 35),
        "Nonanal": ("Ceroso", 30),
        "Octanal": ("Cítrico", 20),
        "Ácido hexanoico": ("Rancidez leve", 15),
    },
    "Ácido Capróico": {
        "Ácido hexanoico": ("Gorduroso, rançoso", 40),
        "Butirato de etila": ("Frutado", 30),
        "Hexanoato de etila": ("Frutado, doce", 20),
        "Butanoato de metila": ("Frutado", 10),
    },
    "Ácido Caprílico": {
        "Ácido octanoico": ("Gorduroso, rançoso", 40),
        "Octanol": ("Fresco, verde", 30),
        "Octanal": ("Cítrico", 20),
        "Compostos lácteos": ("Lácteo", 10),
    }
}

referencias = {
    "Palm Oil": "Kuntum et al. (1989), *Journal of Oil Palm Research*.",
    "Palm Olein": "Omar et al. (2007), *Pakistan Journal of Biological Sciences*.",
    "Palm Stearin": "Omar et al. (2007), *Pakistan Journal of Biological Sciences*.",
    "Palm Kernel Oil": "Zhang et al. (2016), *Food Research International*.",
    "Palm Kernel Olein": "Zhang et al. (2016), *Food Research International*.",
    "Palm Kernel Stearin": "Zhang et al. (2016), *Food Research International*.",
    "PFAD": "Tan et al. (2018), *Journal of Lipid Science & Technology*.",
    "Soapstock": "Lim et al. (2019), *Industrial Crops and Products*.",
    "Ácido Oleico": "Yang et al. (2020), *Molecules*.",
    "Ácido Linoleico": "Delgado et al. (2015), *Food Chemistry*.",
    "Ácido Palmítico": "López-López et al. (2010), *Journal of the American Oil Chemists’ Society*.",
    "Ácido Esteárico": "Zhang et al. (2021), *Food Science & Nutrition*.",
    "Ácido Láurico": "Grosch et al. (1981), *Journal of the American Oil Chemists’ Society*.",
    "Ácido Mirístico": "Reineccius (2006), *Flavor Chemistry and Technology*.",
    "Ácido Capróico": "Van Gemert (2011), *Compilations of Odour Threshold Values*.",
    "Ácido Caprílico": "Van Gemert (2011), *Compilations of Odour Threshold Values*."
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

st.set_page_config(
    page_title="LipidGenesis - Blend LG",
    layout="wide"
)

# === Título e Slogan (fora das abas) ===
st.title("🌴 OGT LipidPalma - Bioengenharia Lipídica Aplicada à Indústria de Óleo de Palma")

# === Interface em Abas (logo abaixo do slogan) ===
tabs = st.tabs([
    "🧭 Home",                     # tabs[0]
    "🏭 Proposta Industrial",      # tabs[1]
    "🧪 Blend Lipídico",           # tabs[2]
    "👃 Assinatura Sensorial",     # tabs[3]
    "📊 Viabilidade Técnica",      # tabs[4]
    "📊 Protocolo de Produção",    # tabs[5]
    "🌱 ESG e Ambiental",          # tabs[6]
    "📍 Rastreabilidade",          # tabs[7]
    "📄 Exportação PDF"            # tabs[8]
])

with tabs[0]:
    st.markdown("""
    ***OGT – The Future of Oil Disruption*** 
    **Apresenta:** 
    
    ### 🌴 LipidPalma™

    ---

    Um app interativo para formulação e simulação de blends lipídicos com foco na cadeia do óleo de palma.

    O **LipidPalma** é um produto da marca **LipidGenesis**, uma linha modular de soluções da **OGT** para impulsionar a inovação e a sustentabilidade em óleos vegetais como palma, soja e algodão.

    ---

    Para começar:
    1. Acesse a aba **"Blend Lipídico"** e monte sua formulação com os ingredientes disponíveis.
    2. Explore as demais abas para entender o perfil físico-químico, sensorial, ambiental e produtivo do seu blend.

    ---
    
    Este MVP é voltado para inovação sustentável em P&D, com foco em alternativas ao refino tradicional.
    """)

with tabs[1]:
    st.markdown("""
    O **LipidPalma** propõe uma abordagem alternativa à produção tradicional de óleos estruturados,
    utilizando **esterificação enzimática com glicerol** para gerar triglicerídeos com perfis sob medida.

    ---
    ### **Categorias de ingredientes disponíveis**
    - **Óleos Refinados:** produtos oriundos do refino tradicional.
    - **Ácidos Graxos Puros:** fornecem controle técnico preciso da composição.
    - **Insumos Industriais (ex: PFAD, soapstock):** alternativas econômicas e sustentáveis provenientes de etapas do refino.

    ---
    ### **Vantagens estratégicas**
    - **Customização de blends** com perfis semelhantes a óleos vegetais reais.
    - **Valorização de subprodutos industriais**, reduzindo custos e impactos ambientais.
    - **Flexibilidade para P&D** em aplicações cosméticas, alimentares ou industriais.

    ---
    ### **Objetivo do MVP**
    Demonstrar a viabilidade técnica e econômica de produzir óleos estruturados por rota enzimática
    a partir de misturas controladas de óleos refinados, insumos industriais e ácidos graxos puros, promovendo inovação e circularidade na cadeia do óleo de palma.
    """)

# === Blend Lipídico ===
with tabs[2]:
    st.header("🧪 Montagem do Blend LG")
    st.sidebar.title("🔬 Monte seu Blend")

    # Agrupamento visual dos ingredientes
    grouped_profiles = {
        "Óleos Refinados": list(FATTY_ACID_PROFILES["Óleos Refinados"].keys()),
        "Ácidos Graxos Puros": list(FATTY_ACID_PROFILES["Ácidos Graxos Puros"].keys()),
        "Insumos Industriais": list(FATTY_ACID_PROFILES["Insumos Industriais"].keys())
    }

    # Sliders para cada categoria
    oil_percentages = {}

    st.sidebar.markdown("### 🧴 Óleos Refinados")
    for oil in grouped_profiles["Óleos Refinados"]:
        oil_percentages[oil] = st.sidebar.slider(f"{oil} (%)", 0, 100, 0, 1)

    st.sidebar.markdown("### 🧬 Ácidos Graxos Puros")
    for oil in grouped_profiles["Ácidos Graxos Puros"]:
        oil_percentages[oil] = st.sidebar.slider(f"{oil} (%)", 0, 100, 0, 1)

    st.sidebar.markdown("### 🧪 Insumos Industriais")
    for oil in grouped_profiles["Insumos Industriais"]:
        oil_percentages[oil] = st.sidebar.slider(f"{oil} (%)", 0, 100, 0, 1)

    # Salva os percentuais brutos no session_state
    st.session_state["oil_percentages"] = oil_percentages

    total_pct = sum(oil_percentages.values())

    if total_pct == 0:
        st.warning("Defina pelo menos um óleo com percentual maior que 0.")
    else:
        # Normalização
        normalized = {
            oil: pct / total_pct
            for oil, pct in oil_percentages.items()
            if pct > 0
        }

        # Função para buscar perfil do óleo em qualquer categoria
        def get_fatty_profile(oil):
            for category in FATTY_ACID_PROFILES:
                if oil in FATTY_ACID_PROFILES[category]:
                    return FATTY_ACID_PROFILES[category][oil]
            return {}

        # União de todos os ácidos graxos presentes
        all_fatty_acids = set().union(
            *[get_fatty_profile(oil) for oil in normalized.keys()]
        )

        # Geração do blend lipídico
        blend_lg = {
            fa: sum(
                normalized[oil] * get_fatty_profile(oil).get(fa, 0)
                for oil in normalized
            )
            for fa in all_fatty_acids
        }

        # Salva no session_state
        st.session_state["blend_lipidico"] = blend_lg
        st.session_state["blend_result"] = blend_lg  # Necessário para produção

        # Visualização em tabela
        df_lipidico = gerar_receita_lipidica(blend_lg)
        st.dataframe(df_lipidico)

        # Gráfico de barras
        st.subheader("📊 Perfil de Ácidos Graxos")
        fig = px.bar(df_lipidico, x="Nome Completo", y="%", template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

        # Parâmetros físico-químicos
        valores_iodo = {"C18:1": 86, "C18:2": 173, "C18:3": 260}
        valores_saponificacao = {
            "C6:0": 325, "C8:0": 305, "C10:0": 295, "C12:0": 276, "C14:0": 255,
            "C16:0": 241, "C18:0": 222, "C18:1": 198, "C18:2": 195, "C18:3": 190
        }
        valores_ponto_fusao = {
            "C6:0": -3, "C8:0": 16, "C10:0": 31, "C12:0": 44, "C14:0": 53,
            "C16:0": 63, "C18:0": 70, "C18:1": 13, "C18:2": -5, "C18:3": -11
        }

        # Cálculos
        ii = sum(blend_lg.get(fa, 0) * valores_iodo.get(fa, 0) / 100 for fa in blend_lg)
        isap = sum(blend_lg.get(fa, 0) * valores_saponificacao.get(fa, 0) / 100 for fa in blend_lg)
        pfusao = sum(blend_lg.get(fa, 0) * valores_ponto_fusao.get(fa, 0) / 100 for fa in blend_lg)

        # Armazenamento no estado
        st.session_state["indice_iodo"] = ii
        st.session_state["indice_saponificacao"] = isap
        st.session_state["ponto_fusao"] = pfusao

        # Exibição
        st.metric("Índice de Iodo", f"{ii:.2f}")
        st.metric("Índice de Saponificação", f"{isap:.2f} mg KOH/g")
        st.metric("Ponto de Fusão Estimado", f"{pfusao:.2f} °C")

# === Assinatura Sensorial ===
with tabs[3]:
    oil_percentages = st.session_state.get("oil_percentages", {})
    oleos_utilizados = [oil for oil, pct in oil_percentages.items() if pct > 0]

    # Mapeamento entre nome completo e chave simplificada usada nos dicionários
    nome_curto = {
    "PFAD (Destilado de Ácidos Graxos de Palma)": "PFAD",
    "Soapstock de Palma (Refino Químico)": "Soapstock",
    "Palm Oil": "Palm Oil",
    "Palm Olein": "Palm Olein",
    "Palm Stearin": "Palm Stearin",
    "Palm Kernel Oil": "Palm Kernel Oil",
    "Palm Kernel Olein": "Palm Kernel Olein",
    "Palm Kernel Stearin": "Palm Kernel Stearin",
    "Ácido Oleico (C18:1)": "Ácido Oleico",
    "Ácido Linoleico (C18:2)": "Ácido Linoleico",
    "Ácido Palmítico (C16:0)": "Ácido Palmítico",
    "Ácido Esteárico (C18:0)": "Ácido Esteárico",
    "Ácido Láurico (C12:0)": "Ácido Láurico",
    "Ácido Mirístico (C14:0)": "Ácido Mirístico",
    "Ácido Capróico (C6:0)": "Ácido Capróico",
    "Ácido Caprílico (C8:0)": "Ácido Caprílico"
}

    if not oleos_utilizados:
        st.warning("Monte seu blend com ao menos um óleo na aba '🧪 Blend Lipídico'.")
    else:
        st.subheader("🔬 Compostos Voláteis Identificados")
        for oleo in oleos_utilizados:
            chave = nome_curto.get(oleo)
            compostos = perfils_volateis.get(chave, {})
            st.markdown(f"**{oleo}**:")
            for composto, (nota, pct) in compostos.items():
                st.markdown(f"- {composto}: {nota} — {pct}%")
            st.markdown("---")

        st.subheader("📚 Referências Científicas")
        for oleo in oleos_utilizados:
            chave = nome_curto.get(oleo)
            ref = referencias.get(chave)
            if ref:
                st.markdown(f"**{oleo}:** {ref}")



# === Viabilidade Técnica ===
with tabs[4]:
    st.markdown("""
O modelo LipidPalma permite a criação de óleos estruturados por meio da esterificação enzimática de ácidos graxos,
oferecendo uma alternativa viável ao refino tradicional de óleos vegetais.

### 📉 Comparativo Econômico: LipidPalma vs. Modelo Tradicional

| Critério                           | LipidPalma (Esterificação Enzimática) | Extração e Refino Tradicional      |
|-----------------------------------|------------------------------------------|-------------------------------------|
| **Matéria-prima**                 | Ácidos graxos puros + álcoois            | Frutos frescos de palma             |
| **Investimento inicial (CAPEX)** | Médio-alto (reatores + controle fino)    | Muito alto (plantio + usinas)       |
| **Custo operacional (OPEX)**      | Moderado (energia, enzima, reagentes)    | Alto (logística + manutenção rural) |
| **Consistência do produto**       | Alta (ajustável digitalmente)            | Média (depende da safra e clima)    |
| **Escalabilidade**                | Alta em módulos industriais              | Alta, mas intensiva em terra        |
| **Sustentabilidade**              | Muito alta (sem uso de solo)             | Baixa (impacto ambiental elevado)   |
| **Custo estimado por kg**         | US$ 1,00-1,50                            | US$ 0,70-1,00                       |
| **Rendimento médio**              | 85-95%                                   | 18-22% de óleo por fruto fresco     |
""")

# === 📊 PROTOCOLO DE PRODUÇÃO ===
with tabs[5]:
    st.header("📊 Protocolo de Produção - Esterificação Enzimática")

    if "blend_result" not in st.session_state:
        st.warning("Por favor, gere um blend lipídico na aba '🧪 Blend Lipídico' antes de prosseguir.")
    else:
        blend = st.session_state["blend_result"]
        st.subheader("Composição Inicial do Blend (Ácidos Graxos)")
        st.dataframe(pd.DataFrame.from_dict(blend, orient="index", columns=["%"]).style.format("{:.2f}"))

        st.markdown("---")
        st.subheader("Parâmetros da Esterificação")

        col1, col2, col3 = st.columns(3)
        with col1:
            rendimento = st.slider("Rendimento da Reação (%)", 50, 100, 90)
        with col2:
            enzima_custo = st.number_input("Custo por kg de enzima imobilizada (R$/kg)", value=3000.0)
        with col3:
            ciclos_enzima = st.number_input("Número de usos da enzima", min_value=1, value=10)

        col4, col5, col6 = st.columns(3)
        with col4:
            enzima_pct = st.slider("% Enzima no processo (m/m)", 1, 10, 5)
        with col5:
            glicerol_pct = st.slider("% Glicerol no processo (m/m)", 5, 50, 15)
        with col6:
            custo_glicerol = st.number_input("Custo do glicerol (R$/kg)", value=5.0)

        st.markdown("---")
        st.subheader("Simulação de Produção")

        massa_blend_kg = 1.0
        massa_glicerol = glicerol_pct / 100 * massa_blend_kg
        massa_enzima = enzima_pct / 100 * massa_blend_kg
        custo_enzima = (massa_enzima * enzima_custo) / ciclos_enzima
        custo_glicerol_total = massa_glicerol * custo_glicerol

        custo_mat_prima = custo_glicerol_total + custo_enzima
        custo_total = custo_mat_prima
        massa_final = massa_blend_kg * (rendimento / 100)

        custo_por_kg = custo_total / massa_final

        st.metric("Massa Final (kg)", f"{massa_final:.2f}")
        st.metric("Custo Total (R$)", f"{custo_total:.2f}")
        st.metric("Custo por kg (R$)", f"{custo_por_kg:.2f}")

        st.markdown("---")
        st.subheader("Comparativo da Composição")

        df_blend = pd.DataFrame.from_dict(blend, orient="index", columns=["Blend Original (%)"])
        df_blend["Esterificado (%)"] = df_blend["Blend Original (%)"] * (rendimento / 100)
        st.dataframe(df_blend.style.format("{:.2f}"))

        fig = px.bar(df_blend.reset_index(), x="index", y=["Blend Original (%)", "Esterificado (%)"],
                     barmode="group", labels={"index": "Ácido Graxo"}, title="Comparação: Antes e Depois da Esterificação")
        st.plotly_chart(fig, use_container_width=True)

# === ESG e Ambiental ===
with tabs[6]:

    st.markdown("""
    Esta seção avalia o impacto ambiental e social do blend produzido via **esterificação enzimática**, com base nos ingredientes selecionados na aba '🧪 Blend Lipídico' e nos parâmetros definidos na aba '📊 Protocolo de Produção'.
    """)

    oil_percentages = st.session_state.get("oil_percentages", {})
    ingredientes_utilizados = {k: v for k, v in oil_percentages.items() if v > 0}

    if not ingredientes_utilizados:
        st.warning("Monte seu blend com ao menos um ingrediente na aba '🧪 Blend Lipídico'.")
    else:
        st.subheader("📌 Ingredientes Utilizados")
        for ingrediente, pct in ingredientes_utilizados.items():
            st.markdown(f"- **{ingrediente}**: {pct:.1f}%")

        st.divider()
        st.subheader("♻️ Avaliação de Sustentabilidade")

        def impacto_individual(nome):
            nome = nome.lower()
            if "soapstock" in nome or "pfad" in nome:
                return "♻️ Subproduto reaproveitado — impacto positivo"
            elif "ácido" in nome:
                return "⚗️ Ácido graxo puro — impacto neutro (verificar origem)"
            elif "palm kernel" in nome or "kernel" in nome:
                return "🌴 Derivado do palmiste — atenção à rastreabilidade"
            elif "palm" in nome:
                return "🌿 Fonte de palma convencional — moderado"
            else:
                return "🧪 Insumo genérico — verificar fonte"

        for ingr in ingredientes_utilizados:
            st.markdown(f"- **{ingr}**: {impacto_individual(ingr)}")

        st.divider()
        st.subheader("🌍 Benefícios Ambientais Estimados")

        total = sum(ingredientes_utilizados.values())
        reaproveitados = sum(v for k, v in ingredientes_utilizados.items() if "Soapstock" in k or "PFAD" in k)
        reaproveitamento_pct = (reaproveitados / total) * 100

        col1, col2 = st.columns(2)
        col1.metric("📉 Redução de Resíduo Industrial", f"{reaproveitamento_pct:.1f}%")
        col2.metric("⚙️ Processo de Baixo Impacto", "Esterificação Enzimática")

        st.markdown(
            """
        A utilização de subprodutos como **PFAD** e **soapstock** permite reduzir significativamente o descarte e aumentar a circularidade da cadeia de produção.

        A síntese enzimática ocorre a baixa temperatura, **reduzindo consumo energético e emissões de CO2** comparado à hidrogenação ou transesterificação química.
            """
        )

        st.divider()
        st.subheader("📘 Narrativa ESG")

        st.markdown(
            """
        > **Este blend foi desenvolvido com foco em economia circular e impacto positivo.**  
        > A substituição de matérias-primas tradicionais por subprodutos valorizados e a aplicação de enzimas como catalisadores verdes demonstram o compromisso com soluções sustentáveis de alta performance.
            """
        )

        if st.button("📄 Gerar Relatório ESG"):
            st.info("🚧 Em desenvolvimento: funcionalidade de exportação em PDF com logotipo, blend utilizado e descrição do impacto.")

# === Rastreabilidade (Placeholder) ===
with tabs[7]:
    st.markdown("Esta seção apresenta informações detalhadas sobre a origem, certificações e rastreabilidade dos ingredientes utilizados no blend final.")

    oil_percentages = st.session_state.get("oil_percentages", {})
    ingredientes_utilizados = {k: v for k, v in oil_percentages.items() if v > 0}

    if not ingredientes_utilizados:
        st.warning("Monte seu blend com ao menos um ingrediente na aba '🧪 Blend Lipídico'.")
    else:
        st.subheader("📦 Ingredientes do Blend")

        data_rastreabilidade = []
        for ingrediente, porcentagem in ingredientes_utilizados.items():
            with st.expander(f"{ingrediente} — {porcentagem:.1f}%"):
                fornecedor = st.text_input(f"Fornecedor de {ingrediente}", key=f"fornecedor_{ingrediente}")
                lote = st.text_input(f"Lote de {ingrediente}", key=f"lote_{ingrediente}")
                origem = st.text_input(f"País de origem de {ingrediente}", key=f"origem_{ingrediente}")
                validade = st.date_input(f"Data de validade de {ingrediente}", key=f"validade_{ingrediente}")
                armazenamento = st.text_area(f"Condições de armazenamento de {ingrediente}", key=f"armazenamento_{ingrediente}", height=80)
                certificacoes = st.multiselect(
                    f"Certificações de {ingrediente}",
                    ["RSPO", "Orgânico", "Fair Trade", "Kosher", "Vegano"],
                    key=f"certificacoes_{ingrediente}"
                )
                data_rastreabilidade.append({
                    "Ingrediente": ingrediente,
                    "% no Blend": f"{porcentagem:.1f}%",
                    "Fornecedor": fornecedor,
                    "Lote": lote,
                    "Origem": origem,
                    "Validade": validade.strftime("%d/%m/%Y"),
                    "Armazenamento": armazenamento,
                    "Certificações": ", ".join(certificacoes) if certificacoes else "—"
                })

        st.divider()
        st.subheader("📊 Tabela Consolidada de Rastreabilidade")
        st.dataframe(data_rastreabilidade, use_container_width=True)

        st.divider()
        st.subheader("📈 Visualização da Composição do Blend")
        df_grafico = pd.DataFrame({
            "Ingrediente": list(ingredientes_utilizados.keys()),
            "Proporção (%)": list(ingredientes_utilizados.values())
        })
        fig = px.pie(df_grafico, names="Ingrediente", values="Proporção (%)", hole=0.4,
                     color_discrete_sequence=px.colors.sequential.Agsunset)
        st.plotly_chart(fig, use_container_width=True)

        st.divider()
        st.success("✅ Rastreabilidade registrada com sucesso! Pronta para exportação ou validação por auditoria externa.")

# === Exportação PDF ===
with tabs[8]:
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

# === Rodapé ===
st.markdown("---")
st.markdown(
    "<p style='text-align: center; font-size: 14px;'>"
    "🌿 Desenvolvido por <b>OGT - The Future of Oil Disruption</b>. "
    "Aplicação modular <b>LipidGenesis</b> com o módulo atual: <b>LipidPalma</b>. "
    "<br>Versão MVP demonstrativa. &copy; 2025 OGT."
    "</p>",
    unsafe_allow_html=True
)
