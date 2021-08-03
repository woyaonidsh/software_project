import time
import re
from collections import Counter
import os


class Count:
    def __init__(self, Dir_name, n):
        self.letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                        't', 'u', 'v', 'w', 'x', 'y', 'z']
        self.Dir_name = Dir_name
        self.n = n

    # 统计字母
    def CountLetters(self):
        print("File name:" + self.Dir_name)
        totalNum = 0
        dicNum = {}
        t0 = time.clock()
        with open(self.Dir_name) as f:
            txt = f.read().lower()
        for letter in self.letters:
            dicNum[letter] = txt.count(letter)  # here count is faster than re
            totalNum += dicNum[letter]
        for letter in self.letters:
            dicNum[letter] = dicNum[letter]
        dicNum = sorted(dicNum.items(), key=lambda k: k[0])
        dicNum = sorted(dicNum, key=lambda k: k[1], reverse=True)
        t1 = time.clock()
        self.display(dicNum, 'character', totalNum, 9)
        print("Time Consuming:%4f" % (t1 - t0))

    # 显示结果
    def display(self, dicNum, type, totalNum, k):
        maxLen = 0
        if not dicNum:
            print("Error:Nothing matched!!")
            return
        for word, fre in dicNum:
            if len(word) > maxLen:
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

    # 统计单词
    def CountWords(self, file_name, n, stopName):
        print("File name:" + file_name)
        if stopName != None:
            stopflag = True
        else:
            stopflag = False
        t0 = time.clock()
        with open(file_name) as f:
            txt = f.read()
        txt = txt.lower()   # 全部变为小写
        if stopflag == True:
            with open(stopName) as f:   # 加载停用词
                stoplist = f.readlines()
        pattern = r"[a-z][a-z0-9]*"   # 使用正则表达式进行匹配
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
        if n == 0:
            dicNum = dict(tempc)
        else:
            dicNum = dict(tempc.most_common(n))

        dicNum = sorted(dicNum.items(), key=lambda k: k[0])
        dicNum = sorted(dicNum, key=lambda k: k[1], reverse=True)
        t1 = time.clock()
        self.display(dicNum, 'Words', totalNum, 3)
        print("Time Consuming:%4f" % (t1 - t0))


def OperateInDir(Fuc, Dir_name, n, stopName, reflag, *arges):
    if reflag:
        for path, _, filelist in os.walk(Dir_name):
            for file in filelist:
                if arges:
                    Fuc(os.path.join(path, file), n, stopName, arges[0])
                else:
                    Fuc(os.path.join(path, file), n, stopName)
    else:
        for file in os.listdir(Dir_name):
            if os.path.isdir(os.path.join(Dir_name, file)):
                pass
            else:
                if arges:
                    Fuc(os.path.join(Dir_name, file), n, stopName, arges[0])
                else:
                    Fuc(os.path.join(Dir_name, file), n, stopName)
