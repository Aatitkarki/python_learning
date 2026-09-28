"""01b: contact CRUD, normalized unique emails, and JSON persistence."""
import json
from pathlib import Path

class ContactBook:
    def __init__(self): self._contacts = {}
    @staticmethod
    def key(email):
        email = email.strip().casefold()
        if email.count('@') != 1 or any(c.isspace() for c in email) or not all(email.split('@')):
            raise ValueError('An email identifier is required')
        return email
    def add(self, email, name, phone=''):
        email = self.key(email)
        if email in self._contacts: raise ValueError('Duplicate email')
        if not name.strip(): raise ValueError('Name is required')
        self._contacts[email] = dict(email=email, name=name.strip(), phone=phone.strip())
    def update(self, email, *, name=None, phone=None):
        key = self.key(email)
        if key not in self._contacts: raise KeyError(key)
        record = dict(self._contacts[key])
        if name is not None:
            if not name.strip(): raise ValueError('Name is required')
            record['name'] = name.strip()
        if phone is not None: record['phone'] = phone.strip()
        self._contacts[key] = record
    def search(self, query):
        query = query.casefold()
        return [dict(value) for key, value in sorted(self._contacts.items())
                if query in key or query in value['name'].casefold() or query in value['phone']]
    def delete(self, email): return self._contacts.pop(self.key(email), None) is not None
    def save(self, path):
        Path(path).write_text(json.dumps(self.search(''), ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    @classmethod
    def load(cls, path):
        result = cls()
        records = json.loads(Path(path).read_text(encoding='utf-8'))
        if not isinstance(records, list): raise ValueError('Expected a JSON list')
        for record in records:
            if not isinstance(record, dict) or set(record) != {'email', 'name', 'phone'}:
                raise ValueError('Invalid contact record')
            result.add(**record)
        return result

if __name__ == '__main__':
    book = ContactBook()
    book.add('ada@example.test', 'Ada', '123')
    book.update('ADA@example.test', phone='456')
    print(book.search('ada'))
    print('Deleted:', book.delete('ada@example.test'))
