# intcode-arduino

# Usage

## Arduino

Copy the [`intcode.ino`](https://github.com/linus-k519/intcode-arduino/blob/main/intcode.ino) file into the [Arduino IDE](https://www.arduino.cc/en/software) and upload it to the Arduino via the `⇨` Button.

```cpp
long long x = 12345678901234LL;
Serial.print((long) (x / 1000000000L % 1000000000L));
Serial.println((long) (x % 1000000000L));
```

## Intcode Language Specifications

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

> From [esolangs.org/wiki/Intcode](https://esolangs.org/wiki/Intcode)

### Parameter Modes

| Mode | Name           | Description                                                  |
| ---- | -------------- | ------------------------------------------------------------ |
| 0    | Position Mode  | The parameter is the address of the value.                   |
| 1    | Immediate Mode | The parameter is the value itself (Not used for writing).    |
| 2    | Relative Mode  | The parameter is added to the relative base register, which results in the memory address of the value. |

> From [esolangs.org/wiki/Intcode](https://esolangs.org/wiki/Intcode)


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

