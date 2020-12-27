#!/usr/bin/env python3.8

from time import time
import serial
from typing import List
import argparse
import re


# A program is an automatically growing list of integers and can apply commands from the Arduino to this list using
# exec().
class Program(List[int]):
    finish = False
    instructCount = 0

    def __init__(self, values):
        super().__init__(values)
        self.start_time = time()

    @classmethod
    def from_text(cls, text: str):
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

        return cls(comma_separated_int)

    # Gets a value at the given position. The list grows if necessary to this index.
    def __getitem__(self, index):
        if index >= len(self):
            self.extend([0] * (index + 1 - len(self)))
        return list.__getitem__(self, index)

    # Sets a value at the given position. The list grows if necessary to this index.
    def __setitem__(self, index, value):
        if index >= len(self):
            self.extend([0] * (index + 1 - len(self)))
        list.__setitem__(self, index, value)

    # Executes a command from the arduino on this list.
    def exec(self, cmd: List[str]):
        if cmd[0] == 'GET':
            # Get the value at position
            return self[int(cmd[1])]
        elif cmd[0] == 'SET':
            # Set the value at the position to the value
            self[int(cmd[1])] = int(cmd[2])
        elif cmd[0] == 'INPUT':
            # Asks the user for an input
            return input('INPUT ')
        elif cmd[0] == 'OUTPUT':
            # Outputs a value from the arduino
            print('OUTPUT', int(cmd[1]))
        elif cmd[0] == 'HALT' or cmd[0] == 'ERROR':
            # Ends the execution of the program
            print(*cmd)
            self.finish = True
        elif cmd[0] == 'INFO' and cmd[1] == 'instruct_count_final':
            print(*cmd)
            self.instructCount = int(cmd[2])
        else:
            print(*cmd)

    def stats(self):
        out = '\033[34mSTATS\n'
        exec_time = time() - self.start_time
        out += f'Execution took {exec_time:.2f}s\n'
        ops_per_sec = self.instructCount / exec_time
        out += f'{ops_per_sec:.2f} Operations/Second\n'
        sec_per_op = exec_time / self.instructCount
        out += f'{sec_per_op:.4f} Seconds/Operation'
        out += '\033[0m'
        return out


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Intcode controller')
    parser.add_argument('-port', type=str, help='The port to connect to the arduino', default='/dev/ttyACM0')
    parser.add_argument('-baud', type=int, help='The baud rate to connect to the arduino', default=115200)
    parser.add_argument('file', type=str, help='Path to program, which should be executed')
    args = parser.parse_args()

    arduino = serial.Serial(args.port, args.baud, timeout=5)

    file_content = ''
    with open(args.file) as file:
        file_content = file.read()

    program = Program.from_text(file_content)
    start_time = time()

    # Run program
    while not program.finish:
        # Read a instruction from the arduino
        instruction = arduino.readline().decode().replace('\r\n', '')
        if not instruction:
            continue
        instruction = instruction.split()
        data = program.exec(instruction)
        if data is not None:
            # Write return value from program.exec() to arduino
            arduino.write((str(data) + '\n').encode())

    print()
    print(program.stats())

