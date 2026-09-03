# vetway-ui

Strato grafico condiviso delle applicazioni Vetway: CSS, JS di utilità,
template base, partial generici e template tag. Un pacchetto Django
installabile, usato da Vetway (`vetcardio`) e dal portale teleconsulto
(`vetconsulti`). Versione corrente: **0.2.0** (vedi `CHANGELOG.md`).

## La regola

**Nessuna logica di dominio.** Qui non ci sono modelli, view, URL né
riferimenti a pazienti, esami, clienti, cardio, echo o consulto. Solo
presentazione. Ogni modifica grafica condivisa passa da qui e viene
rilasciata con un tag (`v0.1.0`, `v0.2.0`, …): le applicazioni ospiti
agganciano un tag preciso, così un ritocco al pacchetto non cambia
l'aspetto di un'app senza che qualcuno lo abbia deciso.

Corollario, perché in sviluppo gli ospiti installano il pacchetto in
modalità editable e vedono ogni modifica all'istante: **tutto è
retrocompatibile**. Le variabili nuove sono facoltative con un default, e
chi non le usa ottiene lo stesso markup di prima (i test del pacchetto lo
verificano byte per byte contro le fotografie della 0.1.0).

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
vetway-ui @ git+ssh://git@github.com/<org>/vetway-ui.git@v0.2.0
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

Test del pacchetto: `python runtests.py` dalla radice del repo (senza
progetto ospite), oppure `manage.py test vetway_ui` da un ospite.

## Contenuto

