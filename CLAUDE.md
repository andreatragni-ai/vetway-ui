# vetway-ui

Pacchetto Django di sola presentazione (CSS, JS, `base.html`, partial,
template tag) condiviso da due ospiti: **VetWay** (`../vetcardio`, in
produzione) e **VetWay Consulti** (`../vetconsulti`, in sviluppo). Le regole
d'uso, i blocchi e i partial sono documentati in `README.md`: leggerlo prima
di toccare qualcosa. Qui solo cio' che il README non dice.

## Le due regole che non si negoziano

- **Nessuna logica di dominio.** Niente modelli, view, URL, niente parole
  come paziente/esame/cliente/cardio/echo/consulto. Se serve un colore o
  una classe per una cosa clinica, va nel CSS dell'ospite (`cardio.css`,
  `consulti.css`), caricato nel blocco `host_head`.
- **Tutto retrocompatibile, byte per byte.** Gli ospiti installano il
  pacchetto in modalita' editable e vedono ogni modifica all'istante, anche
  quella non ancora rilasciata. Variabili nuove sempre facoltative con
  default; chi non le usa deve ottenere lo stesso markup di prima. I test in
  `vetway_ui/tests/` confrontano i partial con le fotografie della 0.1.0:
  se un test rompe, la modifica non e' retrocompatibile, non si aggiorna la
  fotografia per farlo passare.

## Come si rilascia una versione

1. `python runtests.py` verde (14 test, senza progetto ospite).
2. Provare la modifica in **entrambi** gli ospiti (sono in editable): in
   vetcardio le pagine principali e `manage.py test cardio.tests_static`,
   in vetconsulti `venv/bin/python -m pytest`.
3. `version` in `pyproject.toml`, voce in `CHANGELOG.md` (cosa cambia per chi
   ospita, cosa resta invariato), commit `feat: vX.Y.Z — ...`.
4. `git tag -a vX.Y.Z -m "..."` e `git push && git push --tags`.
5. Negli ospiti: `pip install -e ../vetway-ui` di nuovo (i metadati editable
   restano alla versione vecchia: oggi vetconsulti dice 0.1.0 con il codice
   0.2.0), e aggiornare il tag in `vetconsulti/requirements.txt`.

Il tag e' il contratto: un ospite cambia aspetto solo quando qualcuno
aggiorna il tag che aggancia.

## Trappole note

- In produzione VetWay il pacchetto e' in `/home/vetcardio/vetway-ui` e
  Consulti lo avra' in `/home/consulti/vetway-ui`: ce lo porta `deploy.sh`
  dell'ospite (rsync + `pip install -e`) **prima** di `migrate`. Senza,
  gunicorn non parte (`ModuleNotFoundError: vetway_ui`).
- Le favicon in `static/vetway_ui/img/` sono copie: l'originale lo
  rigenerano `genera_marchio`/`sincronizza_marchio` di vetcardio in
  `cardio/static/cardio/brand/`. Dopo una rigenerazione vanno ricopiate qui.
- `.sidebar-mobile-toggle` e il blocco `@media (max-width: 729px)` sono
  deprecati dalla 0.2.0 e si tolgono solo quando nessun ambiente VetWay in
  linea li usa piu'.
- `_campo.html` (etichetta/valore in lettura) NON e' `_campo_form.html` di
  vetconsulti (campo di form): omonimia frequente.
- Chart.js non e' qui: e' dominio, resta all'ospite.

## Convenzioni

Commit `tipo: cosa cambia`, italiano, apostrofo ASCII al posto delle
accentate (`e'`, `piu'`). Vendor (Bootstrap 5.3.3, Icons 1.11.3, HTMX
1.9.12) servito in locale, mai da CDN: aggiornarli e' una versione a se',
con le impronte dei computed style prima/dopo su entrambi gli ospiti.
