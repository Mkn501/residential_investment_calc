
def berechne_maximalen_kaufpreis(
    monatsmiete_netto, 
    ziel_rendite_prozent, 
    makler_prozent=3.57, 
    grunderwerbsteuer_prozent=3.5, 
    notar_grundbuch_prozent=2.0
):
    """
    Berechnet den maximalen Kaufpreis einer Immobilie basierend auf der Zielrendite (Netto-Mietrendite auf Gesamtinvest).
    Rückwärtsrechnung vom Ertrag zum Kaufpreis.
    """
    
    # 1. Jahresmiete berechnen
    jahresmiete = monatsmiete_netto * 12
    
    # 2. Maximales Gesamtinvestment berechnen (All-In Preis)
    # Formel: Jahresmiete / (Zielrendite / 100)
    max_gesamtinvestition = jahresmiete / (ziel_rendite_prozent / 100)
    
    # 3. Faktor für Kaufnebenkosten berechnen
    # Summe der Prozentsätze (z.B. 3.57 + 3.5 + 2.0 = 9.07% -> Faktor 1.0907)
    nebenkosten_faktor = 1 + ((makler_prozent + grunderwerbsteuer_prozent + notar_grundbuch_prozent) / 100)
    
    # 4. Reinen Kaufpreis (Angebotspreis) berechnen
    # Gesamtinvestition = Kaufpreis * Nebenkostenfaktor
    # Umgestellt: Kaufpreis = Gesamtinvestition / Nebenkostenfaktor
    max_kaufpreis = max_gesamtinvestition / nebenkosten_faktor
    
    # 5. Die konkreten Nebenkosten in Euro berechnen (für die Ausgabe)
    nebenkosten_euro = max_gesamtinvestition - max_kaufpreis
    
    return max_kaufpreis, max_gesamtinvestition, nebenkosten_euro

def berechne_netto_mietrendite(kaufpreis, nebenkosten, kaltmiete_pa, bewirtschaftungskosten_pa):
    """
    Berechnet die aktuelle Netto-Mietrendite (Status Quo).
    Formel: (Kaltmiete - Bewirtschaftung) / (Kaufpreis + Nebenkosten) * 100
    """
    reinertrag = kaltmiete_pa - bewirtschaftungskosten_pa
    gesamtinvest = kaufpreis + nebenkosten
    rendite = (reinertrag / gesamtinvest) * 100
    return rendite, reinertrag, gesamtinvest

def berechne_mietpotential(aktuelle_miete, steigerung_prozent=15, jahre=3):
    """
    Berechnet die maximal zulässige Miete nach Erhöhung (Kappungsgrenze).
    Standard: 15% in 3 Jahren (für angespannte Märkte wie München/Starnberg).
    """
    neue_miete = aktuelle_miete * (1 + steigerung_prozent / 100)
    return neue_miete

def berechne_leverage_effekt(objektrendite_prozent, fremdkapital_zins_prozent, eigenkapital_anteil_prozent):
    """
    Berechnet die Eigenkapitalrendite unter Berücksichtigung des Leverage-Effekts.
    Formel: rEK = rGK + (rGK - rFK) * (FK / EK)
    """
    ek_anteil = eigenkapital_anteil_prozent / 100
    fk_anteil = 1 - ek_anteil
    
    # Leverage Formel
    # rGK = Objektrendite (Gesamtkapitalrendite)
    # rFK = Fremdkapitalzins
    
    # Avoid Division by Zero if Equity is 0%
    if ek_anteil == 0:
        # If Spread is positive, infinite return. If negative, infinite loss.
        # We cap it at a high number for display or handle it gracefully.
        spread = objektrendite_prozent - fremdkapital_zins_prozent
        if spread > 0:
            return 999.0 # Infinite positive return
        elif spread < 0:
            return -999.0 # Infinite negative return
        else:
            return objektrendite_prozent

    eigenkapitalrendite = objektrendite_prozent + (objektrendite_prozent - fremdkapital_zins_prozent) * (fk_anteil / ek_anteil)
    
    return eigenkapitalrendite

def vergleich_bundesanleihe(immobilien_rendite, anleihe_rendite=2.8):
    """
    Vergleicht die Immobilienrendite mit einer risikofreien Anlage.
    """
    diff = immobilien_rendite - anleihe_rendite
    return diff

def berechne_kaufnebenkosten(kaufpreis, makler_prozent=3.57, grunderwerb_prozent=3.5, notar_prozent=2.0):
    """
    Berechnet die absoluten Kaufnebenkosten in Euro basierend auf dem Kaufpreis.
    """
    faktor = (makler_prozent + grunderwerb_prozent + notar_prozent) / 100
    nebenkosten_euro = kaufpreis * faktor
    return nebenkosten_euro

