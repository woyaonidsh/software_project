import config3
import step3
from step3 import Count
import sys

args = config3.parse_args()

if __name__ == '__main__':
    if args.phraseNum < 0:  # 短语数量不能为负数
        print("Error: The num of words in a phrase should not be negative!!")
        sys.exit()
    if args.num < 0:  # 单词数量不能为负数
        print("Error: The num of the iterms output should not be negative!!")
        sys.exit()
    count = Count(n=int(args.num), stopName=args.stopFile, verbName=args.verbFile, k=int(args.phraseNum))
    if args.countChar:  # 统计字母
        if args.dirFlag:
            step3.OperateInDir(count.CountLetters, args.path, args.reFlag)
        else:
            count.CountLetters(args.path)
    if args.countWords:  # 统计单词
        if args.dirFlag:
            step3.OperateInDir(count.CountWords, args.path, args.reFlag)
        else:
            count.CountWords(args.path)
    elif args.phraseNum:  # 统计短语
        if args.dirFlag:
            step3.OperateInDir(count.CountPhrases, args.path, args.reFlag)
        else:
            count.CountPhrases(args.path)
    else:
        print("Error: Please input the operation type (-f|-q|-p|-c)")
