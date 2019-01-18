import argparse
import os
import re

#dictionary with c-instructions
instructions = {
    "comp":{
    "0"     :   "101010",
    "1"     :   "111111",
    "-1"    :   "111010",
    "D"     :   "001100",
    "A"     :   "110000",
    "!D"    :   "001101",
    "!A"    :   "110001",
    "-D"    :   "001111",
    "-A"    :   "110011",
    "D+1"   :   "011111",
    "A+1"   :   "110111",
    "D-1"   :   "001110",
    "A-1"   :   "110010",
    "D+A"   :   "000010",
    "D-A"   :   "010011",
    "A-D"   :   "000111",
    "D&A"   :   "000000",
    "D|A"   :   "010101"
},
"dest":{
    ""      :   "000",
    "M"     :   "001",
    "D"     :   "010",
    "MD"    :   "011",
    "A"     :   "100",
    "AM"    :   "101",
    "AD"    :   "110",
    "AMD"   :   "111"
},
"jmp":{
    ""      :   "000",
    "JGT"   :   "001",
    "JEQ"   :   "010",
    "JGE"   :   "011",
    "JLT"   :   "100",
    "JNE"   :   "101",
    "JLE"   :   "110",
    "JMP"   :   "111"
}
}

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


def cDecode(cInstr,instructions):
    p = re.compile(r"([ADM]{0,2})=?([!ADM10]?[+-]?[!ADM10]);?(\w*)\b")
    if p.search(cInstr) == None:
        f=1
        
    groups = p.search(cInstr).groups()
    dest = instructions["dest"][groups[0]]
    if "M" in groups[1]:
        comp = groups[1].replace("M","A")
        comp = instructions["comp"][comp]
        a = "1"
    else:
        comp = instructions["comp"][groups[1]]
        a="0"
    jump = instructions["jmp"][groups[2]]
    return "111" + a + "".join([comp,dest,jump])

def assembler(asmFilePath):
    """
    assembler
    asmFilePath - string - path to .asm file
    
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
    indiciesToRemove=[]
    for row in data:
        if row[0] == "(" and row[-1] == ")":
            symbols[row[1:-1]] = countRow - countSymbols
            indiciesToRemove.append(countRow)
            #data.remove(row)
            countSymbols += 1
        countRow += 1
    #cut symbols from data
    data = [i for j, i in enumerate(data) if j not in indiciesToRemove]

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
            data[idx]=cDecode(i, instructions)
    print(symbols)
    print(data)
    jackFilePath = os.path.split(asmFilePath)
    jackFilePath = jackFilePath[0] + "\\" + jackFilePath[1].split(".")[0] + ".hack"
    with open(jackFilePath,"w") as f:
        f.write("\n".join(data))
        f.close()

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