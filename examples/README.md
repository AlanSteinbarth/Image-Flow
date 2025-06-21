# Przykłady użycia ImageFlow

## 📁 Przykładowe pliki

Ten folder zawiera przykładowe pliki graficzne do testowania aplikacji ImageFlow.

### Zawartość

- `sample_images/` - Przykładowe obrazy w różnych formatach
- `test_scenarios/` - Różne scenariusze testowe
- `benchmarks/` - Pliki do testów wydajności

## 🖼️ Przykładowe obrazy

### Małe pliki (< 1MB)
- `small_photo.jpg` - Standardowe zdjęcie JPEG
- `small_graphic.png` - Grafika PNG z przezroczystością
- `small_icon.bmp` - Prosta ikona BMP

### Średnie pliki (1-10MB)
- `medium_photo.heic` - Zdjęcie HEIC z iPhone
- `medium_document.tiff` - Skan dokumentu TIFF
- `medium_animation.gif` - Animowany GIF

### Duże pliki (10MB+)
- `large_photo.heic` - Wysokiej rozdzielczości HEIC
- `large_poster.png` - Plakat PNG wysokiej jakości

## 📋 Scenariusze testowe

### Scenariusz 1: Podstawowa konwersja
```bash
# Skonwertuj HEIC do JPEG z jakością 90%
Input: sample_images/small_photo.heic
Output Format: JPEG
Quality: 90%
Expected: Udana konwersja, rozmiar zredukowany o ~70%
```

### Scenariusz 2: Batch processing
```bash
# Skonwertuj wiele plików jednocześnie
Input: sample_images/*.heic
Output Format: PNG
Quality: 100%
Expected: Wszystkie pliki skonwertowane bez błędów
```

### Scenariusz 3: Test wydajności
```bash
# Zmierz czas konwersji dużego pliku
Input: sample_images/large_photo.heic
Output Format: JPEG
Quality: 85%
Expected: Konwersja < 5 sekund
```

### Scenariusz 4: Test błędów
```bash
# Próba konwersji uszkodzonego pliku
Input: test_scenarios/corrupted.jpg
Expected: Graceful error handling, informacja w logach
```

## 🔧 Jak używać przykładów

### 1. Automatyczne testy
```bash
cd examples/
python run_examples.py
```

### 2. Ręczne testowanie
1. Uruchom ImageFlow
2. Przeciągnij pliki z `sample_images/`
3. Wybierz format wyjściowy
4. Uruchom konwersję

### 3. Benchmarking
```bash
cd examples/benchmarks/
python benchmark.py
```

## 📊 Oczekiwane wyniki

### Konwersje HEIC → JPEG
- Redukcja rozmiaru: 60-80%
- Zachowanie jakości: 95%+
- Czas konwersji: 0.5-2s per plik

### Konwersje PNG → JPEG
- Możliwa utrata przezroczystości
- Redukcja rozmiaru: 70-90%
- Czas konwersji: 0.2-1s per plik

### Konwersje JPEG → PNG
- Zwiększenie rozmiaru: 20-50%
- Bez utraty jakości
- Czas konwersji: 0.3-1.5s per plik

## ❗ Uwagi

- Wszystkie przykładowe pliki są w domenie publicznej
- Rzeczywiste wyniki mogą się różnić w zależności od sprzętu
- Duże pliki (>50MB) mogą wymagać więcej czasu
- W przypadku błędów sprawdź logi w aplikacji
