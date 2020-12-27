# intcode-arduino

This is an Intcode interpreter that runs on an Arduino.
The code was developed on an Arduino Uno with an ATmega328P microcontroller.

The Intcode programming language was created in the [Advent of Code 2019](https://www.adventofcode.com/2019). For details on the language, see the [Intcode Language Specifications](#intcode-language-specifications) below.

## Installation

The software consists of two parts: On the one hand, the actual Intcode interpreter, which runs on the Arduino. On the other hand, a control and memory unit in form of a Python script. See [Implementation Details](#implementation-details) below for more information.

### Arduino

Copy or open the [`intcode-arduino.ino`](https://github.com/linus-k519/intcode-arduino/blob/main/intcode-arduino.ino) file in the [Arduino IDE](https://www.arduino.cc/en/software) and upload it to the Arduino via the ➡️ button.

### Python

After the software is running on the Arduino, the Python script can be started.

```bash
./intcode-controller.py examples/day9_1.ic
```

## Implementation Details

The Arduino does not have enough SRAM to hold a large Intcode program completely in memory. For example, the program of [Day 9 of Advent of Code 2019](https://adventofcode.com/2019/day/9) has over 950x `int64`s, resulting in a total of 7.6 KB with the available memory on my Arduino being just 2KB.

That is why a Python script acts as an external storage medium. It loads a program from a file on the computer (which hopefully has more than 7.6 KB of RAM 😉) and makes the integers available one by one via the serial interface. The Arduino can read or write the value of a memory address. In addition, the input and output instructions are passed via the serial interface and the Python script to the user.
The commands that the Arduino and the computer use to communicate consist of a list of values separated by spaces. All numbers are written in the decimal system. The zeroth argument is the type of the command, followed by the corresponding arguments for that operation. Below are a few examples:

```
Arduino: GET <address>
Python: <value>

Arduino: SET <address> <value>
Python: (No response)

Arduino: INPUT
Python: <value> (Asks user for input and responses with the value)

Arduino: OUTPUT <value>
Python: (No response, but prints value to stdout)

Arduino: HALT
Python: (No response, but ends the program)

Arduino: INFO InstructionCountCurrent 42
Python: (No response, but prints it to stdout)
```

At a baud rate of 115200, I achieve a performance of breathtaking 37 instructions per second with my Arduino Uno.

In the second part of [Day 9 from Advent of Code 2019](https://adventofcode.com/2019/day/9) over 370000 instructions have to be executed for completing the task. This results in a computing time of just under 3 hours 🎉.

## Intcode Language Specifications

The Intcode programming language was created in the [Advent of Code 2019](adventofcode.com/2019).
The characteristic of the language is that it only consists of integers (`int64`s to be exact). An instruction consists of an operation code, or [opcode](#opcodes) for short, and arguments. The number of arguments depends on the opcode.

### Opcodes

An opcode (operation code) is a 2-digit number indicating which instruction should be performed. If no [parameter modes](#parameter-modes) are specified, the leading 0 can also be omitted.

| Opcode | Params | Name                 | Description                                                  |
| ------ | ------ | -------------------- | ------------------------------------------------------------ |
| 01     | 3      | Addition             | arg[2] = arg[0] + arg[1]                                     |
| 02     | 3      | Multiplication       | arg[2] = arg[0] * arg[1]                                     |
| 03     | 1      | Input                | arg[0] = input                                               |
| 04     | 1      | Output               | output = arg[0]                                              |
| 05     | 2      | Jump non-zero        | If arg[0] is ≠ 0, sets the instruction pointer to arg[1]     |
| 06     | 2      | Jump zero            | If arg[0] == 0, sets the instruction pointer to arg[1]       |
| 07     | 3      | Less Than            | If arg[0] < arg[1], sets arg[2] = 1. If not less, sets it to 0 |
| 08     | 3      | Equals               | If arg[0] == arg[1], sets arg[2] = 1. If not equal, sets it to 0 |
| 09     | 1      | Add to relative base | relative base register += arg[0]                             |

### Parameter Modes

As you can guess from the name: The parameter mode sets the mode for each parameter. This means that a parameter following an [opcode](#opcodes) may be a reference to a memory address, or may be the value itself with which the operation is to be performed. For each parameter belonging to an opcode, the mode can be different. The modes are appended to the 2-digit [opcode](#opcodes) on the left and are in reversed order to the parameters. Why in reverse 🤷? Good question. I didn't make it up.

Because the integers are stored in an array, the first memory address is `0` and negative memory addresses are invalid. A memory address beyond the program length is valid. Thus memory can be occupied dynamically at runtime of the program by enlarging the array accordingly. A possibility to release this memory during runtime does not exist according to the specifications currently.

The relative base register is initiated with the value `0` at program start and can be changed by [opcode](#opcodes) `09`.

| Mode | Name           | Description                                                  |
| ---- | -------------- | ------------------------------------------------------------ |
| 0    | Position Mode  | The parameter is the address of the value.                   |
| 1    | Immediate Mode | The parameter is the value itself (Not used for writing).    |
| 2    | Relative Mode  | The parameter is added to the relative base register, which results in the memory address of the value. |

Below is an example showing how the parameter modes work:

```bash
ABCDE
 1002

DE - two-digit opcode:		02 == opcode 02
 C - mode of 1st parameter:	 0 == position mode
 B - mode of 2nd parameter:	 1 == immediate mode
 A - mode of 3rd parameter:	 0 == position mode,
 								  omitted due to being a leading zero
```
> From [adventofcode.com/2019/day/5](https://adventofcode.com/2019/day/5)

### Examples

All examples can be found in the `examples/` directory.

#### `addition.ic`

This program adds 5 and 8 and outputs the result.

```python
# Addition (everything in immediate mode) from 5+8 and overwrite 42 with the result
11101, 5, 8, 42,

# Output (implicit position mode) from position 3, so the result of 5+8
4, 3,

# End program
99
```

#### `count.ic`

This program shows a simple counting loop outputting the values from `0` to `9`.

```python
# Output value at position 42 (Implicit value 0 at the beginning)
4,42

# Increment value at position 42 by one and save it to position 42
1001,42,1,42

# If (value at position 42) < 10, set value of position 43 to zero
1007,42,10,43

# Jump to begin of program, if value of position 43 is non-zero
1005,43,0

# End program
99
```
