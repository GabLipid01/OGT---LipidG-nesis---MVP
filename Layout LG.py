# LipidGenesis – Plataforma de Formulação Inteligente
import streamlit as st
import pandas as pd
import io
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

st.set_page_config(page_title="LipidGenesis", layout="wide")
st.title("🧪 LipidGenesis")
st.caption("Formulação inteligente para cosmética avançada e sob medida")

abas = st.tabs([
    "🏠 Home",
    "🧬 Blend Lipídico",
    "🌺 Receita Sensorial",
    "🌱 ESG e Ambiental",
    "🛰️ Rastreabilidade",
    "📄 Exportação PDF"
])

# ===================== MÓDULO 1 – HOME =====================
with abas[0]:
    st.image("https://images.unsplash.com/photo-1584988414690-7c24b5b4c703", use_column_width=True)
    st.markdown("""
    ## 🌿 Bem-vindo à LipidGenesis
    Plataforma de formulação de blends lipídicos com base em óleos amazônicos e ciência sensorial aplicada.
    """)

# ===================== MÓDULO 2 – BLEND LIPÍDICO =====================
with abas[1]:
    st.header("🧬 Formulação do Blend Lipídico")

    oleo_palma = st.slider("Óleo de Palma (%)", 0, 100, 30)
    oleo_palmiste = st.slider("Óleo de Palmiste (%)", 0, 100 - oleo_palma, 30)
    oleo_buriti = st.slider("Óleo de Buriti (%)", 0, 100 - oleo_palma - oleo_palmiste, 20)
    oleo_andiroba = 100 - oleo_palma - oleo_palmiste - oleo_buriti

    st.markdown(f"**Óleo de Andiroba (%)**: {oleo_andiroba:.1f}%")

    blend_df = pd.DataFrame({
        "Óleo": ["Palma", "Palmiste", "Buriti", "Andiroba"],
        "%": [oleo_palma, oleo_palmiste, oleo_buriti, oleo_andiroba]
    })
    st.dataframe(blend_df, use_container_width=True)

    perfil_df = pd.DataFrame({
        "Ácido Graxo": ["Palmítico", "Oleico", "Linoleico"],
        "Concentração (%)": [
            oleo_palma * 0.4 + oleo_palmiste * 0.5 + oleo_buriti * 0.1 + oleo_andiroba * 0.2,
            oleo_palma * 0.3 + oleo_palmiste * 0.2 + oleo_buriti * 0.5 + oleo_andiroba * 0.6,
            oleo_palma * 0.1 + oleo_palmiste * 0.1 + oleo_buriti * 0.3 + oleo_andiroba * 0.1
        ]
    })
    st.subheader("📊 Perfil de Ácidos Graxos do Blend")
    st.dataframe(perfil_df, use_container_width=True)

# ===================== MÓDULO 3 – RECEITA SENSORIAL =====================
with abas[2]:
    st.header("🌺 Receita Sensorial Personalizada")

    st.subheader("🎨 Escolha as assinaturas olfativas para cada nota:")
    col_topo, col_corpo, col_fundo = st.columns(3)

    with col_topo:
        nota_topo = st.multiselect("Notas de Topo", ["Cítrico", "Herbal", "Mentolado", "Frutado"], default=["Cítrico"])
    with col_corpo:
        nota_corpo = st.multiselect("Notas de Corpo", ["Floral", "Especiado", "Verde", "Amadeirado"], default=["Floral"])
    with col_fundo:
        nota_fundo = st.multiselect("Notas de Fundo", ["Balsâmico", "Terroso", "Almíscar", "Resinoso"], default=["Balsâmico"])

    banco_sensorial = {
        "Cítrico": {"emoji": "🍋", "emoção": "Refrescância"},
        "Herbal": {"emoji": "🌿", "emoção": "Pureza"},
        "Mentolado": {"emoji": "❄️", "emoção": "Frescor"},
        "Frutado": {"emoji": "🍑", "emoção": "Vitalidade"},
        "Floral": {"emoji": "🌸", "emoção": "Sensualidade"},
        "Especiado": {"emoji": "🌶️", "emoção": "Energia"},
        "Verde": {"emoji": "🍃", "emoção": "Natureza"},
        "Amadeirado": {"emoji": "🌲", "emoção": "Força"},
        "Balsâmico": {"emoji": "🪵", "emoção": "Aconchego"},
        "Terroso": {"emoji": "🌍", "emoção": "Conexão"},
        "Almíscar": {"emoji": "🧴", "emoção": "Intimidade"},
        "Resinoso": {"emoji": "🕯️", "emoção": "Profundidade"}
    }

    def render_piramide(notas, camada):
        st.markdown(f"**{camada}**")
        for nota in notas:
            info = banco_sensorial.get(nota, {})
            emoji = info.get("emoji", "✨")
            emocao = info.get("emoção", "")
            st.markdown(f"- {emoji} {nota} — *{emocao}*")

    st.subheader("🌿 Pirâmide Sensorial do Blend")
    with st.container():
        st.markdown("#### Topo")
        render_piramide(nota_topo, "Notas de Topo")
        st.markdown("#### Corpo")
        render_piramide(nota_corpo, "Notas de Corpo")
        st.markdown("#### Fundo")
        render_piramide(nota_fundo, "Notas de Fundo")

    st.success("A receita sensorial foi criada com alma e ciência 🌱")

