#!/usr/bin/env python3

import os
import logging
from hashlib import md5
from datetime import datetime
from dotenv import load_dotenv # type: ignore

from core.luohe_central import LuoHeCentral
from core.utils.animaciones import RitualNuDaMu, RitualSpeed

# Configure logging
logging.basicConfig(
    filename="nudamu.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Load environment variables
load_dotenv()

# Retrieve encryption key from .env
crypto_key = os.getenv("NUDAMU_CRYPTO_KEY")

if not crypto_key:
    raise EnvironmentError("❌ Missing NUDAMU_CRYPTO_KEY in .env file!")

logging.info("✅ Loaded encryption key for secure memory.")

class NuDaMuSession:
    """
    Manages user interaction session with state tracking.
    """
    def __init__(self):
        self.central = LuoHeCentral()
        self.ritual = RitualNuDaMu(RitualSpeed.MEDIUM)
        self.interaction_count = 0
        self.user_id = self._generate_user_id()

    def _generate_user_id(self) -> str:
        """Generate a unique user ID."""
        return md5(str(datetime.now().timestamp()).encode()).hexdigest()[:8]

    def run(self):
        """Run the interactive session."""
        self.ritual.invocacion()
        print("\n🌌 Type your message (or 'exit' to quit):")
        print("💡 Try special commands like: ///sombra, ///espejo\n")
        
        while True:
            try:
                user_input = self._get_input()
                if self._should_exit(user_input):
                    break
                self.interaction_count += 1
                self._process_input(user_input)
            except KeyboardInterrupt:
                print("\n🌀 Session interrupted by user.")
                break
            except Exception as e:
                print(f"\n⚠️ Error: {str(e)}")
                continue
        
        self._end_session()

    def _get_input(self) -> str:
        """Get user input safely."""
        try:
            return input("👁️  > ").strip()
        except EOFError:
            return "exit"

    def _should_exit(self, input_text: str) -> bool:
        """Check if user wants to exit."""
        return input_text.lower() in ["exit", "salir", "quit"]

    def _process_input(self, user_input: str):
        """Process input and provide appropriate response."""
        response = self.central.procesar(user_input, self.user_id)
        print(f"\n🧠 NuDaMu responds:\n{response}\n")
        
        # Trigger symbolic animation periodically
        if self.interaction_count % 3 == 0:
            self.ritual.arbol.animate_console()

    def _end_session(self):
        """End the session gracefully."""
        print(f"\n📊 Session Summary:")
        print(f"- Interactions: {self.interaction_count}")
        print(f"- User ID: {self.user_id}")
        self.ritual.despedida()

if __name__ == "__main__":
    try:
        session = NuDaMuSession()
        session.run()
    except Exception as e:
        print(f"Critical error: {str(e)}")
        logging.error(f"Critical failure in NuDaMuSession: {str(e)}", exc_info=True)