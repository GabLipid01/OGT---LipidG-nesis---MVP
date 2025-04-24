import streamlit as st
import pandas as pd

# Título e descrição
st.set_page_config(page_title="LipidGenesis", layout="wide")
st.title("LipidGenesis - Reinventing Oils for the Next Generation")
st.markdown("**Simulador de blends lipídicos e receitas sensoriais para a Natura**")

# Escolha de linha de produto e ocasião de uso
linha_produto = st.selectbox("Linha de Produto", ["Ekos", "Chronos", "Tododia", "Mamãe e Bebê"])
ocasiao_uso = st.selectbox("Ocasião de Uso", ["Banho", "Rosto", "Corpo", "Cabelos"])

# Carregando perfis de ácidos graxos
rpk_df = pd.DataFrame({
    'Ácido Graxo': ['C8:0', 'C10:0', 'C12:0', 'C14:0', 'C16:0', 'C18:0', 'C18:1', 'C18:2', 'C18:3'],
    'RPKO (%)': [3.5, 3.8, 45.0, 15.2, 8.1, 1.2, 15.4, 6.4, 1.4],
    'RBDT (%)': [0.2, 0.1, 0.3, 0.5, 13.0, 4.2, 41.0, 39.5, 1.2]
})

# Cálculo automático dos blends
def calcular_blend(rbdt_pct, rpko_pct, proporcao_rbdt, proporcao_rpko):
    return round((rbdt_pct * proporcao_rbdt + rpko_pct * proporcao_rpko), 2)

def gerar_blend_df(rpk_df, prop_rbdt, prop_rpko):
    data = []
    for i, row in rpk_df.iterrows():
        acido = row['Ácido Graxo']
        pct = calcular_blend(row['RBDT (%)'], row['RPKO (%)'], prop_rbdt=prop_rbdt, prop_rpko=prop_rpko)
        data.append({'Ácido Graxo': acido, 'Blend (%)': pct})
    return pd.DataFrame(data)

# Botão para gerar receita lipídica
if st.button("Gerar Receita Lipídica"):
    st.subheader("Blend 82/18 (82% RBDT / 18% RPKO)")
    blend_8218 = gerar_blend_df(rpk_df, 0.82, 0.18)
    st.dataframe(blend_8218)

    st.subheader("Blend 90/10 (90% RBDT / 10% RPKO)")
    blend_9010 = gerar_blend_df(rpk_df, 0.90, 0.10)
    st.dataframe(blend_9010)

# === Banco de assinaturas aromáticas ===
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

# Botão para gerar a receita sensorial
if st.button("Gerar Receita Sensorial"):
    sensorial = get_sensory_recipe(linha_produto, ocasiao_uso)
    st.markdown("### Receita Sensorial")
    st.markdown(f"**Ingrediente-chave:** {sensorial['ingrediente']}")
    st.markdown(f"**Notas olfativas:** {sensorial['notas']}")
    st.markdown(f"**Emoções evocadas:** {sensorial['emoções']}")
    st.markdown(f"*{sensorial['etiqueta']}*")
