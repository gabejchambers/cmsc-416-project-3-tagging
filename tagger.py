#############################################################################################################
'''                                            OVERVIEW

> Record that accuracy in your overview comments:
    My accuracy from the test files is 0.8522279318597775
    I used the P(tag|word)*P(tag|previous tag) method rather than P(word|tag)*(...)
    This numerical accuracy is also output by scorer.py to STDOUT


> Your introduction should also include identifying information (your name, date, etc.)
    Gabriel Chambers
    3/3/2020


> 1) describe the problem to be solved well enough so that someone not familiar with our class could understand:
    Give an input text from a publication. Each word in this text has been tagged by hand by a human for that 
    word's part of speech (POS). 
    Create a program which can read and learn from this input so that it can take untagged text from a similar
    publication, and tag it with maximum accuracy for each part of speech of every word in that text. Then
    Output the result, which is a tagged version of the untagged text.


> 2) give actual examples of program input and output, along with usage instructions:

    Usage Instructions:
    Call the python program with 2 arguments. 
    The first argument should be a path to a text file containing text which ahs already had POS tagging done.
    The second argument should be a path to a file on which there has not been POS tagging done.
    Optionally but reccomended, redirect STDOUT to a text file to store the output of the data.


    Example input output:
    python3 tagger.py pos-train.txt pos-test.txt > pos-test-with-tags.txt

    Where (elipses signify the files continue in length):
        pos-train.txt:
            [ Pierre/NNP Vinken/NNP ]
            ,/, 
            [ 61/CD years/NNS ]
            old/JJ ,/, will/MD join/VB 
            [ the/DT board/NN ]
            as/IN 
            ...
        pos-test.txt:
            No , 
            [ it ]
            [ was n't Black Monday ]
            . 
            But while 
            ...
        
    And the output is sent to: 
        Note: this file is the output
        pos-test-with-tags.txt:
            No/DT ,/, it/PRP was/VBD n't/RB Black/NNP Monday/NNP ./. But/CC while/IN the/DT New/NNP York/NNP 
            Stock/NNP Exchange/NNP did/VBD n't/RB fall/VB apart/NN Friday/NNP as/IN the/DT Dow/NNP Jones/NNP
            ...
    


>  3) describe the algorithm you have used to solve the problem, specified in a stepwise or point by point fashion.
    I will walk through the proccess of the program pretty much line by line here:

    The arguments are popped off one at a time and stored into variables.
    The training file is opened. Each line is read and joined into a single string.

    That training file input is sent into a formatting method.
    The format method strips away all square brackets, replaces all newlines with 
    spaces, then splits entire string by whitespace and concats with a single space
    to ensure only 1 space between each word. That string is then the output.

    This formatted string is then sent to a method which turns it into a list of lists.
    Each sub-list contains 3 items: a "previous POS", a word, and the associated POS.
    This is done by splitting at all spaces, then splitting at all non-deliminated '/'
    to create sub lists of: word, POS. Next, the POS of the previous list is inserted
    at the beginning of the sub-list to create the final: "previous POS", a word, 
    and the associated POS. In the case of .!? or the very first sentence, the previous
    POS is set as <START> rather than the actual prevois POS. This is output is stored
    in a variable to be used at other times.

    Next, a dictionary is created to store the number of occurances of every word in 
    the training data. This is done by passing the list created above, and the index 
    of the word in the sublist, which is 1. An empty dictionary is created, and the
    list is iterated through. For each word that is not in the dictionary, it is
    added and its value is set to 1. FOr each word that is in the dictionary, its
    value is iterated by 1. The resulting dictionary is returned and stored in a
    variable.

    Next, a similar thing to the previous step occurs, but with the tags instead.
    The index of the tags is passed as 2. Beause there are more tags than there
    are words, at the beginning a <Start> tag is added to the dictionary. Then each
    list is iterated through, adding the POS that havent been encountered yet, and 
    iterating their value for each one that has already been encountered. If a .!?
    is hit, another <START> tag is added to the freqnency list. The resulting
    dictionary is returned and stored in a variable.

    Next, a dictionary is created to store the distribution of word-tag pairs.
    Each word-tag pair is extracted from the [prevTag, word, tag] list. These values
    are then stored in a tuple which will become a key in the dictionary. If this 
    tuple is not yet in the dictionary, it is added. If it is already in the dictionary,
    its value (frequency) is iterated. This dictionary is returned and stored in a 
    variable. form of output is {(word, tag):3, (word,tag), 110,...}.

     Next, a dictionary is created to store the distribution of prevTag-tag pairs.
    Each prevTag-tag pair is extracted from the [prevTag, word, tag] list. These values
    are then stored in a tuple which will become a key in the dictionary. If this 
    tuple is not yet in the dictionary, it is added. If it is already in the dictionary,
    its value is iterated. This dictionary is returned and stored in a variable.
    form of output is {(preTag, tag):3, (preTag,tag), 110,...}.

    Next a dictionary is created to store all valid POS for each word. The overall
    structure is: {Word1: [Tag4, Tag12], Word2: [Tag3],...}. This is done by sending
    the Word-Tag dictionary previously created to a function. An empty dictionary is
    created. Then each key/value pair is iterated through. If the word in the tuple
    key is not yet a key in the new dictionary, it is added as a key and its value 
    is set to a list containing the POS which is also in the tuple. If the word in the
    tuple is already a key, its associated POS is appended to the list which is the
    value of the dictionary being created. Once every word-POS tuple in the corpus has
    been looped through, the resulting dictionary is returned and stored in a variable.

    Next the test file is read in. the test file referes to the input file which is
    not tagged. It is read in and converted to a single string.

    This string is formatted.
    The format method strips away all square brackets, replaces all newlines with 
    spaces, then splits entire string by whitespace and concats with a single space
    to ensure only 1 space between each word. That string is then the output.

    This string is then split at whitespace into a list.

    This list is now sent to a function to return a nested list of all the words. 
    For the first sentence or any word which is a .!?, a <START> tag is inserted at
    the head of the list to make a resulting data structure which looks like this:
    [[<START>, He], [was], [tired] [.], [<START>, She],...]. This list is then
    returned.

    Next, this list is sent ot a function to fill in each of the inner lists with
    the correct preTag and Tag to resemble the list created earlier from the training
    data in the form [[preTag, word, POS], [preTag, word, POS],...]. TO do this,
    an empty list is created which will be filled and returned as the output. THe
    the input list created above is iterated through. if a start tag is not the first
    element in each inner list, then the previously generated POS tag is inserted
    at the head, resulting in all lists being [preTag, word] at this step. Next, if 
    the word does not ever occur in the training data, it is assigned a POS of NN.
    If the word does occur in the training data, every tag associated with it is
    iterated through. For each of those tags, the probibility of P(tag|word)*
    P(tag|previous tag) is calculated. The step by step of these occurs after this.
    Once the probibility is calculated, if it is the highest probibility encountered
    it is stored, otherwise nothing happens. When all possible associated tags have
    been iterated through, the [preTag, word] pair is appended with the POS 
    corresponding to the max probibility just calculated. Once this occurs for every
    [preTag, word] pair, the resulting list which will be the output is the format
    [[preTag, word, POS], [preTag, word, POS],...]. This list is returned.

    Probability is calculated with the formula: P(tag|word)*P(tag|previous tag).
    There is one function for each of the terms in this expression.

    Probibility for P(tag|word) is called and passed the word, and the proposed
    tag. This is broken down with the formula P(a|b) = freq(a, b)/freq(b). 
    Therefore the numerator is set to the value associated with the (word, tag)
    tuple in the word-tag dictionary created from the training data. The denominator
    is set to the frequency of the given word in the training data, by accessing
    the word-frequency dictionary created from the training data.

    Probibility for P(tag|previous tag) is called and passed the previousTag, and the 
    proposed tag. This is broken down with the formula P(a|b) = freq(a, b)/freq(b). 
    Therefore the numerator is set to the value associated with the (PrevTag, tag)
    tuple in the prevTag-tag dictionary created from the training data. The 
    denominator is set to the frequency of the given word in the training data, by 
    accessing the word-frequency dictionary created from the training data. 

    The list is then concatenated such that the preTags are cut off. Then the word
    and associated POS are concatenated together with a '/' between, reminicent of
    the training data, and is stored as a string in a new list. each of these strings 
    are then concatentated together as one single string and returned. The output of 
    this is printed.



'''
##############################################################################################################

