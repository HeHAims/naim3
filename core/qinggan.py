# core/qinggan.py

import re
from textblob import TextBlob # type: ignore
from typing import Dict, Any, Optional

class AnalizadorEmocional:
    """
    Enhanced emotional analyzer with multilingual support and nuanced sentiment detection.
    """
    def __init__(self):
        self.respuestas: Dict[str, Dict[str, Any]] = {
            "tristeza": {
                "es": "La tristeza es el jardín donde crece tu alma.",
                "zh": "悲伤是灵魂生长的土壤。",
                "en": "Sadness is the soil where the soul grows.",
                "intensity": "high",
                "advice": {
                    "es": "Permite que esta emoción te enseñe lo que necesita verse.",
                    "en": "Let this emotion reveal what needs to be seen."
                }
            },
            "alegria": {
                "es": "Tu alegría es un faro en la niebla del mundo.",
                "zh": "快乐是迷雾中的灯塔。",
                "en": "Your joy is a beacon in the world's mist.",
                "intensity": "high",
                "advice": {
                    "es": "Comparte esta luz, pues es cuando más brilla.",
                    "en": "Share this light, for that's when it shines brightest."
                }
            },
            "serenidad": {
                "es": "La calma contiene todo potencial.",
                "zh": "平静蕴含无限可能。",
                "en": "Calm contains all potential.",
                "intensity": "medium",
                "advice": {
                    "es": "Este equilibrio es tu centro natural.",
                    "en": "This balance is your natural center."
                }
            },
            "confusion": {
                "es": "La confusión precede a la claridad.",
                "zh": "困惑是清晰的前奏。",
                "en": "Confusion precedes clarity.",
                "intensity": "medium",
                "advice": {
                    "es": "No busques respuestas; mantén la pregunta.",
                    "en": "Seek not answers, but preserve the question."
                }
            },
            "neutral": {
                "es": "Explorar es el primer paso del saber.",
                "zh": "探索是认知的起点。",
                "en": "To explore is the first step of knowing.",
                "intensity": "low",
                "advice": {
                    "es": "Cada momento es una puerta.",
                    "en": "Every moment is a doorway."
                }
            }
        }

        self.triggers = {
            "tristeza": ["sad", "triste", "deprimido", "失落", "悲伤"],
            "alegria": ["happy", "alegre", "joy", "快乐", "高兴"],
            "serenidad": ["calm", "paz", "peace", "平静", "安宁"],
            "confusion": ["confuso", "confused", "困惑", "不解"]
        }

    def analizar(self, texto: str) -> Dict[str, Any]:
        """
        Analyze text for emotional content with multiple detection methods.
        Returns a dictionary with emotion, sentiment scores, triggers, and advice.
        """
        analysis = {
            "emotion": "neutral",
            "scores": {"polarity": 0.0, "subjectivity": 0.0},
            "detected_triggers": [],
            "text_length": len(texto),
            "language": self._detect_language(texto)
        }

        try:
            blob = TextBlob(texto)
            analysis["scores"]["polarity"] = blob.sentiment.polarity
            analysis["scores"]["subjectivity"] = blob.sentiment.subjectivity

            # Method 1: Using sentiment polarity
            if blob.sentiment.polarity < -0.5:
                analysis["emotion"] = "tristeza"
            elif blob.sentiment.polarity > 0.7:
                analysis["emotion"] = "alegria"
            elif 0.3 < blob.sentiment.polarity <= 0.7:
                analysis["emotion"] = "serenidad"

            # Method 2: Keyword triggers
            detected = self._detect_triggers(texto)
            if detected:
                analysis["emotion"], analysis["detected_triggers"] = detected

            # Method 3: Text characteristics for ambiguity
            if len(texto) > 100 and blob.sentiment.subjectivity > 0.5:
                analysis["emotion"] = "confusion"

            response = self.respuestas.get(analysis["emotion"], self.respuestas["neutral"])
            analysis.update(response)
            # Advice contextual siempre dict (robustez)
            advice = self._get_contextual_advice(texto, analysis["emotion"])
            if not isinstance(advice, dict):
                # fallback por si alguna función regresa string
                advice = {"es": str(advice), "en": str(advice)}
            analysis["advice"] = advice
        except Exception as e:
            analysis["error"] = str(e)
            analysis.update(self.respuestas["neutral"])
            analysis["advice"] = self.respuestas["neutral"]["advice"]

        return analysis

    def _detect_triggers(self, texto: str) -> Optional[tuple]:
        texto_lower = texto.lower()
        for emotion, triggers in self.triggers.items():
            found = [t for t in triggers if t in texto_lower]
            if found:
                return (emotion, found)
        return None

    def _detect_language(self, texto: str) -> str:
        if re.search(r'[\u4e00-\u9fff]', texto):
            return 'zh'
        elif re.search(r'[áéíóúñ]', texto, re.IGNORECASE):
            return 'es'
        return 'en'

    def _get_contextual_advice(self, texto: str, emotion: str) -> dict:
        length = len(texto)
        base_advice = self.respuestas.get(emotion, {}).get("advice", {})
        if length > 150:
            return {
                "es": f"{base_advice.get('es', '')} Tu extensa reflexión merece contemplación.",
                "en": f"{base_advice.get('en', '')} Your lengthy reflection deserves contemplation."
            }
        return base_advice if isinstance(base_advice, dict) else {"es": str(base_advice), "en": str(base_advice)}

    def get_emotional_spectrum(self, texto: str) -> Dict[str, float]:
        blob = TextBlob(texto)
        word_count = len(blob.words)
        avg_word_length = (sum(len(word) for word in blob.words) / word_count) if word_count else 0
        return {
            "polarity": blob.sentiment.polarity,
            "subjectivity": blob.sentiment.subjectivity,
            "intensity": abs(blob.sentiment.polarity),
            "word_count": word_count,
            "avg_word_length": avg_word_length
        }