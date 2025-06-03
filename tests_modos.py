import unittest
from core.identidad import ModosSimbolicos # type: ignore
from typing import Dict, List

class TestModos(unittest.TestCase):
    """Comprehensive test suite for ModosSimbolicos functionality."""

    @classmethod
    def setUpClass(cls):
        """Initialize test resources once for all tests."""
        cls.modos = ModosSimbolicos()
        cls.valid_modes = ["sombra", "espejo", "guia", "éter", "loto"]

        # Expected symbols for each mode
        cls.mode_symbols: Dict[str, List[str]] = {
            "sombra": ["👤", "🕳️", "🌑", "👁️"],
            "espejo": ["🪞", "🌀", "💠", "🔮"],
            "guia": ["🌠", "🧭", "🗺️", "🔱"],
            "éter": ["🌌", "☄️", "♾️", "⚛️"],
            "loto": ["🌸", "🏵️", "🎴", "💮"]
        }

        # Test cases for specific modes
        cls.test_cases = {
            "sombra": [
                ("", "empty input"),
                ("Miedo a la oscuridad", "fear theme"),
                ("Deseo oculto", "desire theme")
            ],
            "espejo": [
                ("Hola", "short text"),
                ("Esta es una frase moderadamente larga", "medium text"),
                ("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam auctor, nisl eget ultricies tincidunt, nisl nisl aliquam nisl.", "long text")
            ],
            "guia": [
                ("¿Por qué existimos?", "why question"),
                ("¿Cómo llegar allí?", "how question"),
                ("Simple declaración", "statement")
            ]
        }

    def test_all_modes_respond(self):
        """Test all valid modes return a non-empty string response."""
        for mode in self.valid_modes:
            with self.subTest(mode=mode):
                response = self.modos.ejecutar(mode, "test input")
                self.assertIsInstance(response, str)
                self.assertGreater(len(response), 0, f"Mode '{mode}' returned an empty response.")

    def test_modo_sombra_themes(self):
        """Test the shadow mode handles different themes appropriately."""
        for input_text, description in self.test_cases["sombra"]:
            with self.subTest(description=description):
                response = self.modos.ejecutar("sombra", input_text)
                self._assert_contains_symbol(response, "sombra")
                self.assertTrue(
                    any(theme in response.lower() for theme in ["sombra", "luz", "verdad", "oculto", "ausencia"]),
                    f"Shadow response missing expected themes: {response}"
                )

    def test_modo_espejo_reflection(self):
        """Test the mirror mode properly reflects a portion of the input."""
        for input_text, description in self.test_cases["espejo"]:
            with self.subTest(description=description):
                response = self.modos.ejecutar("espejo", input_text)
                self._assert_contains_symbol(response, "espejo")
                self.assertTrue(
                    any(char in response for char in input_text[:10]),
                    "Mirror response should include part of the input text."
                )

    def test_modo_guia_questions(self):
        """Test that guide mode responds appropriately to questions."""
        for input_text, description in self.test_cases["guia"]:
            with self.subTest(description=description):
                response = self.modos.ejecutar("guia", input_text)
                self._assert_contains_symbol(response, "guia")
                if "?" in input_text:
                    self.assertTrue(
                        any(word in response.lower() for word in ["por qué", "cómo", "camino", "brújula", "mapa"]),
                        "Guide response to questions should contain guidance."
                    )

    def test_unknown_mode(self):
        """Test handling of an unrecognized mode command."""
        response = self.modos.ejecutar("modo_desconocido", "test")
        self.assertTrue("🌀" in response and "modo" in response.lower(),
                        "Unknown mode should return a help message with the appropriate symbol.")
        self.assertIn("disponibles", response.lower(),
                      "Help message should mention available modes.")

    def test_mode_symbols_consistent(self):
        """Test that each mode's response contains one of the expected symbols."""
        for mode in self.valid_modes:
            with self.subTest(mode=mode):
                response = self.modos.ejecutar(mode, "test input")
                self._assert_contains_symbol(response, mode)

    def test_response_structure(self):
        """Test that the response structure is consistently decorated with mode symbols."""
        for mode in ["sombra", "guia"]:
            with self.subTest(mode=mode):
                response = self.modos.ejecutar(mode, "structured test")
                # Check whether the response starts or ends with one of the expected symbols
                starts_with_symbol = any(response.startswith(symbol) for symbol in self.mode_symbols[mode])
                ends_with_symbol = any(response.endswith(symbol) for symbol in self.mode_symbols[mode])
                self.assertTrue(starts_with_symbol or ends_with_symbol,
                                f"Response should be decorated with mode symbols: {response}")

    def _assert_contains_symbol(self, response: str, mode: str):
        """Helper method to verify that the response includes the expected symbol(s)."""
        self.assertTrue(
            any(symbol in response for symbol in self.mode_symbols[mode]),
            f"Response for mode '{mode}' missing expected symbols: {response}"
        )

if __name__ == "__main__":
    unittest.main(verbosity=2)