import argparse


def parse_args():
    parser = argparse.ArgumentParser(description='software homework')

    # 命令行参数
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-c', '--countChar', help="Output character frequencies", action="store_true")
    parser.add_argument('path', help="The file/directory to be operated with")

    args = parser.parse_args()
    return args