'''
2) Detailed comments throughout code that fully explain details of algorithm.
Implementation must work as described and solve problem correctly to get credit for
detailed comments. 

Will Include this above every method and line of code where necissary.
'''

import sys, re, os, random

'''
The format method strips away all square brackets, replaces all newlines with 
    spaces, then splits entire string by whitespace and concats with a single space
    to ensure only 1 space between each word. That string is then the output.
'''
def format(text):
    #delete brackets [ ]
    text = re.sub(r'[\[\]]', '', text)
    #replace newlines with spaces
    text = re.sub(r'[\n]', ' ', text)
    #use split and join to reduce all amounts of whitespace to a single space
    text = ' '.join(text.split())
    return text


'''
     this method which turns input string into a list of lists.
    Each sub-list contains 3 items: a "previous POS", a word, and the associated POS.
    This is done by splitting at all spaces, then splitting at all non-deliminated '/'
    to create sub lists of: word, POS. Next, the POS of the previous list is inserted
    at the beginning of the sub-list to create the final: "previous POS", a word, 
    and the associated POS. In the case of .!? or the very first sentence, the previous
    POS is set as <START> rather than the actual prevois POS. This is output is stored
    in a variable to be used at other times.
'''
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
        temp = POSwordPOS[2].split('|')
        POSwordPOS[2] = temp[-1]
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


