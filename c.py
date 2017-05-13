#!/usr/bin/env python
import argparse


def main(args):
    print('Executing', args.file, 'with arguments', args.args)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Python-based C interpreter')
    parser.add_argument('file', help='Main C source file')
    parser.add_argument('args', help='Program arguments', nargs=argparse.REMAINDER)
    parser_args = parser.parse_args()
    main(parser_args)
