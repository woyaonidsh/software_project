import config1
import step1
from step1 import Count
import sys

args = config1.parse_args()

if __name__ == '__main__':

    count = Count(Dir_name=args.path, n=args.num)

    if args.num < 0:  # 输入前n个数字不能为负
        print("Error: The num of the iterms output should not be negative!!")
        sys.exit()

    if args.countChar:  # 统计字母
        count.CountLetters()
    elif args.countWords:  # 统计单词
        count.CountWords(args.path, int(args.num), args.stopFile)
    elif args.dirFlag:
        step1.OperateInDir(count.CountWords, args.path, int(args.num), args.stopFile, args.reFlag)   # 递归查询所有子目录
    else:
        print("Error: Please input the operation type (-f|-d|-c)")
