import json
import os
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

API_KEY = os.environ.get("FOOTBALL_DATA_API_KEY")
if not API_KEY:
    raise SystemExit("Manca il segreto FOOTBALL_DATA_API_KEY")

url = "https://api.football-data.org/v4/matches"
request = urllib.request.Request(
    url,
    headers={"X-Auth-Token": API_KEY},
)

with urllib.request.urlopen(request, timeout=30) as response:
    data = json.load(response)

partite = []
for match in data.get("matches", []):
    partite.append({
        "id": match.get("id"),
        "data": match.get("utcDate"),
        "competizione": match.get("competition", {}).get("name"),
        "casa": match.get("homeTeam", {}).get("name"),
        "trasferta": match.get("awayTeam", {}).get("name"),
        "stato": match.get("status"),
        "gol_casa": match.get("score", {}).get("fullTime", {}).get("home"),
        "gol_trasferta": match.get("score", {}).get("fullTime", {}).get("away"),
    })

output = {
    "aggiornato_il": datetime.now(timezone.utc).isoformat(),
    "partite": partite,
}

Path("dati").mkdir(exist_ok=True)
Path("dati/partite.json").write_text(
    json.dumps(output, ensure_ascii=False, indent=2),
    encoding="utf-8",
)
print(f"Salvate {len(partite)} partite in dati/partite.json")
