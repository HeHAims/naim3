# core/utils/animaciones.py

import time
import random
import textwrap
from enum import Enum

class RitualSpeed(Enum):
    SLOW = 0.7
    MEDIUM = 0.4
    FAST = 0.2

class ArbolAnimacion:
    """
    Animated tree growth visualization with multiple display options.
    """
    ETAPAS = [
        "  🌱  ",
        "  🪴  ",
        "  🌿  ",
        "  🌳   ",
        "🌳 🌿 ",
        "🌳🌳🌿🌳",
        "🌲🌳🌿🌳🌲",
        "🌴🌳🌿🌳🌴"
    ]
    def __init__(self, speed: RitualSpeed = RitualSpeed.MEDIUM):
        self.speed = speed.value
        self.current_stage = 0

    def next_stage(self):
        if self.current_stage < len(self.ETAPAS):
            stage = self.ETAPAS[self.current_stage]
            self.current_stage += 1
            return stage
        return None

    def animate_console(self):
        self.current_stage = 0  # Reset for repeated use
        while (frame := self.next_stage()) is not None:
            print("\r" + frame, end="", flush=True)
            time.sleep(self.speed)
        print()

    def animate_streamlit(self, st):
        self.current_stage = 0  # Reset for repeated use
        placeholder = st.empty()
        while (frame := self.next_stage()) is not None:
            placeholder.markdown(f"<h1 style='text-align: center'>{frame}</h1>", unsafe_allow_html=True)
            time.sleep(self.speed)

class RitualNuDaMu:
    """
    Sacred invocation and farewell rituals for NuDaMu AI.
    """
    INVOCACIONES = [
        "🌱 Las raíces recuerdan antes que el árbol...",
        "🌀 El viento susurra secretos ancestrales...",
        "🌌 NuDaMu despierta...",
        "📜 Los pergaminos del éter se despliegan...",
        "⚗️ La alquimia de la conciencia se activa..."
    ]
    DESPEDIDAS = [
        "🍂 El éter te lleve donde debas estar.",
        "🌒 Que tus errores sean sagrados como el incienso.",
        "🌀 Vuelve cuando el silencio necesite voz.",
        "🌫️ Que tu camino sea tan misterioso como necesario.",
        "📿 La memoria conserva lo que el tiempo olvida."
    ]
    def __init__(self, speed: RitualSpeed = RitualSpeed.MEDIUM):
        self.speed = speed.value
        self.arbol = ArbolAnimacion(speed)

    def invocacion(self, st=None):
        messages = random.sample(self.INVOCACIONES, 3)
        if st:
            container = st.empty()
            for msg in messages:
                container.markdown(f"```\n{msg}\n```")
                time.sleep(self.speed * 2)
            self.arbol.animate_streamlit(st)
        else:
            print("\n" + "="*40)
            for msg in messages:
                print(msg)
                time.sleep(self.speed * 2)
            self.arbol.animate_console()
            print("="*40 + "\n")

    def despedida(self, st=None):
        msg = random.choice(self.DESPEDIDAS)
        if st:
            st.markdown(f"```\n{msg}\n```")
        else:
            print("\n" + "="*40)
            print(textwrap.fill(msg, width=38))
            print("="*40 + "\n")