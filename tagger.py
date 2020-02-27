import sys, re, os, random


def format(text):
    text = re.sub(r'[\[\]]', '', text)
    text = re.sub(r'[\n]', ' ', text)
    text = ' '.join(text.split())
    return text


#creates: [[prevPOS, word, POS],
#          [prevPOS, word, POS],...]
def toWordList(text):
    text = re.sub(r'\\\/', r'\\', text)#to allow splitting at /
    pairs = text.split()
    dpairs = []
    POSm1 = '<START>'
    for pair in pairs:
        POSwordPOS = pair.split('/')
        POSwordPOS.insert(0, POSm1)
        dpairs.append(POSwordPOS)
        if POSwordPOS[2] == '.' or POSwordPOS[2] == '?' or POSwordPOS[2] == '!':
            POSm1 = '<START>'
        else:
            POSm1 = POSwordPOS[2]
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



def singleFreq(tripls, index):
    sfreq = {}
    #add start tag for beginning of text if we are doing tags.
    if index == 2:
        sfreq['<START>'] = 1
    for tripl in tripls:
        Key = tripl[index]
        if Key in sfreq:
            sfreq[Key] += 1
        else:
            sfreq[Key] = 1
        #add <start> tag if end of a sentence and we are doing tags
        if index == 2 and (Key == '.' or Key == '!' or Key == '?'):
            sfreq['<START>'] += 1
    #this deletes one <start> tag, in the case that the entire text ends in a punctuation, because there is not another sentence to start:
    if index == 2 and (tripls[-1][-1] == '.' or tripls[-1][-1] == '!' or tripls[-1][-1] == '?'):
        sfreq['<START>'] -= 1
    return sfreq


def doubleFreq(tripls, leftIndex):
    dfreq = {}
    for tripl in tripls:
        left = tripl[leftIndex]
        tag = tripl[2]
        Key = (left, tag)
        if Key in dfreq:
            dfreq[Key] += 1
        else:
            dfreq[Key] = 1
    return dfreq


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


tripls = toWordList(format(trainText))
freqWord = singleFreq(tripls, 1)
freqTag = singleFreq(tripls, 2)
freqWordTag = doubleFreq(tripls, 1)
freqTagm1Tag = doubleFreq(tripls, 0)

#dont delete until you have whole correction done so you can see proper order
#guide = createGuide(createFreqency(toWordList(format(trainText))))


###########TESTING#############
#print(trainText)
#print(type(trainText))
#print(toWordList(trainText))
#print(guide)
#print(tripls)
#print(freqTag)
#print(freqWord)
#print(freqTagm1Tag)
#print(freqWordTag)


with open(testFile, 'r+') as f:
    lines = []
    for line in f:
        lines.append(line.strip())
    testText = ' '.join(lines)
#TESTING
#print(testText)