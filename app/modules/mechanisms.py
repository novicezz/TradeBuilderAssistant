# External imports
from math                   import ceil, floor
# Local imports
from modules.calculations   import *
from modules.utils          import get_primitives, check_if_full
import modules.config       as conf

# Constants
HUNDREDTH = 2

def long_position(setupTable: dict, configSettings: dict) -> str:
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
    activationPrice = configSettings["ZONE_SPEC"].get_activation(dzSize, setupTable["entry"])
    activationRule = roundup(activationPrice, HUNDREDTH)
# Limit/stop price calculation
    limitBuffer = configSettings[setupTable["timeframe"]]["ENTRY_BUFFER"]
    limitPrice = roundreg(setupTable["entry"] - limitBuffer, HUNDREDTH)
    stopPrice = setupTable["entry"]
# Stop loss calculation
    stopLossBuffer = configSettings[setupTable["timeframe"]]["SL_BUFFER"]
    stopLoss = setupTable["dzone"]["distal"] - roundreg(setupTable["atr"] * stopLossBuffer, HUNDREDTH)
# Position size calculator
    riskPerShare = abs(setupTable["entry"] - stopLoss)
    positionSize = floor(setupTable["maxrisk"] / riskPerShare)
    positionCost = roundreg(positionSize * setupTable["entry"], HUNDREDTH)
    maxLiquidity = rounddown(setupTable["accsize"] * configSettings["LIQUIDITY_FRACTION"], HUNDREDTH)
    if positionCost > maxLiquidity:
        positionCost = maxLiquidity
        positionSize = floor(positionCost / setupTable["entry"])
        print("Max account liquidity insufficient, position size reduced to:", positionSize)
    tradeRisk = roundreg(positionSize * riskPerShare, HUNDREDTH)
# Target Calculator
    targets = []
    targetShares = []
    for i in configSettings["TARGETS"]:
        distance = abs(setupTable["szone"]["proximal"] - setupTable["entry"])
        targets.append(rounddown(setupTable["entry"] + i * distance, HUNDREDTH))
        targetShares.append(round(configSettings["TARGETS"][i] * positionSize))
# Assemble report
    report  = f"Ticker:             {setupTable['ticker']}\n"
    report += f"Position cost:      ${positionCost:.2f}\n"
    report += f"Position size:      {positionSize}\n"
    report += f"Position risk:      ${tradeRisk:.2f}\n"
    report += f"Limit price:        ${limitPrice:.2f}\n"
    report += f"Stop price:         ${stopPrice:.2f}\n"
    report += f"Activation price:   ${activationRule:.2f}\n"
    report += f"Stop loss:          ${stopLoss:.2f}\n\n"
    for i in range(0, len(targets)):
        report += f"Target {i + 1}:           ${targets[i]:.2f}\n"
    for i in range(0, len(targetShares)):
        report += f"Target {i + 1} split:     {targetShares[i]}"
        if i != len(targetShares) - 1: report += '\n'
    return report

def short_position(setupTable: dict, configSettings: dict) -> str:
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
    activationPrice = configSettings["ZONE_SPEC"].get_activation(szSize, setupTable["entry"])
    activationRule = roundup(activationPrice, HUNDREDTH)
# Limit/stop price calculation
    limitBuffer = configSettings[setupTable["timeframe"]]["ENTRY_BUFFER"]
    limitPrice = roundreg(setupTable["entry"] - limitBuffer, HUNDREDTH)
    stopPrice = setupTable["entry"]
# Stop loss calculation
    stopLossBuffer = configSettings[setupTable["timeframe"]]["SL_BUFFER"]
    stopLoss = setupTable["szone"]["distal"] +  roundreg(setupTable["atr"] * stopLossBuffer, HUNDREDTH)
# Position size calculator
    riskPerShare = abs(stopLoss - setupTable["entry"])
    positionSize = floor(setupTable["maxrisk"] / riskPerShare)
    positionCost = roundreg(positionSize * setupTable["entry"], HUNDREDTH)
    maxLiquidity = rounddown(setupTable["accsize"] * configSettings["LIQUIDITY_FRACTION"], HUNDREDTH)
    if positionCost > maxLiquidity:
        positionCost = maxLiquidity
        positionSize = floor(positionCost / setupTable["entry"])
        print("Max account liquidity insufficient, position size reduced to:", positionSize)
    tradeRisk = roundreg(positionSize * riskPerShare, HUNDREDTH)
# Target Calculator
    targets = []
    targetShares = []
    for i in configSettings["TARGETS"]:
        distance = abs(setupTable["entry"] - setupTable["dzone"]["proximal"])
        targets.append(roundup(setupTable["entry"] - i * distance, HUNDREDTH))
        targetShares.append(round(configSettings["TARGETS"][i] * positionSize))
# Print position 
    report  = f"Ticker:             {setupTable['ticker']}\n"
    report += f"Position cost:      ${positionCost:.2f}\n"
    report += f"Position size:      {positionSize}\n"
    report += f"Position risk:      ${tradeRisk:.2f}\n"
    report += f"Limit price:        ${limitPrice:.2f}\n"
    report += f"Stop price:         ${stopPrice:.2f}\n"
    report += f"Activation price:   ${activationRule:.2f}\n"
    report += f"Stop loss:          ${stopLoss:.2f}\n\n"
    for i in range(0, len(targets)):
        report += f"Target {i + 1}:           ${targets[i]:.2f}\n"
    for i in range(0, len(targetShares)):
        report += f"Target {i + 1} split:     {targetShares[i]}"
        if i != len(targetShares) - 1: report += '\n'
    return report

def generate_position(positionData: dict) -> str:
    setupTable = get_primitives(positionData)
    if not check_if_full(setupTable):
        return "ERROR: Please fill out your setup properties"
    elif setupTable["direction"] == "long":
        return long_position(setupTable, conf.DEFAULT_CONFIG)
    elif setupTable["direction"] == "short":
        return short_position(setupTable, conf.DEFAULT_CONFIG)
    else:
        return "ERROR: No direction specified, please set direction and try again"