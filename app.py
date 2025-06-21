# ---
# # ImageFlow
#
# **Uniwersalna aplikacja do konwersji plików graficznych (HEIC, JPG, PNG, BMP, TIFF, GIF) z graficznym interfejsem użytkownika (Tkinter).**
#
# Autor: Alan Steinbarth
# Wersja: 2.0.0
# ---

# =========================================
# Importy i rejestracja obsługi formatów
# =========================================
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
from pillow_heif import register_heif_opener
import os
import platform
import logging
import threading
import subprocess
import time
import math

try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
except ImportError:
    DND_FILES = None
    TkinterDnD = None

# Wykrywanie systemu operacyjnego
SYSTEM_OS = platform.system()
IS_MACOS = SYSTEM_OS == "Darwin"
IS_WINDOWS = SYSTEM_OS == "Windows"
IS_LINUX = SYSTEM_OS == "Linux"

# Rejestracja obsługi plików HEIC
register_heif_opener()


# =========================================
# Klasy pomocnicze dla UI
# =========================================
class ThemeManager:
    """Zarządzanie motywami aplikacji"""

    def __init__(self, root):
        self.root = root
        self.is_dark = False
        self.style = ttk.Style()

        # Kolory dla motywów
        self.themes = {
            "light": {
                "bg": "#ffffff",
                "fg": "#000000",
                "select_bg": "#0078d4",
                "select_fg": "#ffffff",
                "entry_bg": "#ffffff",
                "entry_fg": "#000000",
                "button_bg": "#f0f0f0",
                "button_fg": "#000000",
            },
            "dark": {
                "bg": "#2d2d30",
                "fg": "#ffffff",
                "select_bg": "#007acc",
                "select_fg": "#ffffff",
                "entry_bg": "#3c3c3c",
                "entry_fg": "#ffffff",
                "button_bg": "#404040",
                "button_fg": "#ffffff",
            },
        }

        # Aplikuj domyślny motyw
        self.apply_theme()

    def toggle_theme(self):
        """Przełącza między jasnym a ciemnym motywem"""
        self.is_dark = not self.is_dark

        # Animacja przy zmianie motywu
        self.animate_theme_change()
        self.apply_theme()

    def apply_theme(self):
        """Aplikuje aktualny motyw"""
        theme = self.themes["dark"] if self.is_dark else self.themes["light"]

        # Konfiguruj style ttk
        self.style.configure("TFrame", background=theme["bg"])
        self.style.configure("TLabel", background=theme["bg"], foreground=theme["fg"])
        self.style.configure(
            "TButton", background=theme["button_bg"], foreground=theme["button_fg"]
        )
        self.style.map(
            "TButton",
            background=[
                ("active", theme["select_bg"]),
                ("pressed", theme["select_bg"]),
            ],
        )

        # Konfiguruj główne okno
        self.root.configure(bg=theme["bg"])

    def animate_theme_change(self):
        """Płynna animacja zmiany motywu"""
        # Fade out i fade in
        steps = [0.9, 0.7, 0.5, 0.7, 0.9, 1.0]
        for alpha in steps:
            self.root.attributes("-alpha", alpha)
            self.root.update()
            time.sleep(0.03)


class ToolTip:
    """Dodaje tooltips do widgetów"""

    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None

        # Bind events
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, _event=None):
        """Pokazuje tooltip"""
        if self.tooltip_window:
            return

        x = self.widget.winfo_rootx() + 25
        y = self.widget.winfo_rooty() + 25

        self.tooltip_window = tk.Toplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.wm_geometry(f"+{x}+{y}")

        # Styling tooltipa
        self.tooltip_window.configure(bg="#ffffe0", relief="solid", borderwidth=1)

        label = tk.Label(
            self.tooltip_window,
            text=self.text,
            background="#ffffe0",
            foreground="#000000",
            font=("Arial", 9),
            padx=6,
            pady=4,
        )
        label.pack()

        # Animacja pojawiania się
        self.tooltip_window.attributes("-alpha", 0.0)
        self.fade_in()

    def fade_in(self):
        """Animacja fade-in tooltipa"""
        alpha_steps = [0.0, 0.3, 0.6, 0.8, 1.0]
        for alpha in alpha_steps:
            if self.tooltip_window:
                try:
                    self.tooltip_window.attributes("-alpha", alpha)
                    self.tooltip_window.update()
                    time.sleep(0.02)
                except tk.TclError:
                    break

    def hide_tooltip(self, _event=None):
        """Ukrywa tooltip"""
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None


