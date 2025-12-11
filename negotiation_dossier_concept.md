# Concept: The "Negotiation Dossier" PDF
*A data-driven document to justify your price offer to the seller.*

The goal is to move from a "Calculator Output" to a **"Professional Purchase Offer"**. It should look like an institutional investor analyzed the deal.

## Structure

### 1. Executive Summary (The "Deal at a Glance")
*   **Property**: [Address / Object Name]
*   **Asking Price**: 469.000 € (Status Quo)
*   **Current Yield**: **1.92%** (Net) 🔴
*   **Verdict**: *"At the current price, the property yields significantly less than a risk-free German Government Bond (2.3%)."*

### 2. Financial Analysis ("Why the price doesn't work")
*   **Cashflow Analysis**:
    *   Show that the property burns initially (first month) (-475€/month).
    *   Highlight that this negative cashflow destroys wealth compared to alternative investments.
*   **Interest Rate Reality**:
    *   "With interest rates at 3.8%, a 1.9% yield is mathematically unsustainable for any investor."

### 3. Due Diligence Findings ("The hidden costs")
*(This section auto-fills from the 'Due Diligence' tab if checked)*
*   **Identified Risks**:
    *   [x] Heating System renewal required shortly (GEG).
    *   [x] Windows need replacement (Common property).
    *   [x] Low Maintenance Reserve in the WEG.
*   *Narrative*: "These upcoming capital expenditures (CapEx) must be deducted from the purchase price."

### 4. Valuation & Fair Price Derivation
*   **Target Yield**: 3.5% (Market Standard for existing stock)
*   **Maximum Supportable Investment**: ~410.000 € (All-in)
*   **Less Closing Costs**: -35.000 €
*   **= Fair Market Value**: **375.000 €**

### 5. The Formal Offer
*   "Based on the required renovations and current interest rate environment, we are prepared to make a binding offer of:"
*   **370.000 €**
*   *Valid until: [Date]*

---
## Implementation Plan (Python/FPDF)
We will rewrite `create_pdf` to be a multi-page document:
1.  **Page 1**: Executive Summary & Financials (Charts).
2.  **Page 2**: Due Diligence Risks & Fair Price Calculation.
3.  **Page 3**: Formal Letter/Offer template.
