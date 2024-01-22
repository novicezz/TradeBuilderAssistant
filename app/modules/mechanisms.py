# External imports
from math import ceil, floor
from modules.calculations import *
# Local imports
from modules.memory import MemoryManager
from modules.utils  import fill_table, check_if_full
from modules.attributes import *

HUNDREDTH = 2
LIQUIDITY_FRACTION = 0.5
DAYORHOUR_SLBUFFER = 0.1
FIFTEEN_SLBUFFER = 0.02
FIFTEENORHOUR_ENTRYBUFFER = 0.02
DAY_ENTRYBUFFER = 0.04

# Tradebuilder mechanisms
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
    if dzSize <= 0.5:
        activationPrice = setupTable["entry"] - (dzSize / 5)
    elif 0.5 < dzSize <= 1.0:
        activationPrice = setupTable["entry"] - (dzSize / 4)
    elif dzSize > 1.0:
        activationPrice = setupTable["entry"] - (dzSize / 3)
    else:
        return "Error with activation rule input, please double check and try again"
    if activationPrice is not None:
        activationRule = rounddown(activationPrice, HUNDREDTH)
    else:
        return "Error: Activation rule cannot be generated with given SZ values, please double check and try again"
# Limit/stop price calculation   
    if setupTable["timeframe"].get_val() == "15" or setupTable["timeframe"].get_val() == "hour":
        limitBuffer = FIFTEENORHOUR_ENTRYBUFFER
    elif setupTable["timeframe"].get_val() == "day":
        limitBuffer = DAY_ENTRYBUFFER
    limitPrice = roundreg(setupTable["entry"] + limitBuffer, HUNDREDTH)
    stopPrice = setupTable["entry"]
# Stop loss calculation
    if setupTable["timeframe"].get_val() == "hour" or setupTable["timeframe"].get_val() == "day": 
        stopLossBuffer = DAYORHOUR_SLBUFFER
    elif setupTable["timeframe"].get_val() == "15":
        stopLossBuffer = FIFTEEN_SLBUFFER
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
    targetOneShares = ceil(0.8 * positionSize)
    targetTwo = setupTable["szone"]["proximal"]
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
    report += f"Target 2 split:     {targetTwoShares}\n"
    return report

def short_position(setupTable: dict):
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
    if szSize <= 0.5:
        activationPrice = setupTable["entry"] + (szSize / 5)
    elif 0.5 < szSize <= 1.0:
        activationPrice = setupTable["entry"] + (szSize / 4)
    elif szSize > 1.0:
        activationPrice = setupTable["entry"] + (szSize / 3)
    else:
        return "Error with activation rule input, please double check and try again"
    if activationPrice is not None:
        activationRule = roundup(activationPrice, HUNDREDTH)
    else:
        return "Error: Activation rule cannot be generated with given SZ values, please double check and try again"
# Limit/stop price calculation
    if setupTable["timeframe"].get_val() == "15" or setupTable["timeframe"].get_val() == "hour":
        limitBuffer = FIFTEENORHOUR_ENTRYBUFFER
    elif setupTable["timeframe"].get_val() == "day":
        limitBuffer = DAY_ENTRYBUFFER
    limitPrice = roundreg(setupTable["entry"] - limitBuffer, HUNDREDTH)
    stopPrice = setupTable["entry"]
# Stop loss calculation
    if setupTable["timeframe"].get_val() == "hour" or setupTable["timeframe"].get_val() == "day": 
        stopLossBuffer = DAYORHOUR_SLBUFFER
    elif setupTable["timeframe"].get_val() == "15":
        stopLossBuffer = FIFTEEN_SLBUFFER
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
    targetOneShares = ceil(0.8 * positionSize)
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
    report += f"Target 2 split:     {targetTwoShares}\n"
    return report

def generate_position():
    setupTable = fill_table(MemoryManager.get_set())
    if not check_if_full(setupTable):
        print("Please fill out setup table")
    elif setupTable["direction"].get_val() == "long":
        print(long_position(setupTable))
    elif setupTable["direction"].get_val() == "short":
        print(short_position(setupTable))
    else:
        print("No direction specified, please set direction and try again")