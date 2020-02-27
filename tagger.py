import sys, re, os, random


def format(text):
    text = re.sub(r'[\[\]]', '', text)
    text = re.sub(r'[\n]', ' ', text)
    text = ' '.join(text.split())
    return text


#creates: [[word, POS],
#          [word, POS],...]
def toWordList(text):
    text = re.sub(r'\\\/', r'\\', text)#to allow splitting at /
    pairs = text.split()
    dpairs = []
    for pair in pairs:
        dpairs.append(pair.split('/'))
    #to put back \/ for consistency with prof expected op:
    for pair in dpairs:
        for itm in pair:
            itm = re.sub(r'\\', r'\\\/', itm)   
    return dpairs


def createFreqency(pairs):
    table = {}
    for pair in pairs:
        word = pair[0]
        tag = pair[1]
        if word in table:
            if tag in table[word]:
                table[word][tag] += 1
            else:
                table[word][tag] = 1
        else:
            table[word] = {tag: 1}
    return table


def createGuide(table):
    guide = {}
    for word, tags in table.items():
        max = ''
        for tag, occurs in tags.items():
            if occurs > tags.get(max, 0):
                max = tag
        guide[word] = max
    return guide


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


guide = createGuide(createFreqency(toWordList(format(trainText))))


#TESTING
#print(trainText)
#print(type(trainText))
#print(toWordList(trainText))
print(guide)


with open(testFile, 'r+') as f:
    lines = []
    for line in f:
        lines.append(line.strip())
    testText = ' '.join(lines)
#TESTING
#print(testText)