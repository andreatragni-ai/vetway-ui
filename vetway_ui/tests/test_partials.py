"""Retrocompatibilita' dei partial: chi non usa le variabili nuove della
0.2.0 deve ottenere ESATTAMENTE il markup della 0.1.0 (fotografie in questa
cartella, prese dal pacchetto 0.1.0 prima delle modifiche)."""
import os
from django.template.loader import render_to_string
from django.test import SimpleTestCase

QUI = os.path.dirname(os.path.abspath(__file__))


def _foto(nome):
    with open(os.path.join(QUI, nome), encoding='utf-8') as f:
        return f.read()


class Msg:
    def __init__(self, testo, tags='success'):
        self.testo, self.tags = testo, tags

    def __str__(self):
        return self.testo


class FooterTest(SimpleTestCase):
    def test_senza_variabili_nuove_identico_alla_0_1_0(self):
        out = render_to_string('vetway_ui/partials/_footer.html', {'privacy_url': '/privacy/', 'prodotto': 'Vetway'})
        self.assertEqual(out, _foto('footer_0_1_0.html'))

    def test_termini_e_link_aggiuntivi(self):
        out = render_to_string('vetway_ui/partials/_footer.html', {
            'privacy_url': '/privacy/', 'termini_url': '/termini/',
            'footer_link': [{'url': '/aiuto/', 'label': 'Aiuto'}]})
        self.assertIn('href="/termini/"', out)
        self.assertIn('Termini del servizio', out)
        self.assertIn('href="/aiuto/"', out)
        self.assertLess(out.index('Privacy'), out.index('Termini'))
        self.assertLess(out.index('Termini'), out.index('Aiuto'))

    def test_senza_privacy_nessun_link(self):
        out = render_to_string('vetway_ui/partials/_footer.html', {})
        self.assertNotIn('<a ', out)
        self.assertIn('Vetway', out)


class NavbarTest(SimpleTestCase):
    CTX = {'nav_voci': [{'url': '/a/', 'label': 'A', 'icona': 'search', 'attiva': True}, {'url': '/b/', 'label': 'B'}],
           'utente_label': 'mario', 'utente_url': '/p/', 'logout_url': '/esci/'}

    def test_senza_brand_e_figli_identico_alla_0_1_0(self):
        out = render_to_string('vetway_ui/partials/_navbar.html', dict(self.CTX))
        self.assertEqual(out, _foto('navbar_0_1_0.html'))

    def test_marchio(self):
        out = render_to_string('vetway_ui/partials/_navbar.html', dict(self.CTX, brand_label='Vetway', brand_url='/', brand_img='/static/x.png'))
        self.assertIn('class="ovic-nav-brand"', out)
        self.assertIn('<img src="/static/x.png"', out)
        self.assertLess(out.index('ovic-nav-brand'), out.index('ovic-nav-hamburger'))

    def test_figli_dropdown_desktop_e_gruppo_offcanvas(self):
        ctx = dict(self.CTX)
        ctx['nav_voci'] = ctx['nav_voci'] + [{'label': 'Altro', 'icona': 'gear', 'figli': [
            {'url': '/x/', 'label': 'X'}, {'url': '/y/', 'label': 'Y', 'attiva': True}]}]
        out = render_to_string('vetway_ui/partials/_navbar.html', ctx)
        self.assertIn('data-bs-toggle="dropdown"', out)
        self.assertIn('class="dropdown-item active" href="/y/"', out)
        self.assertIn('<div class="nav-section-label">Altro</div>', out)
        # la madre e' attiva perche' lo e' una figlia
        self.assertRegex(out, r'dropdown-toggle active"')
        # la voce con figli non compare fra le voci semplici dell\'offcanvas
        self.assertEqual(out.count('href="/x/"'), 2)  # dropdown + gruppo offcanvas


class ModalTest(SimpleTestCase):
    def test_markup_iniziale_identico_alla_0_1_0(self):
        out = render_to_string('vetway_ui/partials/_modal_conferma_elimina.html', {})
        foto = _foto('modal_0_1_0.html')
        # stessa parte HTML (prima dello <script>): il JS puo' cambiare, il DOM di partenza no
        self.assertEqual(out.split('<script>')[0], foto.split('<script>')[0])

    def test_il_js_legge_le_nuove_opzioni(self):
        out = render_to_string('vetway_ui/partials/_modal_conferma_elimina.html', {})
        for attr in ('data-elimina-intestazione', 'data-elimina-azione', 'data-elimina-tono', 'data-elimina-icona'):
            self.assertIn(attr, out)


class CampoTest(SimpleTestCase):
    def test_help_key_degrada_senza_openHelpModal(self):
        out = render_to_string('vetway_ui/partials/_campo.html', {'label': 'Peso (kg)', 'val': 3, 'help_key': 'peso'})
        self.assertIn("typeof openHelpModal === 'function'", out)

    def test_url_rende_il_valore_cliccabile(self):
        out = render_to_string('vetway_ui/partials/_campo.html', {'label': 'Paziente', 'val': 'Milo', 'url': '/paziente/1/'})
        self.assertIn('<a href="/paziente/1/">Milo</a>', out)
        senza = render_to_string('vetway_ui/partials/_campo.html', {'label': 'Paziente', 'val': 'Milo'})
        self.assertNotIn('<a ', senza)
        vuoto = render_to_string('vetway_ui/partials/_campo.html', {'label': 'Paziente', 'val': '', 'url': '/x/'})
        self.assertNotIn('<a ', vuoto)


class GeneraPasswordTest(SimpleTestCase):
    def test_il_partial_non_include_piu_lo_script(self):
        out = render_to_string('vetway_ui/partials/_genera_password.html', {'campo': 'id_pw'})
        self.assertNotIn('<script', out)
        self.assertIn('data-genera-password', out)

    def test_i_layout_lo_caricano_una_volta(self):
        for t in ('vetway_ui/base.html', 'vetway_ui/auth_base.html'):
            out = render_to_string(t, {})
            self.assertEqual(out.count('genera_password.js'), 1, t)


class AuthBaseTest(SimpleTestCase):
    def test_tokens_caricati_e_messaggi(self):
        out = render_to_string('vetway_ui/auth_base.html', {'messages': [Msg('Fatto.')]})
        self.assertIn('vetway-tokens.css', out)
        self.assertIn('alert alert-success', out)
        self.assertIn('Fatto.', out)
        vuoto = render_to_string('vetway_ui/auth_base.html', {})
        self.assertNotIn('alert', vuoto)

    def test_base_carica_tokens_prima_di_vetway_css(self):
        out = render_to_string('vetway_ui/base.html', {})
        self.assertLess(out.index('vetway-tokens.css'), out.index('css/vetway.css'))
