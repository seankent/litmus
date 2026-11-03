###########
# imports #
###########
import operator
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


#############
# test_bool #
#############
@pytest.mark.parametrize("binstr, expected", [
    ("0", False),
    ("1", True),
    ("00", False),
    ("01", True),
    ("10", True),
    ("11", True),
    ("00000000", False),
    ("00000001", True),
    ("10000000", True),
    ("x", False),
    ("z", False),
    ("xx", False),
    ("zz", False),
    ("xz", False),
    ("0x", False),
    ("0z", False),
    ("x0", False),
    ("x1", True),
    ("1x", True),
    ("1z", True),
    ("10x", True),
    ("x10", True),
])
def test_bool(binstr, expected):
    assert bool(Logic(binstr)) is expected


##############
# test_undef #
##############
@pytest.mark.parametrize("binstr, expected", [
    ("0", False),
    ("1", False),
    ("10101011", False),
    ("x", True),
    ("z", True),
    ("1x", True),
    ("1z", True),
    ("xz", True),
    ("0000000x", True),
    ("x0000000", True),
])
def test_undef(binstr, expected):
    assert Logic(binstr).undef() is expected


###########
# test_eq #
###########
@pytest.mark.parametrize("a, b, expected", [
    ("0", "0", True),
    ("1", "1", True),
    ("1010", "1010", True),
    ("10101011", "10101011", True),
    ("x", "x", True),
    ("z", "z", True),
    ("1x0z", "1x0z", True),
    ("0", "1", False),
    ("1010", "1011", False),
    ("x", "z", False),
    ("x", "0", False),
    ("x", "1", False),
    ("z", "0", False),
    ("1x", "11", False),
    ("1x", "1z", False),
])
def test_eq(a, b, expected):
    assert (Logic(a) == Logic(b)) is expected


##########################
# test_eq_width_mismatch #
##########################
@pytest.mark.parametrize("a, b", [
    ("0", "00"),
    ("1", "01"),
    ("x", "xx"),
    ("1010", "01010"),
    ("1010", "000001010"),
])
def test_eq_width_mismatch(a, b):
    assert (Logic(a) == Logic(b)) is False


#####################
# test_eq_non_logic #
#####################
@pytest.mark.parametrize("other", [
    "1'h1",
    "1",
    1,
    True,
    None,
    ["1"],
])
def test_eq_non_logic(other):
    assert (Logic("1") == other) is False


###########
# test_ne #
###########
@pytest.mark.parametrize("a, b, expected", [
    ("1010", "1010", False),
    ("x", "x", False),
    ("1010", "1011", True),
    ("1010", "01010", True),
])
def test_ne(a, b, expected):
    assert (Logic(a) != Logic(b)) is expected


##########################
# test_hash_equal_values #
##########################
@pytest.mark.parametrize("binstr", [
    "0",
    "1",
    "1010",
    "x",
    "1x0z",
])
def test_hash_equal_values(binstr):
    assert hash(Logic(binstr)) == hash(Logic(binstr))


####################
# test_hash_in_set #
####################
def test_hash_in_set():
    values = {Logic("1010"), Logic("1010"), Logic("1011")}

    assert len(values) == 2


#########################
# test_hash_as_dict_key #
#########################
def test_hash_as_dict_key():
    names = {Logic("1010"): "a", Logic("1011"): "b"}

    assert names[Logic("1010")] == "a"


############
# test_and #
############
@pytest.mark.parametrize("a, b, binstr", [
    ("0", "0", "0"),
    ("0", "1", "0"),
    ("0", "x", "0"),
    ("0", "z", "0"),
    ("1", "0", "0"),
    ("1", "1", "1"),
    ("1", "x", "x"),
    ("1", "z", "x"),
    ("x", "0", "0"),
    ("x", "1", "x"),
    ("x", "x", "x"),
    ("x", "z", "x"),
    ("z", "0", "0"),
    ("z", "1", "x"),
    ("z", "x", "x"),
    ("z", "z", "x"),
    ("1100", "1010", "1000"),
    ("11111111", "00000000", "00000000"),
    ("10x1", "1111", "10x1"),
    ("10z1", "0000", "0000"),
])
def test_and(a, b, binstr):
    assert (Logic(a) & Logic(b)).binstr == binstr


