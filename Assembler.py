import argparse
parser = argparse.ArgumentParser()
parser.add_argument("filePath",type=str)
args = parser.parse_args()
print(args.filePath)