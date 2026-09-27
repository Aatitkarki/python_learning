import argparse
from collections import defaultdict
import csv
from datetime import date
from decimal import Decimal
import json
from pathlib import Path

def load_expenses(path):
    records = []
    with Path(path).open(encoding='utf-8', newline='') as handle:
        reader = csv.DictReader(handle)

        for line, row in enumerate(reader, 2):
            exp_date = date.fromisoformat(row['date'])
            category = row['category']
            amount = Decimal(row['amount'])
            if not category or not amount.is_finite() or amount < 0:
                    raise ValueError('Invalid category or amount')
            records.append({'date':exp_date,'category':category,'amount':amount})
    return records

# Build the expense CLI in Stage 01: total, category/month summaries, mean, maximum, and bad-row diagnostics. Use a temporary directory for file tests.
def summarize(records):
    categories, months = defaultdict(Decimal), defaultdict(Decimal)
    for row in records:
        categories[row['category']] += row['amount']
        months[row['date'].strftime('%Y-%m')] += row['amount']
    total = sum(row['amount'] for row in records) 
    return {
         'Count': len(records),
         'Total': str(total),
         'Average': str(total/len(records)), 
         'Highest': str(max(row['amount'] for row in records)),
         'By Category': {
            k:str(v) for k,v in categories.items()
         },
         'By Months': {
            k:str(v) for k,v in months.items()
         },
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('csv', nargs='?', default='datasets/expenses.csv')
    args = parser.parse_args()
    print(json.dumps(summarize(load_expenses(args.csv)), indent=2))
    # print(load_expenses(args.csv))

