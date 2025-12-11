import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from fpdf import FPDF
import io
import max_re_price as re_tools

# --- CONFIGURATION & TRANSLATIONS ---

st.set_page_config(
    page_title="Immobilien Investment Dossier",
    page_icon="🏢",
    layout="wide"
)

# Text Dictionary for DE/EN
TEXTS = {
    "DE": {
        "title": "🏢 Immobilien Investment Dossier",
        "sidebar_header": "1. Einstellungen",
        "lang_select": "Sprache / Language",
        "input_price": "Kaufpreis (€)",
        "input_rent": "Aktuelle Kaltmiete (p.a.)",
        "input_costs": "Bewirtschaftungskosten (p.a.)",
        "input_interest": "Zinssatz (%)",
        "input_equity": "Eigenkapital (%)",
        "input_loc": "Mietpreisbremse (Ort)",
        "loc_active": "Aktiv (max 15% Erhöhung)",
        "loc_inactive": "Inaktiv (max 20% Erhöhung)",
        "tab_status": "1. Status Quo",
        "tab_scenario": "2. Miet-Szenario",
        "tab_leverage": "3. Leverage & Cashflow",
        "tab_tax": "4. Steuern & Sanierung",
        "tab_due_diligence": "5. Due Diligence",
        "calc_yield": "Netto-Mietrendite",
        "calc_cf": "Cashflow",
        "details_header": "🔍 Details & Erklärung",
        "status_expl": "Die Netto-Mietrendite zeigt das Verhältnis von Reinertrag zum Gesamtinvest. Werte unter 2.5% gelten aktuell oft als unwirtschaftlich (negativer Cashflow droht).",
        "scen_header": "Mietsteigerung (3 Jahre)",
        "scen_cap_warn": "⚠️ Kappungsgrenze aktiv (max. 15%)",
        "scen_new_rent": "Neue Kaltmiete (p.a.)",
        "scen_pot_yield": "Potenzielle Rendite",
        "traffic_red": "🔴 Schlecht",
        "traffic_yellow": "🟡 Mäßig",
        "traffic_green": "🟢 Gut",
        "lev_chart_title": "Leverage-Effekt: EK-Rendite vs. Zins",
        "lev_bond_comp": "Vergleich mit Bundesanleihe",
        "lev_wealth_title": "Vermögenszuwachs (Monatlich)",
        "lev_wealth_cf": "Cashflow (Sie zahlen)",
        "lev_wealth_amort": "Tilgung (Mieter zahlt)",
        "lev_wealth_net": "Netto-Vermögen",
        "tax_land_val": "Bodenwertanteil (%)",
        "tax_pers_rate": "Pers. Steuersatz (%)",
        "tax_reno_budget": "Renovierungskosten (3J)",
        "tax_afa_calc": "Steuerrückerstattung (AfA)",
        "tax_15_rule": "15% Grenze (Netto)",
        "dd_checklist": "Prüfungs-Checkliste",
        "dd_weg": "WEG-Protokolle & Rücklage",
        "dd_rules": "Teilungserklärung (Fenster?)",
        "dd_energy": "Energieausweis & Heizung (1992?)",
        "dd_tenant": "Mieterhistorie & Eigenbedarf",
        "disclaimer": "⚠️ HAFTUNGSAUSSCHLUSS: Dieses Tool dient ausschließlich Bildungszwecken. Keine Anlageberatung. Investitionen auf eigenes Risiko.",
    },
    "EN": {
        "title": "🏢 Real Estate Investment Dossier",
        "sidebar_header": "1. Settings",
        "lang_select": "Language / Sprache",
        "input_price": "Purchase Price (€)",
        "input_rent": "Current Net Rent (p.a.)",
        "input_costs": "Maintenance Costs (p.a.)",
        "input_interest": "Interest Rate (%)",
        "input_equity": "Equity Share (%)",
        "input_loc": "Rent Control (Location)",
        "loc_active": "Active (max 15% increase)",
        "loc_inactive": "Inactive (max 20% increase)",
        "tab_status": "1. Status Quo",
        "tab_scenario": "2. Rent Scenario",
        "tab_leverage": "3. Leverage & Cashflow",
        "tab_tax": "4. Tax & Renovation",
        "tab_due_diligence": "5. Due Diligence",
        "calc_yield": "Net Rental Yield",
        "calc_cf": "Cashflow",
        "details_header": "🔍 Context & Explanation",
        "status_expl": "Net Rental Yield shows the return on total investment. Values below 2.5% are currently considered low (risk of negative cashflow).",
        "scen_header": "Rent Increase (3 Years)",
        "scen_cap_warn": "⚠️ Rent Cap Active (max 15%)",
        "scen_new_rent": "New Net Rent (p.a.)",
        "scen_pot_yield": "Potential Yield",
        "traffic_red": "🔴 Poor",
        "traffic_yellow": "🟡 Mediocre",
        "traffic_green": "🟢 Good",
        "lev_chart_title": "Leverage Effect: Equity Yield vs. Interest",
        "lev_bond_comp": "Bond Comparison",
        "lev_wealth_title": "Wealth Accumulation (Monthly)",
        "lev_wealth_cf": "Cashflow (You pay)",
        "lev_wealth_amort": "Amortization (Tenant pays)",
        "lev_wealth_net": "Net Weath Change",
        "tax_land_val": "Land Value Share (%)",
        "tax_pers_rate": "Personal Tax Rate (%)",
        "tax_reno_budget": "Renovation Budget (3Y)",
        "tax_afa_calc": "Tax Refund (Depreciation)",
        "tax_15_rule": "15% Limit (Net)",
        "dd_checklist": "Due Diligence Checklist",
        "dd_weg": "WEG Protocols & Reserves",
        "dd_rules": "Community Rules (Windows?)",
        "dd_energy": "Energy Cert & Boiler (1992?)",
        "dd_tenant": "Tenant History & Own Use",
        "disclaimer": "⚠️ DISCLAIMER: Educational purpose only. Not financial advice. Investments at own risk.",
    }
}

