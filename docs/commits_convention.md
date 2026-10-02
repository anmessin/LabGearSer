# Conventional Commits
Guida al formato dei commit per questo progetto: libreria personale per la comunicazione con strumentazione da banco (alimentatori, carichi elettronici, ecc.).

## Struttura del messaggio
Ogni messaggio di commit deve avere una struttura di questo tipo:

```
<type>(<scope>): <description>

[<body>]
```
**Obbligatori:** `type` e `description`.  
**Opzionale:** `scope` e `body`.

## Type
Il tipo descrive la natura della modifica. È obbligatorio nella struttura del messaggio di commit. Di seguito un elenco dei `type` usati:
- `fix`      : Usato quando è stato corretto un bug nel codice.
- `feat`     : Usato quando è stata introdotta una nuova funzionalità nel codice.
- `build`    : Usato quando è stata modificata la struttura al sistema di build o le dipendenze (es. modificato il file `pyproject.toml` o il file `requirements.txt`).
- `chore`    : Usato quando è stata fatta manutenzione generica che non modifica il codice (es. modificato il file `.gitignore`).
- `docs`     : Usato quando è stato modificata la documentazione.
- `perf`     : Usato quando è stata fatta una modificata al codice con il solo scopo di renderlo più performante.
- `refactor` : Usato quando è stata fatta una modificata al codice che non altera la logica del programma (es. passare da programmazione procedurale a object-oriented (OOP)). In questo type rientra anche il caso in cui si va a modificare la struttura delle cartelle.
- `revert`   : Usato quando deve essere annullato un commit precedente.
- `style`    : Usato quando è stata fatta una modifica al codice esclusivamente di carattere grafico (es. cambiato dei commenti, modificato ordine con cui le funzioni/metodi sono definiti). In questo type non rientrano i casi in cui si vanno a fare delle modifiche al nome di funzioni/variabili per renderle più esplicite; questo caso rientra nel type `refactor`.

Per cambiamenti incompatibili con la versione precedente è possibile usare:
- `!` dopo il tipo (es. `feat!`)
- oppure una sezione nel body: `BREAKING CHANGE: descrizione`

## Scope
Gli scope identificano le parti di codice interessate dalla modifica.

| Scope       | Area del progetto                               | Path
|-------------|-------------------------------------------------|-------------------------
| `strumenti` | Libreria driver per la strumentazione           | `strumenti/`
| `main`      | Script principale/esempio d'uso della libreria  | `main.py`
| `readme`    | Documentazione generale                         | `README.md`

### Regole
Queste sono delle regole di comportamento adottate nella stesura dei commit che mettono in relazione i `type` con gli `scope`.
1. Lo scope `readme` è utilizzabile solo con il type `docs` e `revert`. Per `docs` vuol dire che tutte le modifiche a `./README.md` ricadono in `docs(readme)`. Per `revert` vuol dire che `revert(readme)` annulla un commit relativo allo scope `readme`.
2. Il type `build` è globale e non richiede scope.
3. Il type `chore` è globale e non richiede scope.

## Description
Breve riassunto della modifica sulla stessa riga del tipo. Regole:
 
- Inizia con un **verbo all'imperativo** (`add`, `fix`, `remove`, `update`, `refactor`…)
- In **minuscolo**, senza punto finale
- Non supera i **72 caratteri**
- Risponde alla domanda: *"Cosa fa questo commit?"*

## Body
Il body spiega il **perché** della modifica e non il come. Va usato quando la description da sola non basta: scelte progettuali non ovvie, trade-off, abbandono di un approccio precedente.