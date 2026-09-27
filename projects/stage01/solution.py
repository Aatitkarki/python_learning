"""CSV expense analyzer. Run from repo root: python -m projects.stage01.solution."""
import argparse
import csv
import json
from collections import defaultdict
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path

def load_expenses(path):
    records = []
    with Path(path).open(encoding='utf-8', newline='') as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != ['date', 'category', 'amount']:
            raise ValueError('Expected date,category,amount columns')
        for line, row in enumerate(reader, 2):
            try:
                day = date.fromisoformat(row['date'])
                category = row['category'].strip()
                amount = Decimal(row['amount'])
                if not category or not amount.is_finite() or amount < 0:
                    raise ValueError('Invalid category or amount')
            except (ValueError, TypeError, InvalidOperation, AttributeError) as exc:
                raise ValueError(f'Invalid expense on CSV line {line}') from exc
            records.append({'date': day, 'category': category, 'amount': amount})
    return records

def summarize(records):
    categories, months = defaultdict(Decimal), defaultdict(Decimal)
    for row in records:
        categories[row['category']] += row['amount']
        months[row['date'].strftime('%Y-%m')] += row['amount']
    total = sum((row['amount'] for row in records), Decimal('0'))
    return {'count': len(records), 'total': str(total),
            'average': str(total/len(records)) if records else None,
            'highest': str(max(row['amount'] for row in records)) if records else None,
            'by_category': {k: str(v) for k,v in sorted(categories.items())},
            'by_month': {k: str(v) for k,v in sorted(months.items())}}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('csv', nargs='?', default='datasets/expenses.csv')
    args = parser.parse_args()
    print(json.dumps(summarize(load_expenses(args.csv)), indent=2))
