import csv
from pathlib import Path
from typing import List

class Report:

    @staticmethod
    def save(header: List[str], content: str):
        report = Path(__file__).parents[1] / "resources/appraisals.csv"
        add_header_flag: bool = not report.exists()
        with report.open("a+", newline="") as fh:
            csv_writer = csv.writer(fh)
            if add_header_flag:
                csv_writer.writerow(header)
            csv_writer.writerow(content)