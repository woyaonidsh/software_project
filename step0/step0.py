import time


# 统计字母的类
class Count:
    def __init__(self, file_path):
        self.letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                        't', 'u', 'v', 'w', 'x', 'y', 'z']
        self.file_path = file_path  # 文件路径

    # 统计字母频率
    def CountLetters(self):
        print("File name:" + self.file_path)

        totalNum = 0  # 字母总数
        dicNum = {}
        t0 = time.clock()
        with open(self.file_path, 'r', encoding='utf-8') as f:
            txt = f.read().lower()  # 读写文件内容
        for letter in self.letters:  # 统计字母频率
            dicNum[letter] = txt.count(letter)  # here count is faster than re
            totalNum += dicNum[letter]
        dicNum = sorted(dicNum.items(), key=lambda k: k[0])
        dicNum = sorted(dicNum, key=lambda k: k[1], reverse=True)
        t1 = time.clock()
        self.display(dicNum, 'character', totalNum, 9)
        print("Time Consuming:%4f" % (t1 - t0))

    # 打印排序好的字母结果
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
