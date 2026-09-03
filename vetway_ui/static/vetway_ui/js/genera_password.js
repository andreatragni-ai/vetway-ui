/*
 * Generatore di password: parole italiane + un numero, separate da trattini.
 *
 * Perche' una passphrase e non 16 caratteri casuali: con l'invito via email la
 * password manuale resta per i casi SENZA email, cioe' proprio quelli in cui
 * l'amministratore deve dettarla al telefono. "quercia-lanterna-47-fiume" si
 * detta; "xK9#mQ2vLp" no.
 *
 * Passa da sola le regole di AUTH_PASSWORD_VALIDATORS: ben oltre gli 8
 * caratteri, non e' interamente numerica, non e' una password comune e le
 * parole sono sorteggiate, quindi non somiglia mai a nome utente o email.
 *
 * Uso nei template:
 *   {% include "cardio/_genera_password.html" with campo="id_password" %}
 *   {% include "cardio/_genera_password.html" with campo="id_pw_nuova" conferma="id_pw_conf" %}
 */
(function () {
  'use strict';

  // Sostantivi comuni, senza accenti e senza coppie che si confondono al
  // telefono (niente "pesca/pesce"). Corti, cosi' la password resta scrivibile.
  var PAROLE = [
    'ancora', 'albero', 'aquila', 'arancia', 'balena', 'barca', 'bosco', 'bottone',
    'campana', 'candela', 'cascata', 'castello', 'chiave', 'cipolla', 'collina',
    'cometa', 'corda', 'cortile', 'cucchiaio', 'delfino', 'deserto', 'diamante',
    'falco', 'faro', 'fiume', 'fontana', 'foresta', 'formica', 'fragola',
    'gabbiano', 'ghiaccio', 'giardino', 'gomitolo', 'granito', 'isola', 'lampada',
    'lanterna', 'lavagna', 'limone', 'luna', 'mandorla', 'martello', 'matita',
    'melone', 'montagna', 'mulino', 'nuvola', 'oceano', 'ombrello', 'orologio',
    'pianura', 'piuma', 'pioggia', 'ponte', 'quercia', 'radice', 'ruscello',
    'sabbia', 'scoglio', 'sentiero', 'specchio', 'stella', 'tamburo', 'tavolo',
    'tramonto', 'trifoglio', 'valigia', 'vulcano', 'zafferano', 'zucca'
  ];

  // crypto.getRandomValues, non Math.random: e' una credenziale.
  function intero(max) {
    var buf = new Uint32Array(1);
    var limite = Math.floor(0xFFFFFFFF / max) * max;   // scarta il resto per non
    do { crypto.getRandomValues(buf); } while (buf[0] >= limite);  // sbilanciare
    return buf[0] % max;
  }

  function generaPassword() {
    var scelte = [];
    while (scelte.length < 3) {
      var p = PAROLE[intero(PAROLE.length)];
      if (scelte.indexOf(p) === -1) scelte.push(p);   // niente parole ripetute
    }
    var numero = 10 + intero(90);                     // due cifre, mai in fondo
    scelte.splice(2, 0, String(numero));
    return scelte.join('-');
  }

  function copia(testo, esito) {
    if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard.writeText(testo).then(function () {
        esito.textContent = 'Copiata negli appunti.';
      }, function () {
        esito.textContent = 'Copia non riuscita: selezionala a mano.';
      });
    } else {
      // http (dev locale): l'API appunti non c'e'. Non fingiamo che funzioni.
      esito.textContent = 'Selezionala e copiala a mano.';
    }
  }

  function collega(blocco) {
    // Il partial porta con se' il <script>: se finisse due volte nella stessa
    // pagina, senza questa guardia ogni clic genererebbe due password.
    if (blocco.dataset.collegato === '1') return;
    blocco.dataset.collegato = '1';

    var campo = document.getElementById(blocco.dataset.campo);
    if (!campo) return;
    var conferma = blocco.dataset.conferma ? document.getElementById(blocco.dataset.conferma) : null;
    var btnGenera = blocco.querySelector('.js-genera');
    var btnCopia = blocco.querySelector('.js-copia');
    var esito = blocco.querySelector('.js-esito');

    btnGenera.addEventListener('click', function () {
      var pw = generaPassword();
      campo.value = pw;
      campo.type = 'text';               // va letta: e' il senso del pulsante
      if (conferma) { conferma.value = pw; conferma.type = 'text'; }
      btnCopia.classList.remove('d-none');
      esito.textContent = 'Annotala prima di salvare: dopo non si rilegge.';
      campo.dispatchEvent(new Event('input', { bubbles: true }));
    });

    btnCopia.addEventListener('click', function () { copia(campo.value, esito); });
  }

  document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('[data-genera-password]').forEach(collega);
  });
})();
