# External imports
from math import ceil, floor

def roundup(value: float, digit: int) -> float:
    multiplier = 10 ** digit
    return ceil(value * multiplier) / multiplier

def rounddown(value: float, digit: int) -> float:
    multiplier = 10 ** digit
    return floor(value * multiplier) / multiplier

def roundreg(value: float, digit: int) -> float:
    multiplier = 10 ** digit
    return round(value * multiplier) / multiplier

def stop_buff(zones: int, dailyATR: float):
    targets = zones + 1
    targetPrices = []

    stopLossBuffer = roundup(dailyATR, 2)

#maximumRiskAmount = accountSize * 0.02; % The 2% Rule is kind of shit
# maximumRiskAmount = 120;
# maximumPositionSize = floor(maximumRiskAmount / tradeRisk)

# if entrySize <= 0.5
#     modifier=1/5
# elif entrySize > 0.5 && entrySize <= 1
#     modifier=1/4
# else
#     modifier=1/3


#positionSize = floor(maximumRiskAmount / tradeRisk);
#maximumRiskAmount = 120
#Long:
    #tradeRisk = abs(proximalDZ - stopLoss)
    #stopLoss = stopLoss = distalDZ - stopLossBuffer
#Short:
    #tradeRisk = abs(proximalSZ - stopLoss)
    #stopLoss = distalSZ + stopLossBuffer