SCORE_CARD_FIELD_NAME = 'Score'

BACKEND = {
    0: 'back (5m)',
    1: 'back (15m)',
    2: 'back (30m)',
    3: 'back (1h)',
    4: 'back (2h)',
    5: 'back (4h)',
    6: 'back (8h)',
}
BACKEND_HOURS = {
    0.083333333: 'back (5m)',
    0.25: 'back (15m)',
    0.5: 'back (30m)',
    1: 'back (1h)',
    2: 'back (2h)',
    4: 'back (4h)',
    8: 'back (8h)',
}
BACKEND_CHOICES = [(f'{k}. {v}', f'{k}. {v}') for k, v in BACKEND.items()]
BACKEND_HOURS_CHOICES = [
    (str(k), v)
    for k, v in BACKEND_HOURS.items()
]

FRONTEND = {
    0: 'front (5m)',
    1: 'front (30m)',
    2: 'front (1h)',
    3: 'front (1h30)',
    4: 'front (2h)',
    5: 'front (3h)',
    6: 'front (5h)',
}
FRONTEND_HOURS = {
    0.083333333: 'front (5m)',
    0.5: 'front (30m)',
    1: 'front (1h)',
    1.5: 'front (1h30)',
    2: 'front (2h)',
    3: 'front (3h)',
    5: 'front (5h)',
}
FRONTEND_CHOICES = [(f'{k}. {v}', f'{k}. {v}') for k, v in FRONTEND.items()]

MOBILE = {
    0: 'mobile (5m)',
    1: 'mobile (30m)',
    2: 'mobile (1h)',
    3: 'mobile (2h)',
    4: 'mobile (3h)',
    5: 'mobile (5h)',
    6: 'mobile (8h)',
}
MOBILE_HOURS = {
    0.083333333: 'mobile (5m)',
    0.5: 'mobile (30m)',
    1: 'mobile (1h)',
    2: 'mobile (2h)',
    3: 'mobile (3h)',
    5: 'mobile (5h)',
    8: 'mobile (8h)',
}
MOBILE_CHOICES = [(f'{k}. {v}', f'{k}. {v}') for k, v in MOBILE.items()]

LIB = {
    0: 'lib (5m)',
    1: 'lib (30m)',
    2: 'lib (1h)',
    3: 'lib (2h)',
    4: 'lib (3h)',
    5: 'lib (5h)',
    6: 'lib (8h)',
}
LIB_HOURS = {
    0.083333333: 'lib (5m)',
    0.5: 'lib (30m)',
    1: 'lib (1h)',
    2: 'lib (2h)',
    3: 'lib (3h)',
    5: 'lib (5h)',
    8: 'lib (8h)',
}
LIB_CHOICES = [(f'{k}. {v}', f'{k}. {v}') for k, v in LIB.items()]

PED = {
    0: 'P&D (1H)',
    1: 'P&D (2h)',
    2: 'P&D (4h)',
    3: 'P&D (8h)',
    4: 'P&D (16h)',
}
PED_HOURS = {
    1: 'P&D (1h)',
    2: 'P&D (2h)',
    4: 'P&D (4h)',
    8: 'P&D (8h)',
    16: 'P&D (16h)',
}
PED_CHOICES = [(f'{k}. {v}', f'{k}. {v}') for k, v in PED.items()]

SCORES = {
    'backend': BACKEND,
    'frontend': FRONTEND,
    'mobile': MOBILE,
    'lib': LIB,
    'ped': PED,
}
