import csv
from dataclasses import dataclass
import json
from pathlib import Path
import subprocess
import sys
from typing import Dict, List, Optional, Union, cast
from bs4 import BeautifulSoup, Tag
from src.utils import download_file, get_headers
import magic
import pandas as pd
import requests
from src.consts import drucksachen_text_pattern
from dataclasses_json import dataclass_json

mime = magic.Magic(mime=True)


@dataclass_json
@dataclass
class AbstimmungsText:
    text: str
    drucksachen: List[str]


@dataclass_json
@dataclass
class AbstimmungsColumns:
    periode: int
    sitzung: int
    abstimmung: int
    fraktion: int
    ja: int
    nein: int
    enthaltung: int
    ungueltig: int
    nichtabgegeben: int
    mdb: int
    bemerkung: int


@dataclass_json
@dataclass
class Stimme:
    abtimmungs_id: str
    periode: int
    sitzung: int
    abstimmung: int
    fraktion: str
    ja: int
    nein: int
    enthaltung: int
    ungueltig: int
    nichtabgegeben: int
    mdb: str
    bemerkung: str


def download_abstimmungsergebnis(url, basedir):
    file_name = url.split("/")[-1]
    fi = basedir / file_name
    if fi.is_file() and fi.stat().st_size > 100:
        mime_type = mime.from_file(fi)
        if mime_type.startswith("application"):
            return

    download_file(url, fi)


def download_abstimmungsergebnisse(dir_abstimmungsergebnisse: Path) -> None:
    legislatur_start = 1632614401000
    legislatur_end = 1740268801000

    base_url = f"https://www.bundestag.de/ajax/filterlist/de/parlament/plenum/abstimmung/liste/462112-462112?enddate={legislatur_end}&endfield=date&limit=30&noFilterSet=false&startdate={legislatur_start}&startfield=date"

    offset = 0
    hits = 10

    request_headers = get_headers()

    while offset < hits:
        url = f"{base_url}&offset={offset}"
        r = requests.get(url, allow_redirects=False, headers=request_headers)
        if r.status_code == 303:
            print(r.status_code, f"https://www.bundestag.de{r.headers['Location']}")
            sys.exit(17)

        soup = BeautifulSoup(r.content, "html5lib")

        for element in soup.findAll("a", attrs={"class": "bt-link-dokument"}):
            doc_url = element["href"]
            print(doc_url)
            download_abstimmungsergebnis(
                f"https://www.bundestag.de{doc_url}", dir_abstimmungsergebnisse
            )

        slider = cast(Tag, soup.find("div", attrs={"class": "meta-slider"}))
        if slider is not None:
            print(slider.get("data-hits"), slider.get("data-nextoffset"))
            hits = int(cast(str, slider.get("data-hits")))
            offset = int(cast(str, slider.get("data-nextoffset")))


def xlsx_convert(xlsx_file: Path, dir_csv_ergebnisse: Path) -> Path:
    file_name = xlsx_file.name
    csv_file = dir_csv_ergebnisse / file_name.replace(".xlsx", ".csv")

    if not csv_file.is_file():

        # print(file_name, csv_file)
        data_xls = pd.read_excel(xlsx_file)
        data_xls.to_csv(csv_file, encoding="utf-8", index=False)
    return csv_file


