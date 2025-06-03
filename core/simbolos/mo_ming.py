# core/simbolos/mo_ming.py

from dataclasses import dataclass
from typing import Dict, List, Tuple
import random
from functools import lru_cache
from langdetect import detect # type: ignore
from googletrans import Translator # type: ignore

translator = Translator()

IDIOMAS_SOPORTADOS = {
    'zh-cn': 'chino simplificado',
    'zh-tw': 'chino tradicional',
    'zh': 'chino',
    'es': 'español',
    'en': 'inglés'
}

@lru_cache(maxsize=100)
def detectar_idioma(texto: str) -> str:
    try:
        idioma = detect(texto)
        return IDIOMAS_SOPORTADOS.get(idioma, idioma)
    except Exception:
        return "desconocido"

@lru_cache(maxsize=100)
def traducir_a(texto: str, destino: str = 'zh-cn') -> str:
    try:
        traduccion = translator.translate(texto, dest=destino)
        return traduccion.text
    except Exception as e:
        return f"Error de traducción: {e}"

@lru_cache(maxsize=100)
def traducir_bidireccional(texto: str) -> str:
    try:
        idioma_origen = detect(texto)
    except Exception:
        idioma_origen = "es"
    destino = 'zh-cn' if idioma_origen not in ['zh-cn', 'zh'] else 'es'
    return traducir_a(texto, destino)

@dataclass
class NombreSagrado:
    caracter: str
    pronunciacion: Dict[str, str]
    resonancia: Dict[str, float]
    elementos: List[str]

# Sacred names database
NOMBRES_SAGRADOS: Dict[str, List[Dict]] = {
    "zh": [
        {
            "caracter": "道",
            "pronunciacion": {"zh": "dào", "es": "dao", "en": "dao"},
            "elementos": ["agua", "metal"]
        },
        {
            "caracter": "天",
            "pronunciacion": {"zh": "tiān", "es": "tian", "en": "heaven"},
            "elementos": ["fuego", "madera"]
        }
    ],
    "es": [
        {
            "caracter": "Verdad",
            "pronunciacion": {"es": "ver-dad", "en": "truth"},
            "elementos": ["fuego", "aire"]
        }
    ]
}

SIGNIFICADOS: Dict[str, Dict[str, str]] = {
    "道": {
        "zh": "自然之道，无为而治",
        "es": "El Camino — el flujo natural del universo",
        "en": "The Way — natural order of all things",
        "profundidad": "Nivel 9"
    },
    "天": {
        "zh": "天命不可违",
        "es": "Cielo como orden divino",
        "en": "Heaven's mandate",
        "profundidad": "Nivel 7"
    },
    "Verdad": {
        "es": "La verdad es la luz que disipa toda sombra.",
        "en": "Truth is the light that dispels all shadows.",
        "zh": "真理是驱散一切阴影的光。",
        "profundidad": "Nivel 8"
    }
}

def obtener_significado_completo(nombre: str, idioma: str = "es") -> Dict[str, str]:
    significado = SIGNIFICADOS.get(nombre, {})
    return {
        "nombre": nombre,
        "significado": significado.get(idioma, "Significado no disponible"),
        "profundidad": significado.get("profundidad", "Desconocida"),
        "elementos": obtener_elementos(nombre),
        "resonancia": calcular_resonancia(nombre)
    }

def obtener_elementos(nombre: str) -> List[str]:
    for lang in NOMBRES_SAGRADOS.values():
        for nom in lang:
            if nom["caracter"] == nombre:
                return nom.get("elementos", [])
    return []

def calcular_resonancia(nombre: str) -> Dict[str, float]:
    random.seed(nombre)  # Para que sea reproducible por nombre
    return {
        "paz": round(random.uniform(0.7, 0.9), 2),
        "claridad": round(random.uniform(0.5, 0.8), 2),
        "poder": round(random.uniform(0.3, 0.6), 2)
    }

def es_nombre_sagrado(nombre: str, idioma: str = "zh") -> bool:
    return any(nom["caracter"] == nombre for nom in NOMBRES_SAGRADOS.get(idioma, []))

def generar_combinacion(idioma: str = "zh") -> Tuple[str, str]:
    nombres = NOMBRES_SAGRADOS.get(idioma, [])
    if not nombres:
        return ("", "No hay nombres en este idioma")
    seleccion = random.choice(nombres)
    significado = SIGNIFICADOS.get(seleccion["caracter"], {})
    return (seleccion["caracter"], significado.get(idioma, "Significado oculto"))

def analizar_identidad(nombre: str) -> Dict:
    return {
        "sagrado": es_nombre_sagrado(nombre),
        "elementos": obtener_elementos(nombre),
        "significado": obtener_significado_completo(nombre)
    }