# --- SIDEBAR & STATE ---

# Initialize Session State
if 'lang' not in st.session_state:
    st.session_state.lang = "DE"

# Language Toggle (Top of Sidebar)
with st.sidebar:
    col_l1, col_l2 = st.columns([1,3])
    with col_l1:
        st.write("🌐")
    with col_l2:
        lang_choice = st.radio(
            "Sprache/Language", 
            ["Deutsch", "English"], 
            index=0 if st.session_state.lang == "DE" else 1,
            label_visibility="collapsed"
        )
    st.session_state.lang = "DE" if lang_choice == "Deutsch" else "EN"

T = TEXTS[st.session_state.lang]

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


# --- PDF HELPER ---
def create_pdf(lang_code, inputs, results):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    
    def safe_text(text):
        """Replace non-latin-1 chars"""
        replacements = {
            "€": "EUR", "⚠️": "[WARN]", "✅": "[OK]", "🔴": "[BAD]", 
            "🟡": "[AVG]", "🟢": "[GOOD]", "„": '"', "“": '"'
        }
        for k, v in replacements.items():
            text = text.replace(k, v)
        try:
            return text.encode('latin-1', 'replace').decode('latin-1')
        except:
            return text
            
    title = "Immobilien Investment Dossier" if lang_code == "DE" else "Real Estate Investment Dossier"
    pdf.cell(0, 10, safe_text(title), ln=True, align='C')
    pdf.ln(10)
    
    pdf.set_font("Arial", '', 12)
    
    # 1. Inputs
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, safe_text("1. Key Data / Eckdaten"), ln=True)
    pdf.set_font("Arial", '', 12)
    
    for k, v in inputs.items():
        pdf.cell(100, 8, safe_text(f"{k}:"), 0)
        pdf.cell(0, 8, safe_text(f"{v}"), ln=True)
    
    pdf.ln(5)
    
    # 2. Results
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, safe_text("2. Analysis / Analyse"), ln=True)
    pdf.set_font("Arial", '', 12)
    
    for k, v in results.items():
        pdf.cell(100, 8, safe_text(f"{k}:"), 0)
        pdf.cell(0, 8, safe_text(f"{v}"), ln=True)
        
    pdf.ln(10)
    pdf.set_font("Arial", 'I', 10)
    pdf.multi_cell(0, 5, safe_text("Disclaimer: Educational Purpose Only. No Financial Advice."))
    
    return pdf.output(dest='S').encode('latin-1')

