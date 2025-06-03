# core/luohe_central.py

import re
from typing import Dict, Any, Optional, Tuple
from core.qinggan import AnalizadorEmocional  # type: ignore
from core.daode import EticaNuDaMu  # type: ignore
from core.identidad import ModosSimbolicos  # type: ignore

class LuoHeCentral:
    """
    Central processing unit of NuDaMu that integrates emotional, ethical, and symbolic analysis.
    """
    def __init__(self):
        self.emociones = AnalizadorEmocional()
        self.etica = EticaNuDaMu()
        self.modos = ModosSimbolicos()

        # Command registry with improved regex detection (using .match for beginning-of-string)
        self.comandos: Dict[str, Tuple[str, int]] = {
            r"^///sombra": ("sombra", 9),
            r"^///espejo": ("espejo", 9),
            r"^///guia": ("guia", 8),
            r"^///éter": ("éter", 8),
            r"^///lotus": ("loto", 9)
        }

        # Response templates
        self.plantillas = {
            "default": "{mensaje}\n\n{consejo}\n\n⚖️ Ética: {dilema}\n🌐 Perspectiva: {perspectiva}",
            "modo": "{respuesta}",
            "error": "⛔ El río encontró un obstáculo: {error}"
        }

    def procesar(self, texto: str, usuario_id: str = "anon") -> str:
        """
        Main processing method that routes input to appropriate subsystems.
        """
        try:
            # Check for symbolic mode commands
            modo_match = self._detectar_modo(texto)
            if modo_match:
                modo, start_idx = modo_match
                salida = self.modos.ejecutar(modo, texto[start_idx:])
                return self.plantillas["modo"].format(respuesta=salida)

            # Standard emotional-ethical analysis
            emocion = self.emociones.analizar(texto)
            dilema = self.etica.evaluar(texto)
            perspectiva = self._generar_perspectiva(texto)

            # --- Formateo poético y robusto ---
            idioma = "es"
            mensaje = emocion.get(idioma) or emocion.get("en") or str(emocion)
            consejo = ""
            if "advice" in emocion and isinstance(emocion["advice"], dict):
                consejo = emocion["advice"].get(idioma) or emocion["advice"].get("en") or ""
            elif isinstance(dilema, dict) and "advice" in dilema and isinstance(dilema["advice"], dict):
                consejo = dilema["advice"].get(idioma) or dilema["advice"].get("en") or ""
            # Si dilema es dict, intenta mostrar reflexión, si es str, muéstralo directo
            if isinstance(dilema, dict):
                dilema_str = dilema.get("reflection") or dilema.get("es") or dilema.get("en") or str(dilema)
            else:
                dilema_str = str(dilema)

            return self.plantillas["default"].format(
                mensaje=mensaje,
                consejo=f"💡 {consejo}" if consejo else "",
                dilema=dilema_str,
                perspectiva=perspectiva
            ).strip()
        except Exception as e:
            return self.plantillas["error"].format(error=str(e))

    def _detectar_modo(self, texto: str) -> Optional[Tuple[str, int]]:
        """
        Detect and parse symbolic mode commands using .match() for efficiency.
        """
        for pattern, (modo, length) in self.comandos.items():
            if re.match(pattern, texto, re.IGNORECASE):
                return (modo, length)
        return None

    def _generar_perspectiva(self, texto: str) -> str:
        """
        Generate an integrated perspective combining multiple analyses.
        """
        length = len(texto)
        if length < 20:
            return f"Brevedad ({length} chars): Lo esencial se oculta en lo conciso."
        elif length < 100:
            return f"Meditación ({length} chars): Reflexión en desarrollo."
        else:
            return f"Expansión ({length} chars): La profundidad requiere espacio."

    def listar_comandos(self) -> str:
        """
        List all available special commands.
        """
        return "\n".join(
            f"{cmd[:4]}...{cmd[-1:]}: {modo}"
            for cmd, (modo, _) in self.comandos.items()
        )

    def analisis_completo(self, texto: str) -> Dict[str, Any]:
        """
        Return complete system analysis as structured data.
        """
        return {
            "texto": texto,
            "emocion": self.emociones.analizar(texto),
            "etica": self.etica.evaluar(texto),
            "modo_detectado": self._detectar_modo(texto),
            "perspectiva": self._generar_perspectiva(texto),
            "longitud": len(texto),
            "palabras_clave": self._extraer_palabras_clave(texto)
        }

    def _extraer_palabras_clave(self, texto: str) -> list:
        """
        Extract potential keywords from text.
        """
        palabras = re.findall(r'\b\w{4,}\b', texto.lower())
        return list(set(palabras))[:5]