###########
# test_or #
###########
@pytest.mark.parametrize("a, b, binstr", [
    ("0", "0", "0"),
    ("0", "1", "1"),
    ("0", "x", "x"),
    ("0", "z", "x"),
    ("1", "0", "1"),
    ("1", "1", "1"),
    ("1", "x", "1"),
    ("1", "z", "1"),
    ("x", "0", "x"),
    ("x", "1", "1"),
    ("x", "x", "x"),
    ("x", "z", "x"),
    ("z", "0", "x"),
    ("z", "1", "1"),
    ("z", "x", "x"),
    ("z", "z", "x"),
    ("1100", "1010", "1110"),
    ("00000000", "00000000", "00000000"),
    ("10x1", "1111", "1111"),
    ("10z1", "0000", "10x1"),
])
def test_or(a, b, binstr):
    assert (Logic(a) | Logic(b)).binstr == binstr


############
# test_xor #
############
@pytest.mark.parametrize("a, b, binstr", [
    ("0", "0", "0"),
    ("0", "1", "1"),
    ("0", "x", "x"),
    ("0", "z", "x"),
    ("1", "0", "1"),
    ("1", "1", "0"),
    ("1", "x", "x"),
    ("1", "z", "x"),
    ("x", "0", "x"),
    ("x", "1", "x"),
    ("x", "x", "x"),
    ("x", "z", "x"),
    ("z", "0", "x"),
    ("z", "1", "x"),
    ("z", "x", "x"),
    ("z", "z", "x"),
    ("1100", "1010", "0110"),
    ("11111111", "11111111", "00000000"),
    ("10x1", "1111", "01x0"),
])
def test_xor(a, b, binstr):
    assert (Logic(a) ^ Logic(b)).binstr == binstr


###############
# test_invert #
###############
@pytest.mark.parametrize("binstr, expected", [
    ("0", "1"),
    ("1", "0"),
    ("x", "x"),
    ("z", "x"),
    ("1010", "0101"),
    ("00000000", "11111111"),
    ("10x1", "01x0"),
    ("10z1", "01x0"),
])
def test_invert(binstr, expected):
    assert (~Logic(binstr)).binstr == expected


###############################
# test_invert_z_is_not_cyclic #
###############################
def test_invert_z_is_not_cyclic():
    assert (~~Logic("z")).binstr == "x"


###############################
# test_bitwise_width_mismatch #
###############################
@pytest.mark.parametrize("op", [operator.and_, operator.or_, operator.xor])
@pytest.mark.parametrize("a, b", [
    ("0", "00"),
    ("1010", "01010"),
    ("10101011", "1010"),
])
def test_bitwise_width_mismatch(op, a, b):
    with pytest.raises(ValueError):
        op(Logic(a), Logic(b))


##########################
# test_bitwise_non_logic #
##########################
@pytest.mark.parametrize("op", [operator.and_, operator.or_, operator.xor])
@pytest.mark.parametrize("other", [
    "1010",
    "4'b1010",
    10,
    None,
])
def test_bitwise_non_logic(op, other):
    with pytest.raises(TypeError):
        op(Logic("1010"), other)


############
# test_hex #
############
@pytest.mark.parametrize("binstr, expected", [
    ("0", "1'h0"),
    ("1", "1'h1"),
    ("1010", "4'ha"),
    ("1111", "4'hf"),
    ("10101011", "8'hab"),
    ("00010001", "8'h11"),
    ("000000001010", "12'h00a"),
    ("10101", "5'h15"),
    ("101", "3'h5"),
    ("xxxx", "4'hx"),
    ("zzzz", "4'hz"),
    ("zzz1", "4'hx"),
    ("xxxz", "4'hx"),
    ("1x", "2'hx"),
    ("10x1", "4'hx"),
    ("1010xxxx", "8'hax"),
    ("xxxx1010", "8'hxa"),
    ("zzzz0001", "8'hz1"),
    ("0001zzzz", "8'h1z"),
])
def test_hex(binstr, expected):
    assert Logic(binstr).hex() == expected


############
# test_bin #
############
@pytest.mark.parametrize("binstr, expected", [
    ("0", "1'b0"),
    ("1", "1'b1"),
    ("1010", "4'b1010"),
    ("10101011", "8'b10101011"),
    ("10101", "5'b10101"),
    ("x", "1'bx"),
    ("z", "1'bz"),
    ("10x1", "4'b10x1"),
    ("1010xxxx", "8'b1010xxxx"),
    ("zzzz0001", "8'bzzzz0001"),
])
def test_bin(binstr, expected):
    assert Logic(binstr).bin() == expected


