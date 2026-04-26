import sys
import json
import unicodedata
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from parser import lex
import lexer_rules
lexer = lex.lex(module=lexer_rules)

from parser import yacc
import parser_rules
parser_rules.lexer = lexer
parser = yacc.yacc(module=parser_rules)

def remove_accents(text):
    return ''.join(
        c for c in unicodedata.normalize('NFKD', text)
        if not unicodedata.combining(c)
    )

card_path = Path(__file__).parent.parent.parent / "cards.json"
with open(card_path, "r") as f:
    cards = json.load(f)

parsed_cards = []

for card in cards:
    name = remove_accents(card["player_name"])
    position = card["position"]
    country = remove_accents(card.get("country", ""))
    s = card["stats"]

    card_str = f"{name} | {position} | {country} | {s['pac']} {s['sho']} {s['pas']} {s['dri']} {s['def']} {s['phy']}"
    parsed_card = parser.parse(card_str, lexer=lexer)

    if parsed_card:
        parsed_cards.append(parsed_card)

for c in parsed_cards:
    print(f"{c['player_name']} ({c['position']}) - Rating: {c['rating']}")

from starting11 import build_starting_11, print_lineup
lineup = build_starting_11(parsed_cards)
print_lineup(lineup)