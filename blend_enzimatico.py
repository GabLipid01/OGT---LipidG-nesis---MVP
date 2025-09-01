# -*- coding: utf-8 -*-
# blend_enzimatico.py

import io, json, math
from collections import OrderedDict
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# ----------------- Catálogo de ingredientes (Classe A/C) -----------------
INGREDIENTS = [
    ("rbd_palma",            "🟠 RBD (Óleo de Palma)"),
    ("estearina_palma",      "🧴 Estearina de Palma"),
    ("oleina_palma",         "✨ Oleína de Palma"),
    ("rpko_palmiste",        "🌰 RPKO (Óleo de Palmiste)"),
    ("estearina_palmiste",   "🧼 Estearina de Palmiste"),
    ("oleina_palmiste",      "💧 Oleína de Palmiste"),
    ("pfad",                 "🌿 PFAD"),
    ("soapstock",            "♻️ Soapstock"),
]

# ----------------- Médias calibradas (faixas típicas) -----------------
# II/ISap = médias das faixas mostradas nos expanders; PF = média calibrada se conhecida.
KPI_MEANS = {
    "rbd_palma":          {"II": 52.5, "ISap": 197.5, "PF": 36},  # PF 34–38 → 36
    "estearina_palma":    {"II": 37.0, "ISap": 192.5},            # PF não informado: será estimado do perfil FA
    "oleina_palma":       {"II": 60.0, "ISap": 200.0},
    "rpko_palmiste":      {"II": 18.0, "ISap": 247.5},
    "estearina_palmiste": {"II": 11.0, "ISap": 242.5},
    "oleina_palmiste":    {"II": 23.0, "ISap": 247.5},
    "pfad":               {"II": 50.0, "ISap": 195.0},
    "soapstock":          {"II": 57.5, "ISap": 197.5},
}

# ----------------- Constantes FA -----------------
FA_CONST = {
    "C12:0": {"IV": 0.0,   "MW": 200.32},
    "C14:0": {"IV": 0.0,   "MW": 228.37},
    "C16:0": {"IV": 0.0,   "MW": 256.42},
    "C18:0": {"IV": 0.0,   "MW": 284.48},
    "C18:1": {"IV": 90.0,  "MW": 282.47},
    "C18:2": {"IV": 181.0, "MW": 280.45},
    "C18:3": {"IV": 273.0, "MW": 278.43},
}
FA_ORDER = list(FA_CONST.keys())

# ----------------- Perfis FA por ingrediente (Min/Mean/Max) -----------------
FA_PROFILES_RANGED = {
    "rbd_palma": {
        "mean": {"C16:0": 44, "C18:1": 39, "C18:2": 10, "C18:0": 4, "C14:0": 1, "C12:0": 0},
        "min":  {"C16:0": 41, "C18:1": 36, "C18:2": 8,  "C18:0": 3, "C14:0": 1, "C12:0": 0},
        "max":  {"C16:0": 47, "C18:1": 42, "C18:2": 12, "C18:0": 5, "C14:0": 2, "C12:0": 1},
    },
    "oleina_palma": {
        "mean": {"C16:0": 39, "C18:1": 42, "C18:2": 13, "C18:0": 4, "C14:0": 1, "C12:0": 0},
        "min":  {"C16:0": 36, "C18:1": 39, "C18:2": 11, "C18:0": 3, "C14:0": 1, "C12:0": 0},
        "max":  {"C16:0": 42, "C18:1": 45, "C18:2": 15, "C18:0": 5, "C14:0": 2, "C12:0": 1},
    },
    "estearina_palma": {
        "mean": {"C16:0": 55, "C18:1": 33, "C18:2": 7,  "C18:0": 4, "C14:0": 1, "C12:0": 0},
        "min":  {"C16:0": 52, "C18:1": 30, "C18:2": 6,  "C18:0": 3, "C14:0": 1, "C12:0": 0},
        "max":  {"C16:0": 58, "C18:1": 36, "C18:2": 9,  "C18:0": 5, "C14:0": 2, "C12:0": 1},
    },
    "rpko_palmiste": {
        "mean": {"C12:0": 48, "C14:0": 16, "C16:0": 8,  "C18:1": 15, "C18:2": 2, "C18:0": 2},
        "min":  {"C12:0": 45, "C14:0": 14, "C16:0": 7,  "C18:1": 13, "C18:2": 2, "C18:0": 1},
        "max":  {"C12:0": 51, "C14:0": 18, "C16:0": 9,  "C18:1": 17, "C18:2": 3, "C18:0": 3},
    },
    "oleina_palmiste": {
        "mean": {"C12:0": 42, "C14:0": 15, "C16:0": 10, "C18:1": 20, "C18:2": 4, "C18:0": 2},
        "min":  {"C12:0": 39, "C14:0": 14, "C16:0": 9,  "C18:1": 18, "C18:2": 3, "C18:0": 1},
        "max":  {"C12:0": 45, "C14:0": 17, "C16:0": 11, "C18:1": 22, "C18:2": 5, "C18:0": 3},
    },
    "estearina_palmiste": {
        "mean": {"C12:0": 50, "C14:0": 17, "C16:0": 7,  "C18:1": 12, "C18:2": 3, "C18:0": 3},
        "min":  {"C12:0": 47, "C14:0": 15, "C16:0": 6,  "C18:1": 10, "C18:2": 2, "C18:0": 2},
        "max":  {"C12:0": 53, "C14:0": 19, "C16:0": 8,  "C18:1": 14, "C18:2": 4, "C18:0": 4},
    },
    "pfad": {
        "mean": {"C16:0": 50, "C18:1": 35, "C18:2": 10, "C18:0": 5},
        "min":  {"C16:0": 47, "C18:1": 33, "C18:2": 8,  "C18:0": 4},
        "max":  {"C16:0": 53, "C18:1": 37, "C18:2": 12, "C18:0": 6},
    },
    "soapstock": {
        "mean": {"C16:0": 40, "C18:1": 40, "C18:2": 15, "C18:0": 5},
        "min":  {"C16:0": 37, "C18:1": 38, "C18:2": 13, "C18:0": 4},
        "max":  {"C16:0": 43, "C18:1": 42, "C18:2": 17, "C18:0": 6},
    },
}

