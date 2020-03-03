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

    Given an input from another program which is a text file of programmatically tagged words with their
    expected part of speech (POS), and another input file which is the same text, but hand tagged by
    a human with the correct POS for each word.
    Create a program which can score the accuracy of the original program by comparing it to the correct key.
    Also create a table comparing the part of speech your original program thought every word was to
    what the words tagged as that part of speech actually were (reffered to as a confusion matrix).


> 2) give actual examples of program input and output, along with usage instructions:

    Usage Instructions:
    Call the python program with 2 arguments. 
    The first argument should be a path to a text file containing text which was prgrammatically tagged with POS.
    The second argument should be a path to a file in which the same text is already tagged with the correct POS.
    Optionally but reccomended, redirect STDOUT to a text file to store the output of the data.


    Example input output:
    python scorer.py pos-test-with-tags.txt pos-test-key.txt > pos-tagging-report.txt

    Where (elipses signify the files continue in length):
        pos-test-with-tags.txt
             No/DT ,/, it/PRP was/VBD n't/RB Black/NNP Monday/NNP ./. But/CC while/IN the/DT New/NNP York/NNP 
            Stock/NNP Exchange/NNP did/VBD n't/RB fall/VB apart/NN Friday/NNP as/IN the/DT Dow/NNP Jones/NNP
            ...
        pos-test-key.txt:
            No/RB ,/, 
            [ it/PRP ]
            [ was/VBD n't/RB Black/NNP Monday/NNP ]
            ./. 
            But/CC while/IN 
            ...
        
    And the output is sent to: 
        Note: this file is the output of the program
        pos-tagging-report.txt:
            Accuracy: 0.8522279318597775

            Confusion Matrix, where left value is the calculated, experimental and the inner values are the pos-test-key.txt values.
            For example:
                    DT: {'WP': 0, 'NNS': 4, DT: 1776}
            Can be read as: What the program thought was a DT was correctly tagged as a DT, 1776 times, but 4 times it was actually supposed to be an NNS

            DT: {'SYM': 0, 'RBS': 0, 'EX': 0, 'TO': 0, ',': 0, 'CD': 0, "''": 0, 'PRP$': 0, 'UH': 1, '.': 0, 'JJS': 0, 'WRB': 0, 'FW': 0, 'VB': 0, '(': 0, ')': 0, 'NN': 4, 'WDT': 0, 'MD': 0, '``': 0, 'CC': 11, ':': 0, 'RBR': 0, '$': 0, 'VBP': 0, 'RP': 0, 'JJ': 0, 'WP$': 0, 'PRP': 0, 'VBN': 0, 'PDT': 14, 'LS': 0, 'JJR': 0, 'DT': 4778, 'NNPS': 0, 'RB': 14, '#': 0, 'IN': 4, 'VBZ': 0, 'NNP': 4, 'POS': 0, 'VBD': 0, 'NNS': 0, 'VBG': 0, 'WP': 0}
            ,: {'SYM': 0, 'RBS': 0, 'EX': 0, 'TO': 0, ',': 3070, 'CD': 0, "''": 0, 'PRP$': 0, 'UH': 0, '.': 0, 'JJS': 0, 'WRB': 0, 'FW': 0, 'VB': 0, '(': 0, ')': 0, 'NN': 0, 'WDT': 0, 'MD': 0, '``': 0, 'CC': 0, ':': 0, 'RBR': 0, '$': 0, 'VBP': 0, 'RP': 0, 'JJ': 0, 'WP$': 0, 'PRP': 0, 'VBN': 0, 'PDT': 0, 'LS': 0, 'JJR': 0, 'DT': 0, 'NNPS': 0, 'RB': 0, '#': 0, 'IN': 0, 'VBZ': 0, 'NNP': 0, 'POS': 0, 'VBD': 0, 'NNS': 0, 'VBG': 0, 'WP': 0}
            ...
    


>  3) describe the algorithm you have used to solve the problem, specified in a stepwise or point by point fashion.
    I will walk through the proccess of the program pretty much line by line here:

    program starts at ####START PROGRAM####

    The arguments are popped off one at a time and stored into variables.

    The experimental data, which is the output of the first program, is sent into
    function readIn(). This opens the text file. Each line is read and joined into
    a single string.

    The output string of readIn() is sent to toWordList(). toWordList() splits
    the text at whitespace into a list. A new list is instantiated as empty. the
    original list is then iterated through. each string in it is split by all non-
    deliminated '/', creating smaller lists with two entires, a word and its POS.
    all split tags with '|' have the latter half removed. The POS in each [word, 
    POS] list is appended to the newly instantiated list. once all word/POS pairs 
    have been split and the POS appended to the new list, that new list is returned.
    It is in the form ['Tag1', 'Tag2', 'Tag3',...]. This output is stored in a
    variable called mySolution.

    The second argument, the filepath to the test-key, is sent to the readIn() file.

    The output string of readIn() is sent to toWordList(). toWordList() splits
    the text at whitespace into a list. A new list is instantiated as empty. the
    original list is then iterated through. each string in it is split by all non-
    deliminated '/', creating smaller lists with two entires, a word and its POS.
    all split tags with '|' have the latter half removed. The POS in each [word, 
    POS] list is appended to the newly instantiated list. once all word/POS pairs 
    have been split and the POS appended to the new list, that new list is returned.
    It is in the form ['Tag1', 'Tag2', 'Tag3',...]. This output is stored in a
    variable called testKey.

    The data in mySolution and TestKey lists is sent as input to a function called
    initializeMatrix(). This function Creates an empty nexted dictionary. For each
    POS in the mySolution list, it checks if iit is already in the matrix. If not,
    it is added to as a key of the dictionary, and the value assigned is an empty
    dictionary. Once this loop ends, there is exactly 1 key for each POS present
    in the mySolution set of POSs. Next a loop goes through all POS in the testKey
    list. if the POS is not present in a tuple, it is added to that tuple. Once
    this loop completes, there is exactly 1 item in the tuple for each POS in the
    pos-test-key. Next, a loop iterates over each K/V pair in the dictionary which 
    was created. In each iteration, it loops over every POS in the pos-test-key
    tuple. if the given POS is not already in the inner dictionary for that mySolution
    POS, it is added as a key and initialized with a value of 0. Once all loops are
    complete, the nested dictionary where all values are initialized to 0 is returned
    and stored in variable called empty matrix. dictionary is in form:
    {myPOS1:{KeyPOS1:0, KeyPOS2:0...KeyPOSN:0}, myPOS2:{...},...}

    mySolution and testKey lists are sent to function called compare(). This 
    function loops through the size of both of these lists and uses the index being
    looped to check each list, mySolution and TestKey at the same index. If they
    contain the same string at that given index, a counter iterates which keeps
    track of the similar entries of the lists. if they lists contain a different
    string on the same index or if they are the same, a counter iterates counting
    the total number of items in the list. once items are looped through, a decimal
    number is returned from the division of accurate guesses over total number of 
    entries. This is the same way a test is scored, by dividing "correct" answers
    by the total number of answers. This will be a decimal score from 0, which is 
    completely inacurate, to 1, which is completely accurate.

    This output is printed to STDOUT along with a title specifying that it is the
    accuracy score. 

    The mySolution list, the testKey list, and the emptyMatrix nested dictionary
    are sent to a fuction called buildMatrix(). this function loops through an
    index counter from 0 to the side of the mySolution and testKey list, ie the 
    number of words in the input files. in each loop, the matrix input values
    are iterated for the dictionary key of the POS at the current index of
    mySolution, and the key of the inner dictionary of the POS at the current 
    index of the testKey list. Once all values have been inserted into the confusion
    matrix, the matrix is returned.

    The output of buildMatrix() is then sent to printPretty(). this function prints
    a brief explination of how to read the confusion matrix, and then prints each
    key/value pair on a seperate line, where the key is the mySolution POS, and the 
    value is the dictionary of the testKey POSs, containing values for how many times
    each was the correct tag when the program tagged a word as the mySolution POS.
    This function has no output other than printing, and so returns nothing.


