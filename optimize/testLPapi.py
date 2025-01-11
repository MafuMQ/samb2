from LP_PULP import dictList2Var, optimizeCall

Budget = 13

ListofVar = []

coffee_cake = {"name":"coffee cake", "lowerBound":0, "upperBound":None, "profit":1.80, "multiplier":8}
ListofVar.append(coffee_cake)

chocolate_cake = {"name":"chocolate cake", "lowerBound":0, "upperBound":None, "profit":1.60, "multiplier":1}
ListofVar.append(chocolate_cake)


def nr1(Lv = ListofVar):
    dictList2Var(Lv)

def main(B):
    return optimizeCall(B)
