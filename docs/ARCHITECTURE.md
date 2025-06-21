# Architektura ImageFlow

## 🏗️ Przegląd architektury

ImageFlow to aplikacja desktopowa zbudowana w architekturze MVC (Model-View-Controller) z wykorzystaniem wzorców projektowych:

### Wzorce projektowe:
- **Observer Pattern**: ThemeManager powiadamia widgety o zmianie motywu
- **Strategy Pattern**: Różne strategie eksportu dla różnych formatów
- **Template Method**: Wspólny szablon dla procesu konwersji
- **Facade Pattern**: Uproszczony interfejs dla operacji na plikach

## 📦 Struktura klas

```
ImageFlow (Main Application)
├── ThemeManager (Zarządzanie motywami)
├── ToolTip (Tooltips)
├── LoadingSpinner (Animacje ładowania)
└── System-specific handlers
```

### Klasa ImageFlow
Główna klasa aplikacji odpowiedzialna za:
- Inicjalizację GUI
- Zarządzanie stanem aplikacji
- Koordynację między komponentami
- Obsługę zdarzeń użytkownika

### Klasa ThemeManager
Zarządza motywami aplikacji:
- Przechowuje konfiguracje kolorów
- Rejestruje widgety do aktualizacji
- Aplikuje zmiany motywu globalnie
- Animuje przejścia między motywami

### Klasa ToolTip
Zapewnia interaktywne podpowiedzi:
- Dynamiczne pozycjonowanie
- Animacje fade-in/fade-out
- Integracja z systemem motywów

### Klasa LoadingSpinner
Animowany wskaźnik postępu:
- Niestandardowe renderowanie na Canvas
- Płynne animacje 60 FPS
- Dostosowanie do aktualnego motywu

## 🔄 Przepływ danych

```
User Input → ImageFlow → File Processing → Progress Update → UI Update
     ↑                                                           ↓
     └──────────────── User Feedback ←──────────────────────────┘
```

## 🎨 System motywów

### Rejestracja widgetów
```python
# Widgety rejestrują się do aktualizacji motywu
theme_manager.register_widget(widget, "type")
```

### Dostępne typy widgetów:
- `listbox`: Listy plików
- `text`: Pola tekstowe
- `canvas`: Obszary rysowania
- `frame`: Ramki kontenerowe

## 🔧 Konfiguracja systemowa

### macOS
- Natywne dialogi plików
- Automatyczne centrowanie okien
- Obsługa gestów systemowych

### Windows
- DPI awareness
- Wykrywanie lokalizacji folderów
- Separatory dialogów plików

### Linux
- XDG user directories
- Kompatybilność środowisk graficznych

## 📊 Performance

### Optymalizacje:
- Lazy loading miniatur
- Asynchroniczne przetwarzanie plików
- Efektywne zarządzanie pamięcią
- Throttling aktualizacji UI

### Benchmarki:
- Konwersja HEIC → JPEG: ~50ms/plik
- Ładowanie miniatury: ~20ms
- Zmiana motywu: ~100ms

## 🧪 Testowanie

### Unit Tests:
- Testy logiki konwersji
- Testy zarządzania motywami
- Testy kompatybilności systemowej

### Integration Tests:
- Testy end-to-end workflow
- Testy interfejsu użytkownika
- Testy wydajności

## 🔐 Bezpieczeństwo

### Walidacja plików:
- Sprawdzanie rozszerzeń plików
- Walidacja integralności obrazów
- Ograniczenia rozmiaru plików

### Uprawnienia:
- Sprawdzanie uprawnień do zapisu
- Bezpieczne tworzenie plików tymczasowych
- Oczyszczanie po błędach
