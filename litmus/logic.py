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
        Constructs a Logic from a raw binary string.

        This is the canonical constructor and does no interpretation: `binstr` is
        stored as-is and its length is the width. Use parse() for Verilog literals
        such as "8'hAB". Bit 0 is the LSB, which is the *last* character of the
        string, so "1000" is the 4-bit value 8.

        Args:
            binstr (str): The bits, MSB first, drawn from 0, 1, x and z.

        Raises:
            ValueError: If binstr is empty or holds any other character. A literal
                passed here by mistake, such as "8'hAB", is rejected rather than
                stored as bits.
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
        """
        return len(self.binstr)

    #########
    # undef #
    #########
    def undef(self):
        """
        Returns True if any bit is x or z.
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
        Returns the truth value, following Verilog's rule for `if`.

        True only when the value is fully defined and nonzero. Any x or z makes the
        whole value false, which is stricter than most simulators: they call
        4'b10x true, because bit 1 is known to be 1 and so the value is definitely
        nonzero. The conservative reading is used here so an unknown never silently
        passes a condition.
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
        Returns the value as an unsigned Python int.

        The bits are read as unsigned, so 8'hff is 255 rather than -1. There is no
        signed interpretation, because a bit vector does not carry signedness --
        that is context the caller has.

        Returns:
            int: The unsigned value.

        Raises:
            ValueError: If any bit is x or z.
        """
        if self.undef():
            raise ValueError(f"Cannot convert '{self.binstr}' to int: contains x or z.")

        return int(self.binstr, base = 2)

    #######
    # hex #
    #######
    def hex(self):
        """
        Returns the value as a hex literal, e.g. "8'hab".

        A nibble of all z prints as z, and any other nibble containing x or z prints
        as x, matching how simulators display %h. This is lossy for undefined
        values -- 8'b0000001x prints as 8'h0x -- so use bin() anywhere the exact
        bits matter, such as result logs that get compared.

        Returns:
            str: The hex literal.
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
        Returns the value as a binary literal, e.g. "8'b10101011".

        Every bit is shown exactly, including x and z, so this is the lossless form
        and the one to use for anything that gets compared or written to a log. It
        round-trips: parse() accepts what this produces.

        Returns:
            str: The binary literal.
        """
        return f"{len(self)}'b" + self.binstr

    #######
    # dec #
    #######
    def dec(self):
        """
        Returns the value as a decimal literal, e.g. "8'd171".

        Decimal cannot represent x or z at all, so unlike bin() and hex() this
        raises rather than approximating. The value is unsigned, as in __int__.

        Returns:
            str: The decimal literal.

        Raises:
            ValueError: If any bit is x or z.
        """
        if self.undef():
            raise ValueError(f"Cannot convert '{self.binstr}' to decimal: contains x or z.")

        return f"{len(self)}'d{int(self)}"

    ###########
    # __str__ #
    ###########
    def __str__(self):
        """
        Returns the hex literal, as produced by hex().

        Hex because str() is the readable form, and a 32-bit value as binary is
        unreadable in a log line or an error message. It is lossy for x and z, so
        anything that gets compared -- a result log in particular -- must call
        bin() explicitly rather than relying on str().

        Returns:
            str: The hex literal.
        """
        return self.hex()

    ############
    # __repr__ #
    ############
    def __repr__(self):
        """
        Returns an unambiguous representation, e.g. 'Logic("10101011")'.

        Mirrors the constructor, so eval(repr(value)) reproduces the value for every
        input including x and z.

        Returns:
            str: The representation.
        """
        return f'Logic("{self.binstr}")'

    ############
    # __hash__ #
    ############
    def __hash__(self):
        """
        Returns a hash of the bits.

        Consistent with __eq__, which also compares bits alone. Logic is immutable,
        so this stays valid for the object's lifetime -- the reason there is no
        __setitem__.
        """
        return hash(self.binstr)

    ##########
    # __eq__ #
    ##########
    def __eq__(self, other):
        """
        Returns True if both values have the same width and the same bits.

        This is Verilog's === rather than ==: x and z compare structurally, so
        4'bx equals 4'bx and never equals 4'bz, and the result is always a definite
        True or False. Width is part of the value, so 4'b0101 does not equal
        8'b00000101 -- a width mismatch between a DUT and a reference model is a
        bug worth catching rather than extending away.

        Comparison against an int is not supported, since it would make equality
        intransitive. Use int(value) == n instead.

        Args:
            other (Logic): The value to compare against.

        Returns:
            bool: True if both the width and every bit match. NotImplemented if
                other is not a Logic, so Python can try the reflected comparison.
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
        Selects a bit or a range of bits, using Verilog numbering.

        Bit 0 is the LSB, and slices are descending and inclusive on both ends, so
        value[7:4] is the top nibble of an 8-bit value and value[3:3] is a single
        bit. Out-of-range indices raise rather than wrapping.

        Slicing is also how you narrow a value, since extend() only widens: the
        truncation stays visible at the call site.

        Args:
            index (int or slice): A bit number, or a descending slice such as 7:4.

        Returns:
            Logic: The selected bit or bits.

        Raises:
            IndexError: If the index or either slice bound is outside the width.
            ValueError: If the slice ascends, carries a step, or omits a bound.
            TypeError: If index is neither an int nor a slice.
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
        Returns a copy zero-extended to `width` bits.

        The added high bits are always 0, including for values containing x or z:
        widening 4'b10xz to 8 gives 8'b000010xz. This models assignment to a wider
        unsigned signal, where the upper bits are driven to constant 0, and so
        deliberately differs from parse()'s x/z rule for literals.

        Extending to the current width is a no-op, so this is safe to call when you
        do not know whether the widths already match. Narrowing is not supported --
        slice instead.

        Args:
            width (int): The result width in bits. Must be at least the current width.

        Returns:
            Logic: A new Logic of the requested width.

        Raises:
            ValueError: If width is less than the current width.
        """
        if width < len(self):
            raise ValueError(f"Cannot extend width {len(self)} to {width}.")

        return Logic(self.binstr.zfill(width))

    ###########
    # __and__ #
    ###########
    def __and__(self, other):
        """
        Returns the bitwise AND of the two values, using Verilog's four-state
        truth table.

        A 0 on either side gives 0 even when the other bit is x or z. Two 1s give 1.
        Every other combination gives x, so z never appears in the result.

        Unlike Verilog, the narrower operand is not extended: mismatched widths are
        an error. Verilog's rule also depends on the assignment target, which a
        Python expression cannot see, so equal widths is the only unambiguous rule
        available. Call extend() first when you do mean to widen.

        Args:
            other (Logic): The right-hand operand.

        Returns:
            Logic: The result, the same width as the operands. NotImplemented if
                other is not a Logic, so Python can try the reflected operation.

        Raises:
            ValueError: If the operands differ in width.
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
        Returns the bitwise OR of the two values, using Verilog's four-state
        truth table.

        A 1 on either side gives 1 even when the other bit is x or z. Two 0s give 0.
        Every other combination gives x, so z never appears in the result.

        Widths must match, as for __and__.

        Args:
            other (Logic): The right-hand operand.

        Returns:
            Logic: The result, the same width as the operands. NotImplemented if
                other is not a Logic.

        Raises:
            ValueError: If the operands differ in width.
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
        Returns the bitwise XOR of the two values, using Verilog's four-state
        truth table.

        Any x or z on either side gives x -- unlike AND and OR, no bit value can
        dominate an unknown. Defined bits give 0 when they agree and 1 when they
        differ.

        Widths must match, as for __and__.

        Args:
            other (Logic): The right-hand operand.

        Returns:
            Logic: The result, the same width as the operands. NotImplemented if
                other is not a Logic.

        Raises:
            ValueError: If the operands differ in width.
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
        Returns the bitwise NOT, using Verilog's four-state truth table.

        0 and 1 swap; both x and z give x. Because z collapses to x, invert is not
        reversible for undefined values: ~~4'b10xz is 4'b10xx.

        Returns:
            Logic: The result, the same width as the operand.
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
        Adds two values of the same width, wrapping on overflow.

        The result is the width of the operands, so the carry is discarded:
        8'hff + 8'd1 is 8'h00. This matches a hardware adder whose output is the
        same width as its inputs. To keep the carry, extend() both operands first,
        which is the explicit form of Verilog widening its expression to fit a
        wider assignment target.

        Any x or z in either operand makes the entire result x, since a single
        unknown bit can propagate through the carry chain to every other bit.

        Args:
            other (Logic): The right-hand operand.

        Returns:
            Logic: The sum, the same width as the operands. NotImplemented if
                other is not a Logic.

        Raises:
            ValueError: If the operands differ in width.
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
        Subtracts two values of the same width, wrapping on underflow.

        Underflow wraps as two's complement, so 8'd0 - 8'd1 is 8'hff. The result is
        the width of the operands, and any x or z in either operand makes the
        entire result x, as for __add__.

        Args:
            other (Logic): The right-hand operand.

        Returns:
            Logic: The difference, the same width as the operands. NotImplemented
                if other is not a Logic.

        Raises:
            ValueError: If the operands differ in width.
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
        Builds a Logic from a Verilog-style sized literal.

        Accepts binary, hex and decimal, e.g. "8'b1010_1011", "8'hAB", "8'd171".
        Underscores are ignored and case does not matter. Binary and hex may carry
        x and z digits, and a hex x or z expands to four bits; decimal cannot.

        A literal narrower than its declared width is zero-extended, or x/z-extended
        when its leading digit is x or z, so 8'hx is all x. That rule applies to
        literals only -- extend() always pads with 0, because widening a value is a
        different operation from writing a constant.

        An unsized string of bits is not accepted here; pass it to the constructor.

        Args:
            literal (str): The literal to parse.

        Returns:
            Logic: The parsed value, exactly as wide as the literal declares.

        Raises:
            ValueError: If the literal is malformed, carries digits that are invalid
                for its base, or does not fit within its declared width.
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


