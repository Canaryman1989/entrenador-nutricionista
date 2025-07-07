def calcular_tmb(sexo: str, peso: float, altura: float, edad: int) -> float:
    """
    Calcula el metabolismo basal (TMB) usando la fórmula de Mifflin-St Jeor.
    """
    if sexo.lower() == "h":
        return 10 * peso + 6.25 * altura - 5 * edad + 5
    elif sexo.lower() == "m":
        return 10 * peso + 6.25 * altura - 5 * edad - 161
    else:
        raise ValueError("Sexo debe ser 'h' (hombre) o 'm' (mujer)")

def calcular_tdee(tmb: float, nivel_actividad: int) -> float:
    """
    Calcula el gasto energético total (TDEE) usando un factor de actividad.
    """
    factores = {
        1: 1.2,   # Sedentario
        2: 1.375, # Ligera actividad
        3: 1.55,  # Moderada
        4: 1.725, # Intensa
        5: 1.9    # Muy intensa
    }
    if nivel_actividad not in factores:
        raise ValueError("Nivel de actividad debe estar entre 1 y 5")
    return tmb * factores[nivel_actividad]

def ajustar_calorias(tdee: float, objetivo: str) -> float:
    """
    Ajusta el TDEE según el objetivo: definición, mantenimiento o volumen.
    """
    objetivo = objetivo.lower()
    if objetivo == "definir":
        return tdee - 500
    elif objetivo == "mantener":
        return tdee
    elif objetivo == "volumen":
        return tdee + 500
    else:
        raise ValueError("Objetivo debe ser 'definir', 'mantener' o 'volumen'")

def calcular_calorias(sexo: str, edad: int, peso: float, altura: float, nivel_actividad: int, objetivo: str) -> dict:
    """
    Calcula TMB, TDEE y calorías objetivo a partir de los datos del usuario.
    """
    tmb = calcular_tmb(sexo, peso, altura, edad)
    tdee = calcular_tdee(tmb, nivel_actividad)
    calorias = ajustar_calorias(tdee, objetivo)

    return {
        "TMB": round(tmb, 2),
        "TDEE": round(tdee, 2),
        "calorias_objetivo": round(calorias, 2)
    }
