import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io
import max_re_price as re_tools
from localization import UI_TEXTS
from pdf_generator import create_pdf

# --- CONFIGURATION & TRANSLATIONS ---

st.set_page_config(
    page_title="Immobilien Investment Dossier",
    page_icon="🏢",
    layout="wide"
)

# Text Dictionary for DE/EN
# Text Dictionary moved to localization.py

# --- SIDEBAR & STATE ---

# Initialize Session State
if 'lang' not in st.session_state:
    st.session_state.lang = "DE"
if 'kp' not in st.session_state:
    st.session_state.kp = 469000.0
# Safeguard: If user (or glitch) set it to 0, reset to default (optional UX choice)
if st.session_state.kp == 0.0:
    st.session_state.kp = 469000.0

# Language Toggle (Top of Sidebar)
# Language Toggle (Compact)
with st.sidebar:
    lang_choice = st.radio(
        "Sprache/Language", 
        ["🇩🇪 Deutsch", "🇬🇧 English"],
        index=0 if st.session_state.lang == "DE" else 1,
        label_visibility="collapsed",
        horizontal=True
    )
    st.session_state.lang = "DE" if "Deutsch" in lang_choice else "EN"

T = UI_TEXTS[st.session_state.lang]

# Helper for Traffic Lights
def get_traffic_light(value, threshold_green, threshold_yellow, invert=False):
    # Default: Higher is better (Yield)
    # Invert: Lower is better (Price)
    if not invert:
        if value >= threshold_green: return "🟢"
        if value >= threshold_yellow: return "🟡"
        return "🔴"
    else:
        if value <= threshold_green: return "🟢"
        if value <= threshold_yellow: return "🟡"
        return "🔴"


# create_pdf moved to pdf_generator.py

# --- MAIN GUI ---

# --- MAIN GUI ---

# Initialize Session State Defaults (Basics + Financing)
if 'kp' not in st.session_state: st.session_state.kp = 469000.0
if 'km' not in st.session_state: st.session_state.km = 10800.0
if 'cost' not in st.session_state: st.session_state.cost = 960.0
if 'zins' not in st.session_state: st.session_state.zins = 3.8
if 'ek' not in st.session_state: st.session_state.ek = 20.0
if 'p_makler' not in st.session_state: st.session_state.p_makler = 3.57
if 'p_tax' not in st.session_state: st.session_state.p_tax = 3.5
if 'p_notar' not in st.session_state: st.session_state.p_notar = 2.0
if 'scen_increase' not in st.session_state: st.session_state.scen_increase = 0

# Sidebar Navigation
with st.sidebar:
    st.markdown("---")
    nav_options = [
        T["tab_status"], 
        T["tab_scenario"], 
        T["tab_leverage"], 
        T["tab_tax"], 
        T["tab_due_diligence"]
    ]
    nav_selection = st.radio(
        "Navigation", 
        [T["tab_intro"], T["tab_status"], T["tab_scenario"], T["tab_leverage"], T["tab_tax"], T["tab_due_diligence"], T["tab_report"]]
    )

st.title(T["title"])

# --- SIDEBAR INPUTS (Fixed) ---
with st.sidebar:
    st.markdown("---")
    kaufpreis = st.number_input(T["input_price"], step=5000.0, format="%.2f", key="kp")
    
    st.caption("Kaufnebenkosten / Closing Costs (%)")
    col_nk1, col_nk2, col_nk3 = st.columns(3)
    p_makler = col_nk1.number_input("Makler", step=0.1, key="p_makler")
    p_tax = col_nk2.number_input("Tax/Steuer", step=0.1, key="p_tax")
    p_notar = col_nk3.number_input("Notar", step=0.1, key="p_notar")
    
    st.markdown("---")
    st.warning(T["disclaimer"])

# --- PAGE RENDERING ---

# Global Variables (Rent/Cost from Session State if not on Status tab, otherwise driven by widget below)
kaltmiete_pa = st.session_state.km
costs_pa = st.session_state.cost

