from pathlib import Path
import sys
from typing import Dict, List, Optional, Union
import logging
import pandas as pd

from src.drucksachen import get_drucksachen_url
from src.bundestag_web import BundestagsWebsite
from src.link_resources import AbstimmungsResourcen

sys.path.append("../../abstimmungen")
from abstimmungsparser import Abstimmung

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def calculate_ergebnis(
    df: pd.DataFrame, abstimmungs_id: str
) -> Dict[str, Dict[str, int]]:

    ergebnis = (
        df.loc[df["abtimmungs_id"] == abstimmungs_id]
        .groupby("fraktion")
        .sum(True)[["ja", "nein", "enthaltung", "ungueltig", "nichtabgegeben"]]
    )
    ergebnis["gesamt"] = ergebnis[list(ergebnis.columns)].sum(axis=1)
    return ergebnis.to_dict("index")


def generate_jekyll_pages(
    dir_jekyll_pages: Path,
    resource_links: List[AbstimmungsResourcen],
    website: List[BundestagsWebsite],
    dir_drucksachen: Path,
    texte: Dict[str, Dict[str, Union[str, List[str]]]],
    df: pd.DataFrame,
):
    if not dir_jekyll_pages.is_dir():
        print(f"jekyll page directory does not exist...? {dir_jekyll_pages}")
        sys.exit(24)

    # for page in dir_jekyll_pages.iterdir():
    #     print(page.name)

    for resource_link in resource_links:
        jekyll_dir = dir_jekyll_pages / resource_link.abstimmungs_id
        jekyll_file = jekyll_dir / "index.md"
        if not jekyll_dir.is_dir():
            jekyll_dir.mkdir(parents=True, exist_ok=True)

        if not jekyll_file.is_file():
            abstimmung = Abstimmung()
            logger.info(f"  > erstelle neue abstimmungsseite {jekyll_file}")
            abstimmung.add_tag("Todo")
            abstimmung.add_category("Todo")
            # else:
            #     logger.info("  > lese existierende abstimmungsseite " + jekyll_file)
            #     abstimmung.parse_abstimmung(jekyll_file)

            web_page = next((i for i in website if i.id == resource_link.web_id), None)
            if web_page is None:
                print("did not find a web page for resource link")
                print(resource_link)
                print(website)
                sys.exit(91)

            abstimmung.set_abstimmung(resource_link.abstimmung)
            abstimmung.set_bundestagssitzung(resource_link.sitzung)
            abstimmung.set_legislaturperiode(resource_link.periode)
            abstimmung.set_abstimmungs_ergebnisse(
                calculate_ergebnis(df, resource_link.abstimmungs_id)
            )
            abstimmung.set_title("Abstimmung: " + web_page.title)
            abstimmung.add_link(
                {
                    "title": "Link zu bundestag.de",
                    "url": f"https://www.bundestag.de/parlament/plenum/abstimmung/abstimmung?id={resource_link.web_id}",
                }
            )

            abstimmung.set_datum(web_page.date)

            # datafiles = abstimmung.get_data_files()
            # TODO: check if the files are not there yet!
            abstimmung.add_data_file(
                {
                    "title": f"Abstimmungsergebnis {resource_link.pdf}",
                    "url": f"/res/2025-btw/abstimmungsergebnisse/{resource_link.pdf}",
                }
            )
            abstimmung.add_data_file(
                {
                    "title": f"Abstimmungsergebnis {resource_link.xlsx}",
                    "url": f"/res/2025-btw/abstimmungsergebnisse/{resource_link.xlsx}",
                }
            )
            abstimmung.add_data_file(
                {
                    "title": f"Abstimmungsergebnis {resource_link.csv}",
                    "url": f"/res/2025-btw/abstimmungsergebnisse_csv/{resource_link.csv}",
                }
            )
            for d in resource_link.drucksachen:
                d_id = int(d[2:])
                url = get_drucksachen_url(d)
                summary: Optional[str] = None
                file_drucksache_summary = dir_drucksachen / f"{d}.gemini"
                if file_drucksache_summary.is_file():
                    with open(file_drucksache_summary, "r") as fi:
                        summary = fi.read()

                abstimmung.add_document(
                    {
                        "title": f"Drucksache 20/{d_id}",
                        "url": url,
                        "local": f"/res/2025-btw/drucksachen/{d}.pdf",
                        "summary": summary,
                    }
                )

            if resource_link.pdf in texte:
                abstimmung.set_preview(texte[resource_link.pdf]["text"])
            else:
                print(texte)
                logger.error(
                    f"did not find text for abstimmung {resource_link.abstimmungs_id}"
                )
                sys.exit(44)

            abstimmung.write_abstimmung(jekyll_file)
            logger.info(f"wrote {jekyll_file}")
            # break
