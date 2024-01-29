# External imports
from math import ceil, floor
# Local imports
from modules.calculations import *
from modules.utils  import get_primitives, check_if_full

# Constants
HUNDREDTH = 2
LIQUIDITY_FRACTION = 0.5

FIFTEEN_SLBUFFER = 0.02
HOUR_SLBUFFER = 0.1
DAY_SLBUFFER = 0.1

FIFTEEN_ENTRYBUFFER = 0.02
HOUR_ENTRYBUFFER = 0.02
DAY_ENTRYBUFFER = 0.04

TARGETONE_BUFFER = 0.8

ZONEDENOMIATOR_FIFTH = 5
ZONEDENOMIATOR_QUARTER = 4
ZONEDENOMIATOR_THIRD = 3

ZONESIZE_FIFTYCENTS = 0.5
ZONESIZE_DOLLAR = 1.0

def long_position(setupTable: dict) -> str:
# Convert to Common Calculation
    dzSize = setupTable["dzone"]["proximal"] - setupTable["dzone"]["distal"]
# Error conditions
    if setupTable["dzone"]["proximal"] <= setupTable["dzone"]["distal"]:
        return "Error: Value of DZ proximal cannot be equal to or lower than value of DZ distal"
    elif setupTable["szone"]["distal"] <= setupTable["szone"]["proximal"]:
        return "Error: Value of SZ distal cannot be equal to or lower than value of SZ proximal"
    elif setupTable["szone"]["proximal"] <= setupTable["dzone"]["proximal"]:
        return "Error: Value of SZ proximal cannot be equal to or lower than value of DZ proximal"
# Activation rule calculation
    activationRule = None
    if dzSize <= ZONESIZE_FIFTYCENTS:
        activationPrice = setupTable["entry"] - (dzSize / ZONEDENOMIATOR_FIFTH)
    elif ZONESIZE_FIFTYCENTS < dzSize <= ZONESIZE_DOLLAR:
        activationPrice = setupTable["entry"] - (dzSize / ZONEDENOMIATOR_QUARTER)
    elif dzSize > ZONESIZE_DOLLAR:
        activationPrice = setupTable["entry"] - (dzSize / ZONEDENOMIATOR_THIRD)
    else:
        return "Error with activation rule input, please double check and try again"
    if activationPrice is not None:
        activationRule = rounddown(activationPrice, HUNDREDTH)
    else:
        return "Error: Activation rule cannot be generated with given SZ values, please double check and try again"
# Limit/stop price calculation   
    if setupTable["timeframe"] == "15":
        limitBuffer = FIFTEEN_ENTRYBUFFER
    elif setupTable["timeframe"]== "hour":
        limitBuffer = HOUR_ENTRYBUFFER
    elif setupTable["timeframe"] == "day":
        limitBuffer = DAY_ENTRYBUFFER
    limitPrice = roundreg(setupTable["entry"] + limitBuffer, HUNDREDTH)
    stopPrice = setupTable["entry"]
# Stop loss calculation
    if setupTable["timeframe"] == "15":
        stopLossBuffer = FIFTEEN_SLBUFFER
    elif setupTable["timeframe"] == "hour": 
        stopLossBuffer = HOUR_SLBUFFER
    elif setupTable["timeframe"] == "day":
        stopLossBuffer = DAY_SLBUFFER
    stopLoss = setupTable["dzone"]["distal"] - (setupTable["atr"] * stopLossBuffer)
# Position size calculator
    riskPerShare = abs(setupTable["entry"] - stopLoss)
    positionSize = floor(setupTable["maxrisk"] / riskPerShare)
    positionCost = roundreg(positionSize * setupTable["entry"], HUNDREDTH)
    maxLiquidity = rounddown(setupTable["accsize"] * LIQUIDITY_FRACTION, HUNDREDTH)
    if positionCost > maxLiquidity:
        positionCost = maxLiquidity
        positionSize = floor(positionCost / setupTable["entry"])
        print("Max account liquidity insufficient, position size reduced to:", positionSize)
    tradeRisk = roundreg(positionSize * riskPerShare, HUNDREDTH)
# Target Calculator
    targetOne = setupTable["entry"] + rounddown(0.8 * abs(setupTable["szone"]["proximal"] - setupTable["entry"]), HUNDREDTH)
    targetOneShares = ceil(TARGETONE_BUFFER * positionSize)
    targetTwo = setupTable["szone"]["proximal"]
    targetTwoShares = positionSize - targetOneShares
# Assemble report
    report  = f"Ticker:             {setupTable['ticker']}\n"
    report += f"Position cost:      {positionCost}\n"
    report += f"Position size:      {positionSize}\n"
    report += f"Position risk:      {tradeRisk}\n"
    report += f"Limit price:        {limitPrice}\n"
    report += f"Stop price:         {stopPrice}\n"
    report += f"Activation price:   {activationRule}\n"
    report += f"Target 1:           {targetOne}\n"
    report += f"Target 2:           {targetTwo}\n"
    report += f"Target 1 split:     {targetOneShares}\n"
    report += f"Target 2 split:     {targetTwoShares}"
    return report

