"""Command-line entry point for the Week 4 web crawler."""
import argparse
import logging
from pathlib import Path

from web_crawler.crawler import WebCrawler
from web_crawler.exporter import export_csv, export_json

def configure_logging(output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(output_dir / "crawler.log", encoding="utf-8"),
        ],
    )

def parse_args():
    parser = argparse.ArgumentParser(
        description="Crawl a website politely, extract page information, and export JSON/CSV."
    )
    parser.add_argument("start_url", help="Starting http(s) URL")
    parser.add_argument("--max-pages", type=int, default=10, help="Maximum number of HTML pages to fetch (default: 10)")
    parser.add_argument("--delay", type=float, default=1.0, help="Delay in seconds between requests (default: 1.0)")
    parser.add_argument("--timeout", type=float, default=10.0, help="Request timeout in seconds (default: 10)")
    parser.add_argument("--output-dir", default="output", help="Directory for JSON, CSV, and log files")
    parser.add_argument("--allow-external", action="store_true", help="Follow external-domain links too")
    return parser.parse_args()

def main():
    args = parse_args()
    output_dir = Path(args.output_dir)
    configure_logging(output_dir)
    logger = logging.getLogger("web_crawler")

    try:
        crawler = WebCrawler(
            max_pages=args.max_pages,
            delay=args.delay,
            timeout=args.timeout,
            allow_external=args.allow_external,
        )
        records = crawler.crawl(args.start_url)
        json_path = export_json(records, output_dir / "crawled_data.json")
        csv_path = export_csv(records, output_dir / "crawled_data.csv")
        logger.info("Crawl finished: %d page(s) saved.", len(records))
        logger.info("JSON output: %s", json_path.resolve())
        logger.info("CSV output:  %s", csv_path.resolve())
        if not records:
            logger.warning("No pages were collected. Check URL, connection, site policy, and logs.")
    except (ValueError, OSError) as exc:
        logger.error("%s", exc)
        raise SystemExit(2)

if __name__ == "__main__":
    main()
