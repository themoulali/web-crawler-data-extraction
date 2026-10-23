"""Export crawled records to JSON and CSV."""
import csv
import json
from pathlib import Path

CSV_FIELDS = ["url", "title", "description", "headings", "text", "links", "fetched_at"]

def export_json(records: list[dict], path: str | Path) -> Path:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", encoding="utf-8") as file:
        json.dump(records, file, ensure_ascii=False, indent=2)
    return destination

def export_csv(records: list[dict], path: str | Path) -> Path:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=CSV_FIELDS, extrasaction="ignore")
        writer.writeheader()
        for record in records:
            row = dict(record)
            row["headings"] = " | ".join(row.get("headings", []))
            row["links"] = " | ".join(row.get("links", []))
            writer.writerow(row)
    return destination