'''
##############################################################################################################



import sys, re



'''
    The data is sent into
    function readIn(). This opens the text file. Each line is read and joined into
    a single string.
'''
def readIn(txtFile):
    with open(txtFile, 'r+') as f:
        lines = []
        for line in f:
            lines.append(line.strip())
        textStr = ' '.join(lines)
    return textStr

'''
    The output of the readIn() file is sent to format() file for the test-key input.
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
    toWordList() splits
    the text at whitespace into a list. A new list is instantiated as empty. the
    original list is then iterated through. each string in it is split by all non-
    deliminated '/', creating smaller lists with two entires, a word and its POS.
    all split tags with '|' have the latter half removed. The POS in each [word, 
    POS] list is appended to the newly instantiated list. once all word/POS pairs 
    have been split and the POS appended to the new list, that new list is returned.
    It is in the form ['Tag1', 'Tag2', 'Tag3',...]. 
'''
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
    

'''
    mySolution and testKey lists are sent to function called compare(). This 
    function loops through the size of both of these lists and uses the index being
    looped to check each list, mySolution and TestKey at the same index. If they
    contain the same string at that given index, a counter iterates which keeps
    track of the similar entries of the lists. if they lists contain a different
    string on the same index or if they are the same, a counter iterates counting
    the total number of items in the list. once items are looped through, a decimal
    number is returned from the division of accurate guesses over total number of 
    entries. This is the same way a test is scored, by dividing "correct" answers
    by the total number of answers. This will be a decimal score from 0, which is 
    completely inacurate, to 1, which is completely accurate.
