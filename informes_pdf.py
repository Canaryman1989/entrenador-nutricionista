from fpdf import FPDF
from io import BytesIO


def generar_informe_simple(nombre: str, tmb: float, tdee: float, calorias_objetivo: float) -> BytesIO:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.set_title("Informe Nutricional")

    pdf.cell(200, 10, txt="Informe Nutricional 🥗 NutriCoach", ln=True, align="C")
    pdf.ln(10)

    pdf.cell(200, 10, txt=f"Nombre: {nombre}", ln=True)
    pdf.cell(200, 10, txt=f"TMB: {tmb:.2f} kcal", ln=True)
    pdf.cell(200, 10, txt=f"TDEE: {tdee:.2f} kcal", ln=True)
    pdf.cell(200, 10, txt=f"Calorías Objetivo: {calorias_objetivo:.2f} kcal", ln=True)

    buffer = BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    return buffer
