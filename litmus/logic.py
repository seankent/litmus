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
        """
        if not re.fullmatch(r"[01xz]+", binstr):
            raise ValueError(f"Invalid binstr: '{binstr}'")

        self.binstr = binstr

    ###########
    # __len__ #
    ###########
    def __len__(self):
        """
        """
        return len(self.binstr)

    #########
    # undef #
    #########
    def undef(self):
        """
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
        """
        if self.undef():
            raise ValueError(f"Cannot convert '{self.binstr}' to int: contains x or z.")

        return int(self.binstr, base = 2)

    #######
    # hex #
    #######
    def hex(self):
        """
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
        """
        return f"{len(self)}'b" + self.binstr

    #######
    # dec #
    #######
    def dec(self):
        """
        """
        if self.undef():
            raise ValueError(f"Cannot convert '{self.binstr}' to decimal: contains x or z.")

        return f"{len(self)}'d{int(self)}"

    ###########
    # __str__ #
    ###########
    def __str__(self):
        """
        """
        return self.bin()

    ############
    # __repr__ #
    ############
    def __repr__(self):
        """
        """
        return f'Logic("{self.binstr}")'

    ############
    # __hash__ #
    ############
    def __hash__(self):
        """
        """
        return hash(self.binstr)

    ##########
    # __eq__ #
    ##########
    def __eq__(self, other):
        """
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
        """
        if width < len(self):
            raise ValueError(f"Cannot extend width {len(self)} to {width}.")

        return Logic(self.binstr.zfill(width))

    ###########
    # __and__ #
    ###########
    def __and__(self, other):
        """
        """
        if not isinstance(other, Logic):
            return NotImplemented

        if len(self) != len(other):
            raise ValueError(f"Width mismatch: {len(self)} and {len(other)}.")

        result = ""

        for a, b in zip(self.binstr, other.binstr):
            if a == "0" or b == "0":
                result += "0"
            elif a == "1" and b == "1":
                result += "1"
            else:
                result += "x"

        return Logic(result)

    ##########
    # __or__ #
    ##########
    def __or__(self, other):
        """
        """
        if not isinstance(other, Logic):
            return NotImplemented

        if len(self) != len(other):
            raise ValueError(f"Width mismatch: {len(self)} and {len(other)}.")

        result = ""

        for a, b in zip(self.binstr, other.binstr):
            if a == "1" or b == "1":
                result += "1"
            elif a == "0" and b == "0":
                result += "0"
            else:
                result += "x"

        return Logic(result)

    ###########
    # __xor__ #
    ###########
    def __xor__(self, other):
        """
        """
        if not isinstance(other, Logic):
            return NotImplemented

        if len(self) != len(other):
            raise ValueError(f"Width mismatch: {len(self)} and {len(other)}.")

        result = ""

        for a, b in zip(self.binstr, other.binstr):
            if a in {"x", "z"} or b in {"x", "z"}:
                result += "x"
            elif a == b:
                result += "0"
            else:
                result += "1"

        return Logic(result)

    ##############
    # __invert__ #
    ##############
    def __invert__(self):
        """
        """
        result = ""

        for a in self.binstr:
            if a == "0":
                result += "1"
            elif a == "1":
                result += "0"
            else:
                result += "x"

        return Logic(result)

    ###########
    # __add__ #
    ###########
    def __add__(self, other):
        """
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
        """
        if not isinstance(other, Logic):
            return NotImplemented

        if len(self) != len(other):
            raise ValueError(f"Width mismatch: {len(self)} and {len(other)}.")

        if self.undef() or other.undef():
            return Logic("x"*len(self))

        binstr = bin((int(self) - int(other)) % (2**len(self)))[2:].zfill(len(self))

        return Logic(binstr)

    #########
    # parse #
    #########
    @classmethod
    def parse(cls, literal):
        """
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


