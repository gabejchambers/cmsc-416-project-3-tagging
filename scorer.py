import sys, re


def readIn(txtFile):
    with open(txtFile, 'r+') as f:
        lines = []
        for line in f:
            lines.append(line.strip())
        textStr = ' '.join(lines)
    return textStr


def format(text):
    #delete brackets [ ]
    text = re.sub(r'[\[\]]', '', text)
    #replace newlines with spaces
    text = re.sub(r'[\n]', ' ', text)
    #use split and join to reduce all amounts of whitespace to a single space
    text = ' '.join(text.split())
    return text


def toWordList(text):
    text = re.sub(r'\\\/', r'\\', text)#to allow splitting at /
    pairs = text.split()
    POSlist = []
    for pair in pairs:
        wordPOS = pair.split('/')
        temp = wordPOS[1].split('|')
        wordPOS[1] = temp[-1]
        POSlist.append(wordPOS[1])
    return POSlist
    

def compare(actual, expected):
    same = 0
    total = 0
    for index in range(len(actual)):
        total += 1
        if actual[index] == expected[index]:
            same+=1
    return same/total


def buildMatrix(actual, expected, matrix):
    for index in range(len(actual)):
        matrix[actual[index]][expected[index]] += 1
    return matrix


def initializeMatrix(actual, expected):
    matrix = {}
    expectset = set()
    for pos in actual:
        if pos not in matrix:
            matrix[pos] = {}
    for pos in expected:
        if pos not in expectset:
            expectset.add(pos)
    for actlpos, expectdict in matrix.items():
        for expectpos in expectset:
            if expectpos not in expectdict:
                expectdict[expectpos] = 0
    return matrix


def printPretty(matrix):
    print('Confusion Matrix, where left value is the calculated, experimental and the inner values are the pos-test-key.txt values.')
    print('For example:')
    print("        DT: {'WP': 0, 'NNS': 4, DT: 1776}")
    print('Can be read as: What the program thought was a DT was correctly tagged as a DT, 1776 times, but 4 times it was actually supposed to be an NNS', end='\n\n')
    for actualpos, expecteddict in matrix.items():
        print(actualpos, end=': ')
        print(expecteddict)
    return

#####################START PROGRAM#####################

pythonFileName = sys.argv.pop(0)
mySolutionFile = sys.argv.pop(0)
testKeyFile = sys.argv.pop(0)


mySolution = toWordList(readIn(mySolutionFile))
testKey = toWordList(format(readIn(testKeyFile)))
emptyMatrix = initializeMatrix(mySolution, testKey)
print('Accuracy:', compare(mySolution, testKey), end='\n\n\n')
printPretty(buildMatrix(mySolution, testKey, emptyMatrix))


#print(mySolution)
#print(finalAccuracy)
#print(emptyMatrix)
#print(cMatrix)