def berechne_afa_vorteil(kaufpreis, bodenwert_anteil_prozent=70.0, steuersatz_prozent=42.0):
    """
    Berechnet die steuerliche Abschreibung (AfA).
    Achtung: Nur der Gebäudewert (Kaufpreis - Bodenwert) wird abgeschrieben!
    Standard AfA: 2% (für Gebäude vor 2024).
    """
    gebaeudewert_faktor = (100 - bodenwert_anteil_prozent) / 100
    gebaeudewert = kaufpreis * gebaeudewert_faktor
    
    # AfA Betrag pro Jahr (2% linear)
    afa_betrag = gebaeudewert * 0.02
    
    # Steuererstattung (ungefähr)
    steuer_vorteil = afa_betrag * (steuersatz_prozent / 100)
    
    return afa_betrag, steuer_vorteil, gebaeudewert

def check_15_prozent_grenze(kaufpreis, bodenwert_anteil_prozent, geplante_renovierung):
    """
    Prüft, ob die Renovierungskosten (netto) die 15%-Grenze in den ersten 3 Jahren sprengen.
    Falls ja, können die Kosten nicht sofort abgesetzt werden.
    """
    gebaeudewert = kaufpreis * ((100 - bodenwert_anteil_prozent) / 100)
    limit_15_prozent = gebaeudewert * 0.15
    
    ueberschritten = geplante_renovierung > limit_15_prozent
    rest_budget = limit_15_prozent - geplante_renovierung
    
    return ueberschritten, limit_15_prozent, rest_budget

def berechne_cashflow_detail(kaufpreis, nebenkosten, kaltmiete_jahr, bewirtschaftung_jahr, kredit_zins_prozent, eigenkapital_anteil_prozent):
    """
    Berechnet den detaillierten Cashflow in Euro für die Ausgabe der Zwischenschritte.
    """
    gesamt_invest = kaufpreis + nebenkosten
    eigenkapital = gesamt_invest * (eigenkapital_anteil_prozent / 100)
    fremdkapital = gesamt_invest - eigenkapital
    
    zinsen_euro = fremdkapital * (kredit_zins_prozent / 100)
    reinertrag = kaltmiete_jahr - bewirtschaftung_jahr
    
    # Cashflow vor Steuern (Reinertrag - Zinsen)
    cashflow_vor_steuer = reinertrag - zinsen_euro
    
    ek_rendite_genau = (cashflow_vor_steuer / eigenkapital) * 100 if eigenkapital > 0 else 0
    
    return {
        "kaltmiete": kaltmiete_jahr,
        "bewirtschaftung": bewirtschaftung_jahr,
        "zinsen": zinsen_euro,
        "fremdkapital": fremdkapital,
        "eigenkapital": eigenkapital,
        "cashflow": cashflow_vor_steuer,
        "ek_rendite": ek_rendite_genau
    }

# --- PARAMETER EINSTELLUNG (Hier Werte ändern) ---

if __name__ == "__main__":
    ZIEL_RENDITE = 3.0          # Gewünschte Rendite in %
    MONATSMIETE = 1035.00       # Zukünftige Miete (nach Erhöhung)

    # Kaufnebenkosten Bayern
    MAKLER = 3.57               # Mit MwSt
    GRUNDERWERB = 3.50          # Bayern
    NOTAR = 2.00                # Geschätzt

    # --- BERECHNUNG AUSFÜHREN ---

    kaufpreis, gesamt_invest, kosten = berechne_maximalen_kaufpreis(
        MONATSMIETE, 
        ZIEL_RENDITE, 
        MAKLER, 
        GRUNDERWERB, 
        NOTAR
    )

    # --- ERGEBNIS AUSGABE ---

    print(f"--- KALKULATION FÜR STARNBERG ---")
    print(f"Ziel-Rendite:             {ZIEL_RENDITE} %")
    print(f"Monatsmiete (Soll):       {MONATSMIETE:.2f} €")
    print(f"-----------------------------------")
    print(f"Maximales Gesamtinvest:   {gesamt_invest:,.2f} €  (Das dürfen Sie 'All-In' ausgeben)")
    print(f"Davon Kaufnebenkosten:   -{kosten:,.2f} €  (ca. {MAKLER+GRUNDERWERB+NOTAR}%)")
    print(f"-----------------------------------")
    print(f"MAXIMALER ANGEBOTSPREIS:  {kaufpreis:,.2f} €")
    print(f"-----------------------------------")

    # Vergleich zum aktuellen Preis
    aktueller_preis = 469000
    differenz = aktueller_preis - kaufpreis
    prozent_zu_teuer = (differenz / kaufpreis) * 100

    print(f"\nVergleich:")
    print(f"Aktueller Listenpreis:    {aktueller_preis:,.2f} €")
    print(f"Differenz (zu teuer):     {differenz:,.2f} € (+{prozent_zu_teuer:.1f} %)")