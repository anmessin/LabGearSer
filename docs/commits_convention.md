# Conventional Commits
Guida al formato dei commit per questo progetto: `labgearser`, libreria Python per il controllo remoto di strumentazione da banco (alimentatori, carichi elettronici, multimetri) via SCPI.

## Struttura del messaggio
Ogni messaggio di commit deve avere una struttura di questo tipo:

```
<type>(<scope>): <description>

[<body>]
```
**Obbligatori:** `type` e `description`.  
**Opzionali:** `scope` e `body`.

## Type
Il tipo descrive la natura della modifica ed è obbligatorio. Di seguito l'elenco dei `type` usati:
- `fix`      : è stato corretto un bug nel codice.
- `feat`     : è stata introdotta una nuova funzionalità.
- `build`    : è stato modificato il sistema di build o le dipendenze (es. il file `pyproject.toml`).
- `chore`    : manutenzione generica che non modifica il codice (es. il file `.gitignore`).
- `docs`     : è stata modificata la documentazione (`README.md`, file in `docs/`, docstring).
- `perf`     : modifica al codice con il solo scopo di renderlo più performante.
- `refactor` : modifica al codice che non altera il comportamento della libreria. Rientrano qui anche le modifiche alla struttura delle cartelle.
- `revert`   : annulla un commit precedente.
- `style`    : modifica esclusivamente estetica (es. formattazione, commenti, ordine in cui sono definiti i metodi). Le rinomine di funzioni/variabili non rientrano qui, ma in `refactor`.

Per cambiamenti incompatibili con la versione precedente si usa:
- `!` dopo il tipo (es. `feat!`, `refactor!`)
- oppure una sezione nel body: `BREAKING CHANGE: descrizione`

## Scope
Gli scope identificano le parti di codice interessate dalla modifica.

| Scope    | Area del progetto                                  | Path
|----------|----------------------------------------------------|----------------------------------------
| `e3631a` | Driver alimentatore Agilent E3631A                 | `src/labgearser/agilent_e3631a.py`
| `kel103` | Driver carico elettronico RS PRO RS-KEL103         | `src/labgearser/rspro_rskel103.py`
| `34460a` | Driver multimetro Keysight 34460A                  | `src/labgearser/keysight_34460a.py`
| `lib`    | Package nel suo insieme o più driver insieme       | `src/labgearser/` (es. `__init__.py`)
| `main`   | Script di esempio d'uso della libreria             | `main.py`
| `readme` | Documentazione generale                            | `README.md`
| `docs`   | Documentazione di supporto                         | `docs/`

### Regole
Queste regole mettono in relazione i `type` con gli `scope`.
1. Gli scope `readme` e `docs` si usano solo con i type `docs` e `revert`. Tutte le modifiche a `README.md` ricadono in `docs(readme)`, quelle ai file in `docs/` in `docs(docs)`; `revert(readme)` annulla un commit relativo allo scope `readme`.
2. Le docstring e i commenti di un driver usano lo scope del driver (es. `docs(e3631a)`, `style(kel103)`).
3. Se una modifica tocca un solo driver, si usa lo scope di quel driver; se ne tocca più di uno, si usa `lib`.
4. I type `build` e `chore` sono globali e non richiedono scope.

## Description
Breve riassunto della modifica sulla stessa riga del tipo. Regole:

- Inizia con un **verbo all'imperativo** (`add`, `fix`, `remove`, `update`, `refactor`…)
- In **minuscolo**, senza punto finale
- Non supera i **72 caratteri**
- Risponde alla domanda: *"Cosa fa questo commit?"*