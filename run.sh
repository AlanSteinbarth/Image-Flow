#!/bin/bash
# Skrypt uruchamiający aplikację ImageFlow

echo "🚀 Uruchamianie ImageFlow..."

# Przejdź do katalogu aplikacji
cd "$(dirname "$0")"

# Sprawdź czy Python jest dostępny
if command -v python3 &> /dev/null; then
    echo "✅ Używam Python3"
    python3 app.py
elif command -v python &> /dev/null; then
    echo "✅ Używam Python"
    python app.py
else
    echo "❌ Python nie jest zainstalowany lub nie jest w PATH"
    exit 1
fi

echo "👋 Aplikacja zakończona"
