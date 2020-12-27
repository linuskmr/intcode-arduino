#!/usr/bin/env python3.8

import sys
from time import time
import serial
from typing import List
import argparse
import re


def debug(*args):
    print('\033[34m', end='')
    print(*args, end='')
    print('\033[0m')


class Program(list):
    finish = False

    def __getitem__(self, index):
        if index >= len(self):
            self.extend([0] * (index + 1 - len(self)))
        return list.__getitem__(self, index)

    def __setitem__(self, index, value):
        if index >= len(self):
            self.extend([0] * (index + 1 - len(self)))
        list.__setitem__(self, index, value)

    def exec(self, cmd: List[str]):
        operation = cmd[0]
        args = cmd[1:]
        if operation == "GET":
            val = self[int(args[0])]
            return val
        elif operation == "SET":
            self[int(args[0])] = int(args[1])
        elif operation == "INPUT":
            val = input("INPUT ")
            return val
        elif operation == "OUTPUT":
            print('OUTPUT', int(args[0]))
        elif operation == "HALT" or operation == "ERROR":
            print(*cmd)
            self.finish = True
        else:
            debug(*cmd)


def str_to_comma_separated(text: str):
    # Remove comments
    text = re.sub('\\s*#.*', '', text)

    # Convert spaces and newlines to comma
    text = text.replace('\n', ',')
    text = text.replace(' ', ',')

    # Remove multiple commas
    text = re.sub(r',+', ',', text)

    # Remove possible empty first element
    text = re.sub(r'^,', '', text)

    # Split numbers by comma and parse them to integers
    comma_separated = text.split(',')
    comma_separated_int = [int(x) for x in comma_separated]
    return comma_separated_int


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Intcode controller')
    parser.add_argument('-port', type=str, help='The port to connect to the arduino', default='/dev/ttyACM0')
    parser.add_argument('-baud', type=int, help='The baud rate to connect to the arduino', default=115200)
    parser.add_argument('file', type=str, help='Path to program, which should be executed')
    args = parser.parse_args()

    ard = serial.Serial(args.port, args.baud, timeout=5)

    fileContent = ''
    with open(args.file) as file:
        fileContent = file.read()

    program = Program([int(x) for x in fileContent.split(',')])

    start_time = time()
    while True:
        instruction = ard.readline().decode().replace('\r\n', '')
        if not instruction:
            continue
        instruction = instruction.split()
        data = program.exec(instruction)
        if program.finish:
            end_time = time()
            print(f'Execution took {end_time - start_time:.2f}s')
            exit()
        if data is not None:
            ard.write((str(data) + '\n').encode())
