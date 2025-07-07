from fpdf import FPDF
import os
from datetime import datetime

BASE = os.path.dirname(__file__)
FONT_REG = os.path.join(BASE, "DejaVuSans.ttf")
FONT_BOLD = os.path.join(BASE, "DejaVuSans-Bold.ttf")

class PDFInforme(FPDF):
    def header(self):
        self.set_font("DejaVu", "B", 16)
        self.cell(0, 10, "Informe Nutricional y de Entrenamiento", ln=True, align="C")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("DejaVu", "", 10)
        self.cell(0, 10, f"Página {self.page_no()}", align="C")

    def cuerpo(self, nombre, objetivo, dieta, entrenamiento):
        self.set_font("DejaVu", "", 12)
        self.multi_cell(0, 10, f"Cliente: {nombre}")
        self.multi_cell(0, 10, f"Objetivo: {objetivo}")
        self.ln(5)
        self.set_font("DejaVu", "B", 12)
        self.cell(0, 10, "Dieta recomendada:", ln=True)
        self.set_font("DejaVu", "", 12)
        self.multi_cell(0, 10, dieta)
        self.ln(5)
        self.set_font("DejaVu", "B", 12)
        self.cell(0, 10, "Entrenamiento sugerido:", ln=True)
        self.set_font("DejaVu", "", 12)
        for e in entrenamiento:
            self.multi_cell(0, 10, f"• {e}")
        self.ln(5)

def generar_pdf(datos_cliente: dict, ruta_salida: str) -> str:
    """
    Genera un informe PDF y lo guarda en ruta_salida.
    datos_cliente debe incluir: nombre, objetivo, dieta, entrenamiento (list[str])
    """
    pdf = PDFInforme()
    pdf.add_font("DejaVu", "", FONT_REG, uni=True)
    pdf.add_font("DejaVu", "B", FONT_BOLD, uni=True)
    pdf.add_page()
    pdf.cuerpo(
        datos_cliente.get("nombre", "Cliente"),
        datos_cliente.get("objetivo", ""),
        datos_cliente.get("dieta", ""),
        datos_cliente.get("entrenamiento", []),
    )
    pdf.output(ruta_salida)
    return ruta_salida
