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


#works now in scorer.py, but unoptomized
#creates: [[prevPOS, word, POS],
#          [prevPOS, word, POS],...]
def oldtoWordList(text):
    text = re.sub(r'\\\/', r'\\', text)#to allow splitting at /
    pairs = text.split()
    dpairs = []
    POSm1 = '<START>'
    for pair in pairs:
        POSwordPOS = pair.split('/')
        POSwordPOS.insert(0, POSm1)
        dpairs.append(POSwordPOS[2])
        if POSwordPOS[2] == '.' or POSwordPOS[2] == '?' or POSwordPOS[2] == '!':
            POSm1 = '<START>'
        else:
            POSm1 = POSwordPOS[2]
    #to put back \/ for consistency with prof expected op:
    for pair in dpairs:
        for itm in pair:
            itm = re.sub(r'\\', r'\\\/', itm)   
    return dpairs    


def toWordList(text):
    text = re.sub(r'\\\/', r'\\', text)#to allow splitting at /
    pairs = text.split()
    POSlist = []
    for pair in pairs:
        wordPOS = pair.split('/')
        POSlist.append(wordPOS[1])
    return POSlist
    

#####################START PROGRAM#####################

pythonFileName = sys.argv.pop(0)
mySolutionFile = sys.argv.pop(0)
testKeyFile = sys.argv.pop(0)


mySolution = toWordList(readIn(mySolutionFile))
testKey = toWordList(format(readIn(testKeyFile)))

print(testKey)

