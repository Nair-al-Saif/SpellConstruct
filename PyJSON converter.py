# convert_to_json.py
import json
from Components import COMPONENTS

with open('components.json', 'w', encoding='utf-8') as f:
    json.dump(COMPONENTS, f, ensure_ascii=False, indent=4)