# Changelog — vetway-ui

Ogni versione e' un tag annotato; le applicazioni ospiti agganciano un tag.
Regola fissa: nessuna logica di dominio, ogni modifica retrocompatibile
(variabili nuove sempre facoltative, chi non le usa non vede cambiare nulla).

## 0.3.0 — 2026-09-12

Il primo carattere dichiarato dello strato grafico. **Cambia l'aspetto di
tutti e due gli ospiti**, Consulti compreso: e' l'unica modifica finora che
non si puo' non vedere.

- **IBM Plex Sans**, servito in locale da `vendor/ibm-plex/` come Bootstrap
  e le icone: nessun CDN, nessun IP mandato fuori. Due file soli e non otto,
  perche' sono font variabili — un file per sottoinsieme copre i pesi da 100
  a 700: `latin` 40 KB, `latin-ext` 26 KB. Licenza OFL 1.1, testo in
  `vendor/ibm-plex/OFL.txt`.
- **`--vw-font-sans`** in `vetway-tokens.css`, e `--bs-font-sans-serif`
  ridefinita sullo stesso valore: Bootstrap ci punta con
  `--bs-body-font-family`, e campi e bottoni ereditano, quindi non serve
  inseguire i componenti uno per uno. `vetway.css` lo ripete su `body` per
  non dipendere dalla presenza di Bootstrap.
- **`base.html` e `auth_base.html`** caricano `vendor/ibm-plex/ibm-plex.css`
  prima dei token. In `auth_base.html` lo stack scritto a mano
  (`'Segoe UI', system-ui, sans-serif`) diventa `var(--vw-font-sans)`.
- **Pesi**: IBM Plex Sans arriva a 700. Le regole a 800 e 900 che esistono
  negli ospiti (in Vetway il numero grande del controllo, alcune etichette)
  cadono sul 700 e risultano un filo meno marcate. Voluto, non un errore di
  caricamento: rimappare quelle dichiarazioni e' lavoro dell'ospite.

## 0.2.1 — 2026-09-12

Solo spaziature del menu laterale della scheda esame (`.ovic-sidebar-nav`).
Nessuna variabile nuova, nessun markup cambiato: chi non usa quella barra —
oggi VetWay Consulti — non vede differenze.

- **Menu laterale piu' arioso.** In 190px stavano 18 righe (13 sezioni, 4
  etichette di gruppo, la barra di avanzamento) e fra l'ultima voce di un
  gruppo e l'etichetta del gruppo dopo c'erano gli stessi 10px che separano
  due voci dello stesso gruppo: i gruppi non si staccavano. Ora la barra e'
  larga 214px, le voci sono alte 38px invece di 30 con il testo a 0,84rem
  invece di 0,80, e le etichette di gruppo hanno 24px di stacco sopra
  (12px la prima). La deroga `.diagnostica-group { margin-top: 6px }` e'
  sparita: lo stacco e' uguale per tutti e quattro i gruppi.
- **`body[data-tema="originale"]` deprecato.** Vetway ha tolto quel tema
  dalle scelte del profilo (migrazione `cardio` 0153): le regole restano
  qui finche' nessun ambiente in linea le usa, come `.sidebar-mobile-toggle`.

## 0.2.0 — 2026-09-03

Lacune emerse collegando il secondo ospite (portale VetWay Consulti).

- **`vetway-tokens.css`** (nuovo): le variabili `--ovic-*` (`:root` e la
  variante `body[data-brand="osservatorio"]`) escono da `vetway.css` e vanno
  in un file a se', caricato da `base.html` prima di `vetway.css` e da
  `auth_base.html`: le pagine di accesso possono usare la palette senza
  caricare tutte le regole. Nessuna doppia definizione, cascata invariata
  (verificato con le impronte dei computed style di Vetway).
- **`auth_base.html`**: blocchi `auth_messages` (i `messages` di Django
  dentro `.auth-box`, vuoto se non ce ne sono) e `auth_extra_js`;
  `auth_extra_head` documentato.
- **`partials/_footer.html`**: `termini_url` (link "Termini del servizio"
  accanto a Privacy) e `footer_link` (lista di `{url, label}`). Senza di
  esse il markup e' byte per byte quello della 0.1.0 (test).
- **`partials/_modal_conferma_elimina.html`**: dal trigger si possono
  impostare `data-elimina-intestazione`, `data-elimina-azione` (testo del
  bottone), `data-elimina-tono` (`danger` default, `warning`, `primary`) e
  `data-elimina-icona`. Default invariati; il markup iniziale non cambia
  (il JS sostituisce i nodi di testo, non aggiunge elementi).
- **`partials/_navbar.html`**: slot marchio a sinistra dell'hamburger
  (`brand_url`, `brand_label`, `brand_img`); voci con `figli` (dropdown a
  desktop, gruppo con etichetta nell'offcanvas). **Tolta `nav_sezioni`**
  (nessun ospite la usava; i figli la sostituiscono anche a desktop).
- **`partials/_campo.html`**: `help_key` non fa nulla se `openHelpModal`
  non esiste nell'ospite; variante `url` (valore cliccabile).
- **`vetway.css`**: `.pill-stato` neutra con modificatori `--corso`,
  `--ok`, `--attesa`, `--chiusa`, `--errore` (colori "subtle" di Bootstrap
  5.3); `.ovic-nav-brand` per lo slot marchio.
- **`genera_password.js`**: caricato una volta sola da `base.html` e
  `auth_base.html`, non piu' dal partial a ogni include; guardia
  `window.__vw_genera_password` contro il doppio caricamento. Aggancia
  tutti i blocchi `[data-genera-password]` della pagina.
- **Deprecazioni**: `.sidebar-mobile-toggle` e il blocco
  `@media (max-width: 729px)` restano ma sono marcati `DEPRECATO dalla
  0.2.0`: via quando nessun ambiente Vetway in linea usa piu' il toggle.
- Test del pacchetto: `python runtests.py` (o `manage.py test vetway_ui`
  da un ospite).

## 0.1.0 — 2026-09-03

Estrazione iniziale da `templates/cardio/base.html` di Vetway: CSS
generico, `vetway.js`, `genera_password.js`, vendor Bootstrap 5.3.3 /
Icons 1.11.3 / HTMX 1.9.12 in locale, favicon e brand, `base.html`,
`auth_base.html`, partial generici, filtri di template. Nessun colore, font,
spaziatura o breakpoint cambiato: impronte dei computed style identiche
prima e dopo su sei pagine e due viewport.
