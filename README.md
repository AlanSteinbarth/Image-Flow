# Konwerter plików graficznych

Uniwersalna aplikacja do konwersji plików graficznych z obsługą Windows, macOS i Linux.

## ✨ Funkcje

- **Obsługa wielu formatów**: HEIC, JPG, JPEG, PNG, BMP, TIFF, GIF → JPEG, PNG, BMP, TIFF, WEBP
- **Uniwersalna kompatybilność**: Windows, macOS, Linux
- **Intuicyjny interfejs**: Graficzny interfejs użytkownika (GUI) w Tkinter
- **Przeciągnij i upuść**: Obsługa drag & drop plików
- **Podgląd plików**: Miniaturki i szczegóły plików
- **Kontrola jakości**: Regulacja jakości dla JPEG (0-100%)
- **Pasek postępu**: Śledzenie konwersji w czasie rzeczywistym
- **Obsługa błędów**: Szczegółowe logi i obsługa błędów
- **Wykrywanie duplikatów**: Automatyczne filtrowanie duplikatów

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
cd konwerter-plikow-graficznych
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

## 🤝 Wkład w projekt

Jesteś mile widziany do współpracy! Możesz:
- Zgłaszać błędy i problemy
- Proponować nowe funkcje
- Tworzyć pull requesty z poprawkami
- Testować aplikację na różnych systemach operacyjnych
