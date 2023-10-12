import hashlib, math

def strToSHA512(strPassed: str = ""):
    if "" == strPassed: return ""
    objModule = hashlib.new("sha512")
    bytePassedString = bytes(strPassed, "utf-8")
    objModule.update(bytePassedString)
    strHash = str(objModule.hexdigest())
    return strHash

def intToToken(intPassed: int = 0, intMaxLetters: int = 3):
    if intPassed > (26**intMaxLetters):
        print(f"\tERROR\nintTOToken does not handle more than {intMaxLength} digit tokens; intPassed > 26^{intMaxLetters}")
        return "Error"
    if intPassed < 0:
        print(f"\tERROR\nintToToken does not handle negative integers such as '{intPassed}'")
        return "Error"
    strReturn = ""
    for _ in range (intMaxLetters):
        strReturn = chr(97 + (intPassed %26)) + strReturn
        intPassed //=26
    return strReturn


def tokenizeArray(arrPassed: list = [], strTokenization: str = "token"):
    if arrPassed == []: return []
    print(len(arrPassed))
    if len(arrPassed) != len(set(arrPassed)):
        print("\tERROR\ntokenizeArray: list passed has repeating members")
        return []
    if strTokenization == "token":
        intMaxLetters = math.ceil(math.log(len(arrPassed),26))
    arrReturn = []
    intCounter = 0
    for strItem in arrPassed:
        if strTokenization == "token": 
            strToken = intToToken(intCounter, intMaxLetters)
            intCounter += 1
        elif strTokenization == "hash": strToken = strToSHA512(strItem)
        else:
            print(f"\tERROR\ntokenizeArray: strTokenization invalid = '{strTokenization}'")
            return []
        arrReturn.append([ strItem, strToken ])
    return arrReturn


"""
#Tests:
import random
arrRandom = []
for _ in range(10**7):
    arrRandom.append(str(random.randint(0,(10**7))))

arrRandom = list(set(arrRandom))
print(arrRandom)
print(len(arrRandom))
print(tokenizeArray(arrRandom, "hash"))
print(tokenizeArray(arrRandom, "token"))
"""
