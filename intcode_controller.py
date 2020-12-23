import sys
from time import time
import serial
from typing import List

port = '/dev/ttyACM0'

ard = serial.Serial(port, 9600, timeout=5)


def debug(*args):
    # print('\033[34m', end='')
    # print(*args, end='')
    # print('\033[0m')
    pass


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
            debug(f'GET[{int(args[0])}] = {val}')
            return val
        elif operation == "SET":
            debug(f'SET[{int(args[0])}] = {int(args[1])}')
            self[int(args[0])] = int(args[1])
        elif operation == "INPUT":
            val = input("INPUT ")
            return val
        elif operation == "OUTPUT":
            print('OUTPUT', *args)
        elif operation == "HALT" or operation == "ERROR":
            print(*cmd)
            self.finish = True
        else:
            debug(*cmd)


fileContent = ''
with open(sys.argv[1]) as file:
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
