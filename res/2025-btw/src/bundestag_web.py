from dataclasses import dataclass
import json
from pathlib import Path
import sys
import logging
from typing import Dict, List, Optional

from bs4 import BeautifulSoup
from dataclasses_json import dataclass_json

from src.utils import download_file
from src.consts import drucksachen_url_pattern

logger = logging.getLogger(__name__)

pageids = range(756, 938)
# what happened here: https://www.bundestag.de/parlament/plenum/abstimmung/abstimmung?id=836
broken_pages = list(range(836, 840)) + [862, 896, 899, 901]


@dataclass_json
@dataclass
class BundestagsWebsite:
    id: int
    date: Optional[str]
    title: str
    text: str
    text_html: str
    drucksachen: List[str]
    result: Dict[str, int]


def web_title(soup):
    for i in soup.select(".bt-standard-content .bt-artikel__title"):
        return ("".join(i.findAll(string=True, recursive=False))).strip()


def web_date(soup):
    for i in soup.select("article.bt-artikel .bt-date"):
        return ("".join(i.findAll(string=True, recursive=False))).strip()


def web_text(soup):
    for i in soup.select("article.bt-artikel > p"):
        return i.text


def web_text_html(soup):
    for i in soup.select("article.bt-artikel > p"):
        return i.encode_contents().decode("UTF-8")


def web_gesamt_result_entry(soup, c: str) -> Optional[int]:
    for i in soup.select(c):
        return int(i.encode_contents().decode("UTF-8"))
    return None


def web_gesamt_result(soup) -> Dict[str, int]:
    ja = web_gesamt_result_entry(soup, ".bt-legend-ja > span")
    nein = web_gesamt_result_entry(soup, ".bt-legend-nein > span")
    enthalten = web_gesamt_result_entry(soup, ".bt-legend-enthalten > span")
    return {
        "ja": ja if ja is not None else 0,
        "nein": nein if nein is not None else 0,
        "enthaltung": enthalten if enthalten is not None else 0,
    }


def download_website(
    bundestags_website_dir: Path, bundestags_website_json: Path
) -> List[BundestagsWebsite]:
    bundestag_websites: List[BundestagsWebsite] = []
    if not bundestags_website_json.is_file():
        logging.info(
            f"no bundestags web json summary yet... generating one {bundestags_website_json}"
        )
        for i in pageids:
            if i in broken_pages:
                continue
            target = bundestags_website_dir / f"{i}"
            if not target.is_file():
                logging.info("downloading web page for ", i)
                download_file(
                    f"https://www.bundestag.de/parlament/plenum/abstimmung/abstimmung?id={i}",
                    target,
                )
            with open(target, "r") as target_read:
                soup = BeautifulSoup(target_read, "html.parser")
                text_html = web_text_html(soup)
                o = BundestagsWebsite(
                    id=i,
                    date=web_date(soup),
                    title=web_title(soup),
                    text=web_text(soup),
                    text_html=text_html,
                    drucksachen=drucksachen_url_pattern.findall(text_html),
                    result=web_gesamt_result(soup),
                )
                if o.title is not None:
                    bundestag_websites.append(o)
                else:
                    print(f"error with meta of {i}")
                    sys.exit(1)

        with open(bundestags_website_json, "w") as f:
            f.write(BundestagsWebsite.schema().dumps(bundestag_websites, many=True))
            # f.write(
            #     json.dumps(
            #         bundestag_websites,
            #         sort_keys=True,
            #         indent=2,
            #         separators=(",", ": "),
            #         default=lambda o: o.__dict__,
            #     )
            # )
    else:
        with open(bundestags_website_json, "r") as f:
            bundestag_websites = BundestagsWebsite.schema().load(
                json.load(f), many=True
            )
            # bundestag_websites = json.load(f)
    return bundestag_websites