# ----------------- Helpers -----------------
def _normalize_percentages(d: dict) -> dict:
    total = sum(float(v or 0) for v in d.values())
    if total <= 0:
        return {k: 0.0 for k in d}
    return {k: (float(v or 0) * 100.0 / total) for k, v in d.items()}

def _badge_total(total: float, prefix="Total"):
    msg = f"**{prefix}: {total:.2f}%**"
    if abs(total - 100.0) < 1e-6:
        st.success(msg)
    elif total < 100:
        st.warning(msg + " • abaixo de 100%")
    else:
        st.error(msg + " • acima de 100%")

def _get_profile(ing_key: str, scenario: str) -> dict:
    profs = FA_PROFILES_RANGED.get(ing_key, {})
    return profs.get(scenario, profs.get("mean", {}))

# KPIs FA-based
def iodine_index(fa_pct: dict) -> float:
    return sum((fa_pct.get(k, 0.0) / 100.0) * FA_CONST[k]["IV"] for k in FA_CONST.keys())

def saponification_index(fa_pct: dict) -> float:
    return sum((fa_pct.get(k, 0.0) / 100.0) * (560.0 / FA_CONST[k]["MW"]) for k in FA_CONST.keys())

def melt_index(fa_pct: dict) -> float:
    # índice 0–100 (proxy de ponto de fusão)
    sat = fa_pct.get("C12:0",0)+fa_pct.get("C14:0",0)+fa_pct.get("C16:0",0)+fa_pct.get("C18:0",0)
    mono = fa_pct.get("C18:1",0)
    poly = fa_pct.get("C18:2",0)+fa_pct.get("C18:3",0)
    score = (0.6*sat + 0.2*(fa_pct.get("C16:0",0)+fa_pct.get("C18:0",0)) - 0.3*poly + 0.05*mono)
    return max(0.0, min(100.0, score))

# Sensorial (heurístico)
def _spread(fa):  # espalhabilidade
    insat = fa.get("C18:1",0) + fa.get("C18:2",0) + fa.get("C18:3",0)
    laur = fa.get("C12:0",0) + fa.get("C14:0",0)
    return max(0, min(100, 0.7*insat + 0.2*laur))

def _hidr(fa):
    lin = fa.get("C18:2",0); ole = fa.get("C18:1",0)
    sat = fa.get("C16:0",0) + fa.get("C18:0",0)
    return max(0, min(100, 0.5*lin + 0.4*ole + 0.1*sat))

def _ocl(fa):  # oclusão
    sat = fa.get("C12:0",0)+fa.get("C14:0",0)+fa.get("C16:0",0)+fa.get("C18:0",0)
    return max(0, min(100, 0.9*sat))

def _toque_seco(PF_idx):
    return max(0, min(100, 100 - PF_idx))

def _brilho(fa):
    ole = fa.get("C18:1",0); laur = fa.get("C12:0",0)+fa.get("C14:0",0)
    return max(0, min(100, 0.6*ole + 0.3*laur))

def _scores_finais(fa, PF_idx, II_for_scores):
    spread = _spread(fa); hidr = _hidr(fa)
    ocl = _ocl(fa); toque = _toque_seco(PF_idx); brilho_v = _brilho(fa)
    scores = OrderedDict()
    scores["Mãos"]    = round(0.5*toque + 0.3*spread + 0.2*max(0,100-0.4*II_for_scores), 1)
    scores["Corpo"]   = round(0.4*hidr  + 0.3*ocl    + 0.3*max(0,100-0.4*II_for_scores), 1)
    scores["Rosto"]   = round(0.4*fa.get("C18:1",0) + 0.3*max(0,100-0.4*II_for_scores) + 0.3*toque, 1)
    scores["Cabelos"] = round(0.5*spread + 0.3*fa.get("C18:1",0) + 0.2*max(0,100-0.4*II_for_scores), 1)
    radar = OrderedDict(toque=int(round(toque)), hidr=int(round(hidr)),
                        brilho=int(round(brilho_v)), oclusividade=int(round(ocl)),
                        absorcao=int(round((toque+spread)/2)))
    return scores, radar