# Run Basic Calculations
NK_EURO = re_tools.berechne_kaufnebenkosten(kaufpreis, p_makler, p_tax, p_notar)
rendite, reinertrag, invest = re_tools.berechne_netto_mietrendite(kaufpreis, NK_EURO, kaltmiete_pa, costs_pa)

# 0. INTRODUCTION
if nav_selection == T["tab_intro"]:
    st.header(T["intro_header"])
    st.markdown(T["intro_text"])
    
    st.info(T["disclaimer"])

# 1. STATUS QUO
elif nav_selection == T["tab_status"]:
    st.header(T["tab_status"])
    
    # --- BASICS INPUTS (Rent & Costs only) ---
    with st.expander(T["property_data_header"], expanded=True):
        c1, c2 = st.columns(2)
        with c1:
            st.number_input(T["input_rent"], value=st.session_state.km, step=120.0, format="%.2f", key="km")
        with c2:
            st.number_input(T["input_costs"], value=st.session_state.cost, step=50.0, format="%.2f", key="cost")

    st.markdown("### Analysis")
    col1, col2, col3 = st.columns(3)
    
    col1.metric("Kaufpreis", f"{kaufpreis:,.2f} €")
    col2.metric("Gesamtinvest", f"{invest:,.2f} €", f"+{NK_EURO:,.2f} € NK")
    
    tf = get_traffic_light(rendite, 3.5, 2.5)
    col3.metric(T["calc_yield"], f"{rendite:.2f} %", delta=tf)
    
    with st.expander(T["details_header"]):
        st.markdown(T["status_expl"])
        st.write(f"Reinertrag: {reinertrag:,.2f} € / Gesamtinvest: {invest:,.2f} € = **{rendite:.2f} %**")

# 2. SCENARIO
elif nav_selection == T["tab_scenario"]:
    st.header(T["tab_scenario"])
    
    with st.expander(T["scen_settings_header"], expanded=True):
        col_loc, col_slider = st.columns([1, 2])
        with col_loc:
            loc_setting = st.radio(
                T["input_loc"], 
                ("Active", "Inactive"),
                format_func=lambda x: T["loc_active"] if x == "Active" else T["loc_inactive"],
                horizontal=True
            )
            rent_cap = 15 if loc_setting == "Active" else 20

        with col_slider:
            # Manual State Management for robustness
            current_inc = st.session_state.scen_increase
            increase = st.slider(T["scen_header"], 0, 30, value=current_inc, step=1)
            st.session_state.scen_increase = increase
    
    # Validation & Logic
    if increase > rent_cap:
         st.warning(f"{T['scen_cap_warn']} (Limit: {rent_cap}%)")
    
    new_rent_pa = re_tools.berechne_mietpotential(kaltmiete_pa, increase)
    pot_yield, _, _ = re_tools.berechne_netto_mietrendite(kaufpreis, NK_EURO, new_rent_pa, costs_pa)
    
    # Results
    st.markdown("### Analysis")
    c1, c2 = st.columns(2)
    c1.metric(T["scen_new_rent"], f"{new_rent_pa:,.2f} €", f"+{(new_rent_pa-kaltmiete_pa):,.2f} €")
    
    tf_pot = get_traffic_light(pot_yield, 3.5, 2.5)
    c2.metric(T["scen_pot_yield"], f"{pot_yield:.2f} %", delta=tf_pot)

