import streamlit as st
import pandas as pd
import plotly.express as px
from fpdf import FPDF

# === Perfis de Ácidos Graxos (Codex Alimentarius) ===
RPKO_PROFILE = {
    "C6:0": 0.5, "C8:0": 4.3, "C10:0": 3.8, "C12:0": 50.0,
    "C14:0": 16.0, "C16:0": 8.3, "C16:1": 0.1, "C18:0": 2.0,
    "C18:1": 15.5, "C18:2": 2.25, "C18:3": 0.1, "C20:0": 0.1, "C20:1": 0.0
}

RBDT_PROFILE = {
    "C12:0": 0.5, "C14:0": 0.75, "C16:0": 43.4, "C16:1": 0.3,
    "C18:0": 5.0, "C18:1": 40.0, "C18:2": 10.5, "C18:3": 0.2,
    "C20:0": 0.3, "C20:1": 0.2
}

blend_lg = {k: 0.18 * RPKO_PROFILE.get(k, 0) + 0.82 * RBDT_PROFILE.get(k, 0) for k in set(RPKO_PROFILE) | set(RBDT_PROFILE)}

st.set_page_config(page_title="LipidGenesis - Blend LG", layout="wide")

# === Título principal ===
st.title("🌿 LipidGenesis - Bioengineering Of Oils For Nextgen")
st.markdown("<h3 style='text-align: center; color: #4C9B9C;'>Produto: Blend LG 82/18 RBDT:RPKO</h3>", unsafe_allow_html=True)

# === Sidebar ===
st.sidebar.title("🔬 Configurações")
linha = st.sidebar.selectbox("Linha de Produto:", ["Ekos", "Chronos", "Tododia", "Mamãe e Bebê"], index=0)
ocasião = st.sidebar.selectbox("Ocasião de Uso:", ["Banho", "Rosto", "Corpo", "Cabelos"], index=0)

# === Funções ===
def gerar_receita_lipidica(blend):
    df = pd.DataFrame.from_dict(blend, orient='index', columns=['%'])
    df.index.name = 'Ácido Graxo'
    return df

