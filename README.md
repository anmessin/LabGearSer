# LabGearSer

Libreria Python (`labgearser`) per il controllo remoto di strumentazione da banco via SCPI.

## Strumenti supportati

| Strumento | Classe | Tipo | Interfaccia | Backend VISA |
|---|---|---|---|---|
| Agilent E3631A | `AgilentE3631A` | Alimentatore DC triplo | RS-232 | `pyvisa-py` (incluso) |
| RS PRO RS-KEL103 | `RSProRSKEL103` | Carico elettronico DC | USB-seriale | `pyvisa-py` (incluso) |
| Keysight 34460A | `Keysight34460A` | Multimetro digitale | USBTMC | libreria VISA di sistema (vedi sotto) |

## Requisiti

- **Keysight 34460A**: una libreria VISA di sistema installata separatamente.

## Installazione

### Sviluppo della libreria

```powershell
git clone https://github.com/anmessin/LabGearSer.git
cd LabGearSer
python -m venv .venv
.venv\Scripts\activate
pip install -e .
```

## Struttura del progetto

```
src/labgearser/
├── agilent_e3631a.py    # driver alimentatore Agilent E3631A
├── rspro_rskel103.py    # driver carico elettronico RS-KEL103
└── keysight_34460a.py   # driver multimetro Keysight 34460A
docs/
├── commits_convention.md
└── datasheet.md         # elenco dei manuali dei produttori
main.py                  # esempio d'uso
```

## Datasheet

L'elenco dei documenti e la cartella dove salvarli in locale sono in [docs/datasheet.md](docs/datasheet.md).

## Note

- La libreria assume accesso esclusivo da remoto allo strumento per tutta la durata della connessione: né altri client né il pannello frontale devono modificarne lo stato nel frattempo. I driver si affidano a questa assunzione per tenere in cache alcuni stati (es. l'uscita selezionata sull'alimentatore), evitando interrogazioni ripetute dello strumento.