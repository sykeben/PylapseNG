# Numeric suffix accounter.
def numSuffix(count:int|float, plural:str = "s", single:str = "", offset:int|float = 0):
    return single if (abs(count)+offset == 1) else plural

# Length suffix accounter.
def lenSuffix(items:list, plural:str = "s", single:str = "", offset:int = 0):
    return numSuffix(len(items), plural, single, offset)