# --- MAIN GUI ---

# --- MAIN GUI ---

# --- MAIN GUI ---

# Initialize Session State Defaults for PDF functionality
if 'zins' not in st.session_state: st.session_state.zins = 3.8
if 'ek' not in st.session_state: st.session_state.ek = 20.0

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
    nav_selection = st.radio(T["sidebar_header"], nav_options)

st.title(T["title"])

# --- SHARED INPUTS (Sidebar) ---
with st.sidebar:
    st.markdown("---")
    st.caption("1. Basics")
    kaufpreis = st.number_input(T["input_price"], value=469000.0, step=5000.0, format="%.2f", key="kp")
    kaltmiete_pa = st.number_input(T["input_rent"], value=10800.0, step=120.0, format="%.2f", key="km")
    costs_pa = st.number_input(T["input_costs"], value=960.0, step=50.0, format="%.2f", key="cost")

# --- PAGE RENDERING ---

# Run Basic Calculations
NK_EURO = re_tools.berechne_kaufnebenkosten(kaufpreis)
rendite, reinertrag, invest = re_tools.berechne_netto_mietrendite(kaufpreis, NK_EURO, kaltmiete_pa, costs_pa)


# 1. STATUS QUO
if nav_selection == T["tab_status"]:
    st.header(T["tab_status"])
    col1, col2, col3 = st.columns(3)
    
    col1.metric("Kaufpreis", f"{kaufpreis:,.2f} €")
    col2.metric("Gesamtinvest", f"{invest:,.2f} €", f"+{NK_EURO:,.2f} € NK")
    
    tf = get_traffic_light(rendite, 3.5, 2.5)
    col3.metric(T["calc_yield"], f"{rendite:.2f} %", delta=tf)
    
    with st.expander(T["details_header"]):
        st.info(T["status_expl"])
        st.write(f"Reinertrag: {reinertrag:,.2f} € / Gesamtinvest: {invest:,.2f} € = **{rendite:.2f} %**")

