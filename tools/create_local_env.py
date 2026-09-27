"""Create local-only random demo credentials without printing them or overwriting a file."""
import json
import os
import secrets
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
path=ROOT/'.env'
password=secrets.token_urlsafe(24)
keys={secrets.token_urlsafe(32):'A', secrets.token_urlsafe(32):'B'}
content=f"POSTGRES_PASSWORD={password}\nCOURSE_API_KEYS='{json.dumps(keys,separators=(',',':'))}'\nCOURSE_SEED=1\n"
fd=os.open(path,os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600)
with os.fdopen(fd,'w') as handle: handle.write(content)
print('Created .env with private local demo credentials. Existing files are never overwritten.')
