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
        "title": "🏢 Kapitalanlage-Rechner: Wohnen",
        "subtitle": "Cashflow, Steuern & Opportunitätskosten",
        "sidebar_header": "1. Themen",
        "lang_select": "Sprache / Language",
        "input_price": "Kaufpreis (€)",
        "input_rent": "Aktuelle Kaltmiete (p.a.)",
        "property_data_header": "🏠 Eckdaten",
        "input_costs": "Bewirtschaftungskosten (p.a.)",
        "input_interest": "Zinssatz (%)",
        "input_equity": "Eigenkapital (%)",
        "input_loc": "Mietpreisbremse (Ort)",
        "loc_active": "Aktiv (max 15% Erhöhung)",
        "loc_inactive": "Inaktiv (max 20% Erhöhung)",
        "tab_intro": "Einführung & Anleitung",
        "tab_status": "Ist-Mietrendite",
        "tab_scenario": "Miet-Szenario",
        "tab_leverage": "3. Leverage & Cashflow",
        "tab_tax": "4. Steuern & Sanierung",
        "tab_due_diligence": "5. Due Diligence",
        "tab_report": "6. Verhandlungs-Dossier",
        "report_header": "📄 Verhandlungs-Dossier & Kaufangebot",
        "report_intro": "Dieses Modul erstellt automatisch ein professionelles Investoren-Dossier, um einen niedrigeren Kaufpreis zu verhandeln.",
        "rep_sec0": "1. Basisdaten & Investitionsvolumen",
        "rep_purchase_price": "Kaufpreis",
        "rep_closing_costs": "Kaufnebenkosten",
        "rep_total_invest": "Gesamt-Invest",
        "rep_rent_income": "Mieteinnahmen (Ist)",
        "rep_sec1": "2. Finanzielle Realität",
        "rep_yield": "Aktuelle Rendite",
        "rep_interest": "Zinssatz (Bank)",
        "rep_gap": "Hebel-Lücke (Gap)",
        "rep_neg_lev": "NEGATIVER HEBEL: Die Rendite ({:.2f}%) liegt unter dem Zins ({:.2f}%). Nutzen Sie das als Argument!",
        "rep_sec2": "3. Fairer Kaufpreis (Herleitung)",
        "rep_target_yield": "Wunsch-Rendite (%)",
        "rep_fair_val": "Fairer Marktwert",
        "rep_sec3": "4. Dossier Herunterladen",
        "rep_yield_settings": "🎯 Wunsch-Rendite Einstellungen",
        "rep_caption": "Basierend auf {:.1f}% Wunsch-Rendite & {:.2f}% Kaufnebenkosten.",
        "rep_max_invest": "Max. Gesamt-Invest",
        "rep_deriv_title": "📝 Detaillierte Herleitung anzeigen",
        "rep_step1": "1. Bereinigte Nettomiete (p.a.)",
        "rep_step2": "2. Maximales Volumen (All-in)",
        "rep_step3": "3. Abzug Nebenkosten ({:.2f}%)",
        "rep_step4": "4. Fairer Kaufpreis",
        "intro_header": "👋 Willkommen beim Immobilien-Investment-Rechner",
        "intro_text": """
        Dieses Tool hilft Ihnen, eine Immobilie als Kapitalanlage rational zu bewerten.
        
        **Die Funktionen im Überblick:**
        
        *   **📊 Ist-Mietrendite**: Der "Status Quo". Wie rentiert sich das Objekt heute mit der aktuellen Miete?
        *   **🔮 Miet-Szenario**: Wie entwickelt sich die Rendite bei einer Mieterhöhung (z.B. +15%)? Lohnt sich der Kauf langfristig?
        *   **⚖️ Leverage & Cashflow**: Der wichtigste Tab. Berechnet Ihre Eigenkapitalrendite (Hebel) und Ihren monatlichen Cashflow (was müssen Sie draufzahlen?).
        *   **🏗️ Steuern & Sanierung**: Prüft die "15%-Grenze" für Renovierungen und berechnet Ihren Steuervorteil durch Abschreibung (AfA).
        *   **🕵️ Due Diligence**: Eine Checkliste für die "versteckten Risiken" (WEG-Protokolle, Heizung, Sonderumlagen).
        
        **Tipp**: Starten Sie mit der Eingabe des Kaufpreises links und arbeiten Sie sich durch die Reiter!
        """,
        "status_header": "1. Status Quo: Aktuelle Rendite",
        "calc_yield": "Netto-Mietrendite",
        "calc_cf": "Cashflow",
        "details_header": "🔍 Details & Erklärung",
        "status_expl": """
        **1. Netto-Mietrendite**: Verhältnis von Reinertrag (Miete - Kosten) zum Gesamtinvest.
        
        **2. Was sind Bewirtschaftungskosten?**
        Hier tragen Sie nur die **nicht umlegbaren** Kosten ein.
        *   **Hausgeld**: Das zahlen Sie an die Verwaltung (z.B. 300€).
        *   **Umlagefähig**: Heizung, Wasser, Müll (z.B. 200€). Das zahlt der Mieter via Nebenkostenvorauszahlung (Durchlaufposten).
        *   **Nicht Umlagefähig (Ihr Kostenblock)**: Verwaltergebühr & Instandhaltungsrücklage (z.B. 100€). **Nur dieser Betrag** gehört in das Feld 'Bewirtschaftungskosten', da er Ihre Rendite schmälert.
        """,
        "scen_header": "Mietsteigerung (3 Jahre)",
        "scen_settings_header": "⚙️ Szenario-Einstellungen",
        "fin_settings_header": "⚙️ Finanzierungs-Plan",
        "tax_settings_header": "⚙️ Steuer-Parameter",
        "scen_cap_warn": "⚠️ Kappungsgrenze aktiv (max. 15%)",
        "scen_new_rent": "Neue Kaltmiete (p.a.)",
        "scen_pot_yield": "Potenzielle Rendite",
        "traffic_red": "🔴 Schlecht",
        "traffic_yellow": "🟡 Mäßig",
        "traffic_green": "🟢 Gut",
        "lev_chart_title": "Leverage-Effekt: EK-Rendite vs. Zins Jahr 1",
        "lev_details_header": "🔢 Detail-Rechnung",
        "lev_details_note": "⚠️ *Hinweis: Dies ist eine Betrachtung des 1. Jahres. Da Sie den Kredit tilgen, sinkt der Zinsanteil jährlich, wodurch Ihr Cashflow über die Zeit steigt.*",
        "lev_bond_comp": "Vergleich mit Bundesanleihe",
        "lev_wealth_expl": "ℹ️ Hilfe: Wie lese ich diese Grafik?",
        "lev_wealth_note": "ℹ️ *Hinweis: Start-Momentaufnahme (Monat 1). Da die Tilgung monatlich steigt (und Zinsen sinken), wächst Ihr Vermögen jeden Monat etwas schneller!*",
        "lev_expl_title": "ℹ️ Hilfe: Wie lese ich diese Grafik?",
        "lev_expl_text": """
        Diese Grafik zeigt den **Hebel-Effekt (Leverage)**:
        *   Die **blaue Linie** ist Ihre Eigenkapital-Rendite. Sie hängt stark vom Zins ab.
        *   **Links (Niedriger Zins)**: Der Kredit ist billig, Sie verdienen an der Differenz zur Mietrendite. Ihr Gewinn schießt nach oben! 🚀
        *   **Rechts (Hoher Zins)**: Der Kredit ist teuer. Er frisst die Mieteinnahmen auf. Ihre Rendite fällt unter die der Immobilie – oder wird sogar negativ. 📉
        *   Die **grüne Linie** ist der sichere Hafen (Bundesanleihe). Wenn die blaue Linie *unter* der grünen liegt, gehen Sie ein Risiko ein, das schlechter bezahlt wird als eine risikolose Anlage.
        """,
        "lev_wealth_title": "Vermögenszuwachs 1.Monat",
        "lev_wealth_cf": "Cashflow (Sie zahlen)",
        "lev_wealth_amort": "Tilgung (Mieter zahlt)",
        "lev_wealth_net": "Netto-Vermögen",
        "tax_land_val": "Bodenwertanteil (%)",
        "tax_pers_rate": "Pers. Steuersatz (%)",
        "tax_reno_budget": "Renovierungskosten (3J)",
        "tax_3y_expl": "Warum 3 Jahre? Ausgaben > 15% des Gebäudewerts innerhalb von 3 Jahren nach Kauf gelten steuerlich als 'Anschaffungskosten'. Sie können **nicht** sofort abgesetzt werden, sondern müssen über 50 Jahre abgeschrieben werden. Das drückt die Rendite massiv!",
        "tax_afa_calc": "Steuerrückerstattung (AfA)",
        "tax_15_rule": "15% Grenze (Netto)",
        "tax_expl_title": "ℹ️ Steuer-Wissen: Wie hängen AfA, Bodenwert & 15% zusammen?",
        "tax_expl_text": """
        **1. AfA (Absetzung für Abnutzung)**
        Der Staat beteiligt sich am Wertverlust der Immobilie. Sie dürfen meist **2% des Gebäudewerts** pro Jahr als fiktive Kosten absetzen.
        
        **2. Bodenwertanteil (Der 'Feind' der AfA)**
        Grund und Boden "nutzen sich nicht ab". Daher darf nur das Gebäude abgeschrieben werden.
        *   **Hoher Bodenwert (z.B. München 70%)** = Niedriger Gebäudewert = **Wenig AfA**.
        *   **Niedriger Bodenwert (z.B. Land 20%)** = Hoher Gebäudewert = **Viel AfA**.
        
        **3. Persönlicher Steuersatz**
        Die AfA mindert Ihr zu versteuerndes Einkommen. Je höher Ihr Steuersatz, desto mehr "Geld zurück" gibt es vom Finanzamt.
        *   *Beispiel: 5.000 € AfA x 42% Steuersatz = 2.100 € Cash-Rückfluss p.a.*
        
        **4. Die 15% Grenze (Renovierungs-Falle)**
        Ausgaben > 15% des Gebäudewerts (netto) in den ersten 3 Jahren gelten als **Anschaffungskosten**.
        *   **Folge**: Sie können die Kosten nicht sofort absetzen (Steuerrückfluss jetzt), sondern müssen sie über 50 Jahre abschreiben (Steuerrückfluss tröpfchenweise).
        """,
        "dd_checklist": "Prüfungs-Checkliste",
        "dd_weg": "Wohnungseigentümergemeinschaft (WEG)-Protokolle & Rücklage",
        "dd_rules": "Teilungserklärung (Fenster?)",
        "dd_energy": "Energieausweis & Heizung (1992?)",
        "dd_tenant": "Mieterhistorie & Eigenbedarf",
        "dd_expl_title": "ℹ️ Warum ist das wichtig?",
        "dd_expl_text": """
        **1. WEG-Protokolle & Rücklage**
        *   **Risiko**: Ist die Rücklage leer? Droht eine **Sonderumlage** (z.B. für ein neues Dach)?
        *   **Check**: Protokolle der letzten 3 Jahre lesen! Wurde über teure Sanierungen gestritten?
        
        **2. Teilungserklärung**
        *   **Risiko**: Wer zahlt die neuen Fenster? Sie allein (Sondereigentum) oder die Gemeinschaft (Gemeinschaftseigentum)?
        *   **Check**: In der Teilungserklärung nach "Fenster" suchen.
        
        **3. Energie & Heizung**
        *   **Risiko**: Ein Kessel von 1991 muss oft sofort getauscht werden (Austauschpflicht).
        *   **Check**: Energieausweis & Typenschild der Heizung prüfen.
        
        **4. Mieter & Eigenbedarf**
        *   **Risiko**: Wollen Sie selbst einziehen? Bei Alt-Mietern oder Härtefällen (Alter, Krankheit) kann eine Kündigung Jahre dauern.
        """,
        "disclaimer": "⚠️ HAFTUNGSAUSSCHLUSS: Dieses Tool dient ausschließlich Bildungszwecken. Keine Anlageberatung. Investitionen auf eigenes Risiko.",
    },
    "EN": {
        "title": "🏢 Real Estate Investment Calculator: Residential",
        "subtitle": "Cashflow, Taxes & Opportunity Costs",
        "sidebar_header": "1. Topics",
        "lang_select": "Language / Sprache",
        "input_price": "Purchase Price (€)",
        "input_rent": "Current Net Rent (p.a.)",
        "property_data_header": "🏠 Property Data",
        "input_costs": "Maintenance Costs (p.a.)",
        "input_interest": "Interest Rate (%)",
        "input_equity": "Equity Share (%)",
        "input_loc": "Rent Control (Location)",
        "loc_active": "Active (max 15% increase)",
        "loc_inactive": "Inactive (max 20% increase)",
        "tab_intro": "Introduction & Guide",
        "tab_status": "Status Quo (Yield)",
        "tab_scenario": "Rent Scenario",
        "tab_leverage": "3. Leverage & Cashflow",
        "tab_tax": "4. Tax & Renovation",
        "tab_due_diligence": "5. Due Diligence",
        "tab_report": "6. Negotiation Dossier",
        "report_header": "📄 Negotiation Dossier & Offer",
        "report_intro": "This module automatically generates a professional investor dossier to negotiate a lower purchase price.",
        "rep_sec0": "1. Base Figures & Investment Volume",
        "rep_purchase_price": "Purchase Price",
        "rep_closing_costs": "Closing Costs",
        "rep_total_invest": "Total Investment",
        "rep_rent_income": "Current Rent Income",
        "rep_sec1": "2. Financial Reality Check",
        "rep_yield": "Current Yield",
        "rep_interest": "Interest Rate",
        "rep_gap": "Leverage Gap",
        "rep_neg_lev": "NEGATIVE LEVERAGE: The Yield ({:.2f}%) is lower than the Interest Rate ({:.2f}%). Use this argument to lower the price!",
        "rep_sec2": "3. Fair Price Derivation",
        "rep_target_yield": "Negotiation Target Yield (%)",
        "rep_fair_val": "Fair Market Value",
        "rep_sec3": "4. Download Dossier",
        "rep_yield_settings": "🎯 Target Yield Settings",
        "rep_caption": "Based on {:.1f}% Target Yield & {:.2f}% Closing Costs.",
        "rep_max_invest": "Max All-in",
        "rep_deriv_title": "📝 Show Detailed Derivation",
        "rep_step1": "1. Adjusted Net Rent (p.a.)",
        "rep_step2": "2. Max Volume (All-in)",
        "rep_step3": "3. Deduct Closing Costs ({:.2f}%)",
        "rep_step4": "4. Fair Price",
        "intro_header": "👋 Welcome to the Real Estate Investment Calculator",
        "intro_text": """
        This tool helps you rationally evaluate a property as an investment.
        
        **Overview of Features:**
        
        *   **📊 Status Quo Yield**: How does the property perform today with current rent?
        *   **🔮 Rent Scenario**: How does the yield evolve with a rent increase (e.g. +15%)? Is it worth it long-term?
        *   **⚖️ Leverage & Cashflow**: The most important tab. Calculates Return on Equity (Leverage) and monthly Cashflow (Do you pay on top?).
        *   **🏗️ Tax & Renovation**: Checks the "15% Rule" for renovations and calculates tax benefits (Depreciation/AfA).
        *   **🕵️ Due Diligence**: A checklist for "hidden risks" (HOA protocols, Heating, Special Levies).
        
        **Tip**: Start by entering the Purchase Price on the left and work your way through the tabs!
        """,
        "status_header": "1. Status Quo: Current Yield",
        "calc_yield": "Net Rental Yield",
        "calc_cf": "Cashflow",
        "details_header": "🔍 Context & Explanation",
        "status_expl": """
        **1. Net Rental Yield**: Ratio of Net Profit (Rent - Costs) to Total Investment.
        
        **2. What are 'Maintenance Costs'?**
        Enter only the **non-recoverable** costs here.
        *   **HOA Fee (Hausgeld)**: Total amount you pay to management (e.g. 300€).
        *   **Recoverable**: Heating, Water, Garbage (e.g. 200€). The tenant pays this via utility prepayments (pass-through).
        *   **Non-Recoverable (Your Cost)**: Admin Fee & Maintenance Reserve (e.g. 100€). **Only this amount** belongs in this field, as it reduces your yield.
        """,
        "scen_header": "Rent Increase (3 Years)",
        "scen_settings_header": "⚙️ Scenario Settings",
        "fin_settings_header": "⚙️ Financing Defaults",
        "tax_settings_header": "⚙️ Tax & Renovation Parameters",
        "scen_cap_warn": "⚠️ Rent Cap Active (max 15%)",
        "scen_new_rent": "New Net Rent (p.a.)",
        "scen_pot_yield": "Potential Yield",
        "traffic_red": "🔴 Poor",
        "traffic_yellow": "🟡 Mediocre",
        "traffic_green": "🟢 Good",
        "lev_chart_title": "Leverage Effect: Equity Yield vs. Interest Year 1",
        "lev_details_header": "🔢 Detailed Calculation",
        "lev_details_note": "⚠️ *Note: This is a snapshot of Year 1. As you amortize the loan, interest payments decrease annually, improving your cashflow over time.*",
        "lev_bond_comp": "Bond Comparison",
        "lev_wealth_expl": "ℹ️ Help: How to read this chart?",
        "lev_wealth_note": "ℹ️ *Note: Snapshot of Month 1. Since amortization increases monthly (and interest drops), your wealth accumulation accelerates every month!*",
        "lev_expl_title": "ℹ️ Help: How to read this chart?",
        "lev_expl_text": """
        This chart visualizes the **Leverage Effect**:
        *   The **Blue Line** is your Return on Equity. It reacts sensitively to interest rates.
        *   **Left (Low Interest)**: Money is cheap. You profit from the spread between rent and interest. Your return skyrockets! 🚀
        *   **Right (High Interest)**: Money is expensive. Interest costs eat up your rent. Your return drops below the property's yield – or even turns negative. 📉
        *   The **Green Line** is the safe benchmark (Bond). If the blue line is *below* the green line, you are taking on risk for a return that is worse than a risk-free investment.
        """,
        "lev_wealth_title": "Wealth Accumulation Month 1",
        "lev_wealth_cf": "Cashflow (You pay)",
        "lev_wealth_amort": "Amortization (Tenant pays)",
        "lev_wealth_net": "Net Weath Change",
        "tax_land_val": "Land Value Share (%)",
        "tax_pers_rate": "Personal Tax Rate (%)",
        "tax_reno_budget": "Renovation Costs (3Y)",
        "tax_3y_expl": "Why 3 Years? Costs > 15% of building value within 3 years are treated as 'Acquisition Costs'. They cannot be deducted immediately but must be depreciated over 50 years. This hurts your yield significantly!",
        "tax_afa_calc": "Tax Refund (Depreciation)",
        "tax_15_rule": "15% Limit (Net)",
        "tax_expl_title": "ℹ️ Tax Logic: AfA, Land Value & 15% Rule explained",
        "tax_expl_text": """
        **1. AfA (Depreciation)**
        The state participates in the property's loss of value. You typically deduct **2% of the building value** per year as fictional costs.
        
        **2. Land Value Share (Antagonist of Depreciation)**
        Land does "not depreciate". Therefore, only the building can be written off.
        *   **High Land Value (e.g. Munich 70%)** = Low Building Value = **Low Tax Refund**.
        *   **Low Land Value (e.g. Rural 20%)** = High Building Value = **High Tax Refund**.
        
        **3. Personal Tax Rate**
        Depreciation lowers your taxable income. The higher your tax rate, the more cash you get back.
        *   *Example: 5,000 € AfA x 42% Tax = 2,100 € Cash back p.a.*
        
        **4. The 15% Limit (Renovation Trap)**
        Spending > 15% of the building value (net) in the first 3 years counts as **Acquisition Costs**.
        *   **Result**: You cannot deduct costs immediately but must depreciate them over 50 years (slow trickle instead of cash flood).
        """,
        "dd_checklist": "Due Diligence Checklist",
        "dd_weg": "WEG (Wohnungseigentümergemeinschaft) Protocols & Reserves",
        "dd_rules": "Community Rules (Windows?)",
        "dd_energy": "Energy Cert & Boiler (1992?)",
        "dd_tenant": "Tenant History & Own Use",
        "dd_expl_title": "ℹ️ Why is this important?",
        "dd_expl_text": """
        **1. WEG Protocols & Reserves**
        *   **Risk**: Are reserves empty? Is a **Special Levy** looming (e.g. for a new roof)?
        *   **Check**: Read protocols of the last 3 years! Was there conflict over expensive repairs?
        
        **2. Declaration of Division**
        *   **Risk**: Who pays for new windows? You alone (Special Property) or the Community (Common Property)?
        *   **Check**: Search the Declaration for "Windows".
        
        **3. Energy & Heating**
        *   **Risk**: A boiler from 1991 often needs immediate replacement (mandatory exchange).
        *   **Check**: Check Energy Certificate & Boiler plate.
        
        **4. Tenant & Own Use**
        *   **Risk**: Do you want to move in? With long-term tenants or hardship cases, termination can take years.
        """,
        "disclaimer": "⚠️ DISCLAIMER: Educational purpose only. Not financial advice. Investments at own risk.",
    }
}

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
        ["🇩🇪 Deutsch", "🇺🇸 English"], 
        index=0 if st.session_state.lang == "DE" else 1,
        label_visibility="collapsed",
        horizontal=True
    )
    st.session_state.lang = "DE" if "Deutsch" in lang_choice else "EN"

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


