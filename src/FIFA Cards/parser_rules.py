import lexer_rules
from position_weights import POSITION_WEIGHTS

tokens = lexer_rules.tokens

def p_card(p):
    '''card : name "|" POSITION "|" COUNTRY "|" STATS STATS STATS STATS STATS STATS'''
    # p[1]=name (PLAYER_NAME or COUNTRY), p[3]=position, p[5]=country, p[7-12]=stats
    stats = {'pac': p[7], 'sho': p[8], 'pas': p[9], 'dri': p[10], 'def': p[11], 'phy': p[12]}
    weights = POSITION_WEIGHTS.get(p[3])
    rating = sum(stats[s] * w for s, w in weights.items())
    p[0] = round(rating)

def p_name(p):
    '''name : PLAYER_NAME
            | COUNTRY'''
    p[0] = p[1]

def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}'")
    else:
        print("Syntax error at EOF")
