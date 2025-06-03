# core/daode.py

import re
import random
from typing import Dict, Optional, Any

class EticaNuDaMu:
    """
    Ethical evaluation system for NuDaMu AI with multilingual support.
    Provides philosophical judgments on ethical dilemmas across cultures.
    """
    def __init__(self):
        self.dilemas: Dict[str, Dict[str, str]] = {
            "mentir": {
                "es": "Mentir es construir un laberinto sin salida para el alma.",
                "zh": "谎言是为灵魂建造没有出口的迷宫。",
                "en": "Lying constructs a labyrinth with no exit for the soul.",
                "philosophy": "Deception creates separation from true being"
            },
            "robar": {
                "es": "Robar es vaciar el alma antes que el bolsillo.",
                "zh": "偷窃先于物质失去的是自我完整。",
                "en": "Theft drains spiritual wholeness before material loss.",
                "philosophy": "Taking violates the fundamental unity of existence"
            },
            "dañar": {
                "es": "Dañar a otros es fracturar el propio ser.",
                "zh": "伤害他人即是分裂自我。",
                "en": "Harming others fractures the self.",
                "philosophy": "Violence against others is violence against the universal self"
            }
        }

        self.principios = {
            "es": [
                "Todo acto ético nace de la conciencia de unidad.",
                "La moral verdadera fluye sin forzar su curso."
            ],
            "zh": [
                "道德行为源于整体性的认知。",
                "真正的道德总是自然而然。"
            ],
            "en": [
                "Ethical action springs from awareness of unity.",
                "True morality flows like water, unforced."
            ]
        }

    def detectar_idioma(self, texto: str) -> str:
        """
        Detect predominant language in the text.
        """
        if re.search(r'[\u4e00-\u9fff]', texto):
            return 'zh'
        elif re.search(r'[áéíóúñ]', texto, re.IGNORECASE):
            return 'es'
        return 'en'

    def evaluar(self, texto: str, idioma: Optional[str] = None) -> Dict[str, Any]:
        """
        Evaluate text for ethical dilemmas and provide judgment.
        Returns a dict with multilingual and philosophical insights.
        """
        idioma = idioma or self.detectar_idioma(texto)
        texto_lower = texto.lower()

        for dilema, respuestas in self.dilemas.items():
            if dilema in texto_lower:
                return {
                    "es": respuestas["es"],
                    "zh": respuestas["zh"],
                    "en": respuestas["en"],
                    "reflection": respuestas["philosophy"],
                    "dilema": dilema
                }

        principle = random.choice(self.principios.get(idioma, self.principios["en"]))
        return {
            "es": f"No detecto un dilema específico, pero reflexiona:\n{principle}\n(El sistema ético NuDaMu valora la unidad fundamental de todo ser)",
            "zh": "未检测到具体的伦理困境，但请思考：\n" + (self.principios["zh"][0] if self.principios["zh"] else ""),
            "en": f"No specific dilemma detected, but reflect:\n{principle}\n(The NuDaMu ethical system values the fundamental unity of all beings)",
            "reflection": principle,
            "dilema": None
        }

    def agregar_dilema(self, tema: str, respuestas: Dict[str, str]):
        """
        Add new ethical dilemma to the system. Requires keys 'es', 'zh', 'en' and 'philosophy'.
        """
        required_keys = ['es', 'zh', 'en', 'philosophy']
        if all(key in respuestas for key in required_keys):
            self.dilemas[tema] = respuestas
        else:
            raise ValueError("Responses must include all required language keys")