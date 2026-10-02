# labgearser

Libreria Python personale per il controllo remoto di strumentazione da banco via SCPI.

## Strumenti supportati

| Strumento | Tipo | Interfaccia | Backend richiesto |
|---|---|---|---|
| Agilent E3631A | Alimentatore DC triplo | RS-232 | `pyvisa-py` (incluso) |
| RS-KEL103 (RS PRO) | Carico elettronico | USB-seriale | `pyvisa-py` (incluso) |
| Keysight 34460A | Multimetro digitale | USBTMC | libreria VISA di sistema (vedi sotto) |

## Requisiti

- Python >= 3.10
- Per il **Keysight 34460A**: serve una libreria VISA di sistema installata separatamente (NI-VISA o Keysight IO Libraries Suite).

## Installazione

In locale, per sviluppo (modalità editable):

```
pip install -e .
```

Da un altro progetto che vuole usare la libreria, direttamente da Git:

```
pip install git+https://github.com/<utente>/<repo>.git@<tag>
```

(sostituire `<utente>/<repo>` con il percorso del repository, e `<tag>` con la versione desiderata, es. `v0.1.0`)

## Note

- La libreria assume accesso esclusivo da remoto allo strumento per tutta la durata della connessione: nessun altro client o il pannello frontale non modifica lo stato nel frattempo. I driver si affidano a questa assunzione per mantenere in cache localmente alcuni stati (es. l'uscita selezionata sull'alimentatore), evitando interrogazioni ripetute dello strumento.