# core/identidad.py

import random
import re
from typing import Dict, Callable

class ModosSimbolicos:
    """
    Symbolic interaction modes for NuDaMu's philosophical dialogue system.
    Provides different metaphorical lenses for user interaction.
    """
    def __init__(self):
        # Map mode names to their handler methods
        self.modos: Dict[str, Callable[[str], str]] = {
            "sombra": self._modo_sombra,
            "espejo": self._modo_espejo,
            "guia": self._modo_guia,
            "éter": self._modo_eter,
            "loto": self._modo_loto  # New mode
        }

        # Symbols used for decorating responses
        self.symbols = {
            "sombra": ["👤", "🕳️", "🌑", "👁️"],
            "espejo": ["🪞", "🌀", "💠", "🔮"],
            "guia": ["🌠", "🧭", "🗺️", "🔱"],
            "éter": ["🌌", "☄️", "♾️", "⚛️"],
            "loto": ["🌸", "🏵️", "🎴", "💮"]
        }

    def ejecutar(self, comando: str, texto: str) -> str:
        """
        Execute the requested symbolic mode.
        """
        comando = comando.lower().strip()
        if comando in self.modos:
            try:
                respuesta = self.modos[comando](texto)
                return self._decorar_respuesta(comando, respuesta)
            except Exception as e:
                return f"🌀 El modo falló: {str(e)}"
        sugerencias = random.sample(list(self.modos.keys()), min(3, len(self.modos)))
        return (f"🌀 Modo no reconocido. Prueba con:\n"
                f"///{', ///'.join(sugerencias)}\n"
                f"(Hay {len(self.modos)} modos disponibles)")

    def _decorar_respuesta(self, modo: str, respuesta: str) -> str:
        symbol = random.choice(self.symbols.get(modo, ["🌀"]))
        return f"{symbol} {respuesta} {symbol}"

    def _modo_sombra(self, texto: str) -> str:
        themes = {
            "amor": "El amor que niegas crece en las sombras.",
            "miedo": "Los miedos no nombrados gobiernan en silencio.",
            "deseo": "Lo que más deseas ya te posee."
        }
        texto_lower = texto.lower()
        detected = next((t for t in themes if re.search(rf"\b{t}\b", texto_lower)), None)
        return themes.get(detected, random.choice([
            "Lo no dicho clama desde las sombras.",
            "La verdad duele menos que su ausencia.",
            "Cada luz proyecta su sombra correspondiente."
        ]))

    def _modo_espejo(self, texto: str) -> str:
        length = len(texto)
        analysis = [
            ("corto", "Lo breve contiene lo esencial.", 20),
            ("medio", "El equilibrio busca su centro.", 50),
            ("largo", "La profundidad requiere espacio.", 100)
        ]
        size = next((a for a in analysis if length <= a[2]), analysis[-1])
        return (f"Reflejo {size[0]}: '{texto[:30]}...'\n"
                f"{size[1]} [Caracteres: {length}]")

    def _modo_guia(self, texto: str) -> str:
        questions = {
            r"\bpor qué\b": "Las preguntas de 'por qué' buscan causas, las de 'cómo' caminos.",
            r"\bquién\b": "La identidad es una brújula, no un destino.",
            r"\bcómo\b": "El método emerge cuando el propósito es claro."
        }
        texto_lower = texto.lower()
        matched = next((msg for p, msg in questions.items() if re.search(p, texto_lower)), None)
        return matched or random.choice([
            "A veces las preguntas son faros disfrazados.",
            "Navegar requiere tanto mapa como brújula.",
            "Todo camino comienza con un paso suspendido."
        ])

    def _modo_eter(self, texto: str) -> str:
        cosmic_scales = [
            ("palabra", "Las palabras son constelaciones efímeras."),
            ("frase", "Las frases orbitan como sistemas solares."),
            ("pensamiento", "Los pensamientos son galaxias en formación.")
        ]
        texto_lower = texto.lower()
        return next((msg for key, msg in cosmic_scales if key in texto_lower),
                    "El éter contiene todas las posibilidades.")

    def _modo_loto(self, texto: str) -> str:
        stages = [
            "El loto crece a través del lodo.",
            "Los pétalos se abren a su propio ritmo.",
            "La flor perfecta contiene tanto belleza como decadencia."
        ]
        return " → ".join(stages) + f"\nTu texto '{texto[:15]}...' es semilla potencial."

    def listar_modos(self) -> str:
        descripciones = {
            "sombra": "Revela aspectos ocultos",
            "espejo": "Reflejo simbólico",
            "guia": "Orientación filosófica",
            "éter": "Perspectiva cósmica",
            "loto": "Transformación gradual"
        }
        return "\n".join(f"///{modo}: {desc}" for modo, desc in descripciones.items())