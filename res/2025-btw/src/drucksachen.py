from pathlib import Path
from typing import List
import logging
import os
import google.generativeai as genai

from src.link_resources import AbstimmungsResourcen
from src.consts import drucksachen_url_prefix
from src.utils import download_file

logger = logging.getLogger(__name__)

os.environ["GRPC_VERBOSITY"] = "ERROR"
os.environ["GLOG_minloglevel"] = "2"


def get_drucksachen_url(drucksache: str) -> str:
    return f"{drucksachen_url_prefix}/{drucksache[2:5]}/{drucksache}.pdf"


def retrieve_drucksachen(
    resource_links: List[AbstimmungsResourcen], dir_drucksachen: Path
):
    for resource in resource_links:
        for drucksache in resource.drucksachen:
            file = dir_drucksachen / f"{drucksache}.pdf"
            if not file.is_file():
                url = get_drucksachen_url(drucksache)
                logger.info(f"Download der Drucksache {drucksache} von {url}")
                download_file(url=url, target=file)


def summarise_drucksachen(dir_drucksachen: Path):
    gemini_key = os.environ.get("GEMINI_API_KEY")
    if gemini_key is None:
        logger.error("Fasse Drucksachen nicht zusammen weil API key fehlt")
        return

    genai.configure(api_key=gemini_key)

    prompt = "Fasse die angehängte Drucksache des deutchen Bundestages in einer Überschrift und einem kurzen Absatz zusammen. Die Überschrift sollte auch den Dokumenttyp (Gesetzesentwurf, Antrag, Beschlussempfehlung, Bericht) enthalten. Falls es ein Antrag ist muss klar werden von wem der Antrag kommt. Wenn es keine Beschlussempfehlung ist liste die Kernpunkte und Ziele ohne Erklärung kurz auf. Du brauchst nicht erwähnen um welche Drucksache es geht. Schreib es so, dass es direkt in einem kleinen Widget auf einer Webseite angezeigt werden kann. Nutze Markdown um die Überschrift in dritter Ebene auszuzeichnen und die Überschrift 'Kernpunkte und Ziele:' fett hervorzuheben. Bestätige nicht den Prompt und warne nicht vor der Kürze der Zusammenfassung."

    for drucksache in dir_drucksachen.iterdir():
        if drucksache.name in ["2003100.pdf", "2001000.pdf", "2007800.pdf"]:
            # haushaltsplan ist zu lang...
            continue
        drucksache_summary = dir_drucksachen / drucksache.name.replace("pdf", "gemini")
        if not drucksache_summary.is_file():
            logger.info(f"Fasse {drucksache.name} zusammen...")
            pdf = genai.upload_file(drucksache)
            logger.info(f"{drucksache.name} hochgeladen...")
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content([prompt, pdf])
            with open(drucksache_summary, "w") as f:
                f.write(response.text)
            logger.info(f"Zusammenfassung:\n\n{response.text}\n\n")