# ===================== MÓDULO 4 – ESG =====================
with abas[3]:
    st.header("🌱 Análise ESG e Ambiental")

    origem_amazonica = (oleo_andiroba + oleo_buriti)
    carbono_reduzido = (oleo_palma + oleo_palmiste) * 0.4
    rastreabilidade = 80 + (oleo_andiroba * 0.2)

    st.metric("🌿 Ingredientes Amazônicos no Blend", f"{origem_amazonica:.1f}%")
    st.progress(min(origem_amazonica / 100, 1.0))

    st.metric("♻️ Redução de Pegada de Carbono (estimada)", f"{carbono_reduzido:.1f}%")
    st.progress(min(carbono_reduzido / 100, 1.0))

    st.metric("📍 Índice de Rastreabilidade", f"{rastreabilidade:.1f}%")
    st.progress(min(rastreabilidade / 100, 1.0))

    st.markdown("---")
    st.subheader("📢 Mensagem ESG do Blend")
    msg = ""
    if origem_amazonica > 30:
        msg += "🌿 **Blend com forte base amazônica**, promovendo biodiversidade e bioeconomia.\n"
    if rastreabilidade > 85:
        msg += "📍 **Rastreabilidade elevada**, fortalecendo transparência na cadeia.\n"
    if carbono_reduzido > 30:
        msg += "♻️ **Baixo impacto de carbono**, alinhado à agenda climática global.\n"

    if msg:
        st.success(msg.strip())
    else:
        st.info("🔎 Ajuste os óleos para otimizar os indicadores ESG do seu blend.")

# ===================== MÓDULO 5 – RASTREABILIDADE E PDF =====================
with abas[4]:
    st.header("🛰️ Rastreabilidade e Origem dos Ingredientes")

    mapa_origem = {
        "Palma": "Pará (cultivo responsável)",
        "Palmiste": "Pará",
        "Buriti": "Amazônia Central",
        "Andiroba": "Territórios extrativistas no Acre"
    }

    rastreio_df = pd.DataFrame({
        "Óleo": ["Palma", "Palmiste", "Buriti", "Andiroba"],
        "Origem": [mapa_origem["Palma"], mapa_origem["Palmiste"], mapa_origem["Buriti"], mapa_origem["Andiroba"]],
        "Proporção (%)": [oleo_palma, oleo_palmiste, oleo_buriti, oleo_andiroba]
    })

    st.dataframe(rastreio_df, use_container_width=True)
    st.markdown("🌿 **Todos os ingredientes possuem rastreabilidade geográfica e compromisso ambiental.**")

with abas[5]:
    st.header("📄 Exportação do Relatório em PDF")

    def gerar_relatorio_pdf():
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        flowables = []

        flowables.append(Paragraph("🧪 LipidGenesis – Relatório Técnico do Blend", styles["Heading1"]))
        flowables.append(Spacer(1, 12))

        flowables.append(Paragraph("📌 Composição do Blend", styles["Heading2"]))
        flowables.append(Paragraph(str(blend_df.to_string(index=False)), styles["Normal"]))
        flowables.append(Spacer(1, 12))

        flowables.append(Paragraph("🧬 Perfil de Ácidos Graxos", styles["Heading2"]))
        flowables.append(Paragraph(str(perfil_df.to_string()), styles["Normal"]))
        flowables.append(Spacer(1, 12))

        flowables.append(Paragraph("🌺 Receita Sensorial", styles["Heading2"]))
        for camada, notas in [("Notas de Topo", nota_topo), ("Notas de Corpo", nota_corpo), ("Notas de Fundo", nota_fundo)]:
            flowables.append(Paragraph(camada, styles["Heading3"]))
            for nota in notas:
                emocao = banco_sensorial[nota]["emoção"]
                emoji = banco_sensorial[nota]["emoji"]
                flowables.append(Paragraph(f"{emoji} {nota} — {emocao}", styles["Normal"]))

        flowables.append(Spacer(1, 12))
        flowables.append(Paragraph("🌱 Indicadores ESG", styles["Heading2"]))
        flowables.append(Paragraph(f"Amazônicos: {origem_amazonica:.1f}% | Pegada de Carbono: {carbono_reduzido:.1f}% | Rastreabilidade: {rastreabilidade:.1f}%", styles["Normal"]))

        doc.build(flowables)
        pdf = buffer.getvalue()
        buffer.close()
        return pdf

    if st.button("📤 Gerar PDF"):
        pdf_bytes = gerar_relatorio_pdf()
        st.download_button("📥 Baixar Relatório", data=pdf_bytes, file_name="Relatorio_LipidGenesis.pdf", mime="application/pdf")