def get_sensory_recipe(line, occasion):
    {
  "Vitalis": {
    "Banho": {
      "Ingrediente-chave": "Capim-santo da Amazônia",
      "Notas olfativas": "Verde, Refrescante",
      "Emoções evocadas": "Revitalização, Energia",
      "Etiqueta sensorial": "Despertar amazônico"
    },
    "Rosto": {
      "Ingrediente-chave": "Guaraná",
      "Notas olfativas": "Frutado, Vibrante",
      "Emoções evocadas": "Frescor, Vitalidade",
      "Etiqueta sensorial": "Brisa tropical"
    },
    "Corpo": {
      "Ingrediente-chave": "Andiroba",
      "Notas olfativas": "Herbal, Terroso",
      "Emoções evocadas": "Renovação, Força",
      "Etiqueta sensorial": "Força da floresta"
    },
    "Cabelos": {
      "Ingrediente-chave": "Menta amazônica",
      "Notas olfativas": "Mentolado, Refrescante",
      "Emoções evocadas": "Leveza, Frescor",
      "Etiqueta sensorial": "Toque verde amazônico"
    }
  },
  "Essentia": {
    "Banho": {
      "Ingrediente-chave": "Flor de Vitória-Régia",
      "Notas olfativas": "Aquático, Floral",
      "Emoções evocadas": "Leveza, Plenitude",
      "Etiqueta sensorial": "Flor d'água"
    },
    "Rosto": {
      "Ingrediente-chave": "Açaí",
      "Notas olfativas": "Frutado, Doce",
      "Emoções evocadas": "Vitalidade, Juventude",
      "Etiqueta sensorial": "Brilho tropical"
    },
    "Corpo": {
      "Ingrediente-chave": "Copaíba",
      "Notas olfativas": "Balsâmico, Quente",
      "Emoções evocadas": "Proteção, Bem-estar",
      "Etiqueta sensorial": "Cura da floresta"
    },
    "Cabelos": {
      "Ingrediente-chave": "Buriti",
      "Notas olfativas": "Frutado, Solar",
      "Emoções evocadas": "Luminosidade, Vida",
      "Etiqueta sensorial": "Raio dourado"
    }
  },
  "Ardor": {
    "Banho": {
      "Ingrediente-chave": "Pimenta-de-macaco",
      "Notas olfativas": "Especiado, Quente",
      "Emoções evocadas": "Excitação, Coragem",
      "Etiqueta sensorial": "Chama tropical"
    },
    "Rosto": {
      "Ingrediente-chave": "Breu Branco",
      "Notas olfativas": "Resinoso, Amadeirado",
      "Emoções evocadas": "Misticismo, Foco",
      "Etiqueta sensorial": "Resina da alma"
    },
    "Corpo": {
      "Ingrediente-chave": "Cumaru (Baunilha Amazônica)",
      "Notas olfativas": "Doce, Ambarado",
      "Emoções evocadas": "Sedução, Doçura",
      "Etiqueta sensorial": "Âmbar da floresta"
    },
    "Cabelos": {
      "Ingrediente-chave": "Castanha-do-Pará",
      "Notas olfativas": "Amendoado, Envolvente",
      "Emoções evocadas": "Conforto, Riqueza",
      "Etiqueta sensorial": "Nutrição natural"
    }
  },
  "Lúmina": {
    "Banho": {
      "Ingrediente-chave": "Jambu",
      "Notas olfativas": "Verde, Refrescante",
      "Emoções evocadas": "Sensação, Frescor",
      "Etiqueta sensorial": "Sopro amazônico"
    },
    "Rosto": {
      "Ingrediente-chave": "Priprioca",
      "Notas olfativas": "Terroso, Aromático",
      "Emoções evocadas": "Conexão, Profundidade",
      "Etiqueta sensorial": "Essência da terra"
    },
    "Corpo": {
      "Ingrediente-chave": "Patuá",
      "Notas olfativas": "Frutado, Exótico",
      "Emoções evocadas": "Vitalidade, Energia",
      "Etiqueta sensorial": "Semente vital"
    },
    "Cabelos": {
      "Ingrediente-chave": "Murumuru",
      "Notas olfativas": "Cremoso, Natural",
      "Emoções evocadas": "Maciez, Proteção",
      "Etiqueta sensorial": "Véu protetor"
    }
  }
}

        }
    }
    return aromatic_profiles.get(line, {}).get(occasion, {"ingrediente": "N/A", "notas": "N/A", "emoções": "N/A", "etiqueta": "Não disponível."})

def gerar_pdf(df_lipidica, sensorial_txt):
    pdf = FPDF()
    pdf.add_page()

    # Título + Slogan (Ajustado para estilo refinado)
    pdf.set_font("Arial", 'B', 18)
    pdf.cell(200, 10, "LipidGenesis - Bioengineering Of Oils For Nextgen", ln=True, align='C')
    pdf.ln(10)

    # Produto centralizado
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "Produto: Blend LG 82/18 RBDT:RPKO", ln=True, align='C')
    pdf.ln(20)

    # Receita Lipídica - Tabela Bonita
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Receita Lipídica:", ln=True)
    pdf.set_font("Arial", '', 12)
    for i, row in df_lipidica.iterrows():
        pdf.cell(0, 10, f"{i}: {row['%']:.2f}%", ln=True)

    # Receita Sensorial
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Receita Sensorial:", ln=True)
    pdf.set_font("Arial", '', 12)
    pdf.multi_cell(0, 10, sensorial_txt)

    # Seção Gráficos
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Gráfico de Ácidos Graxos", ln=True)

    # Aqui você pode adicionar um gráfico (em PNG) gerado no Streamlit, se necessário

    caminho = "/mnt/data/relatorio_refinado_blendlg.pdf"
    pdf.output(caminho)
    return caminho

