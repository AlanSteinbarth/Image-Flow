"""
Testy jednostkowe dla aplikacji ImageFlow
"""

import unittest
import tempfile
import os
from unittest.mock import patch, MagicMock, mock_open
import tkinter as tk
from tkinter import ttk

# Importy z głównej aplikacji
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from app import ImageFlow, ThemeManager, ToolTip, LoadingSpinner
except ImportError as e:
    print(f"Błąd importu: {e}")
    print("Upewnij się że uruchamiasz testy z głównego folderu projektu")
    sys.exit(1)


class TestThemeManager(unittest.TestCase):
    """Testy dla zarządzania motywami"""

    def setUp(self):
        self.root = tk.Tk()
        self.theme_manager = ThemeManager(self.root)

    def tearDown(self):
        self.root.destroy()

    def test_initial_theme_is_light(self):
        """Test czy domyślnie używany jest jasny motyw"""
        self.assertFalse(self.theme_manager.is_dark)

    def test_toggle_theme(self):
        """Test przełączania motywów"""
        initial_state = self.theme_manager.is_dark

        # Wyłącz animację w testach aby uniknąć segfault
        original_animate = self.theme_manager.animate_theme_change
        self.theme_manager.animate_theme_change = lambda: None

        self.theme_manager.toggle_theme()
        self.assertNotEqual(initial_state, self.theme_manager.is_dark)

        # Przywróć oryginalną metodę
        self.theme_manager.animate_theme_change = original_animate

    def test_register_widget(self):
        """Test rejestracji widgetów"""
        widget = tk.Label(self.root, text="Test")
        self.theme_manager.register_widget(widget, "label")

        self.assertIn((widget, "label"), self.theme_manager.widgets_to_update)

    def test_themes_contain_required_colors(self):
        """Test czy motywy zawierają wszystkie wymagane kolory"""
        required_colors = [
            "bg",
            "fg",
            "select_bg",
            "select_fg",
            "listbox_bg",
            "text_bg",
            "canvas_bg",
        ]

        for theme_name, theme in self.theme_manager.themes.items():
            for color in required_colors:
                self.assertIn(
                    color, theme, f"Brak koloru '{color}' w motywie '{theme_name}'"
                )


class TestImageFlowCore(unittest.TestCase):
    """Testy podstawowej funkcjonalności ImageFlow"""

    def setUp(self):
        self.root = tk.Tk()
        # Ukryj okno podczas testów
        self.root.withdraw()
        self.app = ImageFlow(self.root, testing_mode=True)

    def tearDown(self):
        self.root.destroy()

    def test_initialization(self):
        """Test czy aplikacja inicjalizuje się poprawnie"""
        self.assertIsInstance(self.app.theme_manager, ThemeManager)
        self.assertEqual(len(self.app.pliki_do_konwersji), 0)
        self.assertIsNotNone(self.app.folder_docelowy)

    @patch("os.path.isfile")
    def test_dodaj_pliki_valid_extensions(self, mock_isfile):
        """Test dodawania plików z prawidłowymi rozszerzeniami"""
        mock_isfile.return_value = True

        pliki = ["/test/image1.jpg", "/test/image2.png", "/test/image3.heic"]

        self.app.dodaj_pliki(pliki)
        self.assertEqual(len(self.app.pliki_do_konwersji), 3)

    @patch("os.path.isfile")
    def test_dodaj_pliki_invalid_extensions(self, mock_isfile):
        """Test ignorowania plików z nieprawidłowymi rozszerzeniami"""
        mock_isfile.return_value = True

        pliki = ["/test/document.pdf", "/test/file.txt", "/test/video.mp4"]

        self.app.dodaj_pliki(pliki)
        self.assertEqual(len(self.app.pliki_do_konwersji), 0)

    @patch("os.path.isfile")
    def test_dodaj_pliki_mixed_extensions(self, mock_isfile):
        """Test mieszanych rozszerzeń plików"""
        mock_isfile.return_value = True

        pliki = [
            "/test/image1.jpg",  # prawidłowy
            "/test/document.pdf",  # nieprawidłowy
            "/test/image2.png",  # prawidłowy
            "/test/file.txt",  # nieprawidłowy
        ]

        self.app.dodaj_pliki(pliki)
        self.assertEqual(len(self.app.pliki_do_konwersji), 2)

    def test_usun_z_listy(self):
        """Test usuwania plików z listy"""
        # Dodaj pliki
        self.app.pliki_do_konwersji = ["/test/img1.jpg", "/test/img2.png"]
        self.app.lista_plikow.insert(0, "img1.jpg")
        self.app.lista_plikow.insert(1, "img2.png")

        # Zaznacz pierwszy plik
        self.app.lista_plikow.selection_set(0)

        # Usuń zaznaczone
        self.app.usun_z_listy()

        self.assertEqual(len(self.app.pliki_do_konwersji), 1)
        self.assertEqual(self.app.pliki_do_konwersji[0], "/test/img2.png")

    def test_aktualizuj_jakosc_label(self):
        """Test aktualizacji etykiety jakości"""
        self.app.aktualizuj_jakosc_label("75")
        expected_text = "Jakość po konwersji pliku: 75%"
        self.assertEqual(self.app.jakosc_label.cget("text"), expected_text)

    @patch("os.access")
    def test_sprawdz_uprawnienia_zapisu_success(self, mock_access):
        """Test sprawdzania uprawnień - sukces"""
        with tempfile.TemporaryDirectory() as temp_dir:
            with patch("builtins.open", mock_open()) as mock_file:
                with patch("os.remove") as mock_remove:
                    result = self.app.sprawdz_uprawnienia_zapisu(temp_dir)
                    self.assertTrue(result)

    @patch("builtins.open")
    def test_sprawdz_uprawnienia_zapisu_failure(self, mock_open_func):
        """Test sprawdzania uprawnień - błąd"""
        mock_open_func.side_effect = PermissionError("Access denied")
        result = self.app.sprawdz_uprawnienia_zapisu("/forbidden/path")
        self.assertFalse(result)


