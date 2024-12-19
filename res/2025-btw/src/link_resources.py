import json
from pathlib import Path
import sys
from typing import Dict, List, Optional, Union
from dataclasses import dataclass
from dataclasses_json import dataclass_json
import pandas as pd

from src.bundestag_web import BundestagsWebsite


@dataclass_json
@dataclass
class AbstimmungsResourcen:
    abstimmungs_id: str
    periode: int
    sitzung: int
    abstimmung: int
    csv: str
    xlsx: str
    pdf: str
    web_id: int
    drucksachen: List[str]


def same_webpage(
    website: BundestagsWebsite, drucksachen: List[str], results: Dict[str, int]
) -> bool:
    if website.drucksachen != drucksachen:
        return False

    print("---")
    print(website.date, drucksachen)
    print(results)
    print(website.result)
    print("---")
    for res in website.result:
        if results[res] != website.result[res]:
            return False

    return True


def link_resources(
    dir_abstimmungsergebnisse: Path,
    dir_csv_ergebnisse: Path,
    texte: Dict[str, Dict[str, Union[str, List[str]]]],
    website: List[BundestagsWebsite],
    abstimmungs_ids: List[List[Union[str, int]]],
    file_resource_links: Path,
    gesamt_result: Dict[str, Dict[str, int]],
):
    links: List[AbstimmungsResourcen] = []

    if not file_resource_links.is_file():
        for abstimmung in abstimmungs_ids:
            # print(abstimmung)

            csv: Optional[Path] = None
            xslx: Optional[Path] = None
            pdf: Optional[Path] = None
            web_id: Optional[int] = None
            drucksachen: Optional[List[str]]

            abstimmungs_nums = f"{abstimmung[1]},{abstimmung[2]},{abstimmung[3]}"
            for f in dir_csv_ergebnisse.iterdir():
                # print(f, abstimmungs_nums)
                with open(f, "r") as fi:
                    if abstimmungs_nums in fi.read():
                        csv = f
                        break
            # print(abstimmung, csv, abstimmungs_nums)
            if csv is None:
                print(f"csv not found {abstimmung[0]}")
                sys.exit(54)

            csv_name = csv.name
            # print(csv_name)
            con = "-" if "-" in csv_name else "_"
            base_name = csv_name.replace(f"{con}xls.csv", "")
            pdf = dir_abstimmungsergebnisse / f"{base_name}.pdf"
            xslx = dir_abstimmungsergebnisse / f"{base_name}{con}xls.xlsx"

            if pdf is None or not pdf.is_file():
                print(f"pdf not found {abstimmung[0]} {pdf}")
                sys.exit(54)

            if xslx is None or not xslx.is_file():
                print(f"pdf not found {abstimmung[0]} {xslx}")
                sys.exit(54)

            if base_name == "20220603_6":
                # there is an error in the PDF
                texte[pdf.name]["drucksachen"] = ["1409", "2090"]

            drucksachen = list(
                map(lambda x: "20" + x.zfill(5), texte[pdf.name]["drucksachen"])
            )
            print(csv_name, base_name, abstimmung, gesamt_result[f"{abstimmung[0]}"])

            for web in website:
                # print(web, content)
                if same_webpage(web, drucksachen, gesamt_result[f"{abstimmung[0]}"]):
                    web_id = web.id
                    break

            if web_id is None:
                print("did not find a web id...")
                sys.exit(96)
            # else:
            #     print(web_id)

            links.append(
                AbstimmungsResourcen(
                    f"{abstimmung[0]}",
                    int(abstimmung[1]),
                    int(abstimmung[2]),
                    int(abstimmung[3]),
                    csv.name,
                    xslx.name,
                    pdf.name,
                    web_id,
                    drucksachen,
                )
            )
        with open(file_resource_links, "w") as fo:
            fo.write(AbstimmungsResourcen.schema().dumps(links, many=True))
    else:
        with open(file_resource_links, "r") as fi:
            links = AbstimmungsResourcen.schema().load(json.load(fi), many=True)

    return links
