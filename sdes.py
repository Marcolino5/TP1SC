def Perm10(bits):
    newString = bits[2]+bits[4]+bits[1]+bits[6]+bits[3]+bits[9]+bits[0]+bits[8]+bits[7]+bits[5]
    print("Após Perm10: " + newString)
    return newString

def Perm8(bits):
    newString = bits[5]+bits[2]+bits[6]+bits[3]+bits[7]+bits[4]+bits[9]+bits[8]
    return newString

def CircularLeftShift(bits):
    finalBits = ""
    for x in range(len(bits)):
        finalBits += bits[(x+1)%5]
    return finalBits

def LS1(bits):
    L = bits[:5]
    R = bits[5:]

    L = CircularLeftShift(L)
    R = CircularLeftShift(R)

    print("Após LS1: " + L+R)
    return L+R

def LS2(bits):
    L = bits[:5]
    R = bits[5:]

    L = CircularLeftShift(L)
    L = CircularLeftShift(L)
    R = CircularLeftShift(R)
    R = CircularLeftShift(R)

    print("Após LS2: " + L+R)
    return L+R

def GenKeys(key):
    print("GERAÇÃO DA CHAVE")
    key = Perm10(key)
    key = LS1(key)
    K1 = Perm8(key)
    print("K1: " + K1)
    key = LS2(key)
    K2 = Perm8(key)
    print("K2: " + K2)
    return K1, K2

def InitialPerm(block):
    print("PERMUTAÇÃO INICIAL")
    block = block[1]+block[5]+block[2]+block[0]+block[3]+block[7]+block[4]+block[6]
    print("Bloco Permutado: " + block)
    return block

def FinalPerm(block):
    print("PERMUTAÇÃO FINAL")
    block = block[3]+block[0]+block[2]+block[4]+block[6]+block[1]+block[7]+block[5]
    print("Bloco Permutado: " + block)
    return block

def SBox(bits, matrix):
    row = bits[0]+bits[3]
    column = bits[1]+bits[2]
    result = matrix[int(row,2)][int(column,2)]

    possibilities = ["00","01","10","11"]
    return possibilities[result]

def FFunction(bits, key):
    Expansion = bits[3]+bits[0]+bits[1]+bits[2]+bits[1]+bits[2]+bits[3]+bits[0]
    AddKey = ""
    for x in range(len(Expansion)):
        AddKey += str(int(Expansion[x])^int(key[x]))
    S0 = SBox(AddKey[:4], [[1,0,3,2],[3,2,1,0],[0,2,1,3],[3,1,3,2]])
    S1 = SBox(AddKey[4:], [[0,1,2,3],[2,0,1,3],[3,0,1,0],[2,1,0,3]])
    SResult = S0+S1
    P4 = SResult[1]+SResult[3]+SResult[2]+SResult[0]
    return P4

def FeistelRound(L, R, key):
    print("L inicial: " + L)
    print("R inicial: " + R)

    NewR = FFunction(R, key)
    XOR = ""
    for x in range(len(NewR)):
        XOR += str(int(NewR[x])^int(L[x]))

    print("L final: " + R)
    print("R final: " + XOR)
    return R, XOR


def SDESEncryption(key, block):
    print("--- SDES ---")
    print("Texto em Claro: " + block)
    print("Chave Inicial: " + key)
    print("")
    K1, K2  = GenKeys(key)
    subkeys = [K1, K2]

    print("")
    permBlock = InitialPerm(block)

    print("")
    print("RODADAS DE FEISTEL")
    R = permBlock[:4]
    L = permBlock[4:]
    for round in range(2):
        print("Round " + str(round+1))
        L, R = FeistelRound(L, R, subkeys[round])
    currentBlock = R + L

    print("")
    cipherBlock = FinalPerm(currentBlock)

    print("")
    print("Texto Cifrado: " + cipherBlock)
    print("")
    return cipherBlock

def SDESDecryption(key, cipherBlock):
    print("--- SDES Descriptação ---")
    print("Texto Cifrado: " + cipherBlock)
    print("Chave Inicial: " + key)
    print("")
    K1, K2  = GenKeys(key)
    keys = [K2, K1]

    print("")
    currentBlock = InitialPerm(cipherBlock) # inverso da permutação final = permutação inicial

    print("")
    print("RODADAS DE FEISTEL")
    L = currentBlock[:4] # R inicial = L final
    R = currentBlock[4:] # L inicial = R final
    for round in range(2):
        print("Round " + str(round+1))
        L, R = FeistelRound(L, R, keys[round])
    permBlock = L + R

    print("")
    block = FinalPerm(permBlock) # inverso da permutação inicial = permutação final

    print("")
    print("Texto em Claro: " + block)

SDESDecryption("1010000010", SDESEncryption("1010000010", "11010111"))