############
# test_dec #
############
@pytest.mark.parametrize("binstr, expected", [
    ("0", "1'd0"),
    ("1", "1'd1"),
    ("1010", "4'd10"),
    ("10101011", "8'd171"),
    ("11111111", "8'd255"),
    ("00000000", "8'd0"),
    ("10101", "5'd21"),
])
def test_dec(binstr, expected):
    assert Logic(binstr).dec() == expected


###################
# test_dec_raises #
###################
@pytest.mark.parametrize("binstr", [
    "x",
    "z",
    "10x1",
    "1010xxxx",
    "zzzz0001",
])
def test_dec_raises(binstr):
    with pytest.raises(ValueError):
        Logic(binstr).dec()


############
# test_int #
############
@pytest.mark.parametrize("binstr, expected", [
    ("0", 0),
    ("1", 1),
    ("1010", 10),
    ("10101011", 171),
    ("11111111", 255),
    ("00000000", 0),
    ("10101", 21),
    ("000000001010", 10),
])
def test_int(binstr, expected):
    assert int(Logic(binstr)) == expected


###################
# test_int_raises #
###################
@pytest.mark.parametrize("binstr", [
    "x",
    "z",
    "10x1",
    "1010xxxx",
    "zzzz0001",
])
def test_int_raises(binstr):
    with pytest.raises(ValueError):
        int(Logic(binstr))


############
# test_str #
############
@pytest.mark.parametrize("binstr, expected", [
    ("0", "1'b0"),
    ("10101011", "8'b10101011"),
    ("10x1", "4'b10x1"),
    ("1010xxxx", "8'b1010xxxx"),
    ("zzzz0001", "8'bzzzz0001"),
])
def test_str(binstr, expected):
    assert str(Logic(binstr)) == expected
    assert repr(Logic(binstr)) == expected


########################
# test_str_round_trips #
########################
@pytest.mark.parametrize("binstr", [
    "0",
    "1",
    "1010",
    "10101011",
    "10101",
    "x",
    "z",
    "10x1",
    "1010xxxx",
    "zzzz0001",
    "1x0z",
])
def test_str_round_trips(binstr):
    assert Logic.from_literal(str(Logic(binstr))).binstr == binstr


############
# test_len #
############
@pytest.mark.parametrize("binstr, expected", [
    ("0", 1),
    ("10", 2),
    ("1010", 4),
    ("10101011", 8),
    ("10101", 5),
    ("1010xxxxzzzz0000", 16),
])
def test_len(binstr, expected):
    assert len(Logic(binstr)) == expected


####################
# test_getitem_int #
####################
@pytest.mark.parametrize("binstr, index, expected", [
    ("1000", 3, "1"),
    ("1000", 2, "0"),
    ("1000", 1, "0"),
    ("1000", 0, "0"),
    ("0001", 0, "1"),
    ("1", 0, "1"),
    ("0", 0, "0"),
    ("10101011", 7, "1"),
    ("10101011", 6, "0"),
    ("10101011", 0, "1"),
    ("10x1", 1, "x"),
    ("10z1", 1, "z"),
    ("1x0z", 0, "z"),
    ("1x0z", 1, "0"),
    ("1x0z", 2, "x"),
    ("1x0z", 3, "1"),
])
def test_getitem_int(binstr, index, expected):
    assert Logic(binstr)[index].binstr == expected


###########################
# test_getitem_int_raises #
###########################
@pytest.mark.parametrize("binstr, index", [
    ("1010", 4),
    ("1010", 10),
    ("1", 1),
])
def test_getitem_int_raises(binstr, index):
    with pytest.raises(IndexError):
        Logic(binstr)[index]


####################################
# test_getitem_negative_int_raises #
####################################
@pytest.mark.parametrize("binstr, index", [
    ("1010", -1),
    ("1010", -4),
    ("1010", -10),
    ("10101011", -1),
    ("1", -1),
])
def test_getitem_negative_int_raises(binstr, index):
    with pytest.raises(IndexError, match = "Bit index"):
        Logic(binstr)[index]