def read_csv(csv_file: Path) -> List[Stimme]:
    rows: List[Stimme] = []

    with open(csv_file, "r") as csvfile:
        dialect = csv.Sniffer().sniff(csvfile.read(1024), delimiters=";,")
        csvfile.seek(0)
        table = csv.reader(csvfile, dialect)
        abst_key = None
        col_nums: Optional[AbstimmungsColumns]
        for row in table:
            # parse row sequence...
            if "Wahlperiode" in row or "Vorname" in row or "Bemerkung" in row:
                col_nums = get_col_nums(row)
                continue

            if col_nums is None:
                continue

            # print (row[rowids["periode"]], row[rowids["siztung"]], row[rowids["abstimmung"]])
            if abst_key is None:
                abst_key = "%03d-%03d-%02d" % (
                    int(row[col_nums.periode]),
                    int(row[col_nums.sitzung]),
                    int(row[col_nums.abstimmung]),
                )
            if abst_key != "%03d-%03d-%02d" % (
                int(row[col_nums.periode]),
                int(row[col_nums.sitzung]),
                int(row[col_nums.abstimmung]),
            ):
                print("different abst_key!?")
                print(abst_key)
                print(
                    "%03d-%03d-%02d"
                    % (
                        int(row[col_nums.periode]),
                        int(row[col_nums.sitzung]),
                        int(row[col_nums.abstimmung]),
                    )
                )
                sys.exit(1)
            rows.append(
                Stimme(
                    abtimmungs_id=abst_key,
                    periode=int(row[col_nums.periode]),
                    sitzung=int(row[col_nums.sitzung]),
                    abstimmung=int(row[col_nums.abstimmung]),
                    fraktion=fraktionsmapper(row[col_nums.fraktion]),
                    ja=int(row[col_nums.ja]),
                    nein=int(row[col_nums.nein]),
                    enthaltung=int(row[col_nums.enthaltung]),
                    ungueltig=int(row[col_nums.ungueltig]),
                    nichtabgegeben=int(row[col_nums.nichtabgegeben]),
                    mdb=row[col_nums.mdb],
                    bemerkung=row[col_nums.bemerkung],
                )
            )
            # fraktion = fraktionsmapper(row[rowids["fraktion"]].lower ())
    return rows


def xlsx_convert_all(
    dir_abstimmungsergebnisse: Path,
    dir_csv_ergebnisse: Path,
    file_csv_ergebnisse: Path,
) -> pd.DataFrame:
    if not file_csv_ergebnisse.is_file():

        table: List[Stimme] = []
        for f in dir_abstimmungsergebnisse.iterdir():
            if f.name.endswith(".xlsx"):
                print(f)
                csv_file = xlsx_convert(f, dir_csv_ergebnisse)
                rows = read_csv(csv_file)
                rows = list(
                    filter(
                        lambda r: "mutterschutz" not in r.bemerkung.lower()
                        or r.nichtabgegeben == 0,
                        rows,
                    )
                )
                table.extend(rows)
        df = pd.DataFrame(table)

        # with open(file_csv_ergebnisse, "w") as fo:
        df.to_csv(file_csv_ergebnisse, encoding="utf-8", index=False)
        # fo.write(Stimme.schema().dumps(table, many=True))
    else:
        # with open(file_csv_ergebnisse) as fi:
        # table = Stimme.schema().load(fi, many=True)
        df = pd.read_csv(
            file_csv_ergebnisse,
        )
    return df


def get_pdf_preview(f: Path) -> str:
    if f.name == "20240131_1.pdf":
        return "Deutscher Bundestag\n\n150. Sitzung des Deutschen Bundestages\nam Mittwoch, 31. Januar 2024\n\nEndg\u00fcltiges Ergebnis der Namentlichen Abstimmung Nr. 1\n\nEinzelplan 04, Bundeskanzler und Bundeskanzleramt\n\nEntwurf eines Gesetzes über die Feststellung des Bundeshaushaltsplans für das Haushaltsjahr 2024 (Haushaltsgesetz 2024) - Einzelplan 04, Geschäftsbereich des Bundeskanzlers und des Bundeskanzleramts (Drucksachen 20/7800, 20/7802, 20/8604 und 20/8661)"
    t = subprocess.check_output(["pdftotext", "-l", "1", f, "-"]).decode("UTF-8")
    i = t.find("Abgegebene Stimmen")
    if i > 0:
        t = t[:i]
    return t.strip()


