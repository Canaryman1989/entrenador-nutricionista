from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from calculadora_calorias import calcular_calorias
from generar_informe_pdf import generar_pdf
import os
import uuid

app = FastAPI(
    title="NutriCoach Pro – API",
    description="API de cálculo de calorías, generación de dietas e informes PDF para asistentes GPT de salud.",
    version="1.0.0"
)

class DatosUsuario(BaseModel):
    nombre: str = Field(..., example="Juan Pérez")
    sexo: str = Field(..., pattern="^(h|m)$", example="h")
    edad: int = Field(..., ge=13, le=99, example=31)
    peso: float = Field(..., gt=30, lt=250, example=67.5)
    altura: float = Field(..., gt=100, lt=250, example=165)
    nivel_actividad: int = Field(..., ge=1, le=5, example=3)
    objetivo: str = Field(..., pattern="^(definir|mantener|volumen)$", example="mantener")

class DatosInforme(DatosUsuario):
    dieta: str = Field(..., example="Desayuno: avena...\nComida: ensalada...")
    entrenamiento: list[str] = Field(..., example=["Sentadillas", "Zancadas", "Peso muerto"])

@app.post("/calcular", tags=["Cálculo"])
def calcular_endpoint(datos: DatosUsuario):
    resultado = calcular_calorias(**datos.dict())
    return {
        "nombre": datos.nombre,
        **resultado
    }

@app.post("/informe", tags=["Informe"])
def generar_informe_endpoint(datos: DatosInforme):
    resultado = calcular_calorias(**datos.dict())
    nombre_archivo = f"informe_{uuid.uuid4().hex[:8]}.pdf"
    ruta = os.path.join("informes", nombre_archivo)
    os.makedirs("informes", exist_ok=True)

    datos_cliente = {
        "nombre": datos.nombre,
        "objetivo": datos.objetivo,
        "dieta": datos.dieta,
        "entrenamiento": datos.entrenamiento
    }

    generar_pdf(datos_cliente, ruta)
    return FileResponse(ruta, media_type="application/pdf", filename=nombre_archivo)
