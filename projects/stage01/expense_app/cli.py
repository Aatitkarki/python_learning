import argparse
import json
import logging
from .parser import CsvRepository
from .domain import ExpenseAnalyzer

def main(argv=None):
    parser = argparse.ArgumentParser(); parser.add_argument('csv'); args = parser.parse_args(argv)
    try: report = ExpenseAnalyzer(CsvRepository(args.csv)).report()
    except (OSError, ValueError) as exc:
        logging.error('Expense input failed: %s', exc)
        return 2
    print(json.dumps(report, indent=2))
    logging.info('Analyzed %d records', report['count'])
    return 0

if __name__ == '__main__': raise SystemExit(main())
