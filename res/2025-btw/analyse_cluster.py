from typing import Dict, Set
import duckdb
import math

abstimmungsergebnisse = duckdb.read_csv("abstimmungsergebnisse.csv")

abstimmungs_votes = duckdb.sql(
    "select abstimmungsergebnisse.abtimmungs_id, fraktion, sum(ja)/(sum(ja)+sum(nein)) from abstimmungsergebnisse group by abstimmungsergebnisse.abtimmungs_id, fraktion order by abstimmungsergebnisse.abtimmungs_id"
)

summary: Dict[str, Dict[str, float]] = {}
fraktionen: Set[str] = set()
for x in abstimmungs_votes.fetchall():
    # print(x[0])
    if x[0] not in summary:
        summary[x[0]] = {}
    summary[x[0]][x[1]] = x[2]
    fraktionen.add(x[1])

with open("analyse_cluster.table", "w") as f:
    f.write(f"Abstimmung\t")
    for fraktion in fraktionen:
        f.write(f"{fraktion}\t")
    f.write("\n")

    for abst_id, ergebnisse in summary.items():
        f.write(f"{abst_id}\t")
        for fraktion in fraktionen:
            if fraktion in ergebnisse:
                v = ergebnisse[fraktion]
                if math.isnan(v):
                    v = -1
                f.write(f"{v}\t")
            else:
                f.write("-1\t")
        f.write("\n")
        # print(abst_id, ergebnisse)
