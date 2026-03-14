# Token types
tokens = (
    'PLAYER_NAME',
    'POSITION',
    'STATS',
    'COUNTRY'
)

literals = ['|']

# Token rules - order matters: POSITION before COUNTRY (so "CF" matches POSITION)
def t_POSITION(t):
    r'(ST|CF|CAM|CM|CDM|LW|RW|LM|RM|LB|RB|CB|GK|LWB|RWB)'
    return t

def t_COUNTRY(t):
    r"[A-Za-z][A-Za-z .\-]*"  # No apostrophe: Argentina, Costa Rica
    return t

t_PLAYER_NAME = r"[A-Za-z][A-Za-z .'\-]*"  # With apostrophe: O'Brien

def t_STATS(t):
    r'[1-9][0-9]?'
    t.value = int(t.value)
    return t

# Ignore spaces and tabs between tokens
t_ignore = ' \t'

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)
