# streamlit_app.py
import os
import streamlit as st  # type: ignore
from dotenv import load_dotenv  # type: ignore
from datetime import datetime

# ¡PON ESTO AQUÍ!
st.set_page_config(
    page_title="NuDaMu Interface",
    page_icon="🌿",
    layout="wide"
)

from core.engine import NuDaMuEngine
from core.utils.animaciones import RitualNuDaMu, RitualSpeed
from memoria_secure.memoria import MemoriaSagrada
from core.simbolos.mo_ming import obtener_significado_completo

LANGS = {"Español": "es", "English": "en", "中文": "zh"}
RITUAL_SPEEDS = {
    "Slow": RitualSpeed.SLOW.value,    
    "Medium": RitualSpeed.MEDIUM.value,
    "Fast": RitualSpeed.FAST.value,
}

def initialize_session():
    if 'engine' not in st.session_state:
        try:
            load_dotenv()
            crypto_key = os.getenv("NUDAMU_CRYPTO_KEY")
            if not crypto_key or len(crypto_key.encode()) not in [16, 24, 32]:
                st.error("❌ Invalid/Missing NUDAMU_CRYPTO_KEY (needs 16/24/32 bytes)")
                st.stop()
            st.session_state.engine = NuDaMuEngine()
            st.session_state.memoria = MemoriaSagrada(crypto_key)  # type: ignore
            st.session_state.ritual = RitualNuDaMu(RitualSpeed.MEDIUM)
            st.session_state.user_id = "anon_" + datetime.now().strftime("%Y%m%d%H%M")
        except Exception as e:
            st.error(f"Initialization failed: {str(e)}")
            st.stop()

def render_sidebar():
    with st.sidebar:
        st.title("⚙️ NuDaMu Controls")
        lang_key = st.selectbox("🌍 Language", list(LANGS.keys()))
        st.session_state.lang = LANGS[lang_key]
        speed_key = st.select_slider("⏳ Ritual Speed", options=list(RITUAL_SPEEDS.keys()))
        st.session_state.ritual_speed = RITUAL_SPEEDS[speed_key]
        if st.button("🔍 View Recent Memories"):
            try:
                recuerdos = st.session_state.memoria.listar_recuerdos(st.session_state.user_id)
                with st.expander("🧠 Memory Vault"):
                    for r in recuerdos:
                        st.caption(r)
            except Exception as e:
                st.error(f"Memory access failed: {str(e)}")

def render_main_interface():
    st.title("🌌 NuDaMu v2.1")
    st.markdown("""
> *"What is remembered lives forever."*  
> — Sacred Codex
""")
    if st.button("🌀 Begin Invocation", help="Activate symbolic protocols"):
        with st.spinner("Awakening ancestral patterns..."):
            st.session_state.ritual.invocacion(st)
    with st.form("dialogue_form"):
        user_input = st.text_area("✍️ Your Question", placeholder="Ask or invoke (///sombra, ///guia)...", height=150)
        submitted = st.form_submit_button("🌠 Submit")
        if submitted and user_input.strip():
            process_input(user_input)

def process_input(user_input: str):
    with st.spinner("Consulting the symbolic matrix..."):
        try:
            if len(user_input) <= 3:
                for lang in LANGS.values():
                    if (
                        st.session_state.memoria
                        and hasattr(st.session_state.memoria, "es_nombre_sagrado")
                        and st.session_state.memoria.es_nombre_sagrado(user_input, lang)
                    ):
                        analisis = obtener_significado_completo(user_input, lang)
                        st.expander(f"📜 {user_input} Analysis").json(analisis)
                        return
            response = st.session_state.engine.procesar(user_input, st.session_state.user_id)
            if user_input.startswith("///sombra"):
                st.warning("Entering Shadow Realm...")
                st.image("simbolos/imagenes/sombra.png", width=300)
            st.markdown("### 🔮 Response")
            st.markdown(f"> {response}")
            if "🌌" in user_input:
                st.balloons()
                st.audio("simbolos/sonidos/eter.mp3")
        except Exception as e:
            st.error(f"Processing error: {str(e)}")
            st.session_state.ritual.despedida(st)

def main():
    initialize_session()
    render_sidebar()
    render_main_interface()
    st.markdown("---")
    st.caption("""
⚠️ Symbolic Interface v2.1 - Responses are poetic constructs, not factual advice.
🔐 Memory encryption: AES-256-GCM
""")

if __name__ == "__main__":
    main()