def pdf_convert(pdf_file: Path, dir_text_ergebnisse: Path) -> AbstimmungsText:
    file_name = pdf_file.name
    text_file = dir_text_ergebnisse / file_name.replace(".pdf", ".json")

    if not text_file.is_file():

        # print(file_name, csv_file)
        data_pdf = get_pdf_preview(pdf_file)
        drs = drucksachen_text_pattern.findall(data_pdf)
        print(drs)
        data = AbstimmungsText(text=data_pdf, drucksachen=drs)
        with open(text_file, "w") as f:
            f.write(
                data.to_json()
                # json.dumps(
                #     data,
                #     sort_keys=True,
                #     indent=2,
                #     separators=(",", ": "),
                #     default=lambda o: o.__dict__,
                # )
            )
    else:
        with open(text_file) as f:
            data = AbstimmungsText.from_json(f.read())
            # data = json.load(f)

    return data


def pdf_convert_all(
    dir_abstimmungsergebnisse: Path,
    dir_text_ergebnisse: Path,
    file_text_ergebnisse: Path,
) -> Dict[str, Dict[str, Union[str, List[str]]]]:
    texte = {}
    if not file_text_ergebnisse.is_file():
        for f in dir_abstimmungsergebnisse.iterdir():
            if f.name.endswith(".pdf"):
                # print(f)
                d = pdf_convert(f, dir_text_ergebnisse)
                # print(d.drucksachen)
                texte[f.name] = d.to_dict()
        with open(file_text_ergebnisse, "w") as fo:
            fo.write(
                json.dumps(
                    texte,
                    sort_keys=True,
                    indent=2,
                    separators=(",", ": "),
                    default=lambda o: o.__dict__,
                )
            )
    else:
        with open(file_text_ergebnisse) as fi:
            texte = json.load(fi)

    return texte


# approach from 2017:
# as they define columnnames and sequence
# arbitarily and everytime differently
# we need to do this effort and match words...
def get_col_nums(header: List[str]) -> AbstimmungsColumns:
    col_ids = AbstimmungsColumns(
        periode=0,
        sitzung=1,
        abstimmung=2,
        fraktion=3,
        ja=7,
        nein=8,
        enthaltung=9,
        ungueltig=10,
        nichtabgegeben=11,
        mdb=13,
        bemerkung=24,
    )

    for i in range(len(header)):
        columnname = header[i].lower()
        # print (str (i) + " -> " + columnname)
        if any(option in columnname for option in ["wahlperiode", "periode"]):
            col_ids.periode = i
            continue
        if any(
            option in columnname for option in ["sitzungnr", "sitzungnummer", "sitzung"]
        ):
            col_ids.sitzung = i
            continue
        if any(
            option in columnname
            for option in ["abstimmnr", "abstimmnummer", "abstimmung"]
        ):
            col_ids.abstimmung = i
            continue
        if any(option in columnname for option in ["fraktion", "gruppe"]):
            col_ids.fraktion = i
            continue
        if any(option in columnname for option in ["ja"]):
            col_ids.ja = i
            continue
        if any(option in columnname for option in ["nein"]):
            col_ids.nein = i
            continue
        if any(
            option in columnname for option in ["enthaltung", "enthalten", "enthiel"]
        ):
            col_ids.enthaltung = i
            continue
        if any(option in columnname for option in ["ungueltig", "ungültig"]) or (
            "ung" in columnname and "ltig" in columnname
        ):
            col_ids.ungueltig = i
            continue
        if any(option in columnname for option in ["nichtabgegeben", "nichtabgg"]):
            col_ids.nichtabgegeben = i
            continue
        if any(option in columnname for option in ["bezeichnung"]):
            col_ids.mdb = i
            continue
        if any(option in columnname for option in ["bemerkung"]):
            col_ids.bemerkung = i
            continue

    return col_ids


def fraktionsmapper(s: str) -> str:
    s = s.lower()
    if "afd" in s:
        return "AfD"
    if "bü90/gr" in s:
        return "Bündnis 90/Die Grünen"
    if "cdu" in s or "csu" in s:
        return "CDU/CSU"
    if "linke" in s:
        return "Die Linke"
    if "fdp" in s:
        return "FDP"
    if "fraktionslos" in s:
        return "Fraktionslos"
    if "spd" in s:
        return "SPD"
    if "bsw" in s:
        return "BSW"
    sys.exit(12)
