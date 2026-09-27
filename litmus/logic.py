###########
# imports #
###########
import re

#########
# Logic #
#########
class Logic:

    ############
    # __init__ #
    ############
    def __init__(self, binstr):
        """
        Constructs a Logic from a binary string.

        Args:
            binstr (str): The value as a string of 0, 1, x and z, e.g. "10xz".
        """
        if not re.fullmatch(r"[01xz]+", binstr):
            raise ValueError(f"Invalid binstr: '{binstr}'")

        self.binstr = binstr

    ###########
    # __len__ #
    ###########
    def __len__(self):
        """
        Returns the width in bits.

        Returns:
            int: The width in bits.
        """
        return len(self.binstr)

    #########
    # undef #
    #########
    def undef(self):
        """
        Returns True if the value contains x or z.

        Returns:
            bool: True if the value contains x or z.
        """
        if "x" in self.binstr or "z" in self.binstr:
            return True
        else:
            return False

    ############
    # __bool__ #
    ############
    def __bool__(self):
        """
        Returns True if any bit is 1 and the value is defined.

        Returns:
            bool: True if any bit is 1 and the value is defined.
        """
        if "1" in self.binstr and not self.undef():
            return True
        else:
            return False

    ###########
    # __int__ #
    ###########
    def __int__(self):
        """
        Returns the unsigned integer value.

        Returns:
            int: The unsigned integer value.
        """
        if self.undef():
            raise ValueError(f"Cannot convert '{self.binstr}' to int: contains x or z.")

        return int(self.binstr, base = 2)

    #######
    # hex #
    #######
    def hex(self):
        """
        Returns the hex literal, e.g. 8'hab.

        Returns:
            str: The hex literal. A nibble renders as z if all four bits are z,
                or x if any bit is undefined.
        """
        txt = ""

        for i in range(len(self) - 1, -1, -4):
            nibble = self.binstr[max(i - 3, 0):i + 1]

            if nibble == "z"*len(nibble):
                txt = "z" + txt
            elif "x" in nibble or "z" in nibble:
                txt = "x" + txt
            else:
                txt = hex(int(nibble, base = 2))[2:] + txt

        return f"{len(self)}'h" + txt

    #######
    # bin #
    #######
    def bin(self):
        """
        Returns the binary literal, e.g. 8'b10101011.

        Returns:
            str: The binary literal.
        """
        return f"{len(self)}'b" + self.binstr

    #######
    # dec #
    #######
    def dec(self):
        """
        Returns the decimal literal, e.g. 8'd171.

        Returns:
            str: The decimal literal.
        """
        if self.undef():
            raise ValueError(f"Cannot convert '{self.binstr}' to decimal: contains x or z.")

        return f"{len(self)}'d{int(self)}"

    ###########
    # __str__ #
    ###########
    def __str__(self):
        """
        Returns the hex literal, e.g. 8'hab.

        Returns:
            str: The hex literal.
        """
        return self.hex()

    ############
    # __repr__ #
    ############
    def __repr__(self):
        """
        Returns the hex literal, e.g. 8'hab.

        Returns:
            str: The hex literal, which is lossy for x and z.
        """
        return self.hex()

    ############
    # __hash__ #
    ############
    def __hash__(self):
        """
        Returns the hash of the binary string.

        Returns:
            int: The hash of the binary string.
        """
        return hash(self.binstr)

    ##########
    # __eq__ #
    ##########
    def __eq__(self, other):
        """
        Returns True if both values have the same width and bits.

        Args:
            other (Logic): The value to compare against.

        Returns:
            bool: True if both values have the same width and bits.
        """
        if not isinstance(other, Logic):
            return NotImplemented
        elif self.binstr == other.binstr:
            return True
        else:
            return False

    ###############
    # __getitem__ #
    ###############
    def __getitem__(self, index):
        """
        Returns a bit or a range of bits.

        Args:
            index (int | slice): A bit position or an inclusive descending slice, e.g. value[7:4].

        Returns:
            Logic: The selected bits.
        """
        if isinstance(index, int):

            if index < 0 or index >= len(self):
                raise IndexError(f"Bit index {index} out of range for width {len(self)}.")

            return Logic(self.binstr[len(self) - index - 1])

        elif isinstance(index, slice):

            if index.step is not None:
                raise ValueError("Bit slices do not support a step.")

            if index.start is None or index.stop is None:
                raise ValueError("Bit slices require explicit bounds, e.g. value[7:4].")

            if index.start < index.stop:
                raise ValueError(f"Bit slice [{index.start}:{index.stop}] must be descending.")

            if index.stop < 0 or index.start >= len(self):
                raise IndexError(f"Bit slice [{index.start}:{index.stop}] out of range for width {len(self)}.")

            return Logic(self.binstr[len(self) - index.start - 1:len(self) - index.stop])

        else:
            raise TypeError(f"Invalid index type: {type(index).__name__}")

    ##########
    # extend #
    ##########
    def extend(self, width):
        """
        Returns the value zero-extended to a wider width.

        Args:
            width (int): The result width, which must be at least the current width.

        Returns:
            Logic: The zero-extended value.
        """
        if width < len(self):
            raise ValueError(f"Cannot extend width {len(self)} to {width}.")

        return Logic(self.binstr.zfill(width))

    ###########
    # __and__ #
    ###########
    def __and__(self, other):
        """
        Returns the bitwise AND.

        Args:
            other (Logic): Operand of the same width.

        Returns:
            Logic: The bitwise AND, with x wherever the result is undefined.
        """
        if not isinstance(other, Logic):
            return NotImplemented

        if len(self) != len(other):
            raise ValueError(f"Width mismatch: {len(self)} and {len(other)}.")

        binstr = ""

        for a, b in zip(self.binstr, other.binstr):
            if a == "0" or b == "0":
                binstr += "0"
            elif a == "1" and b == "1":
                binstr += "1"
            else:
                binstr += "x"

        return Logic(binstr)

    ##########
    # __or__ #
    ##########
    def __or__(self, other):
        """
        Returns the bitwise OR.

        Args:
            other (Logic): Operand of the same width.

        Returns:
            Logic: The bitwise OR, with x wherever the result is undefined.
        """
        if not isinstance(other, Logic):
            return NotImplemented

        if len(self) != len(other):
            raise ValueError(f"Width mismatch: {len(self)} and {len(other)}.")

        binstr = ""

        for a, b in zip(self.binstr, other.binstr):
            if a == "1" or b == "1":
                binstr += "1"
            elif a == "0" and b == "0":
                binstr += "0"
            else:
                binstr += "x"

        return Logic(binstr)

    ###########
    # __xor__ #
    ###########
    def __xor__(self, other):
        """
        Returns the bitwise XOR.

        Args:
            other (Logic): Operand of the same width.

        Returns:
            Logic: The bitwise XOR, with x wherever either operand is undefined.
        """
        if not isinstance(other, Logic):
            return NotImplemented

        if len(self) != len(other):
            raise ValueError(f"Width mismatch: {len(self)} and {len(other)}.")

        binstr = ""

        for a, b in zip(self.binstr, other.binstr):
            if a in {"x", "z"} or b in {"x", "z"}:
                binstr += "x"
            elif a == b:
                binstr += "0"
            else:
                binstr += "1"

        return Logic(binstr)

    ##############
    # __invert__ #
    ##############
    def __invert__(self):
        """
        Returns the bitwise NOT.

        Returns:
            Logic: The bitwise NOT, with x wherever the operand is undefined.
        """
        binstr = ""

        for a in self.binstr:
            if a == "0":
                binstr += "1"
            elif a == "1":
                binstr += "0"
            else:
                binstr += "x"

        return Logic(binstr)

    ###########
    # __add__ #
    ###########
    def __add__(self, other):
        """
        Returns the sum, wrapping on overflow.

        Args:
            other (Logic): Operand of the same width.

        Returns:
            Logic: The sum, or all x if either operand is undefined.
        """
        if not isinstance(other, Logic):
            return NotImplemented

        if len(self) != len(other):
            raise ValueError(f"Width mismatch: {len(self)} and {len(other)}.")

        if self.undef() or other.undef():
            return Logic("x"*len(self))

        binstr = bin((int(self) + int(other)) % (2**len(self)))[2:].zfill(len(self))

        return Logic(binstr)

    ###########
    # __sub__ #
    ###########
    def __sub__(self, other):
        """
        Returns the difference, wrapping on underflow.

        Args:
            other (Logic): Operand of the same width.

        Returns:
            Logic: The difference, or all x if either operand is undefined.
        """
        if not isinstance(other, Logic):
            return NotImplemented

        if len(self) != len(other):
            raise ValueError(f"Width mismatch: {len(self)} and {len(other)}.")

        if self.undef() or other.undef():
            return Logic("x"*len(self))

        binstr = bin((int(self) - int(other)) % (2**len(self)))[2:].zfill(len(self))

        return Logic(binstr)

    ################
    # from_literal #
    ################
    @classmethod
    def from_literal(cls, literal):
        """
        Returns a Logic parsed from a Verilog literal, e.g. 8'hab.

        Args:
            literal (str): A sized binary, hex or decimal literal, e.g. 8'b1010_1011,
                8'hab or 8'd171. Case and underscores are ignored.

        Returns:
            Logic: The parsed value, zero-extended to the declared width, or
                x/z-extended if the leading digit is x or z.
        """
        literal = literal.lower()
        literal = literal.replace("_", "")

        mo = re.fullmatch(r"([0-9]+)'b([01xz]+)", literal)
        if mo:

            width = int(mo.group(1))
            digits = mo.group(2)

            binstr = digits
            if binstr[0] in {"x", "z"}:
                binstr = binstr[0]*(width - len(binstr)) + binstr
            else:
                binstr = binstr.zfill(width)

            if len(binstr) > width:
                raise ValueError(f"Literal '{literal}' wider than declared width {width}.")

            return cls(binstr)

        mo = re.fullmatch(r"([0-9]+)'h([0-9a-fxz]+)", literal)
        if mo:

            width = int(mo.group(1))
            digits = mo.group(2)

            binstr = ""

            for digit in reversed(digits):
                if digit in {"x", "z"}:
                    binstr = digit*4 + binstr
                else:
                    binstr = bin(int(digit, base = 16))[2:].zfill(4) + binstr

            if binstr[0] in {"x", "z"}:
                binstr = binstr[0]*(width - len(binstr)) + binstr
            else:
                binstr = binstr.zfill(width)

            if len(binstr) > width:
                raise ValueError(f"Literal '{literal}' wider than declared width {width}.")

            return cls(binstr)

        mo = re.fullmatch(r"([0-9]+)'d([0-9]+)", literal)
        if mo:

            width = int(mo.group(1))
            digits = mo.group(2)

            binstr = bin(int(digits, base = 10))[2:]
            binstr = binstr.zfill(width)

            if len(binstr) > width:
                raise ValueError(f"Literal '{literal}' wider than declared width {width}.")

            return cls(binstr)

        raise ValueError(f"Cannot parse Logic value: '{literal}'")

    ############
    # from_int #
    ############
    @classmethod
    def from_int(cls, value, width):
        """
        Returns a Logic from an integer, e.g. Logic.from_int(171, 8).

        Args:
            value (int): The value, with negative values encoded as two's complement.
            width (int): The result width, which must be wide enough to hold the value.

        Returns:
            Logic: The value as a binary string of the given width.
        """
        if value < -(2**(width - 1)) or value >= 2**width:
            raise ValueError(f"Value {value} does not fit in width {width}.")

        if value < 0:
            value += 2**width

        return cls(bin(value)[2:].zfill(width))
