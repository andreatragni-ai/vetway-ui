/* vetway.js — utilita' generiche dello strato grafico Vetway (pacchetto vetway-ui).
   Caricato da vetway_ui/base.html dopo bootstrap.bundle. Tre cose, tutte
   inerti se l'elemento a cui servono non c'e' nella pagina:
   1. conto alla rovescia della sessione (#sessione-bar / #sessione-countdown);
      la durata in minuti arriva da data-sessione-minuti sul <body>;
   2. spinner globale HTMX (#global-spinner);
   3. unita' di misura fra parentesi nelle .campo-label resa piu' piccola. */

(function () {
  var MINUTI = parseInt(document.body.getAttribute('data-sessione-minuti'), 10) || 300;
  var secondi = MINUTI * 60;
  // La barra resta nascosta per quasi tutta la sessione: comparirebbe di
  // continuo un timer che scorre, distraendo. Si mostra solo negli ultimi
  // MOSTRA_SOTTO secondi (10 min), poi diventa avviso giallo a 5 min.
  var MOSTRA_SOTTO = 600;
  var bar = document.getElementById('sessione-bar');
  var span = document.getElementById('sessione-countdown');
  if (!span) return;

  function aggiorna() {
    var m = Math.floor(secondi / 60);
    var s = secondi % 60;
    span.textContent = m + ':' + (s < 10 ? '0' : '') + s;

    // Mostra la barra solo quando manca poco
    if (secondi <= MOSTRA_SOTTO) {
      bar.style.display = '';
    }

    // Avviso a 5 minuti
    if (secondi === 300) {
      bar.style.background = '#fff3cd';
      bar.style.borderColor = '#ffc107';
      bar.style.color = '#856404';
      bar.innerHTML = '<i class="bi bi-exclamation-triangle-fill me-1"></i>' +
        'Sessione in scadenza tra <strong>5 minuti</strong>. Salva il lavoro.';
    }

    // Scaduta
    if (secondi <= 0) {
      clearInterval(timer);
      bar.style.background = '#f8d7da';
      bar.style.borderColor = '#f5c2c7';
      bar.style.color = '#842029';
      bar.innerHTML = '<i class="bi bi-x-circle-fill me-1"></i>' +
        'Sessione scaduta. <a href="/login/" style="color:#842029;font-weight:600;">Effettua il login</a>';
      return;
    }
    secondi--;
  }

  aggiorna();
  var timer = setInterval(aggiorna, 1000);
})();

// Mostra spinner HTMX su ogni request
document.addEventListener('htmx:beforeRequest', function() {
  var sp = document.getElementById('global-spinner');
  if (sp) sp.style.display = 'block';
});
document.addEventListener('htmx:afterRequest', function() {
  var sp = document.getElementById('global-spinner');
  if (sp) sp.style.display = 'none';
});

// Riduce visivamente la parte tra parentesi nelle .campo-label (es. unita di misura)
document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('.campo-label').forEach(function(el) {
    el.innerHTML = el.innerHTML.replace(/\s*\(([^)]+)\)/, ' <span class="campo-label-unit">($1)</span>');
  });
});
