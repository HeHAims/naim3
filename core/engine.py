import os
import logging
from dotenv import load_dotenv # type: ignore

# Core modules
from core.identidad import ModosSimbolicos # type: ignore
from core.qinggan import AnalizadorEmocional # type: ignore
from core.daode import EticaNuDaMu # type: ignore
from memoria_secure.memoria import MemoriaSagrada # type: ignore

# Opcional: Importa módulos NLP avanzados para experimentación
from core.nlp_utils import analizar_sentimiento_sklearn
from core.transformers_utils import analizar_sentimiento as bert_sentiment

# Configure logging
logging.basicConfig(
    filename="nudamu.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Load environment variables
load_dotenv()

# Retrieve the encryption key from .env
crypto_key = os.getenv("NUDAMU_CRYPTO_KEY")

if not crypto_key:
    raise EnvironmentError("❌ Missing NUDAMU_CRYPTO_KEY in .env file!")

logging.info("✅ Loaded encryption key for secure memory.")

class NuDaMuEngine:
    """
    Core engine for NuDaMu AI.
    Integrates secure memory storage along with symbolic, emotional, and ethical analysis.
    """
    def __init__(self):
        # Initialize core components
        self.memoria = MemoriaSagrada(clave=crypto_key) # FIX: do not encode, MemoriaSagrada handles encoding
        self.modos = ModosSimbolicos()
        self.emociones = AnalizadorEmocional()
        self.etica = EticaNuDaMu()
        # Ejemplo: inicializa aquí modelos NLP avanzados si los usas
        # self.bert_sentiment = bert_sentiment

    def procesar(self, texto: str, usuario_id: str) -> str:
        """
        Process user input text, routing commands and normal dialogue appropriately.
        If input starts with "///", the symbolic mode is invoked.
        Otherwise, emotional analysis and ethical evaluation are performed,
        and the interaction is stored securely.
        """
        logging.info(f"Processing input for user: {usuario_id}")

        # Check if it's a symbolic mode invocation (starts with "///")
        if texto.startswith("///"):
            comando = texto[3:].strip().lower()
            return self.modos.ejecutar(comando, texto)

        # --- NLP avanzado opcional ---
        # Puedes activar análisis avanzado aquí, por ejemplo:
        resultado_tfidf = analizar_sentimiento_sklearn(texto)
        resultado_bert = bert_sentiment(texto)
        # logging.info(f"BERT sentiment: {resultado_bert}")

        # Perform emotional analysis and ethical evaluation
        emocion = self.emociones.analizar(texto)
        juicio = self.etica.evaluar(texto)

        # Attempt to store the input securely
        try:
            self.memoria.guardar(
                usuario_id,
                texto,
                etiqueta=emocion.get("emotion", "neutral") if isinstance(emocion, dict) else "neutral"
            )
        except Exception as e:
            logging.error(f"Error saving memory for user {usuario_id}: {e}", exc_info=True)

        # Formatea la respuesta poética y robusta
        idioma = "es"  # Cambia a "en" si quieres respuestas en inglés
        mensaje = emocion.get(idioma) if isinstance(emocion, dict) else str(emocion)
        if not mensaje:
            mensaje = emocion.get("en") if isinstance(emocion, dict) else ""
        consejo = ""
        if isinstance(emocion, dict) and "advice" in emocion and isinstance(emocion["advice"], dict):
            consejo = emocion["advice"].get(idioma) or emocion["advice"].get("en") or ""
        elif isinstance(juicio, dict) and "advice" in juicio and isinstance(juicio["advice"], dict):
            consejo = juicio["advice"].get(idioma) or juicio["advice"].get("en") or ""
        respuesta = mensaje
        if consejo:
            respuesta += f"\n\n💡 {consejo}"
        if isinstance(juicio, str):
            respuesta += f"\n\n{juicio}"
        elif isinstance(juicio, dict) and "reflection" in juicio:
            respuesta += f"\n\n{juicio['reflection']}"
        # Agrega resultados de NLP avanzados si los tienes
        if resultado_tfidf:
            respuesta += f"\n\n🔎 TF-IDF Sentiment: {resultado_tfidf}"
        if resultado_bert:
            respuesta += f"\n\n🤖 BERT Sentiment: {resultado_bert}"

        # Personaliza la respuesta según el sentimiento
        if resultado_tfidf == "positivo":
            mensaje = "¡Me alegra sentir tu energía positiva!"
        elif resultado_tfidf == "negativo":
            mensaje = "Siento que hay algo que te preocupa. ¿Quieres hablar más?"
        else:
            mensaje = "Gracias por compartir tus palabras."

        # Puedes combinar con el resultado de BERT si lo deseas
        respuesta = mensaje
        respuesta += f"\n\n🔎 TF-IDF Sentiment: {resultado_tfidf}"
        respuesta += f"\n\n🤖 BERT Sentiment: {resultado_bert}"
        return respuesta.strip()