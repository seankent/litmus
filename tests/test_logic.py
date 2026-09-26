###########
# imports #
###########
import pytest
from litmus.logic import Logic


##############
# test_parse #
##############
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
])
def test_parse(literal, binstr):
    assert Logic.parse(literal).binstr == binstr
