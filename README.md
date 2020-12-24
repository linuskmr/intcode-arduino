# intcode-arduino

This is an Intcode interpreter that runs on an Arduino.
The code was developed on an Arduino Uno with an ATmega328P microcontroller.

The Intcode programming language was created in the [Advent of Code 2019](adventofcode.com/2019). For details on the language, see the [Intcode Language Specifications](##intcode-language-specifications) below.

## Installation

The software consists of two parts: On the one hand, the actual Intcode interpreter, which runs on the Arduino. On the other hand, a control and memory unit in form of a Python script. See [Implementation Details](##implementation-details) below for more information.

### Arduino

Copy the [`intcode-arduino.ino`](https://github.com/linus-k519/intcode-arduino/blob/main/intcode-arduino.ino) file into the [Arduino IDE](https://www.arduino.cc/en/software) and upload it to the Arduino via the ➡️ button.

### Python

After the software is running on the Arduino, the Python script can be started.

```bash
./intcode-controller.py examples/day9_1.ic
```

## Implementation Details

The Arduino does not have enough SRAM to hold a large Intcode program completely in memory. For example, the program of the 19 Dec 2019 has 300 int64's, resulting in a total of 5829 bytes.

That is why a Python script acts as an external storage medium. It loads an intcode program from a file. The Arduino can then communicate with the Python script via the serial interface:

```
Arduino: GET <address>
Python: <value>

Arduino: SET <address> <value>
Python: (No response)

Arduino: INPUT
Python: <value> (Asks user for input and responses with the value)

Arduino: OUTPUT <value>
Python: (No response, but prints value to stdout)
```

At 9600 baud, I achieve a performance of breathtaking 10 instructions per second with my Arduino Uno.

In the second part of 19 December 2019, about 370000 instructions have to be executed. This results in a computing time of over 10 hours 🎉


## Intcode Language Specifications

The Intcode programming language was created in the [Advent of Code 2019](adventofcode.com/2019).
The characteristic of the language is that it consists only of integers. An instruction consists of an [opcode](###opcodes) and the following arguments

### Opcodes

| Opcode | Params | Name                 | Description                                                  |
| ------ | ------ | -------------------- | ------------------------------------------------------------ |
| 01     | 3      | Add                  | arg[2] = arg[0] + arg[1]                                     |
| 02     | 3      | Multiplication       | arg[2] = arg[0] * arg[1]                                     |
| 03     | 1      | Input                | arg[0] = input                                               |
| 04     | 1      | Output               | output = arg[0]                                              |
| 05     | 2      | Jump non-zero        | If arg[0] is ≠ 0, sets the instruction pointer to arg[1]     |
| 06     | 2      | Jump zero            | If arg[0] == 0, sets the instruction pointer to arg[1]       |
| 07     | 3      | Less Than            | If the arg[0] < arg[1], sets arg[2] = 1. If not less, sets it to 0 |
| 08     | 3      | Equals               | If the arg[0] == arg[1], sets arg[2] = 1. If not equal, sets it to 0 |
| 09     | 1      | Add to relative base | relative base register += arg[0]                             |

### Parameter Modes

| Mode | Name           | Description                                                  |
| ---- | -------------- | ------------------------------------------------------------ |
| 0    | Position Mode  | The parameter is the address of the value.                   |
| 1    | Immediate Mode | The parameter is the value itself (Not used for writing).    |
| 2    | Relative Mode  | The parameter is added to the relative base register, which results in the memory address of the value. |

```bash
ABCDE
 1002

DE - two-digit opcode,      02 == opcode 2
 C - mode of 1st parameter,  0 == position mode
 B - mode of 2nd parameter,  1 == immediate mode
 A - mode of 3rd parameter,  0 == position mode,
                                  omitted due to being a leading zero
```
> From [adventofcode.com/2019/day/5](https://adventofcode.com/2019/day/5)
