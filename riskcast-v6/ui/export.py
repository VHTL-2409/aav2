# ui/export.py
"""Report generation (PDF, Excel) for RISKCAST v5.5."""
from fpdf import FPDF
import pandas as pd
import io
from config.constants import ICC_PACKAGES


class ReportGenerator:
    """Generate PDF and Excel reports from analysis results."""
    
    def generate_pdf(self, result, params) -> bytes:
        """Generate PDF report with analysis summary."""
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=10)
        
        # Header
        pdf.set_font("Arial", "B", 20)
        pdf.cell(0, 15, "RISKCAST v5.5 — Enterprise Risk Assessment", ln=1, align="C")
        
        # Metadata
        pdf.set_font("Arial", size=10)
        pdf.cell(0, 5, f"Ngay bao cao: {pd.Timestamp.now().strftime('%d/%m/%Y %H:%M')}", ln=1)
        pdf.cell(0, 5, f"Nguoi dung: RISKCAST System", ln=1)
        pdf.cell(0, 5, f"Muc tieu: {getattr(params, 'priority_profile', 'Tieu chuan')}", ln=1)
        pdf.ln(5)
        
        # Top Recommendation
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "GOI Y TOT NHAT", ln=1)
        
        top_row = result.results.iloc[0]
        pdf.set_font("Arial", size=11)
        pdf.cell(0, 8, f"Cong ty: {top_row.get('Company', 'Unknown')}", ln=1)
        pdf.cell(0, 8, f"Goi ICC: {top_row.get('ICC Package', 'N/A')}", ln=1)
        pdf.cell(0, 8, f"Diem TOPSIS: {top_row.get('TOPSIS Score', 0):.4f}", ln=1)
        pdf.cell(0, 8, f"Chi phi: ${top_row.get('Cost', 0):,.0f}", ln=1)
        pdf.cell(0, 8, f"Tin cay: {top_row.get('Confidence', 0):.2f}", ln=1)
        pdf.ln(5)
        
        # Top 10 Options
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "TIEN TOP 10 PHUONG AN", ln=1)
        
        pdf.set_font("Arial", size=9)
        top10 = result.results.head(10)
        for idx, (_, row) in enumerate(top10.iterrows(), 1):
            pdf.cell(20, 8, f"{idx}.", border=1)
            pdf.cell(60, 8, str(row.get('Company', ''))[:20], border=1)
            pdf.cell(40, 8, str(row.get('ICC Package', ''))[:15], border=1)
            pdf.cell(40, 8, f"${row.get('Cost', 0):,.0f}", border=1)
            pdf.cell(30, 8, f"{row.get('TOPSIS Score', 0):.3f}", border=1, ln=1)
        
        pdf.ln(5)
        
        # Risk Metrics
        if hasattr(result, 'var') and hasattr(result, 'cvar'):
            pdf.set_font("Arial", "B", 14)
            pdf.cell(0, 10, "PHAC TICH RUI RO TAI CHINH", ln=1)
            
            pdf.set_font("Arial", size=11)
            pdf.cell(0, 8, f"VaR 95%: ${result.var:,.0f}", ln=1)
            pdf.cell(0, 8, f"CVaR 95%: ${result.cvar:,.0f}", ln=1)
        
        # Footer
        pdf.ln(10)
        pdf.set_font("Arial", "I", 8)
        pdf.cell(0, 5, "RISKCAST v5.5 | Streamlit Enterprise Edition | Generated automatically", ln=1, align="C")
        
        # Return PDF as bytes
        buffer = io.BytesIO()
        pdf_data = pdf.output(dest='S')
        if isinstance(pdf_data, str):
            buffer.write(pdf_data.encode('latin-1'))
        else:
            buffer.write(pdf_data)
        buffer.seek(0)
        return buffer.getvalue()
    
    def generate_excel(self, result, params) -> bytes:
        """Generate Excel report with results and weights."""
        buffer = io.BytesIO()
        
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            # Sheet 1: Results
            results_df = result.results.copy()
            results_df.to_excel(writer, sheet_name="Ket qua", index=False)
            
            # Sheet 2: Weights
            if hasattr(result, 'weights'):
                weights_df = pd.DataFrame({
                    'Tieu chi': result.weights.index,
                    'Trong so': result.weights.values
                })
                weights_df.to_excel(writer, sheet_name="Trong so", index=False)
            
            # Sheet 3: Risk Metrics (if available)
            if hasattr(result, 'var') and hasattr(result, 'cvar'):
                risk_df = pd.DataFrame({
                    'Metric': ['VaR 95%', 'CVaR 95%'],
                    'Value': [result.var, result.cvar]
                })
                risk_df.to_excel(writer, sheet_name="Rui ro", index=False)
        
        buffer.seek(0)
        return buffer.getvalue()