'''
    a list is now sent to testWordList() to return a nested list of all the words. 
    For the first sentence or any word which is a .!?, a <START> tag is inserted at
    the head of the list to make a resulting data structure which looks like this:
    [[<START>, He], [was], [tired] [.], [<START>, She],...]. This list is then
    returned.
'''
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


'''
    singleFreq(): a dictionary is created to store the number of occurances of every word in 
    the training data. This is done by passing the list created above, and the index 
    of the word in the sublist, which is 1. An empty dictionary is created, and the
    list is iterated through. For each word that is not in the dictionary, it is
    added and its value is set to 1. FOr each word that is in the dictionary, its
    value is iterated by 1. The resulting dictionary is returned and stored in a
    variable.

    also,

    a similar thing to the previous step occurs, but with the tags instead.
    The index of the tags is passed as 2. Beause there are more tags than there
    are words, at the beginning a <Start> tag is added to the dictionary. Then each
    list is iterated through, adding the POS that havent been encountered yet, and 
    iterating their value for each one that has already been encountered. If a .!?
    is hit, another <START> tag is added to the freqnency list. The resulting
    dictionary is returned and stored in a variable.
'''
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

'''
    a dictionary is created to store the distribution of word-tag pairs.
    Each word-tag pair is extracted from the [prevTag, word, tag] list. These values
    are then stored in a tuple which will become a key in the dictionary. If this 
    tuple is not yet in the dictionary, it is added. If it is already in the dictionary,
    its value (frequency) is iterated. This dictionary is returned and stored in a 
    variable. form of output is {(word, tag):3, (word,tag), 110,...}.

also,

    Next, a dictionary is created to store the distribution of prevTag-tag pairs.
    Each prevTag-tag pair is extracted from the [prevTag, word, tag] list. These values
    are then stored in a tuple which will become a key in the dictionary. If this 
    tuple is not yet in the dictionary, it is added. If it is already in the dictionary,
    its value is iterated. This dictionary is returned and stored in a variable.
    form of output is {(preTag, tag):3, (preTag,tag), 110,...}.
'''
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



'''
    a list is sent ot testTriples() to fill in each of the inner lists with
    the correct preTag and Tag to resemble the list created earlier from the training
    data in the form [[preTag, word, POS], [preTag, word, POS],...]. TO do this,
    an empty list is created which will be filled and returned as the output. THe
    the input list created above is iterated through. if a start tag is not the first
    element in each inner list, then the previously generated POS tag is inserted
    at the head, resulting in all lists being [preTag, word] at this step. Next, if 
    the word does not ever occur in the training data, it is assigned a POS of NN.
    If the word does occur in the training data, every tag associated with it is
    iterated through. For each of those tags, the probibility of P(tag|word)*
    P(tag|previous tag) is calculated. The step by step of these occurs after this.
    Once the probibility is calculated, if it is the highest probibility encountered
    it is stored, otherwise nothing happens. When all possible associated tags have
    been iterated through, the [preTag, word] pair is appended with the POS 
    corresponding to the max probibility just calculated. Once this occurs for every
    [preTag, word] pair, the resulting list which will be the output is the format
    [[preTag, word, POS], [preTag, word, POS],...]. This list is returned.
'''
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


'''
    Probibility for P(tag|word) is called and passed the word, and the proposed
    tag. This is broken down with the formula P(a|b) = freq(a, b)/freq(b). 
    Therefore the numerator is set to the value associated with the (word, tag)
    tuple in the word-tag dictionary created from the training data. The denominator
    is set to the frequency of the given word in the training data, by accessing
    the word-frequency dictionary created from the training data.
'''
def wordtagP(word, tag):
    if (word, tag) not in freqWordTag:
        return 0
    num = freqWordTag.get((word, tag))
    denom = freqWord.get(word)
    return num/denom


