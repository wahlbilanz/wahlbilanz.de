The [abgeordnetenwatch.de.json](abgeordnetenwatch.de.json) was obtained from [Abgeordnetenwatch.de](https://www.abgeordnetenwatch.de) and is licensed under the [Open Database License (ODbL) v1.0](https://opendatacommons.org/licenses/odbl/1.0/):

    curl https://www.abgeordnetenwatch.de/api/parliament/eu-parlament%202014-2019/polls.json | python -mjson.tool > abgeordnetenwatch.de.json

As this dataset already aggregated the data according to european alliances, we needed to evaluate the votes of individual MEPs ourselfs..
Thus, `retrieve-individuals.sh` rerieves the data for single MEPs from abgeordnetenwatch and stores it in `abgeordnetenwatch-individual-votes/`.
In addition, `aggregate-individuals.py` iterates the individuals to create json files aggregated by parties:

* `aggregated-individuals.json` still lists individual names
* `aggregated-parties.json` only contains numbers

Go and say thanks to [Abgeordnetenwatch.de](https://www.abgeordnetenwatch.de)! They're doing great work!! :)
