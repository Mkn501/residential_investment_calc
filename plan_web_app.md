# Project Log & History

## Phase 1: Core Logic & Notebook (Completed)
*   **Goal**: Analyze a real estate deal in Starnberg (negative cashflow, high appreciation potential).
*   **Implementation**:
    *   Created `max_re_price.py` with reusable financial functions.
    *   **Yields**: Status Quo vs. Rent Potential (Cap Limit).
    *   **Leverage**: Added dynamic Bond Comparison (Equity Yield vs. Risk-free Rate) and Detailed Cashflow.
    *   **Tax/Renovation**: Implemented AfA (Land Value deduction) & 15% Renovation Limit check.
    *   **Due Diligence**: Added checklist for WEG, Rules, Energy, and Tenants.
    *   **Output**: Developed an educational Jupyter Notebook (`max_re_price.ipynb`) acting as an "Investment Dossier".

## Phase 2: Web App Planning (Current)
*   **Goal**: Convert logic into a shareable Streamlit Web App.
*   **Discussions & Decisions**:
    *   **Localization**: Must support German & English.
    *   **PDF Export**: Feature to download results as a formal Dossier.
    *   **Rent Control**: Added toggle for 15% (Mietpreisbremse) vs. 20% rent cap.
    *   **UX**: Request for "Expandable Explanations" to preserve the educational value of the notebook in a clean dashboard interface.

---

# Implementation Plan - Real Estate Web App

The goal is to make the "Investment Dossier" accessible on the web. The most efficient way to do this with Python is using **Streamlit**. It turns data scripts into shareable web apps in minutes.

## User Review Required
> [!NOTE]
> I will create a single file `app.py` that imports your existing logic from `max_re_price.py`. You can then run it locally, and I can explain how to deploy it (e.g., Streamlit Cloud).

## Proposed Changes

### [Web Application]

#### [NEW] [app.py](file:///Users/mkn501/Library/CloudStorage/GoogleDrive-minkngu@gmail.com/Meine%20Ablage/VS/RE/app.py)

Create a Streamlit application with the following sections:
1.  **Input Sidebar**: Central place for all parameters (Price, Rent, Interest Rate).
    *   **[NEW] Location Setting**: Toggle for "Rent Control Area" (Mietpreisbremse).
        *   If Active: Max increase 15% (Kappungsgrenze).
        *   If Inactive: Max increase 20%.
2.  **Dashboard (Main Area)**:
    *   **Status Quo**: Metrics for Current Yield (Net), Purchase Price, and *Dynamic Nebenkosten*.
    *   **Scenario**: Slider for "Rent Increase in 3 Years" (15% vs 20% cap).
    *   **Leverage & Cashflow**:
        *   Interactive chart: Equity Return vs. Loan Interest.
        *   **[NEW]** Detailed Cashflow Table (Income - Non-recoverable costs - Interest = Cashflow in €).
        *   **[NEW]** Bond Comparison breakdown (Equity Yield vs. Risk-free Rate).
    *   **Tax & Renovation (Steuern & Sanierung)**:
        *   Inputs: Land Value % (Bodenwert), Personal Tax Rate %, Renovation Budget.
        *   Outputs: AfA Tax Refund calculation & "15% Rule" Warning check.
    *   **Fair Price**: Reverse calculation from Target Yield to Max Offer Price.
    *   **Due Diligence**: Interactive Checklist for Soft Factors (WEG-Protokolle, Teilungserklärung, Heizung/GEG, Mieterstruktur).
    *   **[NEW] Contextual Explanations**: "Show Details" expanders for each section.
    *   **[NEW] Visual Aids**:
        *   **Traffic Lights 🚦**: Visual indicators for Yield (<2% Red), Cashflow (Neg Yellow), Renovation (OK Green).
        *   **Wealth Accumulation Chart**: Bar chart comparing "Cash out of pocket" vs. "Tenants paying off loan" (Net Wealth Delta).
        *   **Sensitivity Matrix**: Heatmap showing Yield changes if Interest Rate or Purchase Price varies.

3.  **[NEW] Features**:
    *   **Localization**: Toggle between German (DE) and English (EN).
    *   **PDF Export**: Button to download "Investment Dossier".
    *   **[NEW] Disclaimer**: Prominent footer stating "Educational Purpose Only. Investments at own risk."



### [Dependencies]

#### [NEW] [requirements.txt](file:///Users/mkn501/Library/CloudStorage/GoogleDrive-minkngu@gmail.com/Meine%20Ablage/VS/RE/requirements.txt)
*   `streamlit`
*   `pandas` (for charts/tables)
*   `matplotlib` (for charts)
*   `fpdf` (for PDF generation)

### Deployment (Free on Streamlit Cloud)

1.  **Push to GitHub**: Create a repo and push `app.py`, `max_re_price.py`, and `requirements.txt`.
2.  **Streamlit Cloud**: Sign up at [share.streamlit.io](https://share.streamlit.io).
3.  **Deploy**: Click "New App", select your repo, and click "Deploy".
4.  **Secrets**: If we use any keys (none planned), add them in Streamlit settings.

## Verification Plan

### Manual Verification
*   Run `streamlit run app.py` locally.
*   Interact with sliders and inputs to ensure calculations update in real-time.
*   Verify PDF export works.
*   Check Localization toggles.

## Phase 3: UX Refinement (Based on Alternative Design)
*   **Visual Hierarchy**: Create distinct visual blocks (Cards) for "Status Quo" vs "Potential" using `st.container` + colors.
*   **Direct Comparison**: Replace abstract charts with a simple "Property vs Bond" bar chart + explicit "Verdict" text (Green/Red).
*   **Fair Price Tab**: Implement the "Reverse Calculator" flow: Target Yield -> Fair Price -> "Overpayment" Warning.
*   **Input Grouping**: Group percentage inputs (Makler, Tax, Notary) horizontally to save space.
*   **Key Metrics**: significantly increase font size/visibilty for Net Cashflow & Yield.
