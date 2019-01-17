import argparse
import os
#read input argument
parser = argparse.ArgumentParser()
parser.add_argument("filePath",type=str)
args = parser.parse_args()
asmFilePath = args.filePath
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
        symbols[row[1:-1]] = countRow - countSymbols
        data.remove(row)
        countSymbols += 1
    countRow += 1
#cut symbols from data
#data = [i for j, i in enumerate(data) if j not in symbols.values()]
print(symbols)
print(data)

#test symbol table with max.asm
print (symbols["OUTPUT_FIRST"], 10)
print (symbols["OUTPUT_D"], 12)
print (symbols["INFINITE_LOOP"], 14)

print (data[symbols["OUTPUT_FIRST"]], "@R0")
print (data[symbols["OUTPUT_D"]], "@R2")
print (data[symbols["INFINITE_LOOP"]], "@INFINITE_LOOP")


