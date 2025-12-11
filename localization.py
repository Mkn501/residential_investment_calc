# localization.py

# Text Dictionary for DE/EN
UI_TEXTS = {
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

PDF_TEXTS = {
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