# 3. LEVERAGE
elif nav_selection == T["tab_leverage"]:
    st.header(T["tab_leverage"])
    
    # --- FINANCING INPUTS (Moved to Tab) ---
    with st.expander(T["fin_settings_header"], expanded=True):
        c_zins, c_ek, c_bond = st.columns(3)
        with c_zins:
            zins = st.slider(T["input_interest"], min_value=1.0, max_value=6.0, value=3.8, step=0.1, key="zins")
        with c_ek:
            ek_quote = st.slider(T["input_equity"], min_value=0, max_value=100, value=20, step=5, key="ek")
        with c_bond:
            bond_rate = st.number_input("Risk-free (Bund) %", min_value=0.0, max_value=10.0, value=2.5, step=0.1, key="bond_rate")
            
    st.markdown("---")
    st.subheader(T["lev_chart_title"])
    
    # Chart Data
    obj_yield = rendite
    x_zins = np.linspace(1, 6, 100)
    y_ek_yield = []
    for z in x_zins:
        val = re_tools.berechne_leverage_effekt(obj_yield, z, ek_quote)
        y_ek_yield.append(val)
        
    # Plot Chart
    fig, ax = plt.subplots(figsize=(8,3))
    ax.plot(x_zins, y_ek_yield, label="EK-Rendite", color="blue", linewidth=2)
    ax.axhline(0, color='grey', linewidth=0.8)
    ax.axvline(zins, color='red', linestyle='--', label=f"Ihr Zins ({zins}%)")
    ax.axhline(bond_rate, color='green', linestyle=':', label=f"Bund ({bond_rate}%)")
    ax.set_xlabel("Zins (%)")
    ax.set_ylabel("Eigenkapital-Rendite (%)")
    ax.grid(True, alpha=0.3)
    ax.legend()
    st.pyplot(fig)
    
    with st.expander(T["lev_expl_title"]):
        st.markdown(T["lev_expl_text"])

    st.markdown("---")
    
    # --- SECTION 1: BOND COMPARISON ---
    # bond_rate is now defined above
    ek_yield_leverage = re_tools.berechne_leverage_effekt(rendite, zins, ek_quote) 
    spread = ek_yield_leverage - bond_rate
    
    col1, col2 = st.columns(2) 
    
    with col1:
        st.subheader(T["lev_bond_comp"])
        c_bond1, c_bond2, c_bond3 = st.columns(3)
        c_bond1.metric("Immo-EK-Rendite", f"{ek_yield_leverage:.2f} %", delta=get_traffic_light(ek_yield_leverage, 7.0, 4.0))
        c_bond2.metric("Risk-free (Bund)", f"{bond_rate:.2f} %")
        c_bond3.metric("Risikoprämie (Spread)", f"{spread:.2f} %", delta=get_traffic_light(spread, 2.0, 0))

    with col2:
        # Detailed Calculation Expander (Now on the right side)
        with st.expander(T["lev_details_header"]):
            details = re_tools.berechne_cashflow_detail(
                kaufpreis, NK_EURO, kaltmiete_pa, costs_pa, zins, ek_quote
            )
            
            st.markdown(f"""
            **Einnahmen:**
            *   Nettokaltmiete: `+{details['kaltmiete']:,.2f} €`
            
            **Ausgaben:**
            *   Nicht umlegbar: `-{details['bewirtschaftung']:,.2f} €`
            *   Zinsen an Bank: `-{details['zinsen']:,.2f} €` ({details['fremdkapital']:,.0f} € Kredit x {zins}%)
            
            ---
            **ERGEBNIS (Cashflow):** `{details['cashflow']:,.2f} €` (vor Steuern)
            
            **EK-Rendite:**
            `{details['cashflow']:,.0f} € / {details['eigenkapital']:,.0f} € ≈ {details['ek_rendite']:.2f}%`
            
            {T['lev_details_note']}
            """)

    st.markdown("---")

    # --- SECTION 2: WEALTH ACCUMULATION ---
    c_wealth_1, c_wealth_2 = st.columns(2)

    with c_wealth_1:
         st.subheader(T["lev_wealth_title"])
         details = re_tools.berechne_cashflow_detail(kaufpreis, NK_EURO, kaltmiete_pa, costs_pa, zins, ek_quote)
         tilgung_pa = details['fremdkapital'] * 0.02 
         tilgung_monat = tilgung_pa / 12
         cf_monat = details['cashflow'] / 12
         
         # Custom Matplotlib Chart for better labels
         categories = [T["lev_wealth_cf"], T["lev_wealth_amort"], T["lev_wealth_net"]]
         amounts = [cf_monat, tilgung_monat, cf_monat + tilgung_monat]
         
         fig_wealth, ax_w = plt.subplots(figsize=(5, 4))
         bars = ax_w.bar(categories, amounts, color=['#d32f2f' if amounts[0]<0 else '#1976d2', '#1976d2', '#388e3c'])
         
         # Diagonal labels
         ax_w.set_xticklabels(categories, rotation=45, ha='right')
         
         # Value labels above bars
         for bar in bars:
             height = bar.get_height()
             offset = height * 0.05 if height != 0 else 5
             # Ensure a minimum offset so it doesn't overlap with the bar
             if height >= 0: offset = max(offset, 10)
             else: offset = min(offset, -20)
             
             ax_w.text(bar.get_x() + bar.get_width() / 2, height + offset,
                       f'{height:,.2f} €', ha='center', va='bottom' if height >= 0 else 'top',
                       fontsize=9, fontweight='bold', color='black')
                       
         ax_w.axhline(0, color='grey', linewidth=0.8)
         ax_w.spines['top'].set_visible(False)
         ax_w.spines['right'].set_visible(False)
         ax_w.grid(axis='y', linestyle='--', alpha=0.3)
         plt.tight_layout()
         st.pyplot(fig_wealth)

    with c_wealth_2:
        # Explanation for Wealth Chart
        st.write(" ") # Spacer
        st.write(" ") # Spacer
        with st.expander(T["lev_wealth_expl"]):
            st.markdown(f"""
            **Was sehe ich hier?**
            
            *   **Rot (Cashflow):** Das Geld, das Sie jeden Monat real bezahlen müssen (Mieteinnahmen minus Bankrate & Bewirtschaftung).
            *   **Blau (Tilgung):** Das Geld, das Ihnen der "Mieter schenkt". Er zahlt Ihren Kredit ab. Das ist **Vermögensaufbau**, auch wenn Sie es nicht auf dem Konto sehen.
            *   **Grün (Netto-Vermögen):** Die Summe aus beiden. Wenn der negative Cashflow (Rot) kleiner ist als die Tilgung (Blau), werden Sie jeden Monat reicher – trotz Zuzahlung!
            
            {T['lev_wealth_note']}
            """)

    st.markdown("---")