'''
    Probibility for P(tag|previous tag) is called and passed the previousTag, and the 
    proposed tag. This is broken down with the formula P(a|b) = freq(a, b)/freq(b). 
    Therefore the numerator is set to the value associated with the (PrevTag, tag)
    tuple in the prevTag-tag dictionary created from the training data. The 
    denominator is set to the frequency of the given word in the training data, by 
    accessing the word-frequency dictionary created from the training data. 
'''
def tagm1tagP(tagm1,tag):
    if (tagm1, tag) not in freqTagm1Tag:
        return 0
    num = freqTagm1Tag.get((tagm1, tag))
    denom = freqTag.get(tagm1)
    return num/denom


'''
    allTagsPerWord(): a dictionary is created to store all valid POS for each word. The overall
    structure is: {Word1: [Tag4, Tag12], Word2: [Tag3],...}. This is done by sending
    the Word-Tag dictionary previously created to a function. An empty dictionary is
    created. Then each key/value pair is iterated through. If the word in the tuple
    key is not yet a key in the new dictionary, it is added as a key and its value 
    is set to a list containing the POS which is also in the tuple. If the word in the
    tuple is already a key, its associated POS is appended to the list which is the
    value of the dictionary being created. Once every word-POS tuple in the corpus has
    been looped through, the resulting dictionary is returned and stored in a variable.
'''
def allTagsPerWord(freqWordTag):
    validTags = {}
    for wordPOS, wfreq in freqWordTag.items():
        if wordPOS[0] in validTags:
            validTags[wordPOS[0]].append(wordPOS[1])
        else:
            validTags[wordPOS[0]] = [wordPOS[1]]
    return validTags


'''
    The list is then concatenated such that the preTags are cut off. Then the word
    and associated POS are concatenated together with a '/' between, reminicent of
    the training data, and is stored as a string in a new list. each of these strings 
    are then concatentated together as one single string and returned. The output of 
    this is printed.
'''
def makePretty(trips):
    words = []
    for trip in trips:
        words.append(trip[1] + '/' + trip[2])
    return ' '.join(words)

##########################################################PROGRAM START###################################################################
'''
The arguments are popped off one at a time and stored into variables.
'''
pythonFileName = sys.argv.pop(0)
trainFile = sys.argv.pop(0)
testFile = sys.argv.pop(0)
trainText = ''
testText = ''


'''
The training file is opened. Each line is read and joined into a single string.
'''
#to read about the strip() function, see https://docs.python.org/3/library/stdtypes.html?highlight=strip#str.strip
#to read about the join() function, see https://docs.python.org/2/library/stdtypes.html#str.join
with open(trainFile, 'r+') as f:
    lines = []
    for line in f:
        lines.append(line.strip())
    trainText = ' '.join(lines)


#format() is called on the resultng string.
#toWordList() is called on the output of format.
#the output of toWordList() is stored in variable trips.
#to read about the process(es) go to the function(s).
trips = toWordList(format(trainText))
#singleFreq() is called on trips, and passed the index value of 1.
#the output is stored in freqWords.
#to read about the process(es) go to the function(s).
freqWord = singleFreq(trips, 1)
#singleFreq() is called on trips, and passed the index value of 2.
#the output is stored in freqTags.
#to read about the process(es) go to the function(s).
freqTag = singleFreq(trips, 2)
#doubleFreq() is called on trips, and passed the index value of 1.
#the output is stored in freqWordTag.
#to read about the process(es) go to the function(s).
freqWordTag = doubleFreq(trips, 1)
#doubleFreq() is called on trips, and passed the index value of 0.
#the output is stored in freqTagm1Tag.
#to read about the process(es) go to the function(s).
freqTagm1Tag = doubleFreq(trips, 0)
#allTagsPerWord() is called on freqWordTag,.
#the output is stored in validTagsPerWord.
#to read about the process(es) go to the function(s).
validTagsPerWord = allTagsPerWord(freqWordTag)


'''
Next the test file is read in. the test file referes to the input file which is
not tagged. It is read in and converted to a single string.
'''
#to read about the strip() function, see https://docs.python.org/3/library/stdtypes.html?highlight=strip#str.strip
#to read about the join() function, see https://docs.python.org/2/library/stdtypes.html#str.join
with open(testFile, 'r+') as f:
    lines = []
    for line in f:
        lines.append(line.strip())
    testText = ' '.join(lines)
 

#format() is called on the input text from above.
#The output of format is made into a list with .split() function
#The output of split() is sent to testWordList().
#The output of testWordList() is sent to testTriples().
#The output of testTriples() is sent to makePretty().
#The output of makePretty() is sent to print().
#to read about the process(es) go to the function(s).
#to read about the print() function, see https://docs.python.org/3/library/functions.html#print
#to read about the split() function, see https://docs.python.org/3/library/stdtypes.html?highlight=split#str.split
print(makePretty(testTriples(testWordList(format(testText).split()))))