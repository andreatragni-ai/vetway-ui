# vetway-ui

Strato grafico condiviso delle applicazioni Vetway: CSS, JS di utilità,
template base, partial generici e template tag. Un pacchetto Django
installabile, usato da Vetway (`vetcardio`) e dal portale teleconsulto
(`vetconsulti`).

## La regola

**Nessuna logica di dominio.** Qui non ci sono modelli, view, URL né
riferimenti a pazienti, esami, clienti, cardio, echo o consulto. Solo
presentazione. Ogni modifica grafica condivisa passa da qui e viene
rilasciata con un tag (`v0.1.0`, `v0.2.0`, …): le applicazioni ospiti
agganciano un tag preciso, così un ritocco al pacchetto non cambia
l'aspetto di un'app senza che qualcuno lo abbia deciso.

Le regole di dominio (stepper dello stato scheda, badge specie, range
Cornell, chip stadio, popover clinico, …) restano nell'applicazione ospite,
in un suo CSS caricato **dopo** `vetway.css` (in Vetway:
`cardio/static/cardio/css/cardio.css`, nel blocco `host_head`).

## Installazione

In sviluppo, con i due repo fratelli:

```bash
venv/bin/pip install -e ../vetway-ui
```

Da repository, agganciato a un tag:

```
vetway-ui @ git+ssh://git@github.com/<org>/vetway-ui.git@v0.1.0
```

In `settings.py`, **prima** delle app dell'ospite (così i template e gli
static dell'app hanno la precedenza sui suoi in caso di omonimia):

```python
INSTALLED_APPS = [
    ...
    'django.contrib.staticfiles',
    'vetway_ui',
    'cardio',
    ...
]
```

Richiede Django ≥ 5.1 (< 6) e Python ≥ 3.12.

## Contenuto

```
vetway_ui/
  static/vetway_ui/
    css/vetway.css            regole generiche (variabili, navbar, card, tabelle, …)
    js/vetway.js              countdown sessione, spinner HTMX, unità nelle .campo-label
    js/genera_password.js     pulsante "Genera password" (vedi partial)
    img/                      favicon, icone app, banner/lockup/marchio Vetway, brand/
    vendor/                   Bootstrap, Bootstrap Icons, HTMX (serviti in locale, no CDN)
  templates/vetway_ui/
    base.html                 layout con navbar/sessione/messaggi/footer
    auth_base.html            scheda centrata su fondo scuro (login, reset password)
    partials/…                vedi sotto
  templatetags/vetway_ui.py   filtri generici ({% load vetway_ui %})
```

### Versioni vendor

| Libreria        | Versione | Percorso                                   |
|-----------------|----------|--------------------------------------------|
| Bootstrap       | 5.3.3    | `vetway_ui/vendor/bootstrap/`              |
| Bootstrap Icons | 1.11.3   | `vetway_ui/vendor/bootstrap-icons/` (+ `fonts/`) |
| HTMX            | 1.9.12   | `vetway_ui/vendor/htmx/`                   |

Chart.js **non** è nel pacchetto: è una dipendenza di dominio e resta
all'ospite che la usa.

## `base.html`

```django
{% extends "vetway_ui/base.html" %}
```

Blocchi, nell'ordine in cui compaiono nella pagina:

| Blocco             | Cosa ci va                                                                 |
|--------------------|----------------------------------------------------------------------------|
| `title`            | titolo della pagina                                                        |
| `theme_color`      | contenuto di `<meta name="theme-color">` (default in base a `body_brand`)  |
| `host_head`        | CSS/JS dell'**applicazione** ospite, subito dopo `vetway.css`. Separato da `extra_head` perché le singole pagine sovrascrivono `extra_head` senza `block.super` e perderebbero il CSS di dominio |
| `extra_head`       | head aggiuntivo della **singola pagina**                                   |
| `body_tema`        | valore di `data-tema` sul body (default: variabile `body_tema` o `originale`) |
| `body_brand`       | attributo `data-brand` sul body (default: da variabile `body_brand`)       |
| `body_attrs`       | altri attributi del body                                                   |
| `avvisi`           | banner sopra la testata (es. "account di prova")                           |
| `header`           | testata/banner del marchio                                                 |
| `navbar`           | barra di navigazione                                                       |
| `content`          | contenuto della pagina, dentro `.ovic-main`                                |
| `footer`           | piè di pagina (default: `partials/_footer.html`)                           |
| `extra_js`         | script della pagina, dopo Bootstrap e `vetway.js`                          |
| `modal_import_pdf` | mantenuto per compatibilità con i template Vetway esistenti                |
| `extra_body`       | modali/partial dell'ospite prima di `</body>`                              |

Variabili di contesto lette dal layout: `body_tema`, `body_brand`,
`sessione_minuti`, `privacy_url`, `prodotto`, `messages`,
`user.is_authenticated`.

### `data-brand` e `data-tema`

