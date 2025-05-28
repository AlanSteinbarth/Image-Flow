# ---
# # Konwerter plików graficznych
#
# **Aplikacja do konwersji i podglądu plików graficznych (HEIC, JPG, PNG, BMP, TIFF, GIF) z graficznym interfejsem użytkownika (Tkinter).**
#
# Autor: Alan Steinbarth
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
# Klasa główna aplikacji: KonwerterHEIC
# =========================================
class KonwerterHEIC:
    """
    Główna klasa aplikacji GUI do konwersji plików graficznych.
    Odpowiada za logikę, interfejs oraz obsługę zdarzeń.
    """
    def __init__(self, root):
        # Inicjalizacja głównego okna i ustawienia
        self.root = root
        self.root.title("Konwerter plików graficznych")
        self.root.geometry("600x710")  # zwiększona wysokość okna o 30 pikseli
        
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

        # Najpierw utwórz interfejs, potem loguj
        self.utworz_interfejs()
        self.log(f"System: {SYSTEM_OS}")
        self.log(f"Domyślny folder zapisu: {self.folder_docelowy}")
        
        # Konfiguracja przeciągania i upuszczania
        if DND_FILES is not None:
            self.root.drop_target_register(DND_FILES)
            self.root.dnd_bind('<<Drop>>', self.dodaj_pliki_przeciagniecie)

    # =========================================
    # Konfiguracja specyficzna dla systemu operacyjnego
    # =========================================
    def konfiguruj_system_operacyjny(self):
        """
        Konfiguruje aplikację w zależności od systemu operacyjnego.
        """
        if IS_MACOS:
            # Ustawienia specyficzne dla macOS
            if hasattr(self.root, 'createcommand'):
                self.root.createcommand('::tk::mac::Quit', self.on_quit)
            # Centrowanie okna na macOS
            self.root.update_idletasks()
            width = self.root.winfo_width()
            height = self.root.winfo_height()
            x = (self.root.winfo_screenwidth() // 2) - (width // 2)
            y = (self.root.winfo_screenheight() // 2) - (height // 2)
            self.root.geometry(f"{width}x{height}+{x}+{y}")
            
        elif IS_WINDOWS:
            # Ustawienia specyficzne dla Windows
            self.root.iconbitmap(default='')  # Usuwa domyślną ikonę
            # Windows DPI awareness
            try:
                import ctypes
                ctypes.windll.shcore.SetProcessDpiAwareness(1)
            except:
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
                import subprocess
                result = subprocess.run(['xdg-user-dir', 'DESKTOP'], 
                                      capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    return result.stdout.strip()
            except:
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
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        # Przycisk wybierania plików na samej górze
        ttk.Button(main_frame, text="Wybierz pliki do konwersji", command=self.wybierz_pliki).grid(row=0, column=0, pady=5, columnspan=5, sticky=tk.W)
        # Lista plików i podgląd w jednej ramce
        pliki_podglad_frame = ttk.Frame(main_frame)
        pliki_podglad_frame.grid(row=1, column=0, columnspan=5, pady=5, sticky="nsew")
        pliki_podglad_frame.columnconfigure(0, weight=1)
        pliki_podglad_frame.columnconfigure(1, weight=1)
        pliki_podglad_frame.rowconfigure(0, weight=1)
        # Lista plików (lewa połowa, cała wysokość)
        self.lista_plikow = tk.Listbox(pliki_podglad_frame, width=35, height=16, selectmode=tk.EXTENDED)
        self.lista_plikow.grid(row=0, column=0, sticky="nsew", padx=(0,5))
        self.lista_plikow.bind('<<ListboxSelect>>', self.pokaz_info_plik)
        
        # Scrollbar dla listy plików
        scrollbar_pliki = ttk.Scrollbar(pliki_podglad_frame, orient="vertical", command=self.lista_plikow.yview)
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
        self.miniatura_canvas = tk.Canvas(center_frame, width=210, height=235, bg="white")
        self.miniatura_canvas.grid(row=0, column=0, pady=(0,5), sticky="n")
        # Szczegóły pliku pod miniaturą (wyśrodkowane)
        self.info_label = ttk.Label(center_frame, text="Szczegóły pliku:", anchor="center", justify="center", wraplength=200)
        self.info_label.grid(row=1, column=0, sticky="n", pady=(0,5))
        # Rozciągnięcie obu okien na całą szerokość
        main_frame.columnconfigure(0, weight=1)
        pliki_podglad_frame.grid(sticky="nsew")
        # ...reszta interfejsu bez zmian...
        ttk.Button(main_frame, text="Usuń zaznaczone", command=self.usun_z_listy).grid(row=2, column=0, pady=5, sticky=tk.W)
        
        # Sekcja wyboru formatu i jakości pod przyciskiem Usuń zaznaczone
        format_frame = ttk.Frame(main_frame)
        format_frame.grid(row=3, column=0, columnspan=5, sticky="ew", pady=5)
        format_frame.columnconfigure(0, weight=0)
        format_frame.columnconfigure(1, weight=0)
        format_frame.columnconfigure(2, weight=1)
        format_frame.columnconfigure(3, weight=0)
        format_frame.columnconfigure(4, weight=2)

        # Lewa strona: format
        ttk.Label(format_frame, text="Format wyjściowy:").grid(row=0, column=0, sticky="w", padx=(0,5))
        self.format_var = tk.StringVar(value="JPEG")
        format_box = ttk.Combobox(format_frame, textvariable=self.format_var, values=["JPEG", "PNG", "BMP", "TIFF", "WEBP"], state="readonly", width=8)
        format_box.grid(row=0, column=1, sticky="w")

        # Prawa strona: jakość
        self.jakosc_var = tk.IntVar(value=100)
        self.jakosc_label = ttk.Label(format_frame, text="Jakość po konwersji pliku: 100%")
        self.jakosc_label.grid(row=0, column=3, sticky="e", padx=(10,5))
        jakosc_scale = ttk.Scale(format_frame, from_=0, to=100, orient=tk.HORIZONTAL, variable=self.jakosc_var, command=self.aktualizuj_jakosc_label)
        jakosc_scale.grid(row=0, column=4, sticky="ew")

        # Pasek postępu
        self.pasek_postepu = ttk.Progressbar(main_frame, orient="horizontal", length=300, mode="determinate")
        self.pasek_postepu.grid(row=4, column=0, columnspan=5, pady=5)
        # Pole logów
        self.pole_logow = tk.Text(main_frame, width=70, height=10)
        self.pole_logow.grid(row=5, column=0, columnspan=5, pady=5)
        # Scrollbar dla logów
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.pole_logow.yview)
        scrollbar.grid(row=5, column=5, sticky="ns")
        self.pole_logow.configure(yscrollcommand=scrollbar.set)
        # Przyciski pod sekcją wyboru formatu i jakości - w jednej ramce, równo rozmieszczone
        przyciski_frame = ttk.Frame(main_frame)
        przyciski_frame.grid(row=7, column=0, columnspan=5, pady=5, sticky="ew")
        przyciski_frame.columnconfigure((0,1,2), weight=1)
        ttk.Button(przyciski_frame, text="Wybierz folder docelowy", command=self.wybierz_folder_docelowy).grid(row=0, column=0, padx=5, sticky="ew")
        self.konwertuj_btn = ttk.Button(przyciski_frame, text="Konwertuj", command=self.rozpocznij_konwersje)
        self.konwertuj_btn.grid(row=0, column=1, padx=5, sticky="ew")
        self.anuluj_btn = ttk.Button(przyciski_frame, text="Anuluj", command=self.anuluj, state=tk.DISABLED)
        self.anuluj_btn.grid(row=0, column=2, padx=5, sticky="ew")
        # Pusta przestrzeń, aby przesunąć napis na sam dół
        main_frame.grid_rowconfigure(8, weight=1)        # Napis o autorze na samym dole, wyśrodkowany
        ttk.Label(main_frame, text="Autor: Alan Steinbarth", anchor="center", justify="center").grid(row=9, column=0, columnspan=5, sticky="ew", pady=10)

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
    def pokaz_info_plik(self, event):
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
                info = f"Nazwa: {os.path.basename(plik)}\nFormat: {img.format}\nRozdzielczość: {img.size[0]}x{img.size[1]} px\nRozmiar: {os.path.getsize(plik)//1024} KB"
                self.info_label.config(text=info)
                # Miniatura
                img.thumbnail((200, 200))
                self.miniatura = ImageTk.PhotoImage(img)
                self.miniatura_canvas.delete("all")
                self.miniatura_canvas.create_image(100, 112, image=self.miniatura)
        except Exception as e:
            self.info_label.config(text=f"Błąd odczytu: {e}")
            self.miniatura_canvas.delete("all")

    # =========================================
    # Obsługa zamykania aplikacji na macOS
    # =========================================
    def on_quit(self):
        """
        Obsługa zamykania aplikacji na macOS.
        """
        self.root.quit()    # =========================================
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
                    ("Wszystkie pliki", "*.*")
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
                    ("Wszystkie pliki", "*.*")
                ]
            
            pliki = filedialog.askopenfilenames(
                title="Wybierz pliki do konwersji",
                filetypes=filetypes
            )
            if pliki:  # Sprawdź czy użytkownik wybrał jakieś pliki
                self.dodaj_pliki(pliki)
        except Exception as e:
            self.log(f"Błąd podczas wyboru plików: {e}")
            messagebox.showerror("Błąd", f"Nie można otworzyć dialogu wyboru plików: {e}")

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
        obslugiwane = ('.heic', '.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.gif')
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
            self.lista_plikow.delete(idx)    # =========================================
    # Wybór folderu docelowego
    # =========================================
    def wybierz_folder_docelowy(self):
        """
        Otwiera okno dialogowe do wyboru folderu docelowego zapisu plików.
        """
        try:
            nowy_folder = filedialog.askdirectory(
                initialdir=self.folder_docelowy,
                title="Wybierz folder docelowy"
            )
            if nowy_folder:
                # Normalizuj ścieżkę dla systemu
                self.folder_docelowy = os.path.normpath(nowy_folder)
                self.log(f"Wybrano folder docelowy: {self.folder_docelowy}")
        except Exception as e:
            self.log(f"Błąd podczas wyboru folderu: {e}")
            messagebox.showerror("Błąd", f"Nie można otworzyć dialogu wyboru folderu: {e}")

    # =========================================
    # Sprawdzanie uprawnień systemu
    # =========================================
    def sprawdz_uprawnienia_zapisu(self, folder):
        """
        Sprawdza czy aplikacja ma uprawnienia do zapisu w danym folderze.
        """
        try:
            test_file = os.path.join(folder, "test_write_permission.tmp")
            with open(test_file, 'w') as f:
                f.write("test")
            os.remove(test_file)
            return True
        except (PermissionError, OSError) as e:
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
        self.log("Anulowano konwersję!")    # =========================================
    # Rozpoczęcie procesu konwersji (w osobnym wątku)
    # =========================================
    def rozpocznij_konwersje(self):
        """
        Rozpoczyna konwersję plików w osobnym wątku, blokuje przycisk konwersji.
        """
        if not hasattr(self, 'folder_docelowy'):
            messagebox.showerror("Błąd", "Wybierz folder docelowy!")
            return
        if not self.pliki_do_konwersji:
            messagebox.showerror("Błąd", "Dodaj pliki do konwersji!")
            return
          # Sprawdź uprawnienia do zapisu
        if not self.sprawdz_uprawnienia_zapisu(self.folder_docelowy):
            messagebox.showerror("Błąd", 
                f"Brak uprawnień do zapisu w folderze:\n{self.folder_docelowy}\n\n"
                "Wybierz inny folder lub uruchom aplikację z uprawnieniami administratora.")
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
                    "WEBP": ".webp"
                }[format_out]
                
                # Użyj os.path.join i normalizuj ścieżkę
                plik_docelowy = os.path.normpath(
                    os.path.join(self.folder_docelowy, f"{nazwa_pliku}{ext}")
                )
                if os.path.exists(plik_docelowy):
                    if not messagebox.askyesno("Plik istnieje", f"Plik {nazwa_pliku}{ext} już istnieje. Czy chcesz go nadpisać?"):
                        continue
                self.log(f"Konwertowanie: {plik_zrodlowy}")
                try:
                    with Image.open(plik_zrodlowy) as img:
                        img.thumbnail((200, 200))
                        self.miniatura = ImageTk.PhotoImage(img)
                        self.miniatura_canvas.delete("all")
                        self.miniatura_canvas.create_image(100, 100, image=self.miniatura)
                except Exception:
                    self.miniatura_canvas.delete("all")
                try:
                    with Image.open(plik_zrodlowy) as img:
                        img.verify()
                    with Image.open(plik_zrodlowy) as img:
                        if format_out == "JPEG":
                            img.save(plik_docelowy, format_out, quality=self.jakosc_var.get(), subsampling=0)
                        elif format_out == "PNG":
                            img.save(plik_docelowy, format_out, compress_level=1)
                        else:
                            img.save(plik_docelowy, format_out)
                except (OSError, SyntaxError) as e:
                    self.log(f"Plik uszkodzony lub nieobsługiwany: {plik_zrodlowy}: {str(e)}")
                    bledy += 1
                    continue
                self.log(f"Zapisano: {plik_docelowy}")
                sukcesy += 1
                self.pasek_postepu["value"] = i + 1
                self.root.title(f"Konwersja: {i+1}/{total}")
                if (i+1) % 5 == 0 or i == total-1:
                    self.root.update()
            except Exception as e:
                self.log(f"Błąd podczas konwersji {plik_zrodlowy}: {str(e)}")
                self.logger.error(f"Błąd podczas konwersji {plik_zrodlowy}: {str(e)}")
                bledy += 1
        self.konwertuj_btn.config(state=tk.NORMAL)
        self.anuluj_btn.config(state=tk.DISABLED)
        self.root.title("Konwerter plików graficznych")
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
        ttk.Label(okno, text="Twoje pliki zostały przekonwertowane i zapisane!", anchor="center", justify="center", font=("Arial", 12)).pack(pady=20)
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
# Funkcja główna
# =========================================
def main():
    """Główna funkcja uruchamiająca aplikację"""
    # Tworzy główne okno aplikacji (z obsługą drag&drop jeśli dostępne)
    if TkinterDnD is not None:
        root = TkinterDnD.Tk()
    else:
        root = tk.Tk()
    app = KonwerterHEIC(root)
    root.mainloop()

# =========================================
# Uruchomienie aplikacji
# =========================================
if __name__ == "__main__":
    main()