def short_position(setupTable: dict) -> str:
    # Convert to Common Calculation
    szSize = setupTable["szone"]["distal"] - setupTable["szone"]["proximal"]
# Error conditions
    if setupTable["dzone"]["proximal"] <= setupTable["dzone"]["distal"]:
        return "Error: Value of DZ proximal cannot be equal to or lower than value of DZ distal"
    elif setupTable["szone"]["distal"] <= setupTable["szone"]["proximal"]:
        return "Error: Value of SZ distal cannot be equal to or lower than value of SZ proximal"
    elif setupTable["szone"]["proximal"] <= setupTable["dzone"]["proximal"]:
        return "Error: Value of SZ proximal cannot be equal to or lower than value of DZ proximal"
# Activation rule calculation
    activationRule = None
    if szSize <= ZONESIZE_FIFTYCENTS:
        activationPrice = setupTable["entry"] + (szSize / ZONEDENOMIATOR_FIFTH)
    elif ZONESIZE_FIFTYCENTS < szSize <= ZONESIZE_DOLLAR:
        activationPrice = setupTable["entry"] + (szSize / ZONEDENOMIATOR_QUARTER)
    elif szSize > ZONESIZE_DOLLAR:
        activationPrice = setupTable["entry"] + (szSize / ZONEDENOMIATOR_THIRD)
    else:
        return "Error with activation rule input, please double check and try again"
    if activationPrice is not None:
        activationRule = roundup(activationPrice, HUNDREDTH)
    else:
        return "Error: Activation rule cannot be generated with given SZ values, please double check and try again"
# Limit/stop price calculation
    if setupTable["timeframe"] == "15":
        limitBuffer = FIFTEEN_ENTRYBUFFER
    elif setupTable["timeframe"] == "hour":
        limitBuffer = HOUR_ENTRYBUFFER
    elif setupTable["timeframe"] == "day":
        limitBuffer = DAY_ENTRYBUFFER
    limitPrice = roundreg(setupTable["entry"] - limitBuffer, HUNDREDTH)
    stopPrice = setupTable["entry"]
# Stop loss calculation
    if setupTable["timeframe"] == "15":
        stopLossBuffer = FIFTEEN_SLBUFFER
    elif setupTable["timeframe"] == "hour": 
        stopLossBuffer = HOUR_SLBUFFER
    elif setupTable["timeframe"] == "day":
        stopLossBuffer = DAY_SLBUFFER
    stopLoss = setupTable["szone"]["distal"] + (setupTable["atr"] * stopLossBuffer)
# Position size calculator
    riskPerShare = abs(stopLoss - setupTable["entry"])
    positionSize = floor(setupTable["maxrisk"] / riskPerShare)
    positionCost = roundreg(positionSize * setupTable["entry"], HUNDREDTH)
    maxLiquidity = rounddown(setupTable["accsize"] * LIQUIDITY_FRACTION, HUNDREDTH)
    if positionCost > maxLiquidity:
        positionCost = maxLiquidity
        positionSize = floor(positionCost / setupTable["entry"])
        print("Max account liquidity insufficient, position size reduced to:", positionSize)
    tradeRisk = roundreg(positionSize * riskPerShare, HUNDREDTH)
# Target Calculator
    targetOne = setupTable["entry"] - roundup(0.8 * abs(setupTable["entry"] - setupTable["dzone"]["proximal"]), HUNDREDTH)
    targetOneShares = ceil(TARGETONE_BUFFER * positionSize)
    targetTwo = setupTable["dzone"]["proximal"]
    targetTwoShares = positionSize - targetOneShares
# Print position 
    report  = f"Ticker:             {setupTable['ticker']}\n"
    report += f"Position cost:      {positionCost}\n"
    report += f"Position size:      {positionSize}\n"
    report += f"Position risk:      {tradeRisk}\n"
    report += f"Limit price:        {limitPrice}\n"
    report += f"Stop price:         {stopPrice}\n"
    report += f"Activation price:   {activationRule}\n"
    report += f"Target 1:           {targetOne}\n"
    report += f"Target 2:           {targetTwo}\n"
    report += f"Target 1 split:     {targetOneShares}\n"
    report += f"Target 2 split:     {targetTwoShares}"
    return report

def generate_position(positionData: dict) -> str:
    setupTable = get_primitives(positionData)
    if not check_if_full(setupTable):
        return "ERROR: Please fill out your setup properties"
    elif setupTable["direction"] == "long":
        return long_position(setupTable)
    elif setupTable["direction"] == "short":
        return short_position(setupTable)
    else:
        return "ERROR: No direction specified, please set direction and try again"