# --- PDF HELPER (NEGOTIATION DOSSIER) ---
def create_pdf(lang_code, inputs, results, extra_params={}):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # --- LOCALIZATION DICT ---
    T_PDF = {
        "DE": {
            "title": "Investitions-Analyse & Verhandlungs-Dossier",
            "date": "Datum",
            "p1_header": "1. Finanzielle Realität (Status Quo)",
            "p1_verdict_neg": "FAZIT: Negativer Hebel (Rendite < Zins). Das Investment vernichtet monatlich Kapital. Eine Preisanpassung ist wirtschaftlich zwingend .",
            "p1_verdict_pos": "FAZIT: Das Investment ist cashflow-neutral oder positiv.",
            "p1_gap_text": "Vergleich mit Risiko-freier Anlage (Anleihe {:.2f}%) und Finanzierungskosten ({:.2f}%): Die aktuelle Netto-Mietrendite von {:.2f}% zeigt eine {} Lücke von {:.2f}%.",
            "pos": "POSITIVE", "neg": "NEGATIVE",
            "scen_title": "Optimierungs-Szenario (Potenzial)",
            "scen_text": "Durch eine Mietanpassung von +{:.1f}% steigt die Miete (Soll) auf {:.2f} EUR. Die Rendite verbessert sich auf {:.2f}%.",
            "scen_gap": "Neue Hebel-Lücke (Soll): {:.2f}%",
            "p2_header": "2. Herleitung Fairer Kaufpreis",
            "p2_target": "Marktübliche Ziel-Rendite:",
            "p2_rent": "Bereinigte Nettomiete (p.a.):",
            "p2_max_vol": "Max. Investitionsvolumen (All-in):",
            "p2_expl": "(Berechnet als: Nettomiete / {}%)",
            "p2_costs": "Abzug Kaufnebenkosten ({:.2f}%):",
            "p2_final": "MAXIMALER KAUFPREIS:",
            "p3_header": "FORMALES KAUFANGEBOT",
            "letter": """
Sehr geehrte Damen und Herren,

vielen Dank für die Möglichkeit, das Objekt zu prüfen.
Basierend auf unserer kaufmännischen Due Diligence und dem aktuellen Zinsumfeld ({interest}%) müssen wir einer disziplinierten Investitionsstrategie folgen.

Um eine nachhaltige Bewirtschaftung bei einer Ziel-Rendite von {target}% sicherzustellen (reflektiert den risikofreien Zins von {bond}% plus Risikoprämie), liegt unsere maximale Bewertung für dieses Objekt bei:

{price} EUR

Diese Kalkulation berücksichtigt notwendige Instandhaltungsrücklagen und die nicht umlagefähigen Bewirtschaftungskosten.

Dieses Angebot ist 14 Tage gültig und steht unter dem Vorbehalt der finalen Finanzierungszusage.
Wir sind bereit, kurzfristig einen Notartermin wahrzunehmen.

Mit freundlichen Grüßen,
"""
        },
        "EN": {
            "title": "Investment Analysis & Negotiation Dossier",
            "date": "Date",
            "p1_header": "1. Financial Reality Check (Status Quo)",
            "p1_verdict_neg": "VERDICT: Negative Leverage (Yield < Interest). The investment loses capital monthly. A price adjustment is strictly necessary.",
            "p1_verdict_pos": "VERDICT: The investment is cashflow neutral or positive.",
            "p1_gap_text": "Compared to the Risk-Free Bond Rate ({:.2f}%) and Financing Interest ({:.2f}%): The Net Initial Yield of {:.2f}% shows a {} Leverage Gap of {:.2f}%.",
            "pos": "POSITIVE", "neg": "NEGATIVE",
            "scen_title": "Optimization Scenario (Potential)",
            "scen_text": "With a rent adjustment of +{:.1f}%, the rent (target) increases to {:.2f} EUR. The yield improves to {:.2f}%.",
            "scen_gap": "New Leverage Gap (Potential): {:.2f}%",
            "p2_header": "2. Fair Price Derivation",
            "p2_target": "Target Yield (Market Standard):",
            "p2_rent": "Adjusted Net Rent (p.a.):",
            "p2_max_vol": "Max. Investment Volume (All-in):",
            "p2_expl": "(Calculated as: Net Rent / {}%)",
            "p2_costs": "Less Closing Costs ({:.2f}%):",
            "p2_final": "MAXIMUM PURCH. PRICE:",
            "p3_header": "FORMAL OFFER LETTER",
            "letter": """
Dear Sir or Madam,

Thank you for the opportunity to review the property.
Based on our commercial due diligence and the current interest rate environment ({interest}%), we must adhere to a disciplined investment strategy.

To ensure sustainable operations at a target yield of {target}% (reflecting the risk-free rate of {bond}% plus risk premium), our maximum valuation for this property is:

{price} EUR

This calculation calculates accounts for necessary maintenance reserves and non-recoverable operating costs.

This offer is valid for 14 days and is subject to final financing approval.
We are prepared to move quickly with the notary appointments.

Sincerely,
"""
        }
    }
    
    # Select Language Dict
    L = T_PDF.get(lang_code, T_PDF["EN"])
    
    # --- HELPER: SAFE TEXT ---
    def safe_text(text):
        replacements = {
            "€": "EUR", "⚠️": "(!)", "✅": "[OK]", "🔴": "(!)", 
            "🟡": "(-)", "🟢": "(+)", "„": '"', "“": '"', "ä": "ae", "ö": "oe", "ü": "ue", "ß": "ss",
            "Ä": "Ae", "Ö": "Oe", "Ü": "Ue"
        }
        for k, v in replacements.items():
            text = text.replace(k, v)
        try:
            return text.encode('latin-1', 'replace').decode('latin-1')
        except:
            return "?"

    # --- PAGE 1: EXECUTIVE SUMMARY ---
    pdf.add_page()
    pdf.set_font("Arial", 'B', 20)
    pdf.cell(0, 10, safe_text(L["title"]), 0, 1, 'C')
    pdf.ln(5)
    
    pdf.set_font("Arial", '', 10)
    pdf.cell(0, 10, safe_text(f"{L['date']}: {extra_params.get('date', 'Today')}"), 0, 1, 'C')
    pdf.ln(10)
    
    # Section: Key Metrics
    pdf.set_font("Arial", 'B', 14)
    pdf.set_fill_color(240, 240, 240)
    pdf.cell(0, 10, safe_text(L["p1_header"]), 1, 1, 'L', 1)
    
    pdf.set_font("Arial", '', 12)
    pdf.ln(5)
    
    for k, v in inputs.items():
        pdf.cell(90, 8, safe_text(f"{k}:"), 0, 0)
        pdf.cell(90, 8, safe_text(str(v)), 0, 1)
        
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    for k, v in results.items():
        pdf.cell(90, 8, safe_text(f"{k}:"), 0, 0)
        pdf.cell(90, 8, safe_text(str(v)), 0, 1)
        
    pdf.ln(10)
    
    # Section: Reality Check / Yield Gap
    bond = extra_params.get('bond_rate', 2.5)
    interest = extra_params.get('zins', 3.8)
    yield_num = extra_params.get('yield_num', 0.0)
    gap = yield_num - interest
    
    pdf.set_font("Arial", 'B', 14)
    # Reuse Header style if needed, or just text
    # pdf.cell(0, 10, safe_text("2. Analysis"), 1, 1, 'L', 1) 
    
    pdf.set_font("Arial", '', 11)
    gap_label = L["pos"] if gap > 0 else L["neg"]
    
    pdf.multi_cell(0, 6, safe_text(
        L["p1_gap_text"].format(bond, interest, yield_num, gap_label, gap)
    ))
    pdf.ln(5)
    
    if gap < 0:
        pdf.set_text_color(200, 0, 0)
        pdf.multi_cell(0, 6, safe_text(L["p1_verdict_neg"]))
    else:
        pdf.multi_cell(0, 6, safe_text(L["p1_verdict_pos"]))
        
    # --- POTENTIAL SCENARIO (If applicable) ---
    scen_inc = extra_params.get('scen_increase', 0)
    if scen_inc > 0:
        pdf.ln(5)
        pdf.set_text_color(0, 0, 0) # Reset color
        pdf.set_fill_color(220, 255, 220) # Light Green
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 8, safe_text(L["scen_title"]), 1, 1, 'L', 1)
        
        pdf.set_font("Arial", '', 11)
        pot_rent = extra_params.get('pot_rent_pa', 0)
        pot_yield = extra_params.get('pot_yield', 0)
        pot_gap = pot_yield - interest
        
        pdf.multi_cell(0, 6, safe_text(
            L["scen_text"].format(scen_inc, pot_rent, pot_yield)
        ))
        
        # Gap Visualization
        gap_label_pot = L["pos"] if pot_gap > 0 else L["neg"]
        pdf.cell(0, 6, safe_text(L["scen_gap"].format(pot_gap) + f" ({gap_label_pot})"), 0, 1)
        pdf.set_text_color(0, 0, 0)

    # --- PAGE 2: FAIR PRICE DERIVATION ---
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, safe_text(L["p2_header"]), 0, 1, 'L')
    pdf.ln(5)
    
    # Logic
    target_yield = extra_params.get('target_yield', 3.5)
    km_pa = extra_params.get('km_pa', 0)
    cost_pa = extra_params.get('cost_pa', 0)
    net_rent = km_pa - cost_pa
    
    # Calc
    max_invest = net_rent / (target_yield/100) if target_yield else 0
    p_makler = extra_params.get('p_makler', 3.57)
    p_tax = extra_params.get('p_tax', 3.5)
    p_notar = extra_params.get('p_notar', 2.0)
    total_costs_pct = (p_makler + p_tax + p_notar)/100
    
    fair_price = max_invest / (1 + total_costs_pct)
    
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 8, safe_text(f"{L['p2_target']} {target_yield:.2f} %"), 0, 1)
    pdf.ln(5)
    
    # Table like text
    pdf.cell(100, 8, safe_text(L["p2_rent"]), 0, 0)
    pdf.cell(50, 8, safe_text(f"{net_rent:,.2f} EUR"), 0, 1, 'R')
    
    pdf.cell(100, 8, safe_text(L["p2_max_vol"]), 0, 0)
    pdf.cell(50, 8, safe_text(f"{max_invest:,.2f} EUR"), 0, 1, 'R')
    pdf.set_font("Arial", 'I', 10)
    pdf.cell(0, 5, safe_text(L["p2_expl"].format(target_yield)), 0, 1)
    
    pdf.ln(5)
    pdf.set_font("Arial", '', 12)
    pdf.cell(100, 8, safe_text(L["p2_costs"].format(total_costs_pct*100)), 0, 0)
    costs_abs = max_invest - fair_price
    pdf.cell(50, 8, safe_text(f"- {costs_abs:,.2f} EUR"), 0, 1, 'R')
    
    pdf.ln(2)
    pdf.set_fill_color(220, 255, 220)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(100, 12, safe_text(L["p2_final"]), 1, 0, 'L', 1)
    pdf.cell(50, 12, safe_text(f"{fair_price:,.2f} EUR"), 1, 1, 'R', 1)
    
    # --- PAGE 3: OFFER LETTER ---
    pdf.add_page()
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, safe_text(L["p3_header"]), 0, 1, 'C')
    pdf.ln(10)
    
    pdf.set_font("Arial", '', 11)
    
    formatted_letter = L["letter"].format(
        interest=interest,
        target=target_yield,
        bond=bond,
        price=f"{fair_price:,.2f}"
    )
    
    pdf.multi_cell(0, 6, safe_text(formatted_letter))
    
    return pdf.output(dest='S').encode('latin-1')

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
            increase = st.slider(T["scen_header"], 0, 30, 0, 1, key="scen_increase")
    
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
            reno_invest = st.number_input(T["tax_reno_budget"], value=0, step=5000, help=T["tax_3y_expl"])
    
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