# Baseline calibrado (A + C)
def kpis_calibrados_por_medias(A_vals: dict, C_vals: dict, scenario: str) -> tuple[float,float,float]:
    total_ref = sum(A_vals.values()) + sum(C_vals.values())
    if total_ref <= 0: return 0.0, 0.0, 0.0
    II = 0.0; IS = 0.0; PFm = 0.0
    for bucket, vals in (("A", A_vals), ("C", C_vals)):
        for ing_key, pct in vals.items():
            if pct <= 0: continue
            w = pct / total_ref
            km = KPI_MEANS.get(ing_key, {})
            II  += w * km.get("II", 0.0)
            IS  += w * km.get("ISap", 0.0)
            # PF calibrado: usa média calibrada se existir; senão estima do perfil FA 'mean'
            if "PF" in km:
                pf_loc = km["PF"]
            else:
                prof = _get_profile(ing_key, scenario)
                pf_loc = melt_index(prof)
            PFm += w * pf_loc
    return II, IS, PFm

def _fa_from_mix(ing_mix: dict, total_ref: float, scenario_key: str):
    fa_tmp = {k: 0.0 for k in FA_ORDER}
    if total_ref <= 0: return fa_tmp
    for ing_key, pct in ing_mix.items():
        if pct <= 0: continue
        w = pct / total_ref
        prof = _get_profile(ing_key, scenario_key)
        for fa_key, fa_pct in prof.items():
            fa_tmp[fa_key] += w * fa_pct
    return _normalize_percentages(fa_tmp)

def _plot_tradeoff_bars(title: str, labels: list, deltas: list, ylabel: str):
    fig, ax = plt.subplots()
    ax.bar(range(len(labels)), deltas)
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=45, ha='right')
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    st.pyplot(fig)

def _compute_tradeoffs_heuristico(A_vals, method, B_vals, C_vals, consider_var, scenario):
    total_A = sum(A_vals.values())
    total_adjust = sum(B_vals.values()) if method.startswith("Classe B") else sum(C_vals.values())
    total_all = total_A + total_adjust
    if total_all <= 0: return None

    # ponto de partida
    fa_base = {k:0.0 for k in FA_ORDER}
    for ing_key, pct in A_vals.items():
        if pct <= 0: continue
        w = pct / total_all
        prof = _get_profile(ing_key, scenario if consider_var else "mean")
        for fk, fp in prof.items():
            fa_base[fk] += w * fp
    if method.startswith("Classe B"):
        for fk, pct in B_vals.items():
            if pct <= 0: continue
            w = pct / total_all
            fa_base[fk] += w * 100.0
    else:
        for ing_key, pct in C_vals.items():
            if pct <= 0: continue
            w = pct / total_all
            prof = _get_profile(ing_key, scenario if consider_var else "mean")
            for fk, fp in prof.items():
                fa_base[fk] += w * fp
    fa_base = _normalize_percentages(fa_base)
    II0, IS0, PF0 = iodine_index(fa_base), saponification_index(fa_base), melt_index(fa_base)

    labels, dII, dIS, dPF = [], [], [], []
    for ing_key, pct in A_vals.items():
        inc = 5.0
        A_new = A_vals.copy(); A_new[ing_key] = max(0.0, pct + inc)
        new_total_A = sum(A_new.values())
        factor = (total_all) / (new_total_A + total_adjust) if (new_total_A + total_adjust) > 0 else 1.0
        for k in A_new: A_new[k] *= factor

        fa_new = {k:0.0 for k in FA_ORDER}
        for k, pv in A_new.items():
            if pv <= 0: continue
            w = pv / total_all
            prof = _get_profile(k, scenario if consider_var else "mean")
            for fk, fp in prof.items():
                fa_new[fk] += w * fp
        if method.startswith("Classe B"):
            for fk, pv in B_vals.items():
                if pv <= 0: continue
                w = pv / total_all
                fa_new[fk] += w * 100.0
        else:
            for k, pv in C_vals.items():
                if pv <= 0: continue
                w = pv / total_all
                prof2 = _get_profile(k, scenario if consider_var else "mean")
                for fk, fp in prof2.items():
                    fa_new[fk] += w * fp
        fa_new = _normalize_percentages(fa_new)
        II1, IS1, PF1 = iodine_index(fa_new), saponification_index(fa_new), melt_index(fa_new)

        label = next(lbl for key,lbl in INGREDIENTS if key==ing_key)
        labels.append(label); dII.append(round(II1 - II0, 2)); dIS.append(round(IS1 - IS0, 2)); dPF.append(round(PF1 - PF0, 2))
    return labels, dII, dIS, dPF

def _compute_tradeoffs_upload(fa_start, method_upl, B_vals_u, C_vals_u, consider_var, scenario):
    fa_base = _normalize_percentages(fa_start.copy())
    II0, IS0, PF0 = iodine_index(fa_base), saponification_index(fa_base), melt_index(fa_base)
    labels, dII, dIS, dPF = [], [], [], []
    for ing_key, label in INGREDIENTS:
        add_pct = 5.0
        add_fa = {k:0.0 for k in FA_ORDER}
        prof = _get_profile(ing_key, scenario if consider_var else "mean")
        for fk, fp in prof.items():
            add_fa[fk] += (add_pct * fp / 100.0)

        fa_new = fa_base.copy()
        for fk, inc in add_fa.items():
            fa_new[fk] = fa_new.get(fk, 0.0) + inc
        fa_new = _normalize_percentages(fa_new)

        if method_upl.startswith("Classe B"):
            totB = sum(B_vals_u.values())
            if totB > 0:
                for fk, pv in B_vals_u.items():
                    fa_new[fk] = fa_new.get(fk, 0.0) + pv
                fa_new = _normalize_percentages(fa_new)
        else:
            totC = sum(C_vals_u.values())
            if totC > 0:
                add2 = {k:0.0 for k in FA_ORDER}
                for k, pv in C_vals_u.items():
                    if pv <= 0: continue
                    prof2 = _get_profile(k, scenario if consider_var else "mean")
                    for fk, fp in prof2.items():
                        add2[fk] += (pv * fp / 100.0)
                for fk, inc2 in add2.items():
                    fa_new[fk] = fa_new.get(fk, 0.0) + inc2
                fa_new = _normalize_percentages(fa_new)

        II1, IS1, PF1 = iodine_index(fa_new), saponification_index(fa_new), melt_index(fa_new)
        labels.append(label); dII.append(round(II1 - II0, 2)); dIS.append(round(IS1 - IS0, 2)); dPF.append(round(PF1 - PF0, 2))
    return labels, dII, dIS, dPF

