import sys
import json
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

# Lexer: tokenizes input (checks syntax with rules)
from parser import lex
import lexer_rules
lexer = lex.lex(module=lexer_rules)

# Parser: parses tokens and computes rating (like calc evaluates expressions)
from parser import yacc
import parser_rules
parser_rules.lexer = lexer
parser = yacc.yacc(module=parser_rules)

# Load cards from JSON
card_path = Path(__file__).parent.parent.parent / "cards.json"
with open(card_path, 'r') as f:
    cards = json.load(f)

for card in cards:
    name = card['player_name']
    position = card['position']
    country = card.get('country', '')
    s = card['stats']
    card_str = f"{name} | {position} | {country} | {s['pac']} {s['sho']} {s['pas']} {s['dri']} {s['def']} {s['phy']}"

    rating = parser.parse(card_str)
    print(f"{name} ({position}): {rating}")
