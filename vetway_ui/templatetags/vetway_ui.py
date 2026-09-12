"""Filtri di template generici dello strato grafico Vetway.

Copiati da cardio/templatetags/cardio_extras.py di Vetway (03/09/2026), che
li conserva ancora: i template esistenti continuano a fare
{% load cardio_extras %}; i nuovi progetti fanno {% load vetway_ui %}.
"""
import os

from django import template
from django.contrib.staticfiles import finders
from django.templatetags.static import static as _static_url

register = template.Library()


# Impronte gia' calcolate, per non fare uno stat a ogni riga di ogni pagina.
# Il processo le tiene finche' vive: va bene perche' un file statico cambia
# solo con un deploy, e il deploy riavvia gunicorn.
_IMPRONTE = {}


@register.simple_tag
def vw_static(percorso):
    """Come {% static %}, ma con `?v=<impronta>` attaccato.

    Serve perche' gli statici escono con `Cache-Control: max-age=604800` e
    i file non hanno un'impronta nel nome: si chiamano `vetway.css` oggi
    come una settimana fa. Senza questo, dopo un deploy il browser di chi
    usa l'app continua a servirsi la copia vecchia per giorni, e la
    modifica appena messa in produzione non la vede nessuno. E' successo
    davvero il 2026-09-12 con l'aria nel menu e il carattere nuovo.

    L'impronta e' il timestamp di modifica del file: `rsync -a` lo conserva,
    quindi cambia quando cambia il contenuto e non a ogni deploy. Se il file
    non si trova si torna alla URL nuda, senza rompere la pagina.
    """
    url = _static_url(percorso)
    if percorso not in _IMPRONTE:
        try:
            _IMPRONTE[percorso] = str(int(os.path.getmtime(finders.find(percorso))))
        except (TypeError, OSError, ValueError):
            _IMPRONTE[percorso] = ''
    impronta = _IMPRONTE[percorso]
    return '%s?v=%s' % (url, impronta) if impronta else url


@register.filter
def ifnone(value, fallback):
    """Come |default ma tratta SOLO None come 'assente'.

    |default (value or arg) scarta qualunque falsy — inclusi 0/0.0/Decimal('0'),
    che in un parametro numerico sono valori validi. Usato per il fallback
    strutturato -> legacy senza perdere/sostituire uno 0 reale."""
    return fallback if value is None else value


@register.filter(name='in_multi')
def in_multi(value, joined):
    """
    Ritorna True se `value` e' presente come elemento esatto nella stringa
    `joined` joinata con "; ".

    Utile per campi multi-select salvati come stringa:
        {% if "Voce A"|in_multi:oggetto.campo_multi %}

    Evita falsi match da substring (es. "Stenosi" non matcha "Stenosi moderata").
    """
    if not joined or not value:
        return False
    voci = [v.strip() for v in str(joined).split(';')]
    return str(value).strip() in voci


@register.filter(name='split_multi')
def split_multi(value, sep='; '):
    """Spezza una stringa joinata con "; " in lista. Usato per rendering lettura."""
    if not value:
        return []
    return [v.strip() for v in str(value).split(';') if v.strip()]


@register.filter(name='before_dash')
def before_dash(value):
    """Parte prima di ' – ' / '-'. Estrae codice breve ('B2') da label tipo
    'B2 – asintomatica con rimodellamento'."""
    if not value:
        return ''
    s = str(value)
    for sep in (' – ', ' - ', '–', '-'):
        if sep in s:
            return s.split(sep, 1)[0].strip()
    return s.split()[0] if s.split() else s


@register.filter(name='after_dash')
def after_dash(value):
    """Parte dopo ' – ' / '-'. Estrae descrizione estesa dopo il codice."""
    if not value:
        return ''
    s = str(value)
    for sep in (' – ', ' - ', '–', '-'):
        if sep in s:
            return s.split(sep, 1)[1].strip()
    return ''


@register.filter(name='get_item')
def get_item(d, key):
    """Accesso a dict con chiave dinamica (utile quando la chiave contiene caratteri
    speciali come '|' che non passano nel resolve di Django template)."""
    if not isinstance(d, dict):
        return ''
    return d.get(key, '')


@register.filter(name='nome_proprio')
def nome_proprio(value):
    """Capitalizza nomi e cognomi digitati tutti minuscoli o tutti maiuscoli.

    Il dato NON viene toccato: si normalizza solo la resa a video/stampa.
    Chi ha scritto il nome con maiuscole interne se lo tiene: "McDonald",
    "de Angelis", "D'Amico jr" restano come sono, perche' un .title() cieco
    li rovinerebbe. Si interviene solo sui due casi in cui l'intenzione e'
    inequivocabile — tutto minuscolo o tutto maiuscolo.
    """
    if not value:
        return ''
    s = str(value).strip()
    if s.islower() or s.isupper():
        # title() spezza sugli apostrofi ("d'angelo" -> "D'Angelo"), che in
        # italiano e' la resa voluta.
        return s.title()
    return s
