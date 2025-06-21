# API Documentation - ImageFlow

## 🔌 Rozszerzanie funkcjonalności

ImageFlow został zaprojektowany z myślą o rozszerzalności. Poniżej znajduje się dokumentacja wewnętrznego API.

## Klasy publiczne

### ImageFlow

Główna klasa aplikacji.

#### Inicjalizacja
```python
app = ImageFlow(root)
```

#### Publiczne metody

##### `dodaj_pliki(pliki: List[str])`
Dodaje pliki do listy konwersji.
- **Parametry**: `pliki` - lista ścieżek do plików
- **Zwraca**: None
- **Przykład**:
```python
app.dodaj_pliki(["/path/to/image1.heic", "/path/to/image2.jpg"])
```

##### `rozpocznij_konwersje()`
Rozpoczyna proces konwersji plików.
- **Zwraca**: None
- **Wyjątki**: Może rzucić `PermissionError` jeśli brak uprawnień

##### `wybierz_folder_docelowy()`
Otwiera dialog wyboru folderu docelowego.
- **Zwraca**: None

#### Publiczne właściwości

##### `pliki_do_konwersji: List[str]`
Lista plików oczekujących na konwersję.

##### `folder_docelowy: str`
Ścieżka do folderu gdzie będą zapisane pliki.

##### `format_var: tk.StringVar`
Zmienna przechowująca wybrany format wyjściowy.

##### `jakosc_var: tk.IntVar`
Zmienna przechowująca jakość konwersji (0-100).

---

### ThemeManager

Zarządza motywami aplikacji.

#### Inicjalizacja
```python
theme_manager = ThemeManager(root)
```

#### Publiczne metody

##### `register_widget(widget, widget_type: str)`
Rejestruje widget do automatycznej aktualizacji motywu.
- **Parametry**: 
  - `widget` - widget Tkinter
  - `widget_type` - typ widgetu ("listbox", "text", "canvas", "frame")
- **Przykład**:
```python
theme_manager.register_widget(my_listbox, "listbox")
```

##### `toggle_theme()`
Przełącza między jasnym a ciemnym motywem.
- **Zwraca**: None

##### `apply_theme()`
Aplikuje aktualny motyw do wszystkich komponentów.
- **Zwraca**: None

#### Publiczne właściwości

##### `is_dark: bool`
Czy aktualnie używany jest ciemny motyw.

##### `themes: Dict`
Słownik z konfiguracją kolorów dla motywów.

---

### ToolTip

Dodaje interaktywne podpowiedzi do widgetów.

#### Inicjalizacja
```python
tooltip = ToolTip(widget, "Tekst podpowiedzi", theme_manager)
```

#### Parametry konstruktora
- `widget` - widget do którego dodajemy tooltip
- `text` - tekst podpowiedzi
- `theme_manager` - (opcjonalny) manager motywów

---

### LoadingSpinner

Animowany wskaźnik ładowania.

#### Inicjalizacja
```python
spinner = LoadingSpinner(parent, size=32, theme_manager=None)
```

#### Publiczne metody

##### `start()`
Rozpoczyna animację spinnera.

##### `stop()`
Zatrzymuje animację spinnera.

##### `create_spinner()`
Tworzy canvas ze spinnerem.
- **Zwraca**: `tk.Canvas`

---

## Callbacks i zdarzenia

### Dostępne zdarzenia

#### `<<ThemeChanged>>`
Wywoływane po zmianie motywu.

#### `<<FileAdded>>`
Wywoływane po dodaniu pliku do listy.

#### `<<ConversionStarted>>`
Wywoływane na początku konwersji.

#### `<<ConversionCompleted>>`
Wywoływane po zakończeniu konwersji.

### Przykład rejestracji callbacku
```python
def on_theme_changed(event):
    print("Motyw został zmieniony!")

app.root.bind("<<ThemeChanged>>", on_theme_changed)
```

---

## Rozszerzanie formatów

### Dodawanie nowego formatu wyjściowego

1. Zaktualizuj listę w `format_box`:
```python
values=["JPEG", "PNG", "BMP", "TIFF", "WEBP", "NOWY_FORMAT"]
```

2. Dodaj obsługę w `konwertuj_pliki()`:
```python
ext = {
    "JPEG": ".jpg",
    "PNG": ".png",
    # ... inne formaty
    "NOWY_FORMAT": ".nowy"
}
```

3. Dodaj specjalną logikę zapisu jeśli potrzebna:
```python
if format_out == "NOWY_FORMAT":
    # Specjalna logika dla nowego formatu
    img.save(plik_docelowy, format_out, special_param=value)
```

---

## Konfiguracja systemowa

### Dodawanie obsługi nowego systemu

```python
# Wykrywanie systemu
IS_NEW_SYSTEM = SYSTEM_OS == "NewSystem"

# W metodzie konfiguruj_system_operacyjny()
elif IS_NEW_SYSTEM:
    # Konfiguracja specyficzna dla nowego systemu
    pass

# W metodzie pobierz_domyslny_folder()
elif IS_NEW_SYSTEM:
    return os.path.join(home, "Documents")
```

---

## Przykłady użycia

### Batch processing z API
```python
import tkinter as tk
from app import ImageFlow

# Utwórz aplikację
root = tk.Tk()
app = ImageFlow(root)

# Ustaw pliki i parametry programowo
app.dodaj_pliki([
    "/path/to/photo1.heic",
    "/path/to/photo2.heic"
])
app.folder_docelowy = "/path/to/output"
app.format_var.set("JPEG")
app.jakosc_var.set(90)

# Rozpocznij konwersję
app.rozpocznij_konwersje()

# Uruchom GUI
root.mainloop()
```

### Niestandardowy motyw
```python
# Dodaj nowy motyw
app.theme_manager.themes["custom"] = {
    "bg": "#f0f0f0",
    "fg": "#333333",
    # ... inne kolory
}

# Zastosuj motyw
app.theme_manager.apply_theme()
```