class LoadingSpinner:
    """Animowany loading spinner"""

    def __init__(self, parent, size=32):
        self.parent = parent
        self.size = size
        self.canvas = None
        self.running = False
        self.angle = 0

    def create_spinner(self):
        """Tworzy canvas dla spinnera"""
        # Używaj przezroczystego tła aby dopasować się do motywu
        self.canvas = tk.Canvas(
            self.parent,
            width=self.size,
            height=self.size,
            bg=self.parent.cget("bg") if hasattr(self.parent, "cget") else "white",
            highlightthickness=0,
        )
        return self.canvas

    def start(self):
        """Rozpoczyna animację"""
        if not self.canvas:
            return

        self.running = True
        self.animate()

    def stop(self):
        """Zatrzymuje animację"""
        self.running = False
        if self.canvas:
            self.canvas.delete("all")

    def animate(self):
        """Animuje spinner"""
        if not self.running or not self.canvas:
            return

        self.canvas.delete("all")

        # Rysuj spinner
        center = self.size // 2
        radius = center - 4

        for i in range(8):
            angle_rad = math.radians((self.angle + i * 45) % 360)
            x1 = center + radius * 0.6 * math.cos(angle_rad)
            y1 = center + radius * 0.6 * math.sin(angle_rad)
            x2 = center + radius * math.cos(angle_rad)
            y2 = center + radius * math.sin(angle_rad)

            alpha = 1.0 - (i / 8.0)
            gray_val = int(255 * alpha)
            color = f"#{gray_val:02x}{gray_val:02x}{gray_val:02x}"

            self.canvas.create_line(
                x1, y1, x2, y2, fill=color, width=3, capstyle=tk.ROUND
            )

        self.angle = (self.angle + 15) % 360

        if self.running:
            self.parent.after(50, self.animate)


