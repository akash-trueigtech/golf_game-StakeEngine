"""
Defines all symbol types for the Golf Betting Game.
Each symbol has:
- name: UI-friendly long name
- code: short identifier like P1/H1/S1
- type: payout / soft_end / hard_end / hole / empty
- multiplier: payout multiplier if applicable
"""

from dataclasses import dataclass


@dataclass
class GolfSymbol:
    name: str
    code: str
    type: str                # payout | soft_end | hard_end | hole | empty
    multiplier: int = 0      # only for payout symbols


# ------------------------
# PAYOUTS – ZONE-WISE
# ------------------------

# Zone 1 payouts (small multipliers)
P1 = GolfSymbol(name="Bronze Bunker", code="P1", type="payout", multiplier=1.2)
P2 = GolfSymbol(name="Silver Sands", code="P2", type="payout", multiplier=1.5)
P3 = GolfSymbol(name="Rusty Ridge", code="P3", type="payout", multiplier=1.8)
P4 = GolfSymbol(name="Copper Curve", code="P4", type="payout", multiplier=2.0)

ZONE1_PAYOUTS = [P1, P2, P3, P4]


# Zone 2 payouts (medium multipliers)
P5 = GolfSymbol(name="Golden Fairway", code="P5", type="payout", multiplier=2.5)
P6 = GolfSymbol(name="Emerald Ridge", code="P6", type="payout", multiplier=3.0)
P7 = GolfSymbol(name="Diamond Sandpit", code="P7", type="payout", multiplier=3.5)

ZONE2_PAYOUTS = [P5, P6, P7]


# Zone 3 payout (hole itself)
HOLE = GolfSymbol(name="Hole-in-One", code="HO", type="hole", multiplier=6.0)


# ------------------------
# OBSTACLES
# ------------------------

# Soft-end obstacles (game ends but player keeps running win)
S1 = GolfSymbol(name="Soft Bush", code="S1", type="soft_end")
S2 = GolfSymbol(name="Sticky Mud", code="S2", type="soft_end")

SOFT_ENDS = [S1, S2]


# Hard-end obstacles (game ends with 0)
H1 = GolfSymbol(name="Deep Water Trap", code="H1", type="hard_end")
H2 = GolfSymbol(name="Broken Cliff", code="H2", type="hard_end")
H3 = GolfSymbol(name="Iron Wall", code="H3", type="hard_end")
H4 = GolfSymbol(name="Rocky Doom", code="H4", type="hard_end")

HARD_ENDS = [H1, H2, H3, H4]


# ------------------------
# EMPTY
# ------------------------

EMPTY = GolfSymbol(name="Empty", code="E1", type="empty")


# ------------------------
# ZONE LOADOUT
# ------------------------

# Zone 1: 4 payouts, 2 hard-ends, many empty
ZONE1_SYMBOLS = ZONE1_PAYOUTS + [H1, H2] + [EMPTY] * 9

# Zone 2: payouts, 2 soft-end, 2 hard-end, empties
ZONE2_SYMBOLS = ZONE2_PAYOUTS + [S1, S2, H2, H3] + [EMPTY] * 5

# Zone 3: hole + 2 soft-end + 4 hard-end
ZONE3_SYMBOLS = [HOLE] + SOFT_ENDS + HARD_ENDS
