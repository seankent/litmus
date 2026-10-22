###########
# imports #
###########
import pytest
from litmus.logic import Logic


#####################
# test_from_literal #
#####################
@pytest.mark.parametrize("literal, binstr", [
    ("4'b1010", "1010"),
    ("8'b10101011", "10101011"),
    ("8'hab", "10101011"),
    ("8'hAB", "10101011"),
    ("8'h11", "00010001"),
    ("8'd5", "00000101"),
    ("8'd42", "00101010"),
    ("16'b1000_1101_0011_1010", "1000110100111010"),
    ("5'b10101", "10101"),
    ("4'b10", "0010"),
    ("8'hx", "xxxxxxxx"),
    ("8'hz", "zzzzzzzz"),
    ("8'bx1", "xxxxxxx1"),
    ("8'h1x", "0001xxxx"),
    ("8'b1x", "0000001x"),
    ("12'hz1f", "zzzz00011111"),
    ("1'h0", "0"),
    ("1'h1", "1"),
    ("2'h0", "00"),
    ("2'h2", "10"),
    ("2'h3", "11"),
    ("3'h7", "111"),
    ("6'h3f", "111111"),
    ("2'hx", "xx"),
    ("2'hz", "zz"),
    ("4'hx1", "0001"),
    ("2'b000", "00"),
    ("2'bxxx", "xx"),
    ("4'b00001010", "1010"),
])
def test_from_literal(literal, binstr):
    assert Logic.from_literal(literal).binstr == binstr


############################
# test_from_literal_raises #
############################
@pytest.mark.parametrize("literal", [
    ("1'h2"),
    ("2'h4"),
    ("2'h7"),
    ("4'hab"),
    ("2'b111"),
    ("4'b10101"),
    ("2'd7"),
    ("8'habc"),
    ("0'h0"),
    ("8'q11"),
    ("abc"),
    ("8'h"),
])
def test_from_literal_raises(literal):
    with pytest.raises(ValueError):
        Logic.from_literal(literal)


#################
# test_from_int #
#################
@pytest.mark.parametrize("value, width, binstr", [
    (0, 8, "00000000"),
    (5, 8, "00000101"),
    (171, 8, "10101011"),
    (255, 8, "11111111"),
    (-1, 8, "11111111"),
    (-128, 8, "10000000"),
    (1, 1, "1"),
    (10, 4, "1010"),
    (65535, 16, "1111111111111111"),
])
def test_from_int(value, width, binstr):
    assert Logic.from_int(value, width).binstr == binstr


########################
# test_from_int_raises #
########################
@pytest.mark.parametrize("value, width", [
    (256, 8),
    (-129, 8),
    (2, 1),
])
def test_from_int_raises(value, width):
    with pytest.raises(ValueError):
        Logic.from_int(value, width)
