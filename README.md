# Wealth Vision – Batch Generator per Ideogram (macOS)

Questa app Streamlit genera in blocco immagini usando l’API Ideogram. Non contiene nessuna chiave API nel codice: la chiede all’avvio.

## Installazione

1. Assicurati di avere Python 3 installato su macOS.
2. Apri Terminale e vai nella cartella del progetto.
3. Installa le dipendenze:

   ```bash
   pip3 install -r requirements.txt
   ```

## Avvio

1. Rendi eseguibile lo script di avvio:

   ```bash
   chmod +x avvia_wealth_vision.sh
   ```

2. Avvia l’app con lo script:

   ```bash
   ./avvia_wealth_vision.sh
   ```

   Dopo pochi secondi si aprirà il browser all’indirizzo `http://localhost:8501`.

In alternativa puoi lanciare manualmente Streamlit:

```bash
python3 -m streamlit run wealth_vision_app.py
```

## Uso dell’app

- Inserisci la tua **API key Ideogram** nel campo apposito.
- Inserisci i prompt (uno per riga) nel riquadro.
- Premi **Genera Immagini**.
- Alla fine fai clic su **Scarica tutte le immagini (ZIP)** per ottenere un archivio con tutte le immagini generate.
