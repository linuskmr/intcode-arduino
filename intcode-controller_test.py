import intcode_controller


def test_str_to_comma_separated():
    out = intcode_controller.str_to_comma_separated("1,2,3,4")
    assert out == [1, 2, 3, 4]

    out = intcode_controller.str_to_comma_separated("1,2,\n\n3,4")
    assert out == [1, 2, 3, 4]

    out = intcode_controller.str_to_comma_separated("1,2,,,3,,4")
    assert out == [1, 2, 3, 4]

    out = intcode_controller.str_to_comma_separated("1,2,\n,,\n,3,4")
    assert out == [1, 2, 3, 4]

    out = intcode_controller.str_to_comma_separated("1  2,\n,,\n,3, 4")
    assert out == [1, 2, 3, 4]

    out = intcode_controller.str_to_comma_separated("1  2,\n# Comment,\n\n,3, 4")
    assert out == [1, 2, 3, 4]

    out = intcode_controller.str_to_comma_separated("#Comment at begin\n1  2,\n# Comment,\n\n,3, 4")
    assert out == [1, 2, 3, 4]