# 4. TAX
elif nav_selection == T["tab_tax"]:
    st.header(T["tab_tax"])
    
    # Inputs grouped in Expander (Top)
    with st.expander(T["tax_settings_header"], expanded=True):
        c_tax1, c_tax2, c_tax3 = st.columns(3)
        with c_tax1:
            boden_anteil = st.slider(T["tax_land_val"], 0, 100, 70, 5)
        with c_tax2:
            pers_steuer = st.slider(T["tax_pers_rate"], 0, 50, 42, 1)
        with c_tax3:
            reno_invest = st.number_input(T["tax_reno_budget"], min_value=0, value=0, step=5000, help=T["tax_3y_expl"])
    
    # Calculations
    afa, steuer_back, gebaeude = re_tools.berechne_afa_vorteil(kaufpreis, boden_anteil, pers_steuer)
    ueber_limit, limit_val, rest = re_tools.check_15_prozent_grenze(kaufpreis, boden_anteil, reno_invest)
    
    # Results (Bottom)
    st.markdown("### Analysis")
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(T["tax_afa_calc"], f"+{steuer_back:,.2f} € p.a.", f"Basis: {gebaeude:,.2f} €")
        
    with col2:
        delta_color = "inverse" if ueber_limit else "normal" 
        traffic_limit = "🔴" if ueber_limit else "🟢"
        
        delta_text = f"{traffic_limit} {'OVER' if ueber_limit else 'OK'} ({rest:,.2f} €)"
        st.metric(T["tax_15_rule"], f"{limit_val:,.2f} €", delta=delta_text, delta_color="inverse")
        
    if ueber_limit:
        st.error("Budget > 15% Limit! Abschreibung über 50 Jahre statt Sofortabzug.")

    st.divider()
    with st.expander(T["tax_expl_title"]):
        st.markdown(T["tax_expl_text"])