class TestFileOperations(unittest.TestCase):
    """Testy operacji na plikach"""

    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.app = ImageFlow(self.root, testing_mode=True)

    def tearDown(self):
        self.root.destroy()

    def test_pobierz_domyslny_folder_exists(self):
        """Test pobierania domyślnego folderu gdy istnieje"""
        with patch("os.path.expanduser") as mock_expanduser:
            with patch("os.path.exists") as mock_exists:
                mock_expanduser.return_value = "/home/user"
                mock_exists.return_value = True

                folder = self.app.pobierz_domyslny_folder()
                self.assertIsInstance(folder, str)
                self.assertTrue(len(folder) > 0)

    @patch("platform.system")
    def test_system_detection_windows(self, mock_system):
        """Test wykrywania systemu Windows"""
        mock_system.return_value = "Windows"
        # Reimport po zmianie platform.system
        import importlib
        import app

        importlib.reload(app)

        self.assertEqual(app.SYSTEM_OS, "Windows")
        self.assertTrue(app.IS_WINDOWS)
        self.assertFalse(app.IS_MACOS)
        self.assertFalse(app.IS_LINUX)

    @patch("platform.system")
    def test_system_detection_macos(self, mock_system):
        """Test wykrywania systemu macOS"""
        mock_system.return_value = "Darwin"
        import importlib
        import app

        importlib.reload(app)

        self.assertEqual(app.SYSTEM_OS, "Darwin")
        self.assertTrue(app.IS_MACOS)
        self.assertFalse(app.IS_WINDOWS)
        self.assertFalse(app.IS_LINUX)


class TestLoadingSpinner(unittest.TestCase):
    """Testy animowanego spinnera"""

    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.frame = tk.Frame(self.root)

    def tearDown(self):
        self.root.destroy()

    def test_spinner_initialization(self):
        """Test inicjalizacji spinnera"""
        spinner = LoadingSpinner(self.frame, size=50)
        self.assertEqual(spinner.size, 50)
        self.assertFalse(spinner.running)
        self.assertEqual(spinner.angle, 0)

    def test_create_spinner_canvas(self):
        """Test tworzenia canvas dla spinnera"""
        spinner = LoadingSpinner(self.frame)
        canvas = spinner.create_spinner()

        self.assertIsInstance(canvas, tk.Canvas)
        self.assertEqual(canvas.winfo_reqwidth(), spinner.size)
        self.assertEqual(canvas.winfo_reqheight(), spinner.size)

    def test_start_stop_spinner(self):
        """Test uruchamiania i zatrzymywania spinnera"""
        spinner = LoadingSpinner(self.frame)
        canvas = spinner.create_spinner()

        # Test start
        spinner.start()
        self.assertTrue(spinner.running)

        # Test stop
        spinner.stop()
        self.assertFalse(spinner.running)


class TestGUIComponents(unittest.TestCase):
    """Testy komponentów GUI"""

    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()

    def tearDown(self):
        self.root.destroy()

    def test_tooltip_creation(self):
        """Test tworzenia tooltipa"""
        button = tk.Button(self.root, text="Test")
        tooltip = ToolTip(button, "Test tooltip")

        self.assertEqual(tooltip.text, "Test tooltip")
        self.assertEqual(tooltip.widget, button)
        self.assertIsNone(tooltip.tooltip_window)

    def test_tooltip_with_theme_manager(self):
        """Test tooltipa z theme managerem"""
        button = tk.Button(self.root, text="Test")
        theme_manager = ThemeManager(self.root)
        tooltip = ToolTip(button, "Test tooltip", theme_manager)

        self.assertEqual(tooltip.theme_manager, theme_manager)


class TestIntegration(unittest.TestCase):
    """Testy integracyjne"""

    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.app = ImageFlow(self.root, testing_mode=True)

    def tearDown(self):
        self.root.destroy()

    def test_theme_change_updates_widgets(self):
        """Test czy zmiana motywu aktualizuje widgety"""
        initial_bg = self.app.lista_plikow.cget("bg")

        # Zmień motyw
        self.app.theme_manager.toggle_theme()

        # Sprawdź czy kolor się zmienił
        new_bg = self.app.lista_plikow.cget("bg")
        self.assertNotEqual(initial_bg, new_bg)

    @patch("tkinter.filedialog.askopenfilenames")
    @patch("os.path.isfile")
    def test_wybierz_pliki_integration(self, mock_isfile, mock_dialog):
        """Test integracji wyboru plików"""
        mock_dialog.return_value = ["/test/img1.jpg", "/test/img2.png"]
        mock_isfile.return_value = True

        initial_count = len(self.app.pliki_do_konwersji)
        self.app.wybierz_pliki()

        self.assertEqual(len(self.app.pliki_do_konwersji), initial_count + 2)


if __name__ == "__main__":
    # Konfiguracja testów
    unittest.TestLoader.testMethodPrefix = "test"

    # Uruchom wszystkie testy
    suite = unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Podsumowanie
    print(f"\n{'=' * 50}")
    print(f"Uruchomiono testów: {result.testsRun}")
    print(f"Błędy: {len(result.errors)}")
    print(f"Niepowodzenia: {len(result.failures)}")
    print(f"Sukces: {result.wasSuccessful()}")
    print(f"{'=' * 50}")
