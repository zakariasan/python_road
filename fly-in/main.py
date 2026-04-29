import sys
from parser import ft_parser


def main():
    if len(sys.argv) != 2:
        print("Usage: python path_file.txt", sys.argv)
    try:
        ft_parser(sys.argv[1])
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
