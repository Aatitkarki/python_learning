"""01b: deterministic ASCII word policy; characters include whitespace/punctuation."""
import re
from collections import Counter

def analyze(text, limit=5):
    if limit < 0: raise ValueError('Nonnegative limit required')
    counts = Counter(re.findall(r'[a-z]+', text.lower()))
    top = sorted(counts.items(), key=lambda pair: (-pair[1], pair[0]))[:limit]
    return {'characters': len(text), 'words': sum(counts.values()), 'unique_words': len(counts),
            'top_words': top, 'most_common': top[0][0] if top else None}

if __name__ == '__main__': print(analyze('AI, ai! Data and data.'))
