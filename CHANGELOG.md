# Lista zmian

Wszystkie istotne zmiany w projekcie będą dokumentowane w tym pliku.

Format oparty na [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
projekt przestrzega [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 23-05-2025

### Dodano
- Interfejs graficzny z wykorzystaniem Tkinter
- Obsługa wielu formatów wejściowych (HEIC, JPG, JPEG, PNG, BMP, TIFF, GIF)
- Konwersja do formatów: JPEG, PNG, BMP, TIFF, WEBP
- Obsługa przeciągania i upuszczania plików (drag & drop)
- Podgląd miniatur i szczegółów plików
- Regulacja jakości dla formatu JPEG
- Pasek postępu konwersji
- Logi operacji
- Możliwość anulowania konwersji
- Obsługa błędów i duplikatów
- Centrowanie okien dialogowych
- Pełna dokumentacja w README
- Wsparcie dla współtwórców (CONTRIBUTING.md)
- Licencja MIT

### Zmienione
- Zwiększona wysokość okna aplikacji (+30px)
- Poprawione rozmieszczenie elementów interfejsu
- Dodane scrollbary do list
- Wycentrowane okno sukcesu

### Poprawione
- Obsługa nieprawidłowych plików graficznych
- Filtrowanie duplikatów po nazwie pliku
- Wykrywanie uszkodzonych plików
- Zabezpieczenie przed nadpisywaniem plików

### Techniczne
- Dodano obsługę wątków dla operacji konwersji
- Zoptymalizowano wyświetlanie miniatur
- Dodano logger dla śledzenia błędów
- Utworzono plik requirements.txt z zależnościami
