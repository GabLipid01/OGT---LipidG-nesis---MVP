# proposta_cosmetica.py
import streamlit as st

def render_proposta_cosmetica(st):
    st.header("Proposta Cosmética 💄")
    st.write(
        "O **LipidPalma™** é focado em **blends lipídicos enzimáticos** para **cosméticos**, "
        "ajustando **toque**, **hidratação**, **estabilidade** e **brilho** conforme a aplicação e o perfil do blend.\n\n"
        "Como apresentado na **Home**, o LipidPalma™ integra pilares de **ESG**, **rastreabilidade** e **inovação**. "
        "Aqui destacamos **como esses conceitos se traduzem em valor concreto para a indústria cosmética**, "
        "tanto em termos de **benefícios práticos** quanto de **narrativa amazônica**."
    )

    st.markdown("---")
    st.subheader("Benefícios por aplicação ✨")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            "- ✋ **Mãos**: absorção rápida, **toque seco** e hidratação leve.\n"
            "- 🧴 **Corpo**: **nutrição** e maciez com textura uniforme.\n"
        )
    with c2:
        st.markdown(
            "- 🙂 **Rosto**: perfil **balanceado**, adequado a peles sensíveis.\n"
            "- 💇‍♀️ **Cabelos**: **brilho**, emoliência e redução de frizz.\n"
        )
    st.caption("Observação: os efeitos variam conforme a composição do blend (PFAD/RBD/PKO/derivados) e a presença de essências.")

    st.markdown("---")
    st.subheader("Contribuição dos ingredientes-base 🧪")
    st.markdown(
        """
| Ingrediente                  | Contribuição cosmética                                                                 |
|------------------------------|-----------------------------------------------------------------------------------------|
| 🟠 **RBD(Óleo de Palma)**     | **Estabilidade oxidativa**, textura uniforme, base versátil                             |
| 🧴 **Estearina de Palma**     | Textura **firme**; dá corpo a cremes/manteigas; opacidade em pomadas e sabonetes        |
| ✨ **Oleína de Palma**        | Fração **líquida e leve**; boa espalhabilidade; usada em loções e óleos capilares       |
| 🌰 **RPKO(Óleo de Palmiste)** | **Leveza** e **toque seco**; brilho em cabelos; melhora espalhabilidade                 |
| 🧼 **Estearina de Palmiste**  | **Dureza** e espuma; rica em C12–C14; usada em sabonetes e shampoos sólidos              |
| 💧 **Oleína de Palmiste**     | Fração mais fluida; toque leve; alternativa de baixo custo em hidratantes de absorção rápida |
| 🌿 **PFAD**                   | Emoliência e **hidratação profunda**; corpo de fórmula                                  |
| ♻️ **Soapstock**              | Subproduto do refino químico; pode ser refinado/esterificado em blends sustentáveis com apelo ESG |
        """,
        help="Mapa qualitativo ampliado: inclui frações da palma e palmiste, além de PFAD e soapstock (upcycling)."
    )
    st.caption("Nota: **soapstock** requer adequação regulatória (refino/esterificação e dossiê) antes de uso em cosméticos.")

    st.markdown("---")
    st.subheader("Assinatura Sensorial Amazônica (opcional) 🍃")
    st.caption("Vitrine inspiracional de essências; a seleção efetiva é feita na aba **Assistente de Formulação**.")

    _ess_raw = st.session_state.get("ESSENCIAS", [])
    _default_emojis = ["🌰","🔥","🌿","🌳","🍂","🌸","🌺","🌲"]
    _ess = []
    for i, e in enumerate(_ess_raw[:6]):
        _ess.append({
            "emoji":   e.get("emoji", _default_emojis[i % len(_default_emojis)]),
            "nome":    e.get("nome", "Essência"),
            "acorde":  e.get("acorde", "—"),
            "família": e.get("família", "—"),
            "nota":    e.get("nota", "—"),
        })

    row1 = st.columns(3)
    row2 = st.columns(3)
    cards = row1 + row2
    for col, e in zip(cards, _ess):
        with col:
            st.markdown(
                f"**{e['emoji']} {e['nome']}**\n\n"
                f"- Acorde: *{e['acorde']}*\n"
                f"- Família: *{e['família']}*\n"
                f"- Nota: *{e['nota']}*\n"
            )

    st.markdown("---")
    st.subheader("Proposta de valor para P&D e negócio 🚀")
    st.markdown(
        "- ⚡ **Velocidade de P&D**: triagem digital antes do laboratório.\n"
        "- 🧬 **Precisão**: possibilidade de usar **perfis reais** de ácidos graxos (quando habilitado no Blend).\n"
        "- ♻️ **Sustentabilidade**: upcycling (PFAD/soapstock) e **ESG** transparente.\n"
        "- 🔍 **Rastreabilidade**: ficha de ingredientes e certificações (CSV exportável).\n"
        "- 🛠️ **Customização**: ajuste do blend por **ocasião de uso** e assinatura sensorial (essências amazônicas opcionais).\n"
        "- 📈 **Negócio**: foco em **protótipos + patentes + licenciamento** (modelo B2B)."
    )
    with st.expander("💡 Exemplos de posicionamento/claims (ideias)"):
        st.markdown(
            "- “Toque sedoso com rápida absorção” (mãos/corpo)\n"
            "- “Nutrição e maciez com leveza” (corpo)\n"
            "- “Perfil balanceado para peles delicadas” (rosto)\n"
            "- “Brilho e emoliência com controle de frizz” (cabelos)\n"
        )
        st.caption("Claims dependem de validação de bancada e requisitos regulatórios.")