# =========================================
# Klasa główna aplikacji: ImageFlow
# =========================================
class ImageFlow:
    """
    Główna klasa aplikacji GUI ImageFlow do konwersji plików graficznych.
    Odpowiada za logikę, interfejs oraz obsługę zdarzeń.
    """

    def __init__(self, root):
        # Inicjalizacja głównego okna i ustawienia
        self.root = root
        self.root.title("ImageFlow")
        self.root.geometry("600x740")  # zwiększona wysokość dla nowych elementów

        # Inicjalizacja managera motywów
        self.theme_manager = ThemeManager(root)

        # Ustawienia specyficzne dla systemu operacyjnego
        self.konfiguruj_system_operacyjny()

        # Konfiguracja loggera
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        # Lista plików do konwersji
        self.pliki_do_konwersji = []

        # Ustaw domyślny folder zapisu w zależności od systemu
        self.folder_docelowy = self.pobierz_domyslny_folder()

        self.anuluj_konwersje = False  # Dodane do obsługi anulowania
        self.miniatura = None  # Inicjalizacja atrybutu miniatury
        self.loading_spinner = None  # Spinner dla animacji
        self.callback_po_konwersji = None  # Callback po zakończeniu konwersji

        # Najpierw utwórz interfejs, potem loguj
        self.utworz_interfejs()
        self.log(f"System: {SYSTEM_OS}")
        self.log(f"Domyślny folder zapisu: {self.folder_docelowy}")

        # Konfiguracja przeciągania i upuszczania
        if DND_FILES is not None:
            self.root.drop_target_register(DND_FILES)
            self.root.dnd_bind("<<Drop>>", self.dodaj_pliki_przeciagniecie)

    # =========================================
    # Konfiguracja specyficzna dla systemu operacyjnego
    # =========================================
    def konfiguruj_system_operacyjny(self):
        """
        Konfiguruje aplikację w zależności od systemu operacyjnego.
        """
        if IS_MACOS:
            # Ustawienia specyficzne dla macOS
            if hasattr(self.root, "createcommand"):
                self.root.createcommand("::tk::mac::Quit", self.on_quit)
            # Centrowanie okna na macOS
            self.root.update_idletasks()
            width = self.root.winfo_width()
            height = self.root.winfo_height()
            x = (self.root.winfo_screenwidth() // 2) - (width // 2)
            y = (self.root.winfo_screenheight() // 2) - (height // 2)
            self.root.geometry(f"{width}x{height}+{x}+{y}")

        elif IS_WINDOWS:
            # Ustawienia specyficzne dla Windows
            self.root.iconbitmap(default="")  # Usuwa domyślną ikonę
            # Windows DPI awareness
            try:
                import ctypes

                # windll jest dostępne tylko na Windows
                if hasattr(ctypes, "windll"):
                    windll = getattr(ctypes, "windll")
                    if hasattr(windll, "shcore"):
                        windll.shcore.SetProcessDpiAwareness(1)
            except (ImportError, OSError, AttributeError):
                pass

        elif IS_LINUX:
            # Ustawienia specyficzne dla Linux
            pass

    def pobierz_domyslny_folder(self):
        """
        Zwraca domyślny folder zapisu w zależności od systemu operacyjnego.
        """
        home = os.path.expanduser("~")

        if IS_WINDOWS:
            # Windows: sprawdź czy istnieje folder Pulpit
            desktop_paths = [
                os.path.join(home, "Desktop"),
                os.path.join(home, "Pulpit"),
                os.path.join(home, "Bureau"),  # Francuski Windows
                os.path.join(home, "Escritorio"),  # Hiszpański Windows
            ]
            for path in desktop_paths:
                if os.path.exists(path):
                    return path
            return home

        elif IS_MACOS:
            # macOS: zawsze Desktop
            return os.path.join(home, "Desktop")

        elif IS_LINUX:
            # Linux: sprawdź XDG lub użyj Desktop
            try:
                result = subprocess.run(
                    ["xdg-user-dir", "DESKTOP"],
                    capture_output=True,
                    text=True,
                    timeout=5,
                    check=False,
                )
                if result.returncode == 0:
                    return result.stdout.strip()
            except (ImportError, OSError, subprocess.TimeoutExpired, FileNotFoundError):
                pass
            # Fallback dla Linux
            desktop_path = os.path.join(home, "Desktop")
            if os.path.exists(desktop_path):
                return desktop_path
            return home

        return home  # Fallback dla nieznanych systemów

    # =========================================
    # Tworzenie interfejsu użytkownika (GUI)
    # =========================================
    def utworz_interfejs(self):
        """
        Buduje i rozmieszcza wszystkie elementy GUI w głównym oknie.
        """
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")

        # Ramka górna z przyciskami
        top_frame = ttk.Frame(main_frame)
        top_frame.grid(row=0, column=0, columnspan=5, sticky="ew", pady=(0, 5))
        top_frame.columnconfigure(0, weight=1)

        # Przycisk wybierania plików
        select_btn = ttk.Button(
            top_frame, text="Wybierz pliki do konwersji", command=self.wybierz_pliki
        )
        select_btn.grid(row=0, column=0, sticky=tk.W)
        ToolTip(
            select_btn,
            "Wybierz pliki graficzne do konwersji\nObsługiwane formaty: HEIC, JPG, PNG, BMP, TIFF, GIF",
        )

        # Przycisk zmiany motywu
        theme_btn = ttk.Button(
            top_frame,
            text="🌙" if not self.theme_manager.is_dark else "☀️",
            command=self.toggle_theme_with_animation,
            width=3,
        )
        theme_btn.grid(row=0, column=1, sticky=tk.E, padx=(10, 0))
        ToolTip(theme_btn, "Przełącz między jasnym a ciemnym motywem")
        # Lista plików i podgląd w jednej ramce
        pliki_podglad_frame = ttk.Frame(main_frame)
        pliki_podglad_frame.grid(row=1, column=0, columnspan=5, pady=5, sticky="nsew")
        pliki_podglad_frame.columnconfigure(0, weight=1)
        pliki_podglad_frame.columnconfigure(1, weight=1)
        pliki_podglad_frame.rowconfigure(0, weight=1)
        # Lista plików (lewa połowa, cała wysokość)
        self.lista_plikow = tk.Listbox(
            pliki_podglad_frame, width=35, height=16, selectmode=tk.EXTENDED
        )
        self.lista_plikow.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        self.lista_plikow.bind("<<ListboxSelect>>", self.pokaz_info_plik)

        # Scrollbar dla listy plików
        scrollbar_pliki = ttk.Scrollbar(
            pliki_podglad_frame, orient="vertical", command=self.lista_plikow.yview
        )
        scrollbar_pliki.grid(row=0, column=0, sticky="nse")
        self.lista_plikow.configure(yscrollcommand=scrollbar_pliki.set)
        # Ramka na miniaturę i szczegóły (prawa połowa, cała wysokość)
        miniatura_frame = ttk.Frame(pliki_podglad_frame)
        miniatura_frame.grid(row=0, column=1, sticky="nsew")
        miniatura_frame.rowconfigure(0, weight=1)
        miniatura_frame.rowconfigure(1, weight=0)
        miniatura_frame.columnconfigure(0, weight=1)

        # Dodaj ramkę centrowania w prawej połówce
        center_frame = ttk.Frame(miniatura_frame)
        center_frame.grid(row=0, column=0, sticky="nsew")
        center_frame.columnconfigure(0, weight=1)
        center_frame.rowconfigure(0, weight=1)
        center_frame.rowconfigure(1, weight=0)

        # Miniatura zdjęcia (wyśrodkowana)
        self.miniatura_canvas = tk.Canvas(
            center_frame, width=210, height=235, bg="white"
        )
        self.miniatura_canvas.grid(row=0, column=0, pady=(0, 5), sticky="n")
        # Szczegóły pliku pod miniaturą (wyśrodkowane)
        self.info_label = ttk.Label(
            center_frame,
            text="Szczegóły pliku:",
            anchor="center",
            justify="center",
            wraplength=200,
        )
        self.info_label.grid(row=1, column=0, sticky="n", pady=(0, 5))
        # Rozciągnięcie obu okien na całą szerokość
        main_frame.columnconfigure(0, weight=1)
        pliki_podglad_frame.grid(sticky="nsew")
        # ...reszta interfejsu bez zmian...
        ttk.Button(main_frame, text="Usuń zaznaczone", command=self.usun_z_listy).grid(
            row=2, column=0, pady=5, sticky=tk.W
        )

        # Sekcja wyboru formatu i jakości pod przyciskiem Usuń zaznaczone
        format_frame = ttk.Frame(main_frame)
        format_frame.grid(row=3, column=0, columnspan=5, sticky="ew", pady=5)
        format_frame.columnconfigure(0, weight=0)
        format_frame.columnconfigure(1, weight=0)
        format_frame.columnconfigure(2, weight=1)
        format_frame.columnconfigure(3, weight=0)
        format_frame.columnconfigure(4, weight=2)

        # Lewa strona: format
        ttk.Label(format_frame, text="Format wyjściowy:").grid(
            row=0, column=0, sticky="w", padx=(0, 5)
        )
        self.format_var = tk.StringVar(value="JPEG")
        format_box = ttk.Combobox(
            format_frame,
            textvariable=self.format_var,
            values=["JPEG", "PNG", "BMP", "TIFF", "WEBP"],
            state="readonly",
            width=8,
        )
        format_box.grid(row=0, column=1, sticky="w")

        # Prawa strona: jakość
        self.jakosc_var = tk.IntVar(value=100)
        self.jakosc_label = ttk.Label(
            format_frame, text="Jakość po konwersji pliku: 100%"
        )
        self.jakosc_label.grid(row=0, column=3, sticky="e", padx=(10, 5))
        jakosc_scale = ttk.Scale(
            format_frame,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            variable=self.jakosc_var,
            command=self.aktualizuj_jakosc_label,
        )
        jakosc_scale.grid(row=0, column=4, sticky="ew")

        # Pasek postępu
        self.pasek_postepu = ttk.Progressbar(
            main_frame, orient="horizontal", length=300, mode="determinate"
        )
        self.pasek_postepu.grid(row=4, column=0, columnspan=5, pady=5)
        # Pole logów
        self.pole_logow = tk.Text(main_frame, width=70, height=10)
        self.pole_logow.grid(row=5, column=0, columnspan=5, pady=5)
        # Scrollbar dla logów
        scrollbar = ttk.Scrollbar(
            main_frame, orient="vertical", command=self.pole_logow.yview
        )
        scrollbar.grid(row=5, column=5, sticky="ns")
        self.pole_logow.configure(yscrollcommand=scrollbar.set)
        # Przyciski pod sekcją wyboru formatu i jakości - w jednej ramce, równo rozmieszczone
        przyciski_frame = ttk.Frame(main_frame)
        przyciski_frame.grid(row=7, column=0, columnspan=5, pady=5, sticky="ew")
        przyciski_frame.columnconfigure((0, 1, 2), weight=1)

        # Przycisk wyboru folderu docelowego
        folder_btn = ttk.Button(
            przyciski_frame,
            text="Wybierz folder docelowy",
            command=self.wybierz_folder_docelowy,
        )
        folder_btn.grid(row=0, column=0, padx=5, sticky="ew")
        ToolTip(folder_btn, "Wybierz folder gdzie zostaną zapisane skonwertowane pliki")

        # Przycisk konwersji
        self.konwertuj_btn = ttk.Button(
            przyciski_frame,
            text="Konwertuj",
            command=self.rozpocznij_konwersje_z_animacja,
        )
        self.konwertuj_btn.grid(row=0, column=1, padx=5, sticky="ew")
        ToolTip(self.konwertuj_btn, "Rozpocznij konwersję wybranych plików")

        # Przycisk anulowania
        self.anuluj_btn = ttk.Button(
            przyciski_frame, text="Anuluj", command=self.anuluj, state=tk.DISABLED
        )
        self.anuluj_btn.grid(row=0, column=2, padx=5, sticky="ew")
        ToolTip(self.anuluj_btn, "Anuluj trwającą konwersję")
        # Pusta przestrzeń, aby przesunąć napis na sam dół
        main_frame.grid_rowconfigure(
            8, weight=1
        )  # Napis o autorze na samym dole, wyśrodkowany
        ttk.Label(
            main_frame, text="Autor: Alan Steinbarth", anchor="center", justify="center"
        ).grid(row=9, column=0, columnspan=5, sticky="ew", pady=10)

    # =========================================
    # Aktualizacja etykiety jakości
    # =========================================
    def aktualizuj_jakosc_label(self, val):
        """
        Aktualizuje tekst etykiety pokazującej wybraną jakość konwersji.
        """
        self.jakosc_label.config(text=f"Jakość po konwersji pliku: {int(float(val))}%")

    # =========================================
    # Wyświetlanie szczegółów i miniatury pliku
    # =========================================
    def pokaz_info_plik(self, _event):  # Używamy _ dla nieużywanego parametru
        """
        Po zaznaczeniu pliku na liście wyświetla szczegóły i miniaturę.
        """
        idxs = self.lista_plikow.curselection()
        if not idxs:
            self.info_label.config(text="Szczegóły pliku:")
            self.miniatura_canvas.delete("all")
            return
        idx = idxs[0]
        plik = self.pliki_do_konwersji[idx]
        try:
            with Image.open(plik) as img:
                info = f"Nazwa: {os.path.basename(plik)}\nFormat: {img.format}\nRozdzielczość: {img.size[0]}x{img.size[1]} px\nRozmiar: {os.path.getsize(plik) // 1024} KB"
                self.info_label.config(text=info)
                # Miniatura
                img.thumbnail((200, 200))
                self.miniatura = ImageTk.PhotoImage(img)
                self.miniatura_canvas.delete("all")
                self.miniatura_canvas.create_image(100, 112, image=self.miniatura)
        except (OSError, IOError) as e:
            self.info_label.config(text=f"Błąd odczytu: {e}")
            self.miniatura_canvas.delete("all")

    # =========================================
    # Obsługa zamykania aplikacji na macOS
    # =========================================
    def on_quit(self):
        """
        Obsługa zamykania aplikacji na macOS.
        """
        self.root.quit()

    # =========================================
    # Wybór plików do konwersji (dialog)
    # =========================================
    def wybierz_pliki(self):
        """
        Otwiera okno dialogowe do wyboru plików graficznych do konwersji.
        Konfiguruje format filetypes w zależności od systemu operacyjnego.
        """
        try:
            # Format filetypes różni się między systemami
            if IS_WINDOWS:
                # Windows używa średników jako separatorów
                filetypes = [
                    ("Pliki graficzne", "*.heic;*.jpg;*.jpeg;*.png;*.bmp;*.tiff;*.gif"),
                    ("Pliki HEIC", "*.heic"),
                    ("Pliki JPG", "*.jpg;*.jpeg"),
                    ("Pliki PNG", "*.png"),
                    ("Pliki BMP", "*.bmp"),
                    ("Pliki TIFF", "*.tiff"),
                    ("Pliki GIF", "*.gif"),
                    ("Wszystkie pliki", "*.*"),
                ]
            else:
                # macOS i Linux używają spacji jako separatorów
                filetypes = [
                    ("Pliki graficzne", "*.heic *.jpg *.jpeg *.png *.bmp *.tiff *.gif"),
                    ("Pliki HEIC", "*.heic"),
                    ("Pliki JPG", "*.jpg *.jpeg"),
                    ("Pliki PNG", "*.png"),
                    ("Pliki BMP", "*.bmp"),
                    ("Pliki TIFF", "*.tiff"),
                    ("Pliki GIF", "*.gif"),
                    ("Wszystkie pliki", "*.*"),
                ]

            pliki = filedialog.askopenfilenames(
                title="Wybierz pliki do konwersji", filetypes=filetypes
            )
            if pliki:  # Sprawdź czy użytkownik wybrał jakieś pliki
                self.dodaj_pliki(pliki)
        except (OSError, IOError) as e:
            self.log(f"Błąd podczas wyboru plików: {e}")
            messagebox.showerror(
                "Błąd", f"Nie można otworzyć dialogu wyboru plików: {e}"
            )

    # =========================================
    # Obsługa przeciągania i upuszczania plików
    # =========================================
    def dodaj_pliki_przeciagniecie(self, event):
        """
        Dodaje pliki przeciągnięte do okna aplikacji (drag & drop).
        """
        pliki = self.root.tk.splitlist(event.data)
        self.dodaj_pliki(pliki)

    # =========================================
    # Dodawanie plików do listy (z dialogu lub drag&drop)
    # =========================================
    def dodaj_pliki(self, pliki):
        """
        Dodaje wybrane pliki do listy plików do konwersji, filtruje duplikaty i nieobsługiwane formaty.
        """
        obslugiwane = (".heic", ".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".gif")
        for plik in pliki:
            if not os.path.isfile(plik):
                continue
            ext = os.path.splitext(plik)[1].lower()
            if ext in obslugiwane and plik not in self.pliki_do_konwersji:
                # Filtrowanie duplikatów po nazwie
                nazwa = os.path.basename(plik)
                if any(os.path.basename(p) == nazwa for p in self.pliki_do_konwersji):
                    continue
                self.pliki_do_konwersji.append(plik)
                self.lista_plikow.insert(tk.END, nazwa)
                self.log(f"Dodano plik: {plik}")

    # =========================================
    # Usuwanie plików z listy
    # =========================================
    def usun_z_listy(self):
        """
        Usuwa zaznaczone pliki z listy plików do konwersji.
        """
        zaznaczone = list(self.lista_plikow.curselection())
        zaznaczone.reverse()
        for idx in zaznaczone:
            plik = self.pliki_do_konwersji[idx]
            self.log(f"Usunięto plik: {plik}")
            del self.pliki_do_konwersji[idx]
            self.lista_plikow.delete(idx)

    # =========================================
    # Wybór folderu docelowego
    # =========================================
    def wybierz_folder_docelowy(self):
        """
        Otwiera okno dialogowe do wyboru folderu docelowego zapisu plików.
        """
        try:
            nowy_folder = filedialog.askdirectory(
                initialdir=self.folder_docelowy, title="Wybierz folder docelowy"
            )
            if nowy_folder:
                # Normalizuj ścieżkę dla systemu
                self.folder_docelowy = os.path.normpath(nowy_folder)
                self.log(f"Wybrano folder docelowy: {self.folder_docelowy}")
        except (OSError, IOError) as e:
            self.log(f"Błąd podczas wyboru folderu: {e}")
            messagebox.showerror(
                "Błąd", f"Nie można otworzyć dialogu wyboru folderu: {e}"
            )

    # =========================================
    # Sprawdzanie uprawnień systemu
    # =========================================
    def sprawdz_uprawnienia_zapisu(self, folder):
        """
        Sprawdza czy aplikacja ma uprawnienia do zapisu w danym folderze.
        """
        try:
            test_file = os.path.join(folder, "test_write_permission.tmp")
            with open(test_file, "w", encoding="utf-8") as f:
                f.write("test")
            os.remove(test_file)
            return True
        except (PermissionError, OSError):
            self.log(f"Brak uprawnień do zapisu w folderze: {folder}")
            return False

    # =========================================
    # Logowanie komunikatów do pola tekstowego i loggera
    # =========================================
    def log(self, message):
        """
        Dodaje komunikat do pola logów oraz do loggera.
        """
        self.pole_logow.insert(tk.END, f"{message}\n")
        self.pole_logow.see(tk.END)
        self.logger.info(message)

    # =========================================
    # Anulowanie konwersji
    # =========================================
    def anuluj(self):
        """
        Ustawia flagę anulowania konwersji.
        """
        self.anuluj_konwersje = True
        self.log("Anulowano konwersję!")

    # =========================================
    # Rozpoczęcie procesu konwersji (w osobnym wątku)
    # =========================================
    def rozpocznij_konwersje(self):
        """
        Rozpoczyna konwersję plików w osobnym wątku, blokuje przycisk konwersji.
        """
        if not hasattr(self, "folder_docelowy"):
            messagebox.showerror("Błąd", "Wybierz folder docelowy!")
            return
        if not self.pliki_do_konwersji:
            messagebox.showerror("Błąd", "Dodaj pliki do konwersji!")
            return
        # Sprawdź uprawnienia do zapisu
        if not self.sprawdz_uprawnienia_zapisu(self.folder_docelowy):
            messagebox.showerror(
                "Błąd",
                f"Brak uprawnień do zapisu w folderze:\n{self.folder_docelowy}\n\n"
                "Wybierz inny folder lub uruchom aplikację z uprawnieniami administratora.",
            )
            return

        self.konwertuj_btn.config(state=tk.DISABLED)
        self.anuluj_btn.config(state=tk.NORMAL)
        self.anuluj_konwersje = False
        self.root.title(f"Konwersja: 0/{len(self.pliki_do_konwersji)}")
        thread = threading.Thread(target=self.konwertuj_pliki)
        thread.daemon = True
        thread.start()

    # =========================================
    # Główna logika konwersji plików
    # =========================================
    def konwertuj_pliki(self):
        """
        Przetwarza i konwertuje pliki graficzne do wybranego formatu, obsługuje postęp i błędy.
        """
        total = len(self.pliki_do_konwersji)
        self.pasek_postepu["maximum"] = total
        self.pasek_postepu["value"] = 0
        sukcesy = 0
        bledy = 0
        for i, plik_zrodlowy in enumerate(self.pliki_do_konwersji):
            if self.anuluj_konwersje:
                break
            try:
                nazwa_pliku = os.path.splitext(os.path.basename(plik_zrodlowy))[0]
                format_out = self.format_var.get()
                ext = {
                    "JPEG": ".jpg",
                    "PNG": ".png",
                    "BMP": ".bmp",
                    "TIFF": ".tiff",
                    "WEBP": ".webp",
                }[format_out]

                # Użyj os.path.join i normalizuj ścieżkę
                plik_docelowy = os.path.normpath(
                    os.path.join(self.folder_docelowy, f"{nazwa_pliku}{ext}")
                )
                if os.path.exists(plik_docelowy):
                    if not messagebox.askyesno(
                        "Plik istnieje",
                        f"Plik {nazwa_pliku}{ext} już istnieje. Czy chcesz go nadpisać?",
                    ):
                        continue
                self.log(f"Konwertowanie: {plik_zrodlowy}")
                try:
                    with Image.open(plik_zrodlowy) as img:
                        img.thumbnail((200, 200))
                        self.miniatura = ImageTk.PhotoImage(img)
                        self.miniatura_canvas.delete("all")
                        self.miniatura_canvas.create_image(
                            100, 100, image=self.miniatura
                        )
                except (OSError, IOError):
                    self.miniatura_canvas.delete("all")
                try:
                    with Image.open(plik_zrodlowy) as img:
                        img.verify()
                    with Image.open(plik_zrodlowy) as img:
                        if format_out == "JPEG":
                            img.save(
                                plik_docelowy,
                                format_out,
                                quality=self.jakosc_var.get(),
                                subsampling=0,
                            )
                        elif format_out == "PNG":
                            img.save(plik_docelowy, format_out, compress_level=1)
                        else:
                            img.save(plik_docelowy, format_out)
                except (OSError, SyntaxError) as e:
                    self.log(
                        f"Plik uszkodzony lub nieobsługiwany: {plik_zrodlowy}: {str(e)}"
                    )
                    bledy += 1
                    continue
                self.log(f"Zapisano: {plik_docelowy}")
                sukcesy += 1
                self.pasek_postepu["value"] = i + 1
                self.root.title(f"Konwersja: {i + 1}/{total}")
                if (i + 1) % 5 == 0 or i == total - 1:
                    self.root.update()
            except (OSError, IOError, KeyError) as e:
                self.log(f"Błąd podczas konwersji {plik_zrodlowy}: {str(e)}")
                self.logger.error(
                    "Błąd podczas konwersji %s: %s", plik_zrodlowy, str(e)
                )
                bledy += 1
        self.konwertuj_btn.config(state=tk.NORMAL)
        self.anuluj_btn.config(state=tk.DISABLED)
        self.root.title("ImageFlow")

        # Wywołaj callback po zakończeniu (ukrycie spinnera)
        if hasattr(self, "callback_po_konwersji") and self.callback_po_konwersji:
            self.callback_po_konwersji()
            self.callback_po_konwersji = None

        if self.anuluj_konwersje:
            self.log("Konwersja anulowana przez użytkownika.")
        else:
            self.log(f"Zakończono konwersję. Sukcesy: {sukcesy}, błędy: {bledy}")
            self.pasek_postepu["value"] = 0
            self.root.update()
            self.pokaz_okno_sukcesu()

    # =========================================
    # Okno sukcesu po zakończonej konwersji
    # =========================================
    def pokaz_okno_sukcesu(self):
        """
        Wyświetla okno z informacją o zakończonej konwersji plików.
        """
        okno = tk.Toplevel(self.root)
        okno.title("Sukces!")
        okno.geometry("350x120")
        okno.resizable(False, False)
        ttk.Label(
            okno,
            text="Twoje pliki zostały przekonwertowane i zapisane!",
            anchor="center",
            justify="center",
            font=("Arial", 12),
        ).pack(pady=20)
        ttk.Button(okno, text="OK", command=okno.destroy).pack(pady=5)
        # Centrowanie okna na ekranie
        okno.update_idletasks()
        width = okno.winfo_width()
        height = okno.winfo_height()
        x = (okno.winfo_screenwidth() // 2) - (width // 2)
        y = (okno.winfo_screenheight() // 2) - (height // 2)
        okno.geometry(f"{width}x{height}+{x}+{y}")
        okno.transient(self.root)
        okno.grab_set()
        self.root.wait_window(okno)

    # =========================================
    # Funkcje UI i animacji
    # =========================================
    def toggle_theme_with_animation(self):
        """Przełącza motyw z animacją i aktualizuje ikonę przycisku"""
        self.theme_manager.toggle_theme()

        # Znajdź przycisk motywu i zaktualizuj jego tekst
        for widget in self.root.winfo_children():
            if isinstance(widget, ttk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, ttk.Frame):
                        for btn in child.winfo_children():
                            if isinstance(btn, ttk.Button) and btn.cget("width") == 3:
                                btn.config(
                                    text="☀️" if self.theme_manager.is_dark else "🌙"
                                )
                                break

    def show_loading_spinner(self, parent_widget):
        """Pokazuje spinner ładowania"""
        if self.loading_spinner:
            self.loading_spinner.stop()

        self.loading_spinner = LoadingSpinner(parent_widget)
        spinner_canvas = self.loading_spinner.create_spinner()
        self.loading_spinner.start()
        return spinner_canvas

    def hide_loading_spinner(self):
        """Ukrywa spinner ładowania"""
        if self.loading_spinner:
            self.loading_spinner.stop()
            self.loading_spinner = None

    def rozpocznij_konwersje_z_animacja(self):
        """Rozpoczyna konwersję z animacją loading spinnera"""
        if not hasattr(self, "folder_docelowy"):
            messagebox.showerror("Błąd", "Wybierz folder docelowy!")
            return
        if not self.pliki_do_konwersji:
            messagebox.showerror("Błąd", "Dodaj pliki do konwersji!")
            return

        try:
            # Pokaż spinner w obszarze miniatury
            spinner_canvas = self.show_loading_spinner(self.miniatura_canvas.master)
            spinner_canvas.grid(row=0, column=0, pady=(50, 0))
            self.miniatura_canvas.grid_remove()  # Tymczasowo ukryj miniaturę

            # Uruchom konwersję po krótkiej pauzie (aby spinner zdążył się pokazać)
            self.root.after(100, self._uruchom_konwersje_po_animacji)
        except (tk.TclError, AttributeError) as e:
            self.log(f"Błąd podczas uruchamiania animacji: {e}")
            # Fallback - uruchom konwersję bez animacji
            self.rozpocznij_konwersje()

    def _uruchom_konwersje_po_animacji(self):
        """Pomocnicza metoda uruchamiająca konwersję po pokazaniu spinnera"""

        # Przywróć miniaturę i ukryj spinner po zakończeniu
        def zakoncz_animacje():
            self.hide_loading_spinner()
            self.miniatura_canvas.grid()

        # Dodaj callback do metody konwersji
        self.callback_po_konwersji = zakoncz_animacje
        self.rozpocznij_konwersje()


# =========================================
# Funkcja główna
# =========================================
def main():
    """Główna funkcja uruchamiająca aplikację"""
    # Tworzy główne okno aplikacji (z obsługą drag&drop jeśli dostępne)
    if TkinterDnD is not None:
        root = TkinterDnD.Tk()
    else:
        root = tk.Tk()
    ImageFlow(root)
    root.mainloop()


# =========================================
# Uruchomienie aplikacji
# =========================================
if __name__ == "__main__":
    main()
