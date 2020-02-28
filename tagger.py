import sys, re, os, random


def format(text):
    #delete brackets [ ]
    text = re.sub(r'[\[\]]', '', text)
    #replace newlines with spaces
    text = re.sub(r'[\n]', ' ', text)
    #use split and join to reduce all amounts of whitespace to a single space
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


def testWordList(wordList):
    dList = []
    start = True
    for word in wordList:
        wordasL = [word]
        if start:
            wordasL.insert(0, '<START>')
            start = False
        if wordasL[0] == '.' or wordasL[0] == '?' or wordasL[0] == '!':
            start = True
        dList.append(wordasL)
    return dList


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


def testTriples(testLst):
    prevpos = '<START>'
    pos = ''
    testtriples = []
    for trip in testLst:
        storetrip = trip
        #set tag-1 if it isnt already a start tag
        if storetrip[0] != '<START>':
            storetrip.insert(0,pos)
            prevpos = pos
        else:
            prevpos = '<START>'
        max = 0
        pos = ''
        if storetrip[1] in validTagsPerWord:
            for tag in validTagsPerWord.get(storetrip[1]):
                prob = wordtagP(storetrip[1], tag)*tagm1tagP(storetrip[0], tag)
                if prob >= max:
                    max = prob
                    pos = tag
        else:
            pos = 'NN'
        storetrip.append(pos)
        testtriples.append(storetrip)
    return testtriples


def wordtagP(word, tag):
    if (word, tag) not in freqWordTag:
        print('w1')
        return 0
    num = freqWordTag.get((word, tag))
    denom = freqWord.get(word)
    #print('w2')
    return num/denom


def tagm1tagP(tagm1,tag):
    if (tagm1, tag) not in freqTagm1Tag:
        #print('a1')
        return 0
    num = freqTagm1Tag.get((tagm1, tag))
    denom = freqTag.get(tagm1)
    #print('a2')
    return num/denom


def allTagsPerWord(freqWordTag):
    validTags = {}
    for wordPOS, wfreq in freqWordTag.items():
        if wordPOS[0] in validTags:
            validTags[wordPOS[0]].append(wordPOS[1])
        else:
            validTags[wordPOS[0]] = [wordPOS[1]]
    return validTags


def makePretty(trips):
    words = []
    for trip in trips:
        words.append(trip[1] + '/' + trip[2])
    return ' '.join(words)

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


trips = toWordList(format(trainText))
freqWord = singleFreq(trips, 1)
freqTag = singleFreq(trips, 2)
freqWordTag = doubleFreq(trips, 1)
freqTagm1Tag = doubleFreq(trips, 0)
validTagsPerWord = allTagsPerWord(freqWordTag)

#dont delete until you have whole correction done so you can see proper order
#guide = createGuide(createFreqency(toWordList(format(trainText))))


###########TESTING#############
#print(trainText)
#print(type(trainText))
#print(toWordList(trainText))
#print(guide)
#print(trips)
#print(freqTag)
#print(freqWord)
#print(freqTagm1Tag)
#print(freqWordTag)
#print(validTagsPerWord)


with open(testFile, 'r+') as f:
    lines = []
    for line in f:
        lines.append(line.strip())
    testText = ' '.join(lines)


testtrips = testTriples(testWordList(format(testText).split()))
pretty = makePretty(testtrips)


###########TESTING#############
#print(testText)
#print(wordList)
#print(testwordList)
#print(testtrips)
print(pretty)