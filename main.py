from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from calculadora_calorias import calcular_calorias
from generar_informe_pdf import generar_pdf, generar_informe_simple
import uuid

app = FastAPI(
    title="NutriCoach Pro – API",
    description="API de cálculo de calorías, generación de informes PDF y asistencia nutricional.",
    version="1.0.0"
)

# MODELOS DE ENTRADA
class DatosUsuario(BaseModel):
    sexo: str = Field(..., pattern="^(h|m)$", example="h")
    edad: int = Field(..., ge=13, le=99, example=31)
    peso: float = Field(..., gt=30, lt=250, example=67.5)
    altura: float = Field(..., gt=100, lt=250, example=165)
    nivel_actividad: int = Field(..., ge=1, le=5, example=3)
    objetivo: str = Field(..., pattern="^(definir|mantener|volumen)$", example="mantener")

class DatosInformeCalculo(DatosUsuario):
    nombre: str = Field(..., example="Yefry")

# ENDPOINTS
@app.post("/calcular", tags=["Cálculo"])
def calcular_endpoint(datos: DatosUsuario):
    resultado = calcular_calorias(**datos.dict())
    return {
        **datos.dict(),
        **resultado
    }

@app.post("/informe", tags=["Informe"])
def generar_pdf_calculo(datos: DatosInformeCalculo):
    resultado = calcular_calorias(
        sexo=datos.sexo,
        edad=datos.edad,
        peso=datos.peso,
        altura=datos.altura,
        nivel_actividad=datos.nivel_actividad,
        objetivo=datos.objetivo
    )

    buffer = generar_informe_simple(
        nombre=datos.nombre,
        tmb=resultado["TMB"],
        tdee=resultado["TDEE"],
        calorias_objetivo=resultado["calorias_objetivo"]
    )

    filename = f"informe_{datos.nombre.lower().replace(' ', '_')}.pdf"
    return StreamingResponse(buffer, media_type="application/pdf", headers={
        "Content-Disposition": f"attachment; filename={filename}"
    })