# 2. SCENARIO
elif nav_selection == T["tab_scenario"]:
    st.header(T["tab_scenario"])
    
    with st.expander("⚙️ Scenario Settings", expanded=True):
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
            increase = st.slider(T["scen_header"], 0, 30, rent_cap, 1)
    
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
    with st.expander("⚙️ Financing Settings", expanded=True):
        c_zins, c_ek = st.columns(2)
        with c_zins:
            zins = st.slider(T["input_interest"], min_value=1.0, max_value=6.0, step=0.1, key="zins")
        with c_ek:
            ek_quote = st.slider(T["input_equity"], min_value=0, max_value=100, step=5, key="ek")
            
    st.markdown("---")
    
    details = re_tools.berechne_cashflow_detail(kaufpreis, NK_EURO, kaltmiete_pa, costs_pa, zins, ek_quote)
    ek_yield = details['ek_rendite']
    
    col1, col2 = st.columns(2)
    
    bond_rate = 2.8
    diff = re_tools.vergleich_bundesanleihe(ek_yield, bond_rate)
    
    with col1:
        st.subheader(T["lev_bond_comp"])
        st.metric("Immo-EK-Rendite", f"{ek_yield:.2f} %", delta=get_traffic_light(ek_yield, 4.0, 2.0))
        st.metric("Risk-free (Bund)", f"{bond_rate:.2f} %")
        st.metric("Risikoprämie (Spread)", f"{diff:.2f} bp", delta=get_traffic_light(diff, 1.0, 0.0))

    with col2:
        st.subheader(T["lev_wealth_title"])
        tilgung_pa = details['fremdkapital'] * 0.02 
        tilgung_monat = tilgung_pa / 12
        cf_monat = details['cashflow'] / 12
        
        wealth_data = pd.DataFrame({
            "Category": [T["lev_wealth_cf"], T["lev_wealth_amort"], T["lev_wealth_net"]],
            "Amount": [cf_monat, tilgung_monat, cf_monat + tilgung_monat]
        })
        st.bar_chart(wealth_data, x="Category", y="Amount")

    st.markdown("---")
    st.subheader(T["lev_chart_title"])
    
    x_zins = np.linspace(1.0, 6.0, 50)
    obj_yield = rendite 
    
    y_ek_yield = []
    for z in x_zins:
        val = re_tools.berechne_leverage_effekt(obj_yield, z, ek_quote)
        y_ek_yield.append(val)
        
    fig, ax = plt.subplots(figsize=(8,3))
    ax.plot(x_zins, y_ek_yield, label="EK-Rendite", color="blue", linewidth=2)
    ax.axhline(0, color='grey', linewidth=0.8)
    ax.axvline(zins, color='red', linestyle='--', label=f"Ihr Zins ({zins}%)")
    ax.axhline(bond_rate, color='green', linestyle=':', label="Bund (2.8%)")
    ax.set_xlabel("Zins (%)")
    ax.set_ylabel("Eigenkapital-Rendite (%)")
    ax.grid(True, alpha=0.3)
    ax.legend()
    st.pyplot(fig)

# 4. TAX
elif nav_selection == T["tab_tax"]:
    st.header(T["tab_tax"])
    
    # Inputs grouped in Expander (Top)
    with st.expander("⚙️ Tax & Renovation Parameters", expanded=True):
        c_tax1, c_tax2, c_tax3 = st.columns(3)
        with c_tax1:
            boden_anteil = st.slider(T["tax_land_val"], 0, 100, 70, 5)
        with c_tax2:
            pers_steuer = st.slider(T["tax_pers_rate"], 0, 50, 42, 1)
        with c_tax3:
            reno_invest = st.number_input(T["tax_reno_budget"], value=0, step=5000)
    
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

# --- FOOTER ---
st.markdown("---")
st.caption(T["disclaimer"])

# --- PDF EXPORT (Sidebar Bottom) ---
# Prepare Data for PDF (Recalculate or use current scope?)
# Note: Zins/EK must come from Session State
pdf_zins = st.session_state.get('zins', 3.8) # Default if not set
pdf_ek = st.session_state.get('ek', 20.0)

input_data = {
    T["input_price"]: f"{kaufpreis:,.2f} EUR",
    T["input_rent"]: f"{kaltmiete_pa:,.2f} EUR",
    T["input_interest"]: f"{pdf_zins} %",
    T["input_equity"]: f"{pdf_ek} %"
}
result_data = {
    "Invest (All-in)": f"{invest:,.2f} EUR",
    T["calc_yield"]: f"{rendite:.2f} %",
    "Cashflow (p.m.)": f"{(re_tools.berechne_cashflow_detail(kaufpreis, NK_EURO, kaltmiete_pa, costs_pa, pdf_zins, pdf_ek)['cashflow']/12):,.2f} EUR"
}

with st.sidebar:
    st.markdown("---")
    st.header("💾 Export")
    pdf_bytes = create_pdf(st.session_state.lang, input_data, result_data)
    st.download_button(
        label="📄 PDF Download",
        data=pdf_bytes,
        file_name="investment_dossier.pdf",
        mime="application/pdf"
    )
