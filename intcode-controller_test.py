from intcode_controller import *


def test_program_from_text():
    # Normal text
    out = Program.from_text("1,2,3,4")
    assert out == [1, 2, 3, 4]

    # Text with newlines
    out = Program.from_text("1,2,\n\n3,4")
    assert out == [1, 2, 3, 4]

    # Text with multiple commas
    out = Program.from_text("1,2,,,3,,4")
    assert out == [1, 2, 3, 4]

    # Text with newlines and multiple commas
    out = Program.from_text("1,2,\n,,\n,3,4")
    assert out == [1, 2, 3, 4]

    # Text with newlines, multiple commas and spaces
    out = Program.from_text("1  2,\n,,\n,3, 4")
    assert out == [1, 2, 3, 4]

    # Text with newlines, multiple commas, spaces and comments
    out = Program.from_text("1  2,\n# Comment,\n\n,3, 4")
    assert out == [1, 2, 3, 4]

    # Text with newlines, multiple commas, spaces and comments at beginning
    out = Program.from_text("#Comment at begin\n1  2,\n# Comment,\n\n,3, 4")
    assert out == [1, 2, 3, 4]


def test_program_getitem():
    program = Program([1, 2, 3, 4])
    # Normal get
    assert 1 == program[0]
    assert 4 == program[3]
    assert 0 == program[4]

    # Expecting automatic extending with default value 0
    assert 0 == program[42]


def test_program_setitem():
    program = Program([1, 2, 3, 4])
    # Normal set
    program[0] = 42
    assert 42 == program[0]

    # Expecting automatic extending
    program[42] = 1337
    assert 1337 == program[42]


def test_program_exec():
    program = Program([1, 2, 3, 4])
    # Normal get
    out = program.exec(['GET', '0'])
    assert out == 1

    # Normal set
    program.exec(['SET', '0', '42'])
    out = program.exec(['GET', '0'])
    assert out == 42

    # Get with automatic extending with default value 0
    out = program.exec(['GET', '20'])
    assert out == 0

    # Set with automatic extending
    program.exec(['SET', '42', '1337'])
    out = program.exec(['GET', '42'])
    assert out == 1337
