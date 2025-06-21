# Contributing Guidelines

## 🤝 Jak przyczynić się do projektu ImageFlow

Dziękujemy za zainteresowanie projektem! Każdy wkład jest mile widziany.

## 📋 Przed rozpoczęciem

1. **Fork** repozytorium
2. **Clone** swojego forka lokalnie
3. Stwórz **nową gałąź** dla swojej funkcji
4. Sprawdź czy wszystkie **testy przechodzą**

## 🔧 Środowisko deweloperskie

### Wymagania
- Python 3.8+
- Wszystkie systemy: Windows, macOS, Linux

### Instalacja
```bash
git clone https://github.com/[twoj-username]/Image-Flow.git
cd Image-Flow
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt  # jeśli istnieje
```

### Uruchomienie testów
```bash
python -m pytest tests/
```

## 📝 Style kodowania

### Python
- Używamy **PEP 8** jako standardu
- Maksymalna długość linii: **88 znaków** (Black formatter)
- **Type hints** są mile widziane
- **Docstrings** dla wszystkich publicznych metod

### Formatowanie
```bash
# Auto-formatowanie (jeśli masz Black)
black app.py

# Sprawdzanie stylu
flake8 app.py
```

### Przykład dobrego stylu:
```python
def konwertuj_plik(
    plik_zrodlowy: str, 
    format_docelowy: str, 
    jakosc: int = 100
) -> bool:
    """
    Konwertuje pojedynczy plik do nowego formatu.
    
    Args:
        plik_zrodlowy: Ścieżka do pliku źródłowego
        format_docelowy: Format wyjściowy (JPEG, PNG, etc.)
        jakosc: Jakość kompresji (0-100)
        
    Returns:
        True jeśli konwersja się powiodła, False w przeciwnym przypadku
        
    Raises:
        FileNotFoundError: Jeśli plik źródłowy nie istnieje
        PermissionError: Jeśli brak uprawnień do zapisu
    """
    # Implementacja...
    return True
```

## 🐛 Zgłaszanie błędów

### Przed zgłoszeniem
1. Sprawdź czy błąd nie został już zgłoszony
2. Upewnij się że używasz najnowszej wersji
3. Przetestuj na "czystej" instalacji

### Template zgłoszenia błędu
```markdown
**Opis błędu**
Krótki opis tego co się dzieje.

**Kroki do reprodukcji**
1. Krok 1
2. Krok 2
3. ...

**Oczekiwane zachowanie**
Co powinno się stać.

**Aktualne zachowanie**
Co się faktycznie dzieje.

**Środowisko**
- OS: [Windows 10/macOS 12/Ubuntu 20.04]
- Python: [3.9.1]
- Wersja ImageFlow: [2.0.0]

**Dodatkowe informacje**
Logi, zrzuty ekranu, etc.
```

## ✨ Proponowanie nowych funkcji

### Przed implementacją
1. Otwórz **Issue** z opisem funkcji
2. Poczekaj na feedback od maintainerów
3. Omów implementację i API

### Template propozycji funkcji
```markdown
**Opis funkcji**
Co chcesz dodać i dlaczego.

**Przypadki użycia**
Konkretne scenariusze gdzie funkcja będzie przydatna.

**Proponowane API**
```python
# Przykład jak mogłoby to działać
app.nowa_funkcja(parametr1, parametr2)
```

**Alternatywy**
Czy rozważałeś inne sposoby rozwiązania problemu?
```

## 🔀 Pull Requests

### Przed PR
1. **Wszystkie testy** muszą przechodzić
2. **Dodaj testy** dla nowej funkcjonalności
3. **Zaktualizuj dokumentację**
4. **Sprawdź backwards compatibility**

