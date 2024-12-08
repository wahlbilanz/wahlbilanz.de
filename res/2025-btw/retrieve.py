import json
from pathlib import Path
from typing import Dict, Mapping, cast
import requests
from bs4 import BeautifulSoup, Tag
import random, string
import sys
import pandas as pd
from src.jekyll_generator import generate_jekyll_pages
from src.drucksachen import retrieve_drucksachen, summarise_drucksachen
from src.link_resources import link_resources
import magic
import os
import re
import argparse
import logging

from src.abstimmungsergebnisse import (
    download_abstimmungsergebnisse,
    pdf_convert_all,
    xlsx_convert_all,
)
from src.bundestag_web import (
    BundestagsWebsite,
    download_website,
    web_date,
    web_text,
    web_text_html,
    web_title,
)
from src.utils import download_file

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

mime = magic.Magic(mime=True)

BASE_PATH = Path(__file__).parent.resolve()


dir_abstimmungsergebnisse = BASE_PATH / "abstimmungsergebnisse"
dir_abstimmungsergebnisse.mkdir(parents=True, exist_ok=True)

dir_csv_ergebnisse = BASE_PATH / "abstimmungsergebnisse_csv"
dir_csv_ergebnisse.mkdir(parents=True, exist_ok=True)
file_csv_ergebnisse = BASE_PATH / "abstimmungsergebnisse.csv"

dir_text_ergebnisse = BASE_PATH / "abstimmungsergebnisse_text"
dir_text_ergebnisse.mkdir(parents=True, exist_ok=True)
file_text_ergebnisse = BASE_PATH / "abstimmungsergebnisse_text.json"

dir_website = BASE_PATH / "bundestag.de"
dir_website.mkdir(parents=True, exist_ok=True)
file_website = BASE_PATH / "bundestagspages.json"

file_resource_links = BASE_PATH / "linked_resources.json"

dir_drucksachen = BASE_PATH / "drucksachen"
dir_drucksachen.mkdir(parents=True, exist_ok=True)

dir_jekyll_pages = BASE_PATH / "../../abstimmungen/"


arg_parser = argparse.ArgumentParser("retrieve.py")

arg_parser.add_argument(
    "--download-abstimmungsergbisse",
    help="download abstimmungsergebnisse",
    action="store_true",
)
arg_parser.add_argument(
    "--download-website", help="download website", action="store_true"
)
arg_parser.add_argument("--csv", help="convert xlsc to csv files", action="store_true")
arg_parser.add_argument(
    "--pdf", help="convert pdf to text / json files", action="store_true"
)
arg_parser.add_argument(
    "--link",
    help="link spreadsheets and CSV and PDFs and bundestagspages",
    action="store_true",
)

args = arg_parser.parse_args()

print(args)

if args.download_abstimmungsergbisse:
    download_abstimmungsergebnisse(dir_abstimmungsergebnisse)

# if args.csv:
df = xlsx_convert_all(
    dir_abstimmungsergebnisse, dir_csv_ergebnisse, file_csv_ergebnisse
)
# print(df["fraktion"].value_counts())


# if args.pdf:
texte = pdf_convert_all(
    dir_abstimmungsergebnisse, dir_text_ergebnisse, file_text_ergebnisse
)

# if args.download_website:
website = download_website(dir_website, file_website)

resource_links = link_resources(
    dir_abstimmungsergebnisse,
    dir_csv_ergebnisse,
    texte,
    website,
    df[["abtimmungs_id", "periode", "sitzung", "abstimmung"]]
    .drop_duplicates()
    .sort_values(["periode", "sitzung", "abstimmung"])
    .values.tolist(),
    file_resource_links,
    df.groupby("abtimmungs_id")
    .sum(True)[["ja", "nein", "enthaltung", "ungueltig", "nichtabgegeben"]]
    .to_dict(orient="index"),
)

retrieve_drucksachen(resource_links, dir_drucksachen)
summarise_drucksachen(dir_drucksachen)
generate_jekyll_pages(
    dir_jekyll_pages,
    resource_links,
    website,
    dir_drucksachen,
    texte,
    df,
)
