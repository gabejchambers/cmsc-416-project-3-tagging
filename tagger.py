import sys, re, os, random


def format(text):
    text = re.sub(r'[\[\]]', '', text)
    text = re.sub(r'[\n]', ' ', text)
    text = ' '.join(text.split())
    return text

##########################################################PROGRAM START###################################################################

pythonFileName = sys.argv.pop(0)
trainFile = sys.argv.pop(0)
testFile = sys.argv.pop(0)
trainText = ''
testText = ''

#TESTING
#print(pythonFileName, trainText, testText)


with open(trainFile, 'r+') as f:
    lines = []
    for line in f:
        lines.append(line.strip())
    trainText = ' '.join(lines)

trainText = format(trainText)
#TESTING
print(trainText)
#print(type(trainText))



with open(testFile, 'r+') as f:
    lines = []
    for line in f:
        lines.append(line.strip())
    testText = ' '.join(lines)
#TESTING
#print(testText)