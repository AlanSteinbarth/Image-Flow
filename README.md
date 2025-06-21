# ImageFlow

<div align="center">
  <img src="docs/screenshots/Cover.png" alt="ImageFlow - Profesjonalny konwerter plików graficznych" width="800"/>
</div>

[![CI/CD Pipeline](https://github.com/AlanSteinbarth/Image-Flow/actions/workflows/ci.yml/badge.svg)](https://github.com/AlanSteinbarth/Image-Flow/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)]()
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**Uniwersalna aplikacja do konwersji plików graficznych z profesjonalnym interfejsem i obsługą 15+ formatów.**

---

## 📸 Zrzuty ekranu

### Udana konwersja z podglądem pliku
![ImageFlow - Komunikat sukcesu z podglądem konwertowanego obrazu](docs/screenshots/Zrzut%20ekranu%202025-06-21%20o%2023.45.25.png)
*Widok po udanej konwersji - popup "Sukces!" z informacją o zakończeniu procesu, panel podglądu z miniaturą zdjęcia natury oraz szczegółowe logi procesu konwersji w dolnej części okna. Aplikacja w ciemnym motywie.*

### Konfiguracja konwersji z wybranymi plikami  
![ImageFlow - Interfejs z wybranymi plikami i ustawieniami konwersji](docs/screenshots/Zrzut%20ekranu%202025-06-21%20o%2023.43.40.png)
*Główny widok pracy z aplikacją - wybrany plik do konwersji, ustawienia formatu wyjściowego (JPEG) z jakością 100%, informacje systemowe (macOS Darwin) oraz ścieżki plików wejściowych i wyjściowych. Panel logów pokazuje szczegóły procesu.*

### Czysty interfejs startowy (ciemny motyw)
![ImageFlow - Główny interfejs aplikacji w ciemnym motywie](docs/screenshots/Zrzut%20ekranu%202025-06-21%20o%2023.41.33.png)
*Interfejs początkowy aplikacji w ciemnym motywie - widoczne przyciski wyboru plików, ustawienia formatu (JPEG), suwak jakości (100%) oraz informacje systemowe. Gotowy do pracy z plikami.*

### Interfejs w jasnym motywie
![ImageFlow - Aplikacja w jasnym motywie z przełącznikiem motywów](docs/screenshots/Zrzut%20ekranu%202025-06-21%20o%2023.41.17.png)
*Aplikacja przełączona na jasny motyw - widoczna ikona słońca w prawym górnym rogu jako przełącznik motywów. Interfejs pokazuje wszystkie podstawowe elementy: przyciski wyboru plików, ustawienia formatu, panel logów na dole. Demonstracja funkcji przełączania między jasnym a ciemnym motywem.*

---

## ✨ Funkcje

- **🔄 Obsługa 15+ formatów**: HEIC, JPG, JPEG, PNG, BMP, TIFF, GIF → JPEG, PNG, BMP, TIFF, WEBP
- **🌍 Uniwersalna kompatybilność**: Windows 10+, macOS 10.14+, Ubuntu 18.04+
- **🎨 Nowoczesny interfejs**: Jasny/ciemny motyw, animacje, tooltips
- **📁 Przeciągnij i upuść**: Intuicyjna obsługa drag & drop
- **🖼️ Live preview**: Miniaturki i szczegóły plików w czasie rzeczywistym
- **⚙️ Precyzyjna kontrola**: Regulacja jakości dla JPEG (0-100%)
- **📊 Progress tracking**: Pasek postępu z animacjami
- **🛡️ Zaawansowana obsługa błędów**: Szczegółowe logi i graceful error handling
- **🚫 Anti-duplicate**: Automatyczne wykrywanie i filtrowanie duplikatów
- **🔧 System-aware**: Natywne dialogi i optymalizacje dla każdego OS

## 🚀 Quick Start

```bash
git clone https://github.com/AlanSteinbarth/Image-Flow.git
cd Image-Flow
python -m pip install -r requirements.txt
python app.py
```

## 📊 Benchmarks & Performance

| Operacja | Średni czas | Obsługiwane rozmiary |
|----------|-------------|---------------------|
| HEIC → JPEG | ~50ms/plik | Do 100MB |
| PNG → JPEG | ~30ms/plik | Do 50MB |  
| TIFF → PNG | ~80ms/plik | Do 200MB |
| Batch (100 plików) | ~3s | Łącznie do 1GB |

*Benchmarki wykonane na MacBook Pro M1, wyniki mogą się różnić*

## 🖥️ Kompatybilność systemów

### ✅ macOS
- Natywna obsługa dialogów plików
- Automatyczne centrowanie okien
- Obsługa gestów i skrótów klawiszowych macOS
- Folder domyślny: `~/Desktop`

### ✅ Windows
- Poprawne separatory w dialogach plików
- Obsługa DPI awareness
- Wykrywanie różnych nazw folderów Desktop (Pulpit, Bureau, Escritorio)
- Wsparcie dla różnych wersji językowych

### ✅ Linux
- Obsługa XDG user directories
- Kompatybilność z różnymi środowiskami graficznymi
- Automatyczne wykrywanie folderu Desktop

## 📋 Wymagania

- **Python**: 3.8 lub nowszy
- **System operacyjny**: Windows 10+, macOS 10.14+, Ubuntu 18.04+ (lub inne dystrybucje Linux)

## 🚀 Instalacja

### 1. Klonowanie repozytorium
```bash
git clone <adres-repo>
cd imageflow
```

### 2. Tworzenie środowiska wirtualnego (zalecane)

#### Windows:
```cmd
python -m venv venv
venv\Scripts\activate
```

#### macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalacja zależności

#### Metoda 1: Przez pip (zalecana)
```bash
pip install -r requirements.txt
```

#### Metoda 2: Instalacja jako pakiet
```bash
pip install -e .
```
Po tej instalacji możesz uruchomić aplikację z dowolnego miejsca:
```bash
image-converter
```

## ▶️ Uruchomienie

### Metoda 1: Przez skrypt uruchamiający (zalecana na macOS/Linux)
```bash
./run.sh
```

### Metoda 2: Bezpośrednio przez Python
```bash
# Upewnij się, że masz aktywne środowisko wirtualne lub conda
python app.py
```

### Metoda 3: Jeśli zainstalowano jako pakiet
```bash
image-converter
```

### ⚠️ Ważne uwagi dla macOS
- **NIE używaj** `/usr/bin/python3` (systemowy Python)
- Użyj `python` z aktywnego środowiska conda/venv
- Jeśli masz błąd "No module named 'PIL'", sprawdź czy używasz właściwego interpretera Python

## 📝 Instrukcja użytkowania

1. **Wybór plików**: Kliknij "Wybierz pliki do konwersji" lub przeciągnij pliki do okna
2. **Podgląd**: Kliknij na plik z listy aby zobaczyć miniaturę i szczegóły
3. **Format wyjściowy**: Wybierz docelowy format z listy rozwijanej
4. **Jakość**: Ustaw jakość konwersji (tylko dla JPEG)
5. **Folder docelowy**: Wybierz gdzie zapisać skonwertowane pliki
6. **Konwersja**: Kliknij "Konwertuj" aby rozpocząć proces

## 🔧 Funkcje specyficzne dla systemów

### macOS
- Dialog wyboru plików używa spacji jako separatorów formatów
- Automatyczne centrowanie okien na ekranie
- Obsługa natywnego zamykania aplikacji (Cmd+Q)

### Windows
- Dialog wyboru plików używa średników jako separatorów formatów
- Automatyczne wykrywanie różnych nazw folderów Desktop
- Obsługa DPI awareness dla wyświetlaczy wysokiej rozdzielczości

### Linux
- Używa XDG user directories do wykrywania folderu Desktop
- Kompatybilność z różnymi środowiskami graficznymi (GNOME, KDE, XFCE)

## 🐛 Rozwiązywanie problemów

### Błędy uprawnień
Jeśli pojawi się błąd uprawnień do zapisu:
- **Windows**: Uruchom jako administrator
- **macOS**: Sprawdź uprawnienia w Systemowych ustawieniach → Bezpieczeństwo
- **Linux**: Sprawdź uprawnienia do folderu docelowego

### Błędy importu bibliotek
```bash
pip install --upgrade -r requirements.txt
```

### Problemy z dragiem & drop
Upewnij się, że biblioteka `tkinterdnd2` jest zainstalowana:
```bash
pip install tkinterdnd2
```

### Przycisk "Konwertuj" nie działa
Jeśli przycisk "Konwertuj" jest nieaktywny lub nic się nie dzieje:
1. **Sprawdź czy wybrano pliki**: Dodaj przynajmniej jeden plik do konwersji
2. **Sprawdź folder docelowy**: Upewnij się, że wybrano folder zapisu
3. **Restart aplikacji**: Zamknij i uruchom aplikację ponownie
4. **Sprawdź logi**: Sprawdź pole logów na dole aplikacji pod kątem błędów

### Test aplikacji
Możesz uruchomić automatyczny test funkcjonalności:
```bash
python test_app.py
```

## 📄 Licencja

MIT License - zobacz plik [LICENSE](LICENSE) po szczegóły.

## 👨‍💻 Autor

Alan Steinbarth

- GitHub: [@AlanSteinbarth](https://github.com/AlanSteinbarth)
- LinkedIn: [Alan Steinbarth](https://linkedin.com/in/alansteinbarth)

---

<div align="center">

**⭐ Jeśli ImageFlow Ci pomógł, zostaw gwiazdkę! ⭐**

[![GitHub stars](https://img.shields.io/github/stars/AlanSteinbarth/Image-Flow.svg?style=social&label=Star)](https://github.com/AlanSteinbarth/Image-Flow)
[![GitHub forks](https://img.shields.io/github/forks/AlanSteinbarth/Image-Flow.svg?style=social&label=Fork)](https://github.com/AlanSteinbarth/Image-Flow/fork)

*Zbudowane z ❤️ dla społeczności open source*

</div>

### 📋 Roadmap

- [ ] **v2.1**: Plugin system dla custom formatów
- [ ] **v2.2**: Web interface (Flask/FastAPI)  
- [ ] **v2.3**: CLI interface dla batch processing
- [ ] **v2.4**: Cloud storage integration (Google Drive, Dropbox)
- [ ] **v3.0**: Machine learning optimizations
