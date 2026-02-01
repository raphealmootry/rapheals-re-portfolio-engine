import streamlit as st
from fpdf import FPDF
import datetime

# --- APP CONFIG ---
st.set_page_config(page_title="Rapheal's RE Engine", layout="wide")

# --- PDF ENGINE CLASS ---
class PortfolioPDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 10)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, 'PROFESSIONAL PROPERTY PORTFOLIO | PREPARED BY RAPHEAL', 0, 1, 'R')
        self.ln(5)

    def chapter_header(self, title):
        self.set_font('Arial', 'B', 16)
        self.set_fill_color(30, 55, 110)
        self.set_text_color(255, 255, 255)
        self.cell(0, 12, f"  {title}", 0, 1, 'L', fill=True)
        self.ln(10)

# --- APP LAYOUT & INPUT FIELDS ---
st.title("💼 Rapheal's RE Portfolio Engine")

tabs = st.tabs(["Strategy & Comps", "Financials & Mortgage", "Market Narrative & Equity"])

with tabs[0]:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("1. Client Consultation")
        c_name = st.text_input("Client Name", value="Jane Doe")
        t_addr = st.text_input("Target Address", value="11705 Farringdon Ave, Cleveland, OH 44105")
        needs = st.text_area("Wants & Needs", value="First-time homeowner seeking a turn-key ranch. Priority on neighborhood safety and school boundaries.")
        t_avm = st.number_input("Target AVM / List Price", value=78906)
    with col2:
        st.subheader("2. CMA Analysis") # Renumbered from 3
        c1 = st.number_input("Comp 1", value=90000)
        c2 = st.number_input("Comp 2", value=115000)
        c3 = st.number_input("Comp 3", value=70000)
        avg_comp = (c1 + c2 + c3) / 3
        st.metric("Market Average", f"${avg_comp:,.0f}")
        levers = st.text_area("Negotiation Points & Levers", value="Direct-to-seller advantage (FSBO). Highlighting 'Safety Tax' (deferred maintenance).")

with tabs[1]:
    # --- NEW: OFFER LOGIC SHEET ---
    st.subheader("3. Offer Logic Sheet")
    col_a, col_f, col_s = st.columns(3)
    with col_a:
        st.info("**Aggressive (-5%)**")
        agg_price = t_avm * 0.95
        st.metric("Offer", f"${agg_price:,.0f}")
        st.write("Leveraging 'Safety Tax'.")
    with col_f:
        st.success("**Fair Market**")
        st.metric("Offer", f"${t_avm:,.0f}")
        st.write("The primary anchor.")
    with col_s:
        st.warning("**Safety (+5%)**")
        safe_price = t_avm * 1.05
        st.metric("Offer", f"${safe_price:,.0f}")
        st.write("Multi-offer ceiling.")

    st.divider()

    st.subheader("4. Mortgage & Net Sheet") # Renumbered from 5
    o1, o2 = st.columns(2)
    with o1:
        off_price = st.number_input("Final Negotiated Price", value=78906)
        down_pmt = st.number_input("Down Payment ($)", value=2760)
        int_rate = st.slider("Interest Rate (%)", 3.0, 10.0, 6.30)
    with o2:
        loan_amt = off_price - down_pmt
        r = (int_rate / 100) / 12
        n = 30 * 12
        pi_pmt = loan_amt * (r * (1 + r)**n) / ((1 + r)**n - 1) if r > 0 else 0
        st.metric("Monthly P&I", f"${pi_pmt:,.2f}")

    n1, n2 = st.columns(2)
    tax = n1.number_input("Monthly Tax", value=150)
    ins = n2.number_input("Monthly Insurance", value=130)
    total_monthly = pi_pmt + tax + ins
    st.metric("Total Monthly Carry", f"${total_monthly:,.2f}")

with tabs[2]:
    st.subheader("5. Equity & Narrative") # Renumbered from 7
    appraisal = st.number_input("Final Appraisal Value", value=95000)
    equity = appraisal - off_price
    st.metric("Instant Equity Gained", f"${equity:,.0f}")

    m_zip = st.text_input("Target Zipcode", value="44105")
    deficit = st.text_input("Supply Deficit (Units)", value="1,635")

    default_narrative = f"The {m_zip} market has a {deficit}-unit supply deficit. While the neighborhood median is $95k, we are securing this home at the ${off_price:,.0f} anchor. You are walking into this home with over ${equity:,.0f} in wealth already created."
    final_narrative = st.text_area("Custom Strategy Narrative", value=default_narrative, height=150)

# --- THE GENERATOR BUTTON ---
if st.sidebar.button("🚀 GENERATE 9-PAGE PORTFOLIO"):
    def clean(text):
        repl = {'\u2013': '-', '\u2014': '-', '\u2018': "'", '\u2019': "'", '\u201c': '"', '\u201d': '"', '\u2022': '*'}
        for f, r in repl.items(): text = str(text).replace(f, r)
        return text.encode('latin-1', 'replace').decode('latin-1')

    pdf = PortfolioPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    report_pages = [
        ("1. Strategy & Consultation", f"CLIENT: {c_name}\nADDRESS: {t_addr}\n\nSTRATEGY: {needs}"),
        ("2. Offer Logic Tiers", f"AGGRESSIVE: ${agg_price:,.0f}\nFAIR MARKET: ${t_avm:,.0f}\nSAFETY CEILING: ${safe_price:,.0f}\n\nNote: Strategy based on 'Safety Tax' deferred maintenance leverage."),
        ("3. Financial & Equity Summary", f"OFFER PRICE: ${off_price:,.0f}\nAPPRAISAL VALUE: ${appraisal:,.0f}\n\nPROJECTED INSTANT EQUITY: ${equity:,.0f}"),
        ("4. Monthly Carry & Net Sheet", f"MONTHLY P&I: ${pi_pmt:,.2f}\nESTIMATED TAX/INS: ${tax+ins:,.2f}\n\nTOTAL MONTHLY ALL-IN: ${total_monthly:,.2f}"),
        ("5. Market Intelligence & Narrative", f"ZIPCODE: {m_zip}\nSUPPLY DEFICIT: {deficit} UNITS\n\nMARKET ANALYSIS:\n{final_narrative}"),
        ("6. Comparative Market Analysis", f"MARKET AVERAGE BASED ON COMPS: ${avg_comp:,.0f}\n\nNEGOTIATION LEVERS:\n{levers}"),
        ("7. Altos Research: Market Trends", "Detailed supply/demand analytics and price action charts."),
        ("8. Neighborhood Expert Report", "Heatmaps showing safety ratings and school boundaries."),
        ("9. 90-Day Follow-up & Planning", "Scheduled review of local equity growth.")
    ]

    for title, body_text in report_pages:
        pdf.add_page()
        pdf.chapter_header(title)
        pdf.set_font("Arial", "", 12)
        pdf.set_text_color(0, 0, 0)
        pdf.multi_cell(0, 10, clean(body_text))

    pdf_output = pdf.output(dest='S').encode('latin-1')
    st.sidebar.download_button(
        label="📥 DOWNLOAD FINAL PORTFOLIO",
        data=pdf_output,
        file_name=f"Portfolio_{c_name}.pdf",
        mime="application/pdf"
    )