La palette è definita da proprietà custom `--ovic-*` in `:root`
(petrol/teal Vetway). La variante OVIC (navy/oro) si attiva con
`data-brand="osservatorio"` sul `<body>`: l'attributo vince sempre su
`:root`, quindi l'ordine dei fogli non conta.

```django
{# nel template ospite #}
{% block body_brand %}{% if esame.tipo_scheda == 'osservatorio' %} data-brand="osservatorio"{% endif %}{% endblock %}
{% block body_tema %}{{ user.profilo.tema_colori|default:'originale' }}{% endblock %}
```

`data-tema` (`originale`, `oceano`, `terra`, `monocromo`) governa lo stile
della sidebar a gruppi: il pacchetto definisce solo il tema `originale`
(etichette a blocco pieno, voce attiva a fondo pieno); i colori dei gruppi
(`--gc`, `--gc-tint`) e le loro varianti per tema li dichiara l'ospite sulle
proprie classi di gruppo.

### Scadenza sessione

`vetway.js` legge i minuti da `data-sessione-minuti` sul body (default 300);
il layout lo popola dalla variabile `sessione_minuti`. Un context processor
di due righe nell'ospite la ricava da `settings.SESSION_COOKIE_AGE // 60`.

## `auth_base.html`

Blocchi: `auth_title` (seguito da " – Vetway"), `auth_extra_head`,
`auth_content` (dentro `.auth-box`). Classi: `.auth-head` (`.ico`, `h2`,
`p`), `.btn-auth`, `.auth-link`, `.errorlist`.

## Partial

Ogni partial ha in testa un `{% comment %}` con le variabili attese.

| Partial                            | Variabili                                                                                  |
|------------------------------------|--------------------------------------------------------------------------------------------|
| `_navbar.html`                     | `nav_voci` [{url, label, icona, attiva, title}], `nav_sezioni` [{label, voci}], `nav_menu_titolo`, `utente_label`, `utente_url`, `utente_logo`, `logout_url`. Cornice generica: chi ha dropdown o voci condizionate dai permessi sovrascrive il blocco `navbar` con il proprio markup, riusando `.ovic-nav`, `.ovic-nav-hamburger`, `#navOffcanvas`, `.nav-section-label`, `.user-info` |
| `_footer.html`                     | `prodotto` (default "Vetway"), `privacy_url` (se vuoto niente link)                        |
| `_messages.html`                   | `messages` (framework messages di Django)                                                  |
| `_modal_conferma_elimina.html`     | nessuna; incluso da `base.html`. Trigger: `data-bs-toggle="modal" data-bs-target="#modalConfermaElimina" data-elimina-href data-elimina-titolo data-elimina-dettaglio` |
| `_pill_nav.html`                   | `pill_titolo`, `pill_progresso` {fatti, totali}, `pill_gruppi` [{label, classe, gruppo, voci: [{url, label, icona, attiva, stato ok/vuota/manca, manca_n, title}]}]. Contenitore `.ovic-sidebar-nav` + toggle mobile; da affiancare a un `.ovic-sidebar-content` |
| `_campo.html`                      | `label`, `val`, `decimals` (0/1/altro→2), `multiline`, `mono`, `calc`, `field_name` (→ `data-range-field`), `help_key` (→ `openHelpModal()` dell'ospite) |
| `_regole_password.html`            | `regole_password` (lista di stringhe)                                                      |
| `_genera_password.html`            | `campo` (id dell'input), `conferma` (id del campo di conferma, facoltativo)                |

## Template tag

`{% load vetway_ui %}` → filtri `ifnone`, `in_multi`, `split_multi`,
`before_dash`, `after_dash`, `get_item`, `nome_proprio`.

## Cosa contiene `vetway.css`

Variabili e palette, numeri tabellari, navbar/offcanvas/hamburger, barra
sessione, contenuto principale (`.ovic-main`), card sezione (`.ovic-card`),
filtri di ricerca e input compatti, tabella risultati (`.tbl-risultati`,
kebab), badge stato, bottoni (`.btn-sel`, `.btn-nuova`, `.btn-testata-ghost`,
`.barra-azioni-testata`), indicatore HTMX e spinner, tab (`.ovic-tabs`),
sidebar/pill-nav (`.ovic-sidebar-nav`, `.sidebar-*`, `.tab-stato`), etichetta
e valore campo (`.campo-label`, `.campo-valore`), sezioni (`.sezione-titolo`,
`.sezione-sottotitolo`), footer, helper responsive (`.ovic-meta`,
`.ovic-num-badge`, `.ovic-divider-md`, input a 16px su iOS, indicatore di
scroll orizzontale delle tabelle).

## Storia

`v0.1.0` (03/09/2026) — estrazione iniziale da `templates/cardio/base.html`
di Vetway: nessun colore, font, spaziatura o breakpoint è stato cambiato,
solo spostato. Verificato con impronte dei computed style su sei pagine e
due viewport: identiche prima e dopo.
