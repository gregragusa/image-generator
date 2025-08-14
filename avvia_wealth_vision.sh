#!/bin/bash
# Script di avvio per Mac/Linux: lancia l'app e apre il browser

# Trova la cartella dello script
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Avvia Streamlit (usa python3 -m streamlit per evitare problemi di PATH)
python3 -m streamlit run "$SCRIPT_DIR/wealth_vision_app.py" --server.port 8501 &

# Attendi 10 secondi per permettere al server di avviarsi
sleep 10

# Prova ad aprire il browser
if command -v xdg-open >/dev/null; then
    xdg-open http://localhost:8501
elif command -v open >/dev/null; then
    open http://localhost:8501
else
    echo "App avviata. Apri manualmente http://localhost:8501 nel tuo browser."
fi
