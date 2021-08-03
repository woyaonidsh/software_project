import time
import re
from collections import Counter
import os


class Count:
    def __init__(self, n, stopName, verbName, k):
        self.letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                        't', 'u', 'v', 'w', 'x', 'y', 'z']
        self.n = n
        self.stopName = stopName
        self.verbName = verbName
        self.k = k

    def CountLetters(self, file_name):
        print("File name:" + file_name)
        if self.stopName != None:
            stopflag = True
        else:
            stopflag = False
        if self.verbName != None:
            print("Verb tenses normalizing is not supported in this function!")
        else:
            pass
        totalNum = 0
        dicNum = {}
        t0 = time.clock()
        if stopflag == True:
            with open(self.stopName, 'r') as f:
                stoplist = f.readlines()
        with open(file_name) as f:
            txt = f.read().lower()
        for letter in self.letters:
            dicNum[letter] = txt.count(letter)  # here count is faster than re
            totalNum += dicNum[letter]
        for letter in self.letters:
            dicNum[letter] = dicNum[letter]
        if stopflag == True:
            for word in stoplist:
                word = word.replace('\n', '')
                try:
                    del dicNum[word]
                except:
                    pass
        dicNum = sorted(dicNum.items(), key=lambda k: k[0])
        dicNum = sorted(dicNum, key=lambda k: k[1], reverse=True)
        t1 = time.clock()
        self.display(dicNum, 'character', totalNum, 9)
        print("Time Consuming:%4f" % (t1 - t0))

    def CountWords(self, file_name):
        print("File name:" + file_name)
        if self.stopName != None:
            stopflag = True
        else:
            stopflag = False
        if self.verbName != None:
            verbflag = True
        else:
            verbflag = False
        t0 = time.clock()
        with open(file_name) as f:
            txt = f.read()
        txt = txt.lower()
        if stopflag == True:
            with open(self.stopName, 'r') as f:
                stoplist = f.readlines()
        pattern = r"[a-z][a-z0-9]*"
        wordList = re.findall(pattern, txt)
        totalNum = len(wordList)
        tempc = Counter(wordList)
        if stopflag == True:
            for word in stoplist:
                word = word.replace('\n', '')
                try:
                    del tempc[word]
                except:
                    pass
        dicNum = dict(tempc.most_common(self.n))
        if verbflag == True:
            totalNum = 0
            verbDic = {}
            verbDicNum = {}
            with open(self.verbName, 'r') as f:
                for line in f.readlines():
                    key, value = line.split(' -> ')
                    verbDic[key] = value.replace('\n', '').split(',')
                    verbDicNum[key] = tempc[key]
                    for word in verbDic[key]:
                        verbDicNum[key] += tempc[word]
                    totalNum += verbDicNum[key]
            verbDicNum = sorted(dicNum.items(), key=lambda k: k[0])
            verbDicNum = sorted(verbDicNum, key=lambda k: k[1], reverse=True)
        dicNum = sorted(dicNum.items(), key=lambda k: k[0])
        dicNum = sorted(dicNum, key=lambda k: k[1], reverse=True)
        t1 = time.clock()
        if verbflag == True:
            self.display(verbDicNum[:self.n], 'words', totalNum, 3)
        else:
            self.display(dicNum, 'words', totalNum, 3)
        print("Time Consuming:%4f" % (t1 - t0))

    def CountPhrases(self, file_name):
        print("File name:" + file_name)
        totalNum = 0
        if self.stopName != None:    # 停用词表
            stopflag = True
        else:
            stopflag = False
        if self.verbName != None:    # 动词形态转换表
            verbflag = True
        else:
            verbflag = False
        t0 = time.clock()
        with open(file_name) as f:
            txt = f.read()
        txt = txt.lower()    # 转换为小写字母
        txt = re.sub(r'\s+', ' ', txt)
        pword = r'(([a-z]+ )+[a-z]+)'  # 抽取句子
        pattern = re.compile(pword)
        sentence = pattern.findall(txt)
        txt = ','.join([sentence[m][0] for m in range(len(sentence))])
        if stopflag == True:   # 加载停用词表
            with open(self.stopName, 'r') as f:
                stoplist = f.readlines()
                stopNum = len(stoplist)
        pattern = "[a-z]+[0-9]*"
        for i in range(self.k - 1):
            pattern += "[\s|,][a-z]+[0-9]*"
        wordList = []
        for i in range(self.k):
            if i == 0:
                tempList = re.findall(pattern, txt)
            else:
                wordpattern = "[a-z]+[0-9]*"
                txt = re.sub(wordpattern, '', txt, 1).strip()
                tempList = re.findall(pattern, txt)
            wordList += tempList
        tempc = Counter(wordList)
        if stopflag == True:
            for word in stoplist:
                word = word.replace('\n', '')
                try:
                    del tempc[word]
                except:
                    pass
        dicNum = {}
        if verbflag == True:
            verbDic = {}
            with open(self.verbName, 'r') as f:    # 打开动词形态转换表
                for line in f.readlines():
                    key, value = line.split(' -> ')
                    for tverb in value.replace('\n', '').split(','):
                        verbDic[tverb] = key
                    verbDic[key] = key
            for phrase in tempc.keys():
                if ',' not in phrase:
                    totalNum += 1
                    verba, verbb = phrase.split(' ')
                    if verba in verbDic.keys() and verbb in verbDic.keys():
                        normPhrase = verbDic[verba] + ' ' + verbDic[verbb]
                        changeFlag = True
                    elif verba in verbDic.keys():
                        changeFlag = True
                        normPhrase = verbDic[verba] + ' ' + verbb
                    elif verbb in verbDic.keys():
                        changeFlag = True
                        normPhrase = verba + ' ' + verbDic[verbb]
                    else:
                        changeFlag = False
                    if changeFlag:
                        if normPhrase in dicNum.keys():
                            dicNum[normPhrase] += tempc[phrase]
                        else:
                            dicNum[normPhrase] = tempc[phrase]
        else:
            phrases = tempc.keys()
            for phrase in phrases:
                if ',' not in phrase:
                    dicNum[phrase] = tempc[phrase]
                    totalNum += tempc[phrase]
        dicNum = sorted(dicNum.items(), key=lambda k: k[0])
        dicNum = sorted(dicNum, key=lambda k: k[1], reverse=True)
        t1 = time.clock()
        self.display(dicNum[:self.n], 'Phrases', totalNum, 3)
        print("Time Consuming:%4f" % (t1 - t0))

    def display(self, dicNum, type, totalNum, k):
        maxLen = 0
        if (not dicNum):
            print("Error:Nothing matched!!")
            return
        for word, fre in dicNum:
            if (len(word) > maxLen):
                maxLen = len(word)
        print("-" * int(2.18 * k * maxLen))
        formatstr = "{:^" + str(2 * k * maxLen + 1) + "}"
        print(formatstr.format('The Rank List'))
        formatstr = "{:" + str(k * maxLen) + "}|{:<" + str(k * maxLen) + "}"
        print(formatstr.format(type, "Frequency"))
        if totalNum > 0:
            formatstr = "{:" + str(k * maxLen) + "}|{:<" + str(k * maxLen) + ".2%}"
            for word, fre in dicNum:
                print(formatstr.format(word, fre / totalNum))
            print("-" * int(2.18 * k * maxLen))


def OperateInDir(Fuc, Dir_name, reflag, *arges):
    for path, _, filelist in os.walk(Dir_name):
        for file in filelist:
            if arges:
                Fuc(os.path.join(path, file), arges[0])
            else:
                Fuc(os.path.join(path, file))
        if not reflag:
            break
