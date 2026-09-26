# -*- coding: utf-8 -*-
"""Genera el fitxer .ics del calendari del concurs Cordoncillo 2026.

Les dates oficials provenen de la pagina publica del concurs (content/concurs.md).
Les tasques tecniques s'afegeixen per ordre de l'usuari.
"""
import io

DOM = "9barrisimatge.org"
CASAL = "Casal de Barri de Prosperitat, Plaça d'Àngel Pestanya, 08016 Barcelona"
CAL = "Concurs Cordoncillo 2026 — 9 Barris Imatge"
STAMP = "20260926T073000Z"


def esc(text):
    """Escapa els caracters especials d'iCalendar (RFC 5545)."""
    return (text.replace("\\", "\\\\").replace(";", "\\;")
                .replace(",", "\\,").replace("\n", "\\n"))


def seguent_dia(ymd):
    """DTSTART;VALUE=DATE + 1. RFC 5545: el final d'un esdeveniment de tot el
    dia és exclusiu, així que ha de ser el dia següent."""
    import datetime
    d = datetime.date(int(ymd[:4]), int(ymd[4:6]), int(ymd[6:8]))
    return (d + datetime.timedelta(days=1)).strftime("%Y%m%d")


def vevent(uid, summary, start, end=None, all_day=False, desc="", loc="",
            alarms=()):
    """Retorna les línies d'un VEVENT. Les hores són hora local (sense Z)."""
    lines = ["BEGIN:VEVENT", "UID:%s" % uid, "DTSTAMP:" + STAMP]
    if all_day:
        lines.append("DTSTART;VALUE=DATE:" + start)
        lines.append("DTEND;VALUE=DATE:" + (end or seguent_dia(start)))
    else:
        lines.append("DTSTART:" + start)
        lines.append("DTEND:" + (end or start))
    lines.append("SUMMARY:" + esc(summary))
    if desc:
        lines.append("DESCRIPTION:" + esc(desc))
    if loc:
        lines.append("LOCATION:" + esc(loc))
    for trigger, text in alarms:
        lines += ["BEGIN:VALARM", "ACTION:DISPLAY", "TRIGGER:" + trigger,
                  "DESCRIPTION:" + esc(text), "END:VALARM"]
    lines.append("END:VEVENT")
    return lines


