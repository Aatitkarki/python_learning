"""Stage 01 inventory project and independent CSV assessment answer."""
import csv
from decimal import Decimal, InvalidOperation
from pathlib import Path

class Inventory:
    def __init__(self): self._items = {}
    @property
    def items(self): return dict(self._items)
    def change(self, sku, delta):
        if not sku.strip() or type(delta) is not int: raise ValueError('SKU and integer quantity required')
        quantity = self._items.get(sku, 0) + delta
        if quantity < 0: raise ValueError('Insufficient stock')
        self._items[sku] = quantity
        return quantity

def summarize_inventory(path):
    """CSV sku,quantity,unit_price; duplicate SKUs rejected, exact Decimal totals."""
    items, total = [], Decimal('0')
    seen = set()
    with Path(path).open(newline='', encoding='utf-8') as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != ['sku', 'quantity', 'unit_price']: raise ValueError('Invalid columns')
        for line, row in enumerate(reader, 2):
            try:
                sku = row['sku'].strip()
                quantity = int(row['quantity'])
                price = Decimal(row['unit_price'])
                if not sku or sku in seen or quantity < 0 or not price.is_finite() or price < 0:
                    raise ValueError('Invalid record')
            except (ValueError, TypeError, AttributeError, InvalidOperation) as exc:
                raise ValueError(f'Invalid inventory row {line}') from exc
            seen.add(sku)
            value = quantity * price
            items.append(dict(sku=sku, quantity=quantity, value=str(value)))
            total += value
    return {'items': items, 'total_value': str(total)}

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(); parser.add_argument('csv'); args = parser.parse_args()
    print(summarize_inventory(args.csv))