# === Interface ===
st.header("🔬 Análise Lipídica e Sensorial Refinada")

# Botões com design refinado
if st.button("🧪 Gerar Receita Lipídica", key="lipidica_btn"):
    df_lipidica = gerar_receita_lipidica(blend_lg)
    st.dataframe(df_lipidica)

if st.button("👃 Gerar Receita Sensorial", key="sensorial_btn"):
    sensorial_data = get_sensory_recipe(linha, ocasião)
    sensorial_txt = f"Ingrediente-chave: {sensorial_data['ingrediente']}\nNotas olfativas: {sensorial_data['notas']}\nEmoções evocadas: {sensorial_data['emoções']}\nEtiqueta sensorial: {sensorial_data['etiqueta']}"
    st.success(sensorial_txt)

# Estilo visual para o gráfico
st.subheader("📊 Perfil de Ácidos Graxos no Blend LG")
df_blend_lg = gerar_receita_lipidica(blend_lg)
fig = px.bar(df_blend_lg.reset_index(), x='Ácido Graxo', y='%', title='Distribuição dos Ácidos Graxos', template="plotly_dark")
st.plotly_chart(fig, use_container_width=True)

# === Indicadores Ambientais e ESG ===
st.subheader("🌎 Indicadores Ambientais e ESG")

# Benchmark de CO₂ eq/kg de algumas empresas do setor
benchmark_co2 = {
    "Natura": 1.25,  # Emissões do blend da Natura
    "Unilever": 1.20,  # Benchmark do setor (valores hipotéticos)
    "Johnson & Johnson": 1.15,  # Benchmark de outra empresa do setor (hipotético)
    "LipidGenesis": 0.98  # Sua pegada de CO₂ eq/kg
}

# Cálculo da diferença entre seu produto e os benchmarks
for company, co2_value in benchmark_co2.items():
    delta = (co2_value - benchmark_co2["LipidGenesis"]) / co2_value * 100
    st.metric(f"Emissão de CO₂ eq/kg ({company})", f"{co2_value:.2f}", delta=f"{delta:.1f}%", delta_color="inverse" if delta > 0 else "normal")

# Adicionando outros indicadores ambientais como água, energia, e impacto social
# (Os valores aqui são fictícios e podem ser ajustados conforme necessário)
impacto_ambiental = {
    "Água Consumida (L/kg)": {
        "LipidGenesis": 5.0,  # Exemplo de valor
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

# Exibir os dados de impacto ambiental em tabelas comparativas
for indicator, values in impacto_ambiental.items():
    st.subheader(f"Impacto Ambiental - {indicator}")
    df_impacto = pd.DataFrame.from_dict(values, orient='index', columns=[indicator])
    st.dataframe(df_impacto)

# Estilos refinados para facilitar a leitura e a comparação visual
st.markdown("""
    <style>
        .css-1d391kg { font-size: 1.2em; font-weight: bold; }
        .stDataFrame { font-size: 1em; padding: 10px; border: 1px solid #ddd; }
    </style>
""", unsafe_allow_html=True)

# Exportação Refinada
if st.button("📄 Exportar Relatório PDF", key="export_pdf"):
    df_lipidica = gerar_receita_lipidica(blend_lg)
    sensorial_data = get_sensory_recipe(linha, ocasião)
    sensorial_txt = f"Ingrediente-chave: {sensorial_data['ingrediente']}\nNotas olfativas: {sensorial_data['notas']}\nEmoções evocadas: {sensorial_data['emoções']}\nEtiqueta sensorial: {sensorial_data['etiqueta']}"
    caminho_pdf = gerar_pdf(df_lipidica, sensorial_txt)
    st.markdown(f"**[Baixar Relatório PDF]({caminho_pdf})**")