######################
# test_getitem_slice #
######################
@pytest.mark.parametrize("binstr, start, stop, expected", [
    ("10101011", 7, 4, "1010"),
    ("10101011", 3, 0, "1011"),
    ("10101011", 7, 0, "10101011"),
    ("10101011", 5, 2, "1010"),
    ("10101011", 7, 7, "1"),
    ("10101011", 0, 0, "1"),
    ("1010", 2, 1, "01"),
    ("1x0z", 3, 2, "1x"),
    ("1x0z", 1, 0, "0z"),
])
def test_getitem_slice(binstr, start, stop, expected):
    assert Logic(binstr)[start:stop].binstr == expected


###################################
# test_getitem_slice_is_inclusive #
###################################
@pytest.mark.parametrize("start, stop, width", [
    (7, 0, 8),
    (7, 4, 4),
    (3, 0, 4),
    (5, 2, 4),
    (7, 7, 1),
    (0, 0, 1),
])
def test_getitem_slice_is_inclusive(start, stop, width):
    assert len(Logic("10101011")[start:stop]) == width


#############################
# test_getitem_slice_bounds #
#############################
@pytest.mark.parametrize("binstr, index, expected", [
    ("10101011", slice(None, None), "10101011"),
    ("10101011", slice(7, None), "10101011"),
    ("10101011", slice(None, 0), "10101011"),
    ("10101011", slice(3, None), "1011"),
    ("10101011", slice(None, 4), "1010"),
    ("1010", slice(None, None), "1010"),
    ("1", slice(None, None), "1"),
    ("1x0z", slice(None, None), "1x0z"),
    ("1x0z", slice(None, 2), "1x"),
    ("1x0z", slice(1, None), "0z"),
])
def test_getitem_slice_bounds(binstr, index, expected):
    assert Logic(binstr)[index].binstr == expected


###################################
# test_getitem_slice_value_raises #
###################################
@pytest.mark.parametrize("index", [
    slice(7, 4, 1),
    slice(7, 4, 2),
    slice(None, None, 1),
    slice(4, 7),
    slice(0, 1),
    slice(0, 7),
])
def test_getitem_slice_value_raises(index):
    with pytest.raises(ValueError):
        Logic("10101011")[index]


###################################
# test_getitem_slice_index_raises #
###################################
@pytest.mark.parametrize("binstr, index", [
    ("10101011", slice(8, 0)),
    ("10101011", slice(10, 0)),
    ("10101011", slice(3, -1)),
    ("1010", slice(4, 0)),
    ("1010", slice(4, None)),
])
def test_getitem_slice_index_raises(binstr, index):
    with pytest.raises(IndexError):
        Logic(binstr)[index]


############################
# test_getitem_type_raises #
############################
@pytest.mark.parametrize("index", [
    "0",
    "7:4",
    1.0,
    None,
    (1, 0),
    [1, 0],
])
def test_getitem_type_raises(index):
    with pytest.raises(TypeError):
        Logic("10101011")[index]


############
# test_add #
############
@pytest.mark.parametrize("a, b, expected", [
    ("0000", "0000", "0000"),
    ("0001", "0001", "0010"),
    ("1010", "0101", "1111"),
    ("0", "1", "1"),
    ("00000001", "00000001", "00000010"),
    ("00001111", "00000001", "00010000"),
    ("10101011", "00000001", "10101100"),
    ("1", "1", "0"),
    ("1111", "0001", "0000"),
    ("1000", "1000", "0000"),
    ("11111111", "00000001", "00000000"),
    ("11111111", "11111111", "11111110"),
])
def test_add(a, b, expected):
    assert (Logic(a) + Logic(b)).binstr == expected


############
# test_sub #
############
@pytest.mark.parametrize("a, b, expected", [
    ("0000", "0000", "0000"),
    ("0010", "0001", "0001"),
    ("1111", "0001", "1110"),
    ("1", "1", "0"),
    ("10101011", "00000001", "10101010"),
    ("10000000", "00000001", "01111111"),
    ("0", "1", "1"),
    ("0000", "0001", "1111"),
    ("00000000", "00000001", "11111111"),
    ("00000001", "00000010", "11111111"),
])
def test_sub(a, b, expected):
    assert (Logic(a) - Logic(b)).binstr == expected


#########################
# test_arithmetic_undef #
#########################
@pytest.mark.parametrize("op", [operator.add, operator.sub])
@pytest.mark.parametrize("a, b, expected", [
    ("000x", "0000", "xxxx"),
    ("0000", "000x", "xxxx"),
    ("x000", "0000", "xxxx"),
    ("000z", "0000", "xxxx"),
    ("0000", "000z", "xxxx"),
    ("xxxx", "xxxx", "xxxx"),
    ("1x1x", "0101", "xxxx"),
    ("x", "0", "x"),
    ("0", "x", "x"),
    ("z", "1", "x"),
])
def test_arithmetic_undef(op, a, b, expected):
    assert op(Logic(a), Logic(b)).binstr == expected


