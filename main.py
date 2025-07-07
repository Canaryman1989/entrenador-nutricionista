from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="NutriCoach Pro – API",
    description="API para cálculo de calorías.",
    version="1.0.0",
    openapi_tags=[
        {"name": "Cálculo", "description": "Cálculo de calorías"}
    ]
)

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos
class DatosUsuario(BaseModel):
    sexo: str
    edad: int
    peso: float
    altura: float
    nivel_actividad: int
    objetivo: str

# Función de cálculo
def calcular_calorias(sexo: str, edad: int, peso: float, altura: float, nivel_actividad: int, objetivo: str):
    if sexo.lower() == "masculino":
        tmb = 10 * peso + 6.25 * altura - 5 * edad + 5
    else:
        tmb = 10 * peso + 6.25 * altura - 5 * edad - 161

    factores = {
        1: 1.2,
        2: 1.375,
        3: 1.55,
        4: 1.725,
        5: 1.9
    }

    factor = factores.get(nivel_actividad, 1.2)
    tdee = tmb * factor

    if objetivo == "definicion":
        calorias_objetivo = tdee - 500
    elif objetivo == "volumen":
        calorias_objetivo = tdee + 500
    else:
        calorias_objetivo = tdee

    return {
        "TMB": round(tmb, 2),
        "TDEE": round(tdee, 2),
        "calorias_objetivo": round(calorias_objetivo, 2)
    }

# Endpoint principal
@app.post("/calcular", tags=["Cálculo"])
def calcular(datos: DatosUsuario):
    return calcular_calorias(
        sexo=datos.sexo,
        edad=datos.edad,
        peso=datos.peso,
        altura=datos.altura,
        nivel_actividad=datos.nivel_actividad,
        objetivo=datos.objetivo
    )
