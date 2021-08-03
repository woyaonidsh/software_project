from step0 import Count
import config0

args = config0.parse_args()


if __name__ == '__main__':
    if args.countChar:   # 统计字母
        letter = Count(file_path=args.path)
        letter.CountLetters()
    else:
        print("Error: Please input the operation type (-f|-q|-p|-c)")