def _plot_fa_bars(fa_norm):
    data = [fa_norm.get(k, 0.0) for k in FA_ORDER]
    fig, ax = plt.subplots()
    ax.bar(range(len(FA_ORDER)), data)
    ax.set_xticks(range(len(FA_ORDER))); ax.set_xticklabels(FA_ORDER, rotation=45, ha='right')
    ax.set_ylabel('%'); ax.set_title('Composição por Ácido Graxo (%)')
    st.pyplot(fig)

def _plot_radar(rad_dict):
    labels = list(rad_dict.keys()); values = [rad_dict[k] for k in labels]
    N = len(labels); import math as _m
    angles = [n / float(N) * 2 * _m.pi for n in range(N)]
    values += values[:1]; angles += angles[:1]
    fig, ax = plt.subplots(subplot_kw=dict(polar=True))
    ax.plot(angles, values); ax.fill(angles, values, alpha=0.25)
    ax.set_xticks(angles[:-1]); ax.set_xticklabels(labels); ax.set_yticklabels([])
    ax.set_title("Radar Sensorial (0–100)")
    st.pyplot(fig)

# ----------------- RENDER -----------------
def render_blend_enzimatico():
    st.header("Blend Enzimático ⚗️")
    st.caption(
        "Defina o blend por **Classe A (Ingredientes da palma)** e, se necessário, aplique **ajuste fino** por "
        "**Classe B (Ácidos graxos puros)** ou **Classe C (Ingredientes)**. "
        "No modo Upload real (CSV/XLSX), você também pode aplicar o mesmo ajuste fino. "
        "⚠️ KPIs no modo heurístico são **estimativas** calibradas (médias por ingrediente)."
    )

    # Variabilidade
    st.markdown("### Variabilidade de lote (opcional)")
    consider_var = st.toggle("Considerar variabilidade de lote", value=False, help="Usa perfis Min/Típico/Max por ingrediente.")
    scenario = "mean"
    if consider_var:
        scen_label = st.radio("Cenário", ["Típico", "Min", "Max"], horizontal=True, index=0, key="var_scenario")
        scenario = {"Típico": "mean", "Min": "min", "Max": "max"}[scen_label]

    # Modo
    mode = st.radio("Modo de entrada", ["Heurísticas (rápido)", "Upload de planilha (real)"],
                    horizontal=True, key="blend_mode_radio")

    # ---------------- HEURÍSTICO ----------------
    if mode == "Heurísticas (rápido)":
        st.subheader("Heurísticas com duas camadas: Base (Classe A) + Ajuste fino (B ou C)")
        st.caption("⚠️ **Médias calibradas** para II/ISap/PF quando **sem ajuste**; com ajuste, KPIs passam a ser **técnicos (perfil FA)**.")

        # Classe A
        A_vals = OrderedDict()
        with st.expander("Classe A — Ingredientes da palma (base do blend)", expanded=True):
            colsA = st.columns(4)
            for idx, (k, label) in enumerate(INGREDIENTS):
                with colsA[idx % 4]:
                    A_vals[k] = st.slider(label, 0.0, 100.0, 0.0, 1.0, key=f"slider_ing_{k}")
            total_A = sum(A_vals.values()); _badge_total(total_A, "Total Classe A")

        # Método ajuste
        st.markdown("**Ajuste fino** (opcional): escolha o método")
        method = st.radio("Método de ajuste", ["Classe B — Ácidos graxos puros", "Classe C — Ingredientes"],
                          horizontal=True, key="ajuste_method_heur")

        # Classe B
        B_vals = OrderedDict((fa, 0.0) for fa in FA_ORDER)
        total_B = 0.0
        if method.startswith("Classe B"):
            with st.expander("Classe B — Ajuste fino por Ácidos graxos puros", expanded=True):
                colsB = st.columns(4)
                for idx, fa in enumerate(FA_ORDER):
                    with colsB[idx % 4]:
                        B_vals[fa] = st.slider(f"FA {fa}", 0.0, 100.0, 0.0, 1.0, key=f"slider_fa_{fa}")
                total_B = sum(B_vals.values()); _badge_total(total_B, "Total Classe B")
                if total_B > 30:
                    st.warning("A Classe B excede 30% do blend — considere reduzir para manter o caráter do óleo base.")

        # Classe C
        C_vals = OrderedDict((k, 0.0) for k, _ in INGREDIENTS)
        total_C = 0.0
        if method.endswith("Ingredientes"):
            with st.expander("Classe C — Ajuste fino por Ingredientes", expanded=True):
                colsC = st.columns(4)
                for idx, (k, label) in enumerate(INGREDIENTS):
                    with colsC[idx % 4]:
                        C_vals[k] = st.slider(f"{label} (ajuste)", 0.0, 100.0, 0.0, 1.0, key=f"slider_adj_{k}")
                total_C = sum(C_vals.values()); _badge_total(total_C, "Total Classe C")
                if total_C > 30:
                    st.warning("A Classe C excede 30% do blend — considere reduzir para manter o caráter do óleo base.")

        total_all = total_A + (total_B if method.startswith("Classe B") else total_C)
        st.markdown("---")
        _badge_total(total_all, "Total Global (A + Ajuste)")
        if total_all > 0 and st.button("🔄 Normalizar Global (A + Ajuste) para 100%", key="btn_norm_AB_or_AC"):
            scale = 100.0 / total_all
            for k in A_vals: A_vals[k] *= scale
            if method.startswith("Classe B"):
                for k in B_vals: B_vals[k] *= scale
            else:
                for k in C_vals: C_vals[k] *= scale
            # sincroniza sliders
            for k, v in A_vals.items(): st.session_state[f"slider_ing_{k}"] = round(v, 2)
            if method.startswith("Classe B"):
                for fa, v in B_vals.items(): st.session_state[f"slider_fa_{fa}"] = round(v, 2)
            else:
                for k, v in C_vals.items(): st.session_state[f"slider_adj_{k}"] = round(v, 2)
            st.experimental_rerun()

        # Perfil FA estimado (para gráficos e PF índice)
        fa_est = {k: 0.0 for k in FA_ORDER}
        if total_all > 0:
            for ing_key, pct in A_vals.items():
                if pct <= 0: continue
                w = pct / total_all
                prof = _get_profile(ing_key, scenario if consider_var else "mean")
                for fa_key, fa_pct in prof.items():
                    fa_est[fa_key] += w * fa_pct
            if method.startswith("Classe B"):
                for fa_key, pct in B_vals.items():
                    if pct <= 0: continue
                    w = pct / total_all
                    fa_est[fa_key] += w * 100.0
            else:
                for ing_key, pct in C_vals.items():
                    if pct <= 0: continue
                    w = pct / total_all
                    prof = _get_profile(ing_key, scenario if consider_var else "mean")
                    for fa_key, fa_pct in prof.items():
                        fa_est[fa_key] += w * fa_pct
        fa_est = _normalize_percentages(fa_est)

        # KPIs — baseline calibrado (A + C) x atual técnico (se houver ajuste)
        II_base, IS_base, PF_base = kpis_calibrados_por_medias(A_vals, C_vals, scenario if consider_var else "mean")
        has_adjust = (total_B > 0) or (total_C > 0)
        if has_adjust:
            II_now, IS_now, PF_now = iodine_index(fa_est), saponification_index(fa_est), melt_index(fa_est)
        else:
            II_now, IS_now, PF_now = II_base, IS_base, PF_base

        st.markdown("---")
        st.subheader("KPIs")
        if has_adjust:
            st.caption("🟢 **KPIs no modo técnico (perfil FA)** — ajuste fino ativo.")
        cols1 = st.columns(3)
        cols1[0].metric("Índice de Iodo (II)", f"{II_now:.1f}")
        cols1[1].metric("Índice de Saponificação (ISap)", f"{IS_now:.1f} mgKOH/g")
        cols1[2].metric("Ponto de Fusão", f"{PF_now:.0f}")

        if has_adjust:
            st.caption("Linha de referência (médias calibradas por ingrediente, sem ajuste):")
            cols2 = st.columns(3)
            cols2[0].metric("II — baseline", f"{II_base:.1f}")
            cols2[1].metric("ISap — baseline", f"{IS_base:.1f} mgKOH/g")
            cols2[2].metric("PF — baseline", f"{PF_base:.0f}")

        st.caption("• Sem ajuste: KPIs exibem **médias calibradas por ingrediente**. "
                   "• Com ajuste (B/C): KPIs passam a ser **calculados do perfil FA**. "
                   "• ‘Ponto de Fusão’ é um **índice 0–100** derivado do perfil FA.")

        # Expanders (faixas típicas)
        e1, e2, e3 = st.columns(3)
        with e1:
            with st.expander("ℹ️ Faixas típicas — II (estimativo)"):
                st.markdown(
                    "- **RBD (Palma)**: ~50–55\n"
                    "- **Estearina de Palma**: ~32–42\n"
                    "- **Oleína de Palma**: ~55–65\n"
                    "- **RPKO (Palmiste)**: ~14–22\n"
                    "- **Estearina de Palmiste**: ~8–14\n"
                    "- **Oleína de Palmiste**: ~18–28\n"
                    "- **PFAD**: ~45–55\n"
                    "- **Soapstock**: ~50–65\n"
                )
        with e2:
            with st.expander("ℹ️ Faixas típicas — ISap (mgKOH/g, estimativo)"):
                st.markdown(
                    "- **RBD (Palma)**: ~190–205\n"
                    "- **Estearina de Palma**: ~185–200\n"
                    "- **Oleína de Palma**: ~195–205\n"
                    "- **RPKO (Palmiste)**: ~240–255\n"
                    "- **Estearina de Palmiste**: ~235–250\n"
                    "- **Oleína de Palmiste**: ~240–255\n"
                    "- **PFAD**: ~185–205\n"
                    "- **Soapstock**: ~185–210\n"
                )
        with e3:
            with st.expander("ℹ️ Faixas típicas — Ponto de Fusão (índice 0–100)"):
                st.markdown(
                    "- **Mais saturados/estearinas** → **índice mais alto** (textura firme)\n"
                    "- **Mais insaturados/oleínas** → **índice mais baixo** (toque fluido)\n"
                    "_No baseline exibimos a **média calibrada**; com ajuste exibimos o **índice técnico**._"
                )

        st.info("📄 Após finalizar sua formulação, gere o dossiê completo na aba **Exportação PDF** (perfil FA, KPIs, preview e narrativa).")

        # Gráficos
        g1, g2 = st.columns(2)
        with g1: _plot_fa_bars(fa_est)
        with g2:
            II_for_radar = iodine_index(fa_est)  # coerente com heurísticas sensoriais
            _, radar_vals = _scores_finais(fa_est, melt_index(fa_est), II_for_radar)
            _plot_radar(radar_vals)

        # Trade-offs
        st.markdown("---")
        st.subheader("Análise de Trade-offs (variação de +5% em cada ingrediente da Classe A)")
        trade = _compute_tradeoffs_heuristico(A_vals, method, B_vals, C_vals, consider_var, scenario)
        if trade is None:
            st.caption("Defina a base (Classe A) para visualizar os trade-offs.")
        else:
            labels, dII, dIS, dPF = trade
            cto1, cto2, cto3 = st.columns(3)
            with cto1: _plot_tradeoff_bars("Δ Índice de Iodo (II)", labels, dII, "Δ II")
            with cto2: _plot_tradeoff_bars("Δ Índice de Saponificação (ISap)", labels, dIS, "Δ ISap")
            with cto3: _plot_tradeoff_bars("Δ Ponto de Fusão", labels, dPF, "Δ PF")
            st.caption("Leitura: impacto em KPIs ao variar **+5%** (renormalizado).")

        # Preview finalidade (estimativo)
        st.subheader("Preview de notas por finalidade (0–100) – estimativas")
        scores, _ = _scores_finais(fa_est, melt_index(fa_est), iodine_index(fa_est))
        p1, p2, p3, p4 = st.columns(4)
        p1.metric("Mãos", f"{scores['Mãos']}"); p2.metric("Corpo", f"{scores['Corpo']}")
        p3.metric("Rosto", f"{scores['Rosto']}"); p4.metric("Cabelos", f"{scores['Cabelos']}")

        # Salvar/Carregar
        st.markdown("---")
        st.subheader("Salvar / Carregar Blend (JSON)")
        heur_blend = {
            "modo": "heuristico",
            "classeA_pct": {k: float(v) for k, v in A_vals.items()},
            "classeB_pct": {k: float(v) for k, v in B_vals.items()},
            "classeC_pct": {k: float(v) for k, v in C_vals.items()},
            "ajuste_method": "B" if method.startswith("Classe B") else "C",
            "fa_profile": _normalize_percentages(fa_est),
            "total_pct": float(total_all),
            "variabilidade": {"ativada": bool(consider_var), "cenario": scenario},
            "nota": "Heurístico com Classe A (base) + ajuste fino (B=FA puros OU C=Ingredientes). "
                    "KPIs: baseline (médias calibradas) e atual (técnico se ajuste).",
        }
        cjs1, cjs2 = st.columns(2)
        with cjs1:
            st.download_button(
                label="💾 Baixar Blend (JSON)",
                data=json.dumps(heur_blend, ensure_ascii=False, indent=2).encode("utf-8"),
                file_name="blend_heuristico_ajuste.json",
                mime="application/json",
                key="dl_blend_heuristico_ajuste.json",
            )
        with cjs2:
            uploaded_json = st.file_uploader("📂 Carregar Blend (JSON)", type=["json"], key="blend_json_upload_heur")
            if uploaded_json is not None:
                try:
                    loaded = json.load(uploaded_json)
                    if loaded.get("modo") == "heuristico":
                        for k, v in loaded.get("classeA_pct", {}).items():
                            st.session_state[f"slider_ing_{k}"] = float(v)
                        for k, v in loaded.get("classeB_pct", {}).items():
                            st.session_state[f"slider_fa_{k}"] = float(v)
                        for k, v in loaded.get("classeC_pct", {}).items():
                            st.session_state[f"slider_adj_{k}"] = float(v)
                        st.session_state["blend"] = loaded
                        st.success("Blend heurístico (A + ajuste) carregado e sliders atualizados.")
                        st.experimental_rerun()
                    else:
                        st.warning("JSON não parece ser um blend heurístico.")
                except Exception as e:
                    st.error(f"Erro ao carregar JSON: {e}")

        st.markdown("---")
        st.info("Pronto para detalhar por finalidade no **Assistente de Formulação** (estimativa baseada em heurística).")
        assist_payload = {
            "fa_profile": fa_est,
            "kpis": {"II": II_now, "ISap": IS_now, "PF_proxy": melt_index(fa_est)},  # mantém chave PF_proxy p/ compatibilidade
            "kpis_baseline": {"II": II_base, "ISap": IS_base, "PF": PF_base},
            "source": "heuristica_estimada_A+" + ("B" if method.startswith("Classe B") else "C"),
            "classes": {"A": dict(A_vals), "B": dict(B_vals), "C": dict(C_vals)},
            "variabilidade": {"ativada": bool(consider_var), "cenario": scenario},
        }
        st.session_state["assist_payload"] = assist_payload
        if st.button("➜ Enviar para Assistente de Formulação", key="btn_handoff_assist_est_ABC"):
            st.session_state["go_to_assistente"] = True
            st.success("Perfil estimado enviado. Abra a aba **Assistente de Formulação** para continuar.")

    # ---------------- UPLOAD (perfil real) ----------------
    else:
        st.subheader("Upload de planilha real")
        st.caption(
            "Aceita **CSV/XLSX** com **Ingredientes (%)** ou **Ácidos graxos (%)**. "
            "O sistema **auto-normaliza**. Após carregar, você pode aplicar **ajuste fino** por "
            "**B (FA)** ou **C (Ingredientes)**."
        )

        formato = st.selectbox("Formato da planilha", ["Ingredientes (%)", "Ácidos graxos (%)"], key="formato_planilha")
        if formato == "Ingredientes (%)":
            modelo_df = pd.DataFrame({"Ingrediente": [lbl for _, lbl in INGREDIENTS], "Percentual": [0]*len(INGREDIENTS)})
        else:
            modelo_df = pd.DataFrame({"AcidoGraxos": list(FA_CONST.keys()), "Percentual": [0]*len(FA_CONST)})
        buf = io.BytesIO(); modelo_df.to_csv(buf, index=False)
        st.download_button("📥 Baixar modelo CSV", data=buf.getvalue(), file_name="modelo_blend.csv",
                           mime="text/csv", key="dl_modelo_csv_upload")

        file = st.file_uploader("Carregar planilha (CSV/XLSX)", type=["csv", "xlsx"], key="uploader_real")
        parsed_ing, parsed_fa = OrderedDict(), OrderedDict()
        original_total = None; fa_norm = None

        if file is not None:
            try:
                df = pd.read_csv(file) if file.name.lower().endswith(".csv") else pd.read_excel(file)
            except Exception as e:
                st.error(f"Erro ao ler arquivo: {e}"); df = None

            if df is not None:
                st.write("Prévia da planilha carregada:"); st.dataframe(df, use_container_width=True)
                if formato == "Ingredientes (%)":
                    col_ing, col_pct = "Ingrediente", "Percentual"
                    if col_ing in df.columns and col_pct in df.columns:
                        label_to_key = {lbl: k for k, lbl in INGREDIENTS}
                        for _, row in df.iterrows():
                            lbl = str(row[col_ing]).strip()
                            pct = float(row[col_pct]) if pd.notna(row[col_pct]) else 0.0
                            k = label_to_key.get(lbl)
                            if k: parsed_ing[k] = parsed_ing.get(k, 0.0) + pct
                            else: st.warning(f"Ingrediente não reconhecido e ignorado: '{lbl}'")
                        original_total = sum(parsed_ing.values()); _badge_total(original_total, "Total da planilha (ingredientes)")
                        # converte p/ FA
                        fa_tmp = {k: 0.0 for k in FA_ORDER}
                        tot = sum(parsed_ing.values()) or 1.0
                        for ing_key, pct in parsed_ing.items():
                            w = pct / tot
                            prof = _get_profile(ing_key, "mean")
                            for fa_key, fa_pct in prof.items():
                                fa_tmp[fa_key] += w * fa_pct
                        fa_norm = _normalize_percentages(fa_tmp)
                    else:
                        st.error("Planilha deve ter colunas 'Ingrediente' e 'Percentual'.")
                else:
                    col_fa, col_pct = "AcidoGraxos", "Percentual"
                    if col_fa in df.columns and col_pct in df.columns:   # (fix do '&&')
                        for _, row in df.iterrows():
                            fa = str(row[col_fa]).strip()
                            pct = float(row[col_pct]) if pd.notna(row[col_pct]) else 0.0
                            parsed_fa[fa] = parsed_fa.get(fa, 0.0) + pct
                        original_total = sum(parsed_fa.values()); _badge_total(original_total, "Total da planilha (FA)")
                        fa_norm = _normalize_percentages(parsed_fa)
                    else:
                        st.error("Planilha deve ter colunas 'AcidoGraxos' e 'Percentual'.")

        if fa_norm:
            st.markdown("---")
            st.subheader("KPIs do Blend (perfil real) + Ajuste fino (opcional)")
            method_upl = st.radio("Método de ajuste", ["Classe B — Ácidos graxos puros", "Classe C — Ingredientes"],
                                  horizontal=True, key="ajuste_method_upload")

            # Ajuste B
            B_vals_u = OrderedDict((fa, 0.0) for fa in FA_ORDER)
            total_B_u = 0.0
            if method_upl.startswith("Classe B"):
                with st.expander("Classe B — Ajuste fino por Ácidos graxos puros (sobre perfil real)", expanded=True):
                    colsB = st.columns(4)
                    for idx, fa in enumerate(FA_ORDER):
                        with colsB[idx % 4]:
                            B_vals_u[fa] = st.slider(f"FA {fa} (ajuste fino)", 0.0, 30.0, 0.0, 0.5, key=f"slider_upload_fa_{fa}")
                    total_B_u = sum(B_vals_u.values())
                    if total_B_u > 30:
                        st.warning("Classe B excede 30% do blend — considere reduzir para manter o caráter do óleo base.")

            # Ajuste C
            C_vals_u = OrderedDict((k, 0.0) for k, _ in INGREDIENTS)
            total_C_u = 0.0
            if method_upl.endswith("Ingredientes"):
                with st.expander("Classe C — Ajuste fino por Ingredientes (sobre perfil real)", expanded=True):
                    colsC = st.columns(4)
                    for idx, (k, label) in enumerate(INGREDIENTS):
                        with colsC[idx % 4]:
                            C_vals_u[k] = st.slider(f"{label} (ajuste fino)", 0.0, 30.0, 0.0, 0.5, key=f"slider_upload_adj_{k}")
                    total_C_u = sum(C_vals_u.values())
                    if total_C_u > 30:
                        st.warning("Classe C excede 30% do blend — considere reduzir para manter o caráter do óleo base.")

            # Combina
            fa_comb = fa_norm.copy()
            if method_upl.startswith("Classe B") and total_B_u > 0:
                for fa, pct in B_vals_u.items():
                    fa_comb[fa] = fa_comb.get(fa, 0.0) + pct
                fa_comb = _normalize_percentages(fa_comb)
            elif method_upl.endswith("Ingredientes") and total_C_u > 0:
                add = {k: 0.0 for k in FA_ORDER}
                for ing_key, pct in C_vals_u.items():
                    if pct <= 0: continue
                    prof = _get_profile(ing_key, "mean")
                    for fa_key, fa_pct in prof.items():
                        add[fa_key] += (pct * fa_pct / 100.0)
                for fa_key, inc in add.items():
                    fa_comb[fa_key] = fa_comb.get(fa_key, 0.0) + inc
                fa_comb = _normalize_percentages(fa_comb)

            II, ISap, PF_idx = iodine_index(fa_comb), saponification_index(fa_comb), melt_index(fa_comb)
            c1, c2, c3 = st.columns(3)
            c1.metric("Índice de Iodo (II)", f"{II:.1f}")
            c2.metric("Índice de Saponificação (ISap)", f"{ISap:.1f} mgKOH/g")
            c3.metric("Ponto de Fusão", f"{PF_idx:.0f}")
            st.caption("KPIs calculados sobre o perfil **combinado** (real + ajuste fino, se houver).")

            # Gráficos + Radar
            g1, g2 = st.columns(2)
            with g1: _plot_fa_bars(fa_comb)
            with g2:
                _, radar_vals = _scores_finais(fa_comb, PF_idx, II)
                _plot_radar(radar_vals)

            # Trade-offs (upload)
            st.markdown("---")
            st.subheader("Análise de Trade-offs (variação de +5% por ingrediente sobre o perfil real)")
            trade_u = _compute_tradeoffs_upload(fa_start=fa_comb, method_upl=method_upl,
                                                B_vals_u=B_vals_u if method_upl.startswith("Classe B") else {fa:0.0 for fa in FA_ORDER},
                                                C_vals_u=C_vals_u if method_upl.endswith("Ingredientes") else {k:0.0 for k,_ in INGREDIENTS},
                                                consider_var=False, scenario="mean")
            if trade_u:
                labels_u, dII_u, dIS_u, dPF_u = trade_u
                ctu1, ctu2, ctu3 = st.columns(3)
                with ctu1: _plot_tradeoff_bars("Δ Índice de Iodo (II)", labels_u, dII_u, "Δ II")
                with ctu2: _plot_tradeoff_bars("Δ Índice de Saponificação (ISap)", labels_u, dIS_u, "Δ ISap")
                with ctu3: _plot_tradeoff_bars("Δ Ponto de Fusão", labels_u, dPF_u, "Δ PF")
            else:
                st.caption("Carregue um perfil e/ou ajuste fino para visualizar os trade-offs.")

            # Preview finalidade
            st.subheader("Preview de notas por finalidade (0–100)")
            scores, _ = _scores_finais(fa_comb, PF_idx, II)
            p1, p2, p3, p4 = st.columns(4)
            p1.metric("Mãos", f"{scores['Mãos']}"); p2.metric("Corpo", f"{scores['Corpo']}")
            p3.metric("Rosto", f"{scores['Rosto']}"); p4.metric("Cabelos", f"{scores['Cabelos']}")

            # Handoff
            st.markdown("---")
            st.info("Pronto para detalhar por finalidade e assinatura sensorial no **Assistente de Formulação**.")
            assist_payload = {
                "fa_profile": fa_comb,
                "kpis": {"II": II, "ISap": ISap, "PF_proxy": PF_idx},
                "scores_preview": scores,
                "source": "upload_real+" + ("ajusteB" if method_upl.startswith("Classe B") else "ajusteC"),
                "ajuste": {"method": "B" if method_upl.startswith("Classe B") else "C",
                           "B_vals": dict(B_vals_u), "C_vals": dict(C_vals_u)},
            }
            st.session_state["assist_payload"] = assist_payload
            if st.button("➜ Enviar para Assistente de Formulação", key="btn_handoff_assist_real_adj"):
                st.session_state["go_to_assistente"] = True
                st.success("Perfil enviado (Upload + Ajuste fino). Abra a aba **Assistente de Formulação** para continuar.")
        else:
            st.caption("Carregue um **perfil de ácidos graxos** (ou ingredientes) para habilitar KPIs, gráficos e ajuste fino.")
