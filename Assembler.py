import argparse
import os
#decoding functions
def aDecode(address,symbols):
    if address in symbols:
        address = f"{symbols[address]:016b}"
    else:
        if address[0]=="R":
            address=address[1:]
        try:
            address = int(address)
            address = f"{address:016b}"
        except:
            pass
    return address    


def cDecode(cInstr):
    return cInstr

def assembler(asmFilePath):
    """
    assembler
    asmFilePath - string - path to .asm file
    creates .jack file in same directory with .asm
    """
    #open asm file
    with open(asmFilePath) as f:
        data = f.read().split("\n")
        f.close()
    #cut comments and blank rows

    for idx in range(len(data)):
        commIdx = data[idx].find("//")
        if commIdx >= 0:
            data[idx] = data[idx][:commIdx]
        data[idx] = data[idx].strip()
    data = list(filter(lambda x: len(x)>0, data))
    #make symbol table
    symbols={}
    countRow=0
    countSymbols=0
    for row in data:
        if row[0] == "(" and row[-1] == ")":
            symbols[row[1:-1]] = countRow #- countSymbols
            data.remove(row)
            #countSymbols += 1
        countRow += 1
    #cut symbols from data
    #data = [i for j, i in enumerate(data) if j not in symbols.values()]

    """
    #test symbol table with max.asm
    print (symbols["OUTPUT_FIRST"], 10)
    print (symbols["OUTPUT_D"], 12)
    print (symbols["INFINITE_LOOP"], 14)

    print (data[symbols["OUTPUT_FIRST"]], "@R0")
    print (data[symbols["OUTPUT_D"]], "@R2")
    print (data[symbols["INFINITE_LOOP"]], "@INFINITE_LOOP")
    """
    #decode instructions
    for idx in range(len(data)):
        i=data[idx]
        if i[0]=="@":#A-instruction
            data[idx]=aDecode(i[1:],symbols)
        else:#C-instruction
            data[idx]=cDecode(i)
    print(symbols)
    print(data)

#read input argument
parser = argparse.ArgumentParser()
parser.add_argument("filePath",type=str)
args = parser.parse_args()
asmFilePath = args.filePath
assembler(asmFilePath)
"""
#test aDecode
print(aDecode("26532",{})=="0110011110100100")
print(aDecode("1",{})=="0000000000000001")
print(aDecode("1",{}))
print(aDecode("test",{"test":1000})=="0000001111101000")
"""