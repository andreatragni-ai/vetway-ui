# Changelog — vetway-ui

Ogni versione e' un tag annotato; le applicazioni ospiti agganciano un tag.
Regola fissa: nessuna logica di dominio, ogni modifica retrocompatibile
(variabili nuove sempre facoltative, chi non le usa non vede cambiare nulla).

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