##################################
# test_arithmetic_width_mismatch #
##################################
@pytest.mark.parametrize("op", [operator.add, operator.sub])
@pytest.mark.parametrize("a, b", [
    ("0", "00"),
    ("1010", "01010"),
    ("10101011", "1010"),
])
def test_arithmetic_width_mismatch(op, a, b):
    with pytest.raises(ValueError):
        op(Logic(a), Logic(b))


#############################
# test_arithmetic_non_logic #
#############################
@pytest.mark.parametrize("op", [operator.add, operator.sub])
@pytest.mark.parametrize("other", [
    "1010",
    "4'b1010",
    10,
    None,
])
def test_arithmetic_non_logic(op, other):
    with pytest.raises(TypeError):
        op(Logic("1010"), other)


############################
# test_add_sub_are_inverse #
############################
@pytest.mark.parametrize("a, b", [
    ("00000000", "00000001"),
    ("10101011", "01010101"),
    ("11111111", "11111111"),
    ("1010", "0011"),
    ("1", "1"),
])
def test_add_sub_are_inverse(a, b):
    assert ((Logic(a) + Logic(b)) - Logic(b)).binstr == a


###############
# test_extend #
###############
@pytest.mark.parametrize("binstr, width, expected", [
    ("0", 1, "0"),
    ("1", 1, "1"),
    ("1010", 4, "1010"),
    ("11111111", 8, "11111111"),
    ("0", 4, "0000"),
    ("1", 4, "0001"),
    ("1", 8, "00000001"),
    ("1010", 8, "00001010"),
    ("1010", 16, "0000000000001010"),
    ("x", 4, "000x"),
    ("z", 4, "000z"),
    ("xxxx", 8, "0000xxxx"),
    ("10x1", 8, "000010x1"),
    ("1x0z", 8, "00001x0z"),
])
def test_extend(binstr, width, expected):
    assert Logic(binstr).extend(width).binstr == expected


#############################
# test_extend_is_not_signed #
#############################
@pytest.mark.parametrize("binstr, width, expected", [
    ("1", 4, "0001"),
    ("1111", 8, "00001111"),
    ("10000000", 16, "0000000010000000"),
])
def test_extend_is_not_signed(binstr, width, expected):
    assert Logic(binstr).extend(width).binstr == expected


#####################
# test_extend_width #
#####################
@pytest.mark.parametrize("binstr, width", [
    ("1", 1),
    ("1", 32),
    ("1010", 8),
    ("10x1", 16),
])
def test_extend_width(binstr, width):
    assert len(Logic(binstr).extend(width)) == width


######################
# test_extend_raises #
######################
@pytest.mark.parametrize("binstr, width", [
    ("1010", 3),
    ("1010", 1),
    ("1010", 0),
    ("1010", -1),
    ("1", 0),
    ("10101011", 4),
])
def test_extend_raises(binstr, width):
    with pytest.raises(ValueError):
        Logic(binstr).extend(width)


#############
# test_init #
#############
@pytest.mark.parametrize("binstr", [
    "0",
    "1",
    "x",
    "z",
    "1010",
    "10101011",
    "1x0z",
    "xxxx",
    "zzzz",
    "0101010101010101",
])
def test_init(binstr):
    assert Logic(binstr).binstr == binstr


####################
# test_init_raises #
####################
@pytest.mark.parametrize("binstr", [
    "",
    "2",
    "9",
    "X",
    "Z",
    "10X1",
    "10Z1",
    "XXXX",
    "1X0Z",
    "1010XXXX",
    "1 0",
    "0b1010",
    "4'b1010",
    "abc",
    "10-1",
    "1.0",
    "1_0",
])
def test_init_raises(binstr):
    with pytest.raises(ValueError):
        Logic(binstr)


#########################
# test_init_type_raises #
#########################
@pytest.mark.parametrize("binstr", [
    1010,
    1.0,
    True,
    None,
    ["1", "0"],
    Logic("1010"),
])
def test_init_type_raises(binstr):
    with pytest.raises(TypeError):
        Logic(binstr)
