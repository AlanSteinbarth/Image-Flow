# Konwerter plików graficznych

Aplikacja umożliwia konwersję plików graficznych (HEIC, JPG, JPEG, PNG, BMP, TIFF, GIF) do wybranego formatu (JPEG, PNG, BMP, TIFF, WEBP) z możliwością ustawienia jakości wyjściowej. Program posiada przyjazny interfejs graficzny i obsługuje przeciąganie i upuszczanie plików.

## Funkcje programu

- Konwersja wielu formatów plików:
  - Formaty wejściowe: HEIC, JPG, JPEG, PNG, BMP, TIFF, GIF
  - Formaty wyjściowe: JPEG, PNG, BMP, TIFF, WEBP
- Zaawansowany interfejs użytkownika:
  - Wybór wielu plików (dialog lub drag&drop)
  - Podgląd miniatury i szczegółów pliku
  - Lista wybranych plików ze scrollbarem
  - Możliwość usuwania plików z listy
- Kontrola nad konwersją:
  - Wybór formatu wyjściowego
  - Regulacja jakości dla formatu JPEG (0-100%)
  - Wybór folderu docelowego
  - Możliwość anulowania konwersji
  - Pasek postępu i szczegółowe logi
- Obsługa błędów i zabezpieczenia:
  - Wykrywanie uszkodzonych plików
  - Ostrzeżenia przy nadpisywaniu
  - Filtrowanie duplikatów

## Wymagania systemowe

- Python 3.8 lub nowszy
- Windows/Linux/macOS
- Biblioteki: patrz requirements.txt

## Instalacja

1. Sklonuj repozytorium:
   ```
   git clone <adres-repo>
   cd konwerter-plikow-graficznych
   ```

2. Utwórz wirtualne środowisko (opcjonalnie, ale zalecane):
   ```
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Linux/macOS:
   source venv/bin/activate
   ```

3. Zainstaluj wymagane biblioteki:
   ```
   pip install -r requirements.txt
   ```

## Uruchomienie

W katalogu z programem uruchom:
```
python app.py
```

## Licencja

Program jest dostępny na licencji MIT. Szczegóły w pliku LICENSE.

## Autor

Alan Steinbarth
