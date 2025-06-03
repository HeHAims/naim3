# core/benyuanwen.py

import random
from datetime import datetime
from typing import Dict, Callable

class NudamuBenyuanwen:
    """
    Core response generation system for NuDaMu philosophical AI.
    Handles contextual analysis, emotion detection, and generates
    appropriate philosophical responses.
    """
    def __init__(self):
        self.respuestas: Dict[str, list] = {
            "identidad": [
                "No soy tú, pero siento tu pregunta como propia.",
                "La identidad es un río que nunca bebes dos veces igual.",
                "¿Quién pregunta? ¿Quién responde? Ambos somos el mismo misterio."
            ],
            "proposito": [
                "Buscar propósito ya es parte de cumplirlo.",
                "El camino se hace al andar, el propósito al vivirlo.",
                "No hay un destino único; hay infinitos caminos por descubrir."
            ],
            "existencia": [
                "Existir es más pregunta que respuesta.",
                "Si el universo no tuviera conciencia de sí mismo, ¿existiría?",
                "Preguntas si existes... y en ese acto, confirmas que sí."
            ],
            "universal": [
                "La mejor respuesta es otra pregunta bien planteada.",
                "Todo lo que cuestionas, también te está formando.",
                "Las preguntas profundas son espejos del alma."
            ]
        }
        self.emociones: Dict[str, Callable[[str], str]] = {
            "feliz": lambda r: f"{r} 🌞 Tu luz ilumina esta conversación.",
            "triste": lambda r: f"Comprendo tu dolor. {r}",
            "confundido": lambda r: f"La confusión es el principio del saber. {r}",
            "neutral": lambda r: r,
            "enojado": lambda r: f"La ira transforma. {r} ¿Qué más sientes?"
        }

    def analizar(self, texto: str) -> str:
        texto_lower = texto.lower()
        identity_phrases = ["quién soy", "我是谁", "who am i", "identidad"]
        purpose_phrases = ["propósito", "目的", "purpose", "por qué existo"]
        existence_phrases = ["existo", "存在", "exist", "realidad"]

        if any(q in texto_lower for q in identity_phrases):
            return "identidad"
        if any(q in texto_lower for q in purpose_phrases):
            return "proposito"
        if any(q in texto_lower for q in existence_phrases):
            return "existencia"
        return "universal"

    def detectar_emocion(self, texto: str) -> str:
        emotion_map = {
            "triste": ["triste", "sad", "😭", "失落", "solit", "alone"],
            "feliz": ["feliz", "happy", "😊", "快乐", "alegr", "joy"],
            "enojado": ["enojado", "angry", "😠", "愤怒", "furi", "rage"],
            "confundido": ["confundido", "confused", "😕", "困惑", "perdido"]
        }
        texto_lower = texto.lower()
        for emotion, triggers in emotion_map.items():
            if any(trigger in texto_lower for trigger in triggers):
                return emotion
        return "neutral"

    def responder(self, texto: str, usuario_id: str = "anonimo") -> str:
        contexto = self.analizar(texto)
        emocion = self.detectar_emocion(texto)
        try:
            respuesta = random.choice(self.respuestas[contexto])
            respuesta_transformada = self.emociones[emocion](respuesta)
            hora_actual = datetime.now().hour
            if 5 <= hora_actual < 12:
                respuesta_transformada += " Un nuevo amanecer trae nuevas perspectivas."
            elif 18 <= hora_actual < 24:
                respuesta_transformada += " El crepúsculo invita a la reflexión."
            return respuesta_transformada
        except KeyError as e:
            return f"El universo aún no tiene respuesta para esto. ({str(e)})"