### Template PR
```markdown
**Opis zmian**
Co ten PR robi.

**Typ zmiany**
- [ ] Bug fix
- [ ] Nowa funkcja
- [ ] Breaking change
- [ ] Dokumentacja

**Testy**
- [ ] Napisałem/zaktualizowałem testy
- [ ] Wszystkie testy przechodzą
- [ ] Przetestowałem na różnych systemach

**Checklist**
- [ ] Kod następuje style guidelines
- [ ] Przejrzałem własny kod
- [ ] Dodałem komentarze w trudnych miejscach
- [ ] Zaktualizowałem dokumentację
```

## 📖 Dokumentacja

### Co dokumentować
- Wszystkie **publiczne API**
- **Nowe funkcje** w README
- **Breaking changes** w CHANGELOG
- **Przykłady użycia**

### Format docstrings
```python
def metoda(param1: str, param2: int = 0) -> bool:
    """
    Jednoliniowy opis metody.
    
    Dłuższy opis jeśli potrzebny. Może być w kilku
    liniach i zawierać szczegóły implementacji.
    
    Args:
        param1: Opis pierwszego parametru
        param2: Opis drugiego parametru (domyślnie 0)
        
    Returns:
        Opis wartości zwracanej
        
    Raises:
        ValueError: Kiedy param1 jest pusty
        RuntimeError: W przypadku błędu systemu
        
    Example:
        >>> metoda("test", 5)
        True
    """
```

## 🧪 Testowanie

### Typy testów
1. **Unit tests** - testują pojedyncze funkcje
2. **Integration tests** - testują współpracę komponentów
3. **System tests** - testują całą aplikację

### Struktura testów
```
tests/
├── unit/
│   ├── test_theme_manager.py
│   ├── test_file_operations.py
│   └── test_gui_components.py
├── integration/
│   ├── test_conversion_flow.py
│   └── test_system_compatibility.py
└── fixtures/
    ├── sample_images/
    └── mock_data.py
```

### Przykład testu
```python
import unittest
from unittest.mock import patch, MagicMock
from app import ImageFlow

class TestImageFlow(unittest.TestCase):
    def setUp(self):
        """Przygotowanie przed każdym testem"""
        self.root = MagicMock()
        self.app = ImageFlow(self.root)
    
    def test_dodaj_pliki_valid(self):
        """Test dodawania prawidłowych plików"""
        pliki = ["/test/image1.jpg", "/test/image2.png"]
        
        with patch('os.path.isfile', return_value=True):
            self.app.dodaj_pliki(pliki)
            
        self.assertEqual(len(self.app.pliki_do_konwersji), 2)
    
    def test_dodaj_pliki_invalid_extension(self):
        """Test ignorowania plików z nieprawidłowym rozszerzeniem"""
        pliki = ["/test/document.pdf", "/test/image.txt"]
        
        with patch('os.path.isfile', return_value=True):
            self.app.dodaj_pliki(pliki)
            
        self.assertEqual(len(self.app.pliki_do_konwersji), 0)
```

## 🚀 Release Process

### Wersjonowanie
Używamy **Semantic Versioning**:
- `MAJOR.MINOR.PATCH`
- **MAJOR**: Breaking changes
- **MINOR**: Nowe funkcje (backwards compatible)
- **PATCH**: Bug fixes

### Przygotowanie release
1. Zaktualizuj `setup.py` z nową wersją
2. Zaktualizuj `CHANGELOG.md`
3. Tag commit: `git tag v2.1.0`
4. Push tag: `git push origin v2.1.0`

## 💬 Komunikacja

### Gdzie szukać pomocy
- **GitHub Issues** - błędy i pytania
- **GitHub Discussions** - ogólne dyskusje
- **Email**: alan.steinbarth@example.com (dla prywatnych spraw)

### Code of Conduct
- Bądź **szanujący** dla innych
- **Konstruktywna krytyka** jest mile widziana
- **Nie tolerujemy** dyskryminacji w żadnej formie

## 🏆 Uznanie

Wszyscy kontrybutorzy będą wymienieni w:
- `CONTRIBUTORS.md`
- Release notes
- README.md (dla znaczących wkładów)

**Dziękujemy za Twój wkład w ImageFlow! 🎉**