```
vetway_ui/
  static/vetway_ui/
    css/vetway-tokens.css     SOLO le variabili --ovic-* (:root + variante data-brand)
    css/vetway.css            regole generiche (navbar, card, tabelle, pill-stato, …)
    js/vetway.js              countdown sessione, spinner HTMX, unità nelle .campo-label
    js/genera_password.js     pulsante "Genera password" (caricato dai layout, una volta)
    img/                      favicon, icone app, banner/lockup/marchio Vetway, brand/
    vendor/                   Bootstrap, Bootstrap Icons, HTMX (serviti in locale, no CDN)
  templates/vetway_ui/
    base.html                 layout con navbar/sessione/messaggi/footer
    auth_base.html            scheda centrata su fondo scuro (login, reset password)
    partials/…                vedi sotto
  templatetags/vetway_ui.py   filtri generici ({% load vetway_ui %})
  tests/                      test dei partial + fotografie del markup 0.1.0
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

Ordine di caricamento nell'head: Bootstrap, Icons, HTMX, `vetway-tokens.css`,
`vetway.css`, `host_head`, `extra_head`. In coda al body: Bootstrap bundle,
`vetway.js`, `genera_password.js`, `extra_js`.

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
| `extra_js`         | script della pagina, dopo Bootstrap, `vetway.js` e `genera_password.js`    |
| `modal_import_pdf` | mantenuto per compatibilità con i template Vetway esistenti                |
| `extra_body`       | modali/partial dell'ospite prima di `</body>`                              |

Variabili di contesto lette dal layout: `body_tema`, `body_brand`,
`sessione_minuti`, `privacy_url`, `termini_url`, `footer_link`, `prodotto`,
`messages`, `user.is_authenticated`.

### `vetway-tokens.css`, `data-brand` e `data-tema`

La palette è definita da proprietà custom `--ovic-*` in `:root`
(petrol/teal Vetway) dentro `vetway-tokens.css`, che contiene **solo**
variabili: il layout lo carica prima di `vetway.css`, le pagine di accesso
(`auth_base.html`) lo caricano da solo e possono così usare gli stessi
colori senza tutte le regole. La variante OVIC (navy/oro) si attiva con
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
`auth_messages` (i `messages` di Django dentro `.auth-box`, uno `.alert`
per messaggio; vuoto se non ce ne sono, sovrascrivibile), `auth_content`
(dentro `.auth-box`), `auth_extra_js` (dopo `genera_password.js`).
Classi: `.auth-head` (`.ico`, `h2`, `p`), `.btn-auth`, `.auth-link`,
`.errorlist`. Le variabili `--ovic-*` sono disponibili (`vetway-tokens.css`);
`vetway.css` no.

## Partial

Ogni partial ha in testa un `{% comment %}` con le variabili attese. Tutte le
variabili sono facoltative salvo dove indicato.

| Partial                            | Variabili                                                                                  |
|------------------------------------|--------------------------------------------------------------------------------------------|
| `_navbar.html`                     | `brand_url`, `brand_label`, `brand_img` (marchio a sinistra dell'hamburger, `.ovic-nav-brand`); `nav_voci` [{url, label, icona, attiva, title, **figli**: [{url, label, icona, attiva, title}]}] — con `figli` la voce è un dropdown a desktop e un gruppo con etichetta nell'offcanvas; `nav_menu_titolo`; `utente_label`, `utente_url`, `utente_logo`; `logout_url`. Cornice generica: chi ha bisogno di più sovrascrive il blocco `navbar` riusando `.ovic-nav`, `.ovic-nav-brand`, `.ovic-nav-hamburger`, `#navOffcanvas`, `.nav-section-label`, `.user-info`. (`nav_sezioni` della 0.1.0 è stata tolta: nessun ospite la usava, i `figli` la sostituiscono anche a desktop.) |
| `_footer.html`                     | `prodotto` (default "Vetway"), `privacy_url`, `termini_url` (link "Termini del servizio"), `footer_link` [{url, label}]; senza link non compare nessun `<a>` |
| `_messages.html`                   | `messages` (framework messages di Django)                                                  |
| `_modal_conferma_elimina.html`     | nessuna; incluso da `base.html`. Trigger: `data-bs-toggle="modal" data-bs-target="#modalConfermaElimina" data-elimina-href data-elimina-titolo data-elimina-dettaglio`; facoltativi `data-elimina-intestazione` ("Conferma eliminazione"), `data-elimina-azione` ("Sì, elimina"), `data-elimina-tono` (`danger` \| `warning` \| `primary`), `data-elimina-icona` ("trash") |
| `_pill_nav.html`                   | `pill_titolo`, `pill_progresso` {fatti, totali}, `pill_gruppi` [{label, classe, gruppo, voci: [{url, label, icona, attiva, stato ok/vuota/manca, manca_n, title}]}]. Contenitore `.ovic-sidebar-nav` + toggle mobile; da affiancare a un `.ovic-sidebar-content` |
| `_campo.html`                      | `label` (obbligatoria), `val`, `decimals` (0/1/altro→2), `multiline`, `mono`, `calc`, `field_name` (→ `data-range-field`), `help_key` (→ `openHelpModal()` dell'ospite, se esiste), `url` (valore cliccabile) |
| `_regole_password.html`            | `regole_password` (lista di stringhe)                                                      |
| `_genera_password.html`            | `campo` (obbligatoria: id dell'input), `conferma` (id del campo di conferma). Il JS lo caricano i layout, non il partial: un layout proprio deve caricare `vetway_ui/js/genera_password.js` da sé |

## Template tag

`{% load vetway_ui %}` → filtri `ifnone`, `in_multi`, `split_multi`,
`before_dash`, `after_dash`, `get_item`, `nome_proprio`.

## Cosa contiene `vetway.css`

Numeri tabellari, navbar/offcanvas/hamburger (+ `.ovic-nav-brand`), barra
sessione, contenuto principale (`.ovic-main`), card sezione (`.ovic-card`),
filtri di ricerca e input compatti, tabella risultati (`.tbl-risultati`,
kebab), badge stato, bottoni (`.btn-sel`, `.btn-nuova`, `.btn-testata-ghost`,
`.barra-azioni-testata`), indicatore HTMX e spinner, tab (`.ovic-tabs`),
sidebar/pill-nav (`.ovic-sidebar-nav`, `.sidebar-*`, `.tab-stato`), etichetta
e valore campo (`.campo-label`, `.campo-valore`), sezioni (`.sezione-titolo`,
`.sezione-sottotitolo`), footer, helper responsive (`.ovic-meta`,
`.ovic-num-badge`, `.ovic-divider-md`, input a 16px su iOS, indicatore di
scroll orizzontale delle tabelle).

### `.pill-stato`

Pillola di stato neutra (grigia) con modificatori sui colori "subtle" di
Bootstrap 5.3, così resta coerente con alert e badge anche se la palette
cambia: `.pill-stato--corso` (primary), `--ok` (success), `--attesa`
(warning), `--chiusa` (secondary), `--errore` (danger).

```html
<span class="pill-stato pill-stato--attesa">Presa in carico</span>
```

### Deprecazioni

`.sidebar-mobile-toggle` e il blocco `@media (max-width: 729px)` sono marcati
`DEPRECATO dalla 0.2.0`: Vetway su `main` non usa più il toggle
(scheda esame con nav a pill), ma restano finché ogni ambiente in linea non è
su quel commit. Verranno tolti in una versione successiva.

## Storia

Vedi `CHANGELOG.md`. In breve: `v0.1.0` estrazione da `base.html` di Vetway
senza cambiare colori, font, spaziature o breakpoint (impronte dei computed
style identiche prima e dopo su sei pagine e due viewport); `v0.2.0` le
lacune emerse collegando il portale VetWay Consulti, ancora a impronte
identiche.
