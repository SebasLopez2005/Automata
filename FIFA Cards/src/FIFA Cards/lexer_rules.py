# Token types
tokens = (
    'PLAYER_NAME',
    'POSITION',
    'STATS',
    'COUNTRY'
)

literals = ['|']

# Token rules
def t_POSITION(t):
    r'(ST|CF|CAM|CM|CDM|LW|RW|LM|RM|LB|RB|CB|GK|LWB|RWB)'
    return t

def t_COUNTRY(t):
    r"[A-Za-z][A-Za-z .\-]*"
    return t

t_PLAYER_NAME = r"[A-Za-z][A-Za-z .'\-]*"

def t_STATS(t):
    r'[1-9][0-9]?'
    t.value = int(t.value)
    return t

t_ignore = ' \t'

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)
