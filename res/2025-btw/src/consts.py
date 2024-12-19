import re


drucksachen_url_pattern = re.compile(
    r"dserver.bundestag.de/btd/20/[0-9]+/([0-9]+).pdf", re.MULTILINE
)
drucksachen_text_pattern = re.compile(r"\s20/([0-9]+)", re.MULTILINE)
drucksachen_url_prefix = "https://dserver.bundestag.de/btd/20"
