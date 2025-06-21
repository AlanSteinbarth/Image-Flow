#!/bin/bash
# Skrypt uruchamiający aplikację ImageFlow
# Automatycznie aktywuje środowisko conda i uruchamia aplikację

echo "🚀 Uruchamianie ImageFlow..."

# Przejdź do katalogu aplikacji
cd "$(dirname "$0")"

# Sprawdź czy conda jest dostępne
if ! command -v conda &> /dev/null; then
    echo "❌ Conda nie jest zainstalowana lub nie jest w PATH"
    echo "Próbuję uruchomić z systemowym Pythonem..."
    python3 app.py
    exit $?
fi

# Aktywuj środowisko conda
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate od_zera_do_ai

# Sprawdź czy aktywacja się powiodła
if [ $? -ne 0 ]; then
    echo "❌ Nie można aktywować środowiska 'od_zera_do_ai'"
    echo "Próbuję uruchomić z aktualnym środowiskiem..."
    python app.py
    exit $?
fi

echo "✅ Środowisko 'od_zera_do_ai' aktywowane"
echo "🎯 Uruchamianie aplikacji..."

# Uruchom aplikację
python app.py

echo "👋 Aplikacja zakończona"