# 6. NEGOTIATION DOSSIER
elif nav_selection == T["tab_report"]:
    st.header(T["report_header"])
    st.info(T["report_intro"])
    
    # Needs Params from other tabs (use session state or defaults)
    rep_bond = st.session_state.get('bond_rate', 2.5)
    rep_zins = st.session_state.get('zins', 3.8)
    rep_km = st.session_state.km
    rep_cost = st.session_state.cost
    
    # 0. Base Figures
    st.subheader(T["rep_sec0"])
    c_base1, c_base2 = st.columns(2)
    
    with c_base1:
        st.metric(T["rep_total_invest"], f"{invest:,.2f} €", help=f"{kaufpreis:,.2f} € {T['rep_purchase_price']} + {NK_EURO:,.2f} € {T['rep_closing_costs']}")
        st.caption(f"🏠 {kaufpreis:,.0f} € + 🏗️ {NK_EURO:,.0f} €")
        
    with c_base2:
        st.metric(T["rep_rent_income"], f"{kaltmiete_pa:,.2f} €", "p.a.")
    
    st.markdown("---")
    
    # 1. Reality Check
    st.subheader(T["rep_sec1"])
    col_rep1, col_rep2, col_rep3 = st.columns(3)
    
    col_rep1.metric(T["rep_yield"], f"{rendite:.2f} %", delta=f"{rendite-rep_bond:.2f} % vs Bond")
    col_rep1.caption(f"{T['rep_rent_income']}: {kaltmiete_pa:,.0f} €")
    col_rep2.metric(T["rep_interest"], f"{rep_zins:.2f} %", delta=None)
    
    gap = rendite - rep_zins
    col_rep3.metric(T["rep_gap"], f"{gap:.2f} %", delta=get_traffic_light(gap, 0.5, 0), delta_color="normal")
    
    if gap < 0:
        st.error(f"🔴 {T['rep_neg_lev'].format(rendite, rep_zins)}")

    # Add Potential Yield (Scenario)
    scen_increase = st.session_state.get('scen_increase', 0)
    
    new_rent_rep = re_tools.berechne_mietpotential(rep_km, scen_increase)
    pot_yield_rep, _, _ = re_tools.berechne_netto_mietrendite(kaufpreis, NK_EURO, new_rent_rep, rep_cost)
    pot_gap = pot_yield_rep - rep_zins
    
    st.markdown("---")
    st.caption(f"Szenario: Mietanpassung +{scen_increase}%: {new_rent_rep:,.0f} € (Soll)")
    
    c_pot1, c_pot2, c_pot3 = st.columns(3)
    c_pot1.metric(f"Soll-Rendite", f"{pot_yield_rep:.2f} %", delta=f"+{(pot_yield_rep-rendite):.2f}% vs Ist")
    
    c_pot2.metric(T["rep_interest"], f"{rep_zins:.2f} %", delta=None)
    
    c_pot3.metric("Soll-Lücke (Gap)", f"{pot_gap:.2f} %", delta=get_traffic_light(pot_gap, 0.5, 0), delta_color="normal")

    st.markdown("---")

    # 2. Fair Price Calc
    st.subheader(T["rep_sec2"])
    
    # Adjustable Target Yield
    with st.expander(T["rep_yield_settings"], expanded=True):
        target_yield = st.number_input(
            T["rep_target_yield"], 
            min_value=0.1, max_value=10.0, value=3.5, step=0.1,
            help="Standard ~3.5-4.5%"
        )
    
    net_rent = rep_km - rep_cost
    max_invest_target = net_rent / (target_yield / 100)
    
    # Reverse Closing Costs
    factor_nk = (p_makler + p_tax + p_notar) / 100
    fair_price_calc = max_invest_target / (1 + factor_nk)
    diff_price = kaufpreis - fair_price_calc
    
    c_fair1, c_fair2 = st.columns(2)
    with c_fair1:
        st.metric(T["rep_fair_val"], f"{fair_price_calc:,.2f} €", delta=f"-{diff_price:,.2f} € vs Ask", delta_color="inverse")
    with c_fair2:
        st.caption(T["rep_caption"].format(target_yield, factor_nk*100))
        st.write(f"{T['rep_max_invest']}: {max_invest_target:,.2f} €")
    
    # Detailed Derivation Logic
    with st.expander(T["rep_deriv_title"]):
        st.markdown(f"""
        **{T["rep_step1"]}**  
        `{rep_km:,.2f} € (Miete) - {rep_cost:,.2f} € (Kosten) = {net_rent:,.2f} €`
        
        **{T["rep_step2"]}**  
        `{net_rent:,.2f} € / {target_yield/100:.3f} = {max_invest_target:,.2f} €`
        
        **{T["rep_step3"].format(factor_nk*100)}**  
        `{max_invest_target:,.2f} € / (1 + {factor_nk:.4f}) = {fair_price_calc:,.2f} €`
        
        **{T["rep_step4"]}**  
        **`= {fair_price_calc:,.2f} €`**
        """)
        
    st.markdown("---")
    
    # 3. PDF Generation
    st.subheader(T["rep_sec3"])
    
    # Pre-Generate PDF Logic
    inputs_pdf = {
        T["rep_purchase_price"]: f"{kaufpreis:,.2f} EUR",
        T["rep_rent_income"]: f"{kaltmiete_pa:,.2f} EUR",
        T["rep_closing_costs"]: f"{NK_EURO:,.2f} EUR"
    }
    results_pdf = {
        T["rep_yield"]: f"{rendite:.2f} %",
        T["rep_fair_val"]: f"{fair_price_calc:,.2f} EUR"
    }
    
    import datetime
    today_str = datetime.date.today().strftime("%d.%m.%Y")
    
    extra_params = {
        'bond_rate': rep_bond,
        'zins': rep_zins,
        'yield_num': rendite,
        'target_yield': target_yield,
        'km_pa': rep_km,
        'cost_pa': rep_cost,
        'p_makler': st.session_state.p_makler,
        'p_tax': st.session_state.p_tax,
        'p_notar': st.session_state.p_notar,
        'date': today_str,
        'scen_increase': scen_increase,
        'pot_rent_pa': new_rent_rep,
        'pot_yield': pot_yield_rep
    }
    
    # Generate PDF Bytes
    pdf_bytes = create_pdf(st.session_state.lang, inputs_pdf, results_pdf, extra_params)
    
    # download_button (Standard Streamlit Widget)
    st.download_button(
        label=f"📥 {T['rep_sec3']} (.pdf)",
        data=pdf_bytes,
        file_name="Negotiation_Dossier.pdf",
        mime="application/pdf"
    )

# 5. DUE DILIGENCE
elif nav_selection == T["tab_due_diligence"]:
    st.header(T["tab_due_diligence"])
    
    checks = [
        (T["dd_weg"], "Ohne Protokolle ist die WEG eine Blackbox. Drohen Sonderumlagen?"),
        (T["dd_rules"], "Wer zahlt Fenster? Gemeinschaft oder Sie? (Teilungserklärung prüfen)"),
        (T["dd_energy"], "Gasheizung 1992? Austauschpflicht prüfen!"),
        (T["dd_tenant"], "Risiko Eigenbedarfskündigung & Mietrückstände?")
    ]
    
    score = 0
    for label, help_text in checks:
        if st.checkbox(label, help=help_text):
            score += 1
            
    st.progress(score / len(checks))
    if score == len(checks):
        st.success("✅ Due Diligence Complete")
        
    st.markdown("---")
    with st.expander(T["dd_expl_title"]):
        st.markdown(T["dd_expl_text"])

# --- FOOTER & PDF EXPORT ---
# --- PDF EXPORT ---
# Moved to Tab 6: Negotiation Dossier
