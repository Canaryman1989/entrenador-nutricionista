from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from calculadora_calorias import calcular_calorias

from informes_pdf import generar_informe_simple


app = FastAPI(
    title="NutriCoach Pro – API",
    description="API para cálculo de calorías y generación de informes personalizados",
    version="1.0.0"
)

# ✅ Modelo base
class DatosUsuario(BaseModel):
    sexo: str
    edad: int
    peso: float
    altura: float
    nivel_actividad: int
    objetivo: str

# ✅ Endpoint /calcular
@app.post("/calcular", tags=["Cálculo"])
def calcular_endpoint(datos: DatosUsuario):
    resultado = calcular_calorias(
        sexo=datos.sexo,
        edad=datos.edad,
        peso=datos.peso,
        altura=datos.altura,
        nivel_actividad=datos.nivel_actividad,
        objetivo=datos.objetivo
    )
    return {
        "nombre": getattr(datos, "nombre", "usuario"),
        **resultado
    }

# ✅ Modelo extendido para informe
class DatosInformeCalculo(DatosUsuario):
    nombre: str

# ✅ Endpoint /informe
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