EVENTS = [
    # --- esdeveniments oficials del concurs -------------------------------
    vevent("9bi-2026-concurs-obertura@" + DOM,
           "[Concurs 2026] Obertura de la convocatòria", "20260925", all_day=True,
           desc="Data oficial publicada a la pàgina del concurs. Ja ha passat; "
                "es deixa com a referència."),

    vevent("9bi-2026-concurs-limit@" + DOM,
           "[Concurs 2026] Data límit de presentació de fotografies", "20261120",
           all_day=True,
           desc="Data límit oficial per enviar les fotografies a "
                "dinamitzacio@casalprospe.org amb l'assumpte «CONCURS DE FOTOGRAFIA "
                "CORDONCILLO 2026» i les dades personals (nom, telèfon, correu "
                "electrònic i adreça postal).",
           alarms=[("-P1D", "Demà és l'últim dia per presentar fotografies"),
                   ("-PT2H", "Falten 2 hores per tancar la presentació")]),

    vevent("9bi-2026-exposicio-inici@" + DOM,
           "[Concurs 2026] Exposició i obertura de la votació del públic", "20261201",
           all_day=True,
           desc="Inici de l'exposició (del 1 al 30 de desembre). Aquest mateix dia "
                "s'obre la votació del públic, de l'1 al 15 de desembre, amb el codi "
                "QR de l'exposició.",
           loc=CASAL,
           alarms=[("-P1D", "Demà s'obre l'exposició i la votació del públic"),
                   ("-PT1H", "Comprovar que la votació s'ha obert")]),

    vevent("9bi-2026-votacio-tancament@" + DOM,
           "[Concurs 2026] Tancament de la votació del públic", "20261215T235900",
           desc="La votació es tanca sola a les 23:59 per rellotge: no cal fer res. "
                "Aquesta entrada serveix per no oblidar-la.",
           alarms=[("-P1D", "Demà es tanca la votació del públic")]),

    vevent("9bi-2026-resultats@" + DOM,
           "[9bi · votació] Exportar resultats i verificar el recompte", "20261216T100000",
           desc="Després del tancament: exportar el recompte oficial (CSV signat) i "
                "verificar que el resultat és coherent abans d'anunciar el guanyador "
                "del premi del públic de 100 €."),

    vevent("9bi-2026-premis@" + DOM,
           "[Concurs 2026] Lliurament de premis i concert", "20261218T190000",
           desc="Lliurament de premis i concert, divendres 18 de desembre a les 19 h. "
                "L'assistència és obligatòria per recollir el premi; si no s'hi pot "
                "anar, cal delegar una persona autoritzada.",
           loc=CASAL,
           alarms=[("-P1D", "Demà és el lliurament de premis i el concert")]),

    vevent("9bi-2026-exposicio-fi@" + DOM,
           "[Concurs 2026] Fi de l'exposició", "20261230", all_day=True,
           desc="Últim dia de l'exposició a la sala del Casal."),

    # --- tasques tecniques de 9 Barris Imatge -----------------------------
    vevent("9bi-2026-obres@" + DOM,
           "[9bi · votació] Carregar la llista definitiva d'obres", "20261130T090000",
           desc="TASCA OBLIGATÒRIA. Les obres del concurs només es carreguen quan es "
                "crea la base de dades, de manera que cal: 1) inserir la llista "
                "definitiva (número, títol, autor i categoria), 2) esborrar les 100 "
                "obres de prova i els 5 vots de prova. Si no es fa, a l'exposició es "
                "votaran fotos que no són del concurs.",
           alarms=[("-P1D", "Demà cal carregar la llista definitiva d'obres"),
                   ("-PT1H", "Avui s'ha de deixar la llista d'obres carregada")]),

    vevent("9bi-2026-comprovacio@" + DOM,
           "[9bi · votació] Comprovar l'obertura de la votació al Casal",
           "20261201T110000",
           desc="Al Casal, amb telèfon i xarxa mòbil: obrir el codi QR i fer un vot "
                "real. Comprovar: (1) que la votació accepta vots; (2) que el geofence "
                "rebutja fora del radi de 500 m; (3) que des del mateix dispositiu no "
                "es pot tornar a votar la mateixa obra; (4) que en un segon "
                "dispositiu sí que es pot.",
           loc=CASAL,
           alarms=[("-P2D", "Falten 2 dies per la comprovació d'obertura"),
                   ("-PT2H", "Anar al Casal per comprovar la votació")]),

    vevent("9bi-2026-certificat@" + DOM,
           "[9bi · tècnic] Renovar el certificat dels subdominis", "20261222T100000",
           desc="TÈCNIC. El certificat del subdomini de votació i el de formularis "
                "caduca el 24 de desembre de 2026. No afecta la votació, que acaba el "
                "15, però cal renovar-lo abans: a la configuració SSL d'Apache del "
                "servidor de LinuxBCN (vl28359.dinaserver.com)."),
]

HEAD = ["BEGIN:VCALENDAR", "VERSION:2.0",
        "PRODID:-//9 Barris Imatge//Calendari concurs Cordoncillo 2026//CAT",
        "CALSCALE:GREGORIAN", "METHOD:PUBLISH",
        "X-WR-CALNAME:" + CAL, "X-WR-TIMEZONE:Europe/Madrid"]

ics = "\r\n".join(HEAD + [l for e in EVENTS for l in e] + ["END:VCALENDAR", ""])
io.open("drafts/calendari-concurs-cordoncillo-2026.ics", "w",
        encoding="utf-8", newline="").write(ics)
print("escrit: drafts/calendari-concurs-cordoncillo-2026.ics (%d esdeveniments)"
      % len(EVENTS))