'''
def compare(actual, expected):
    same = 0
    total = 0
    for index in range(len(actual)):
        total += 1
        if actual[index] == expected[index]:
            same+=1
    return same/total


'''
    The mySolution list, the testKey list, and the emptyMatrix nested dictionary
    are sent to a fuction called buildMatrix(). this function loops through an
    index counter from 0 to the side of the mySolution and testKey list, ie the 
    number of words in the input files. in each loop, the matrix input values
    are iterated for the dictionary key of the POS at the current index of
    mySolution, and the key of the inner dictionary of the POS at the current 
    index of the testKey list. Once all values have been inserted into the confusion
    matrix, the matrix is returned.
'''
def buildMatrix(actual, expected, matrix):
    for index in range(len(actual)):
        matrix[actual[index]][expected[index]] += 1
    return matrix


'''
    The data in mySolution and TestKey lists is sent as input to a function called
    initializeMatrix(). This function Creates an empty nexted dictionary. For each
    POS in the mySolution list, it checks if iit is already in the matrix. If not,
    it is added to as a key of the dictionary, and the value assigned is an empty
    dictionary. Once this loop ends, there is exactly 1 key for each POS present
    in the mySolution set of POSs. Next a loop goes through all POS in the testKey
    list. if the POS is not present in a tuple, it is added to that tuple. Once
    this loop completes, there is exactly 1 item in the tuple for each POS in the
    pos-test-key. Next, a loop iterates over each K/V pair in the dictionary which 
    was created. In each iteration, it loops over every POS in the pos-test-key
    tuple. if the given POS is not already in the inner dictionary for that mySolution
    POS, it is added as a key and initialized with a value of 0. Once all loops are
    complete, the nested dictionary where all values are initialized to 0 is returned
    and stored in variable called empty matrix. dictionary is in form:
    {myPOS1:{KeyPOS1:0, KeyPOS2:0...KeyPOSN:0}, myPOS2:{...},...}
'''
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


'''
    The output of buildMatrix() is then sent to printPretty(). this function prints
    a brief explination of how to read the confusion matrix, and then prints each
    key/value pair on a seperate line, where the key is the mySolution POS, and the 
    value is the dictionary of the testKey POSs, containing values for how many times
    each was the correct tag when the program tagged a word as the mySolution POS.
    This function has no output other than printing, and so returns nothing.
'''
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

'''
The arguments are popped off one at a time and stored into variables.
'''
pythonFileName = sys.argv.pop(0)
mySolutionFile = sys.argv.pop(0)
testKeyFile = sys.argv.pop(0)


#readIn() is called on the first argument.
#toWordList() is called on the output of readIn().
#the output of toWordList() is stored in variable mySolution.
#to read about the process(es) go to the function(s).
mySolution = toWordList(readIn(mySolutionFile))
#readIn() is called on the second argument.
#format() is called on the output of readIn().
#toWordList() is called on the output of format().
#the output of toWordList() is stored in variable testKey.
#to read about the process(es) go to the function(s).
testKey = toWordList(format(readIn(testKeyFile)))
#initializeMatrix() is called on mySolution and testKey.
#the output of initializeMatrix() is stored in variable emptyMatrix.
#to read about the process(es) go to the function(s).
emptyMatrix = initializeMatrix(mySolution, testKey)
#compare() is called on mySolution and testKey.
#the output of compare() is printed to STDOUT along with a title specifying that it is the
#    accuracy score. and extra trailing whitespace for the next thing to print
#to read about the process(es) go to the function(s).
print('Accuracy:', compare(mySolution, testKey), end='\n\n\n')
#buildMatrix() is called on mySolution, testKey, emptyMatrix.
#printPretty() is called on the output of buildMatrix().
#to read about the process(es) go to the function(s).
printPretty(buildMatrix(mySolution, testKey, emptyMatrix))


