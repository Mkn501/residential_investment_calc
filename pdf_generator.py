from fpdf import FPDF
from localization import PDF_TEXTS

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

# --- PDF GENERATOR FUNCTION ---
def create_pdf(lang_code, inputs, results, extra_params={}):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Select Language Dict
    L = PDF_TEXTS.get(lang_code, PDF_TEXTS["EN"])
    
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
