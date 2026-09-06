
###############
# Transaction #
###############
class Transaction:

    ############
    # __init__ #
    ############
    def __init__(self, itf, payload):
        """
        Constructs a transaction on an interface.

        The payload is a dict rather than keyword arguments so that a field can be
        named anything. Keywords would restrict field names to valid Python
        identifiers and let a field called "itf" collide with the interface.

        Transactions compare by identity, never by value: two transactions with
        the same interface and the same payload are still different transactions.
        A TransactionGraph holds them as dict keys, so value equality would
        collapse repeats of the same value into a single vertex and silently drop
        stimulus. Do not give this class __eq__ or __hash__.

        Args:
            itf (str): The interface this transaction belongs to, e.g. "req" or
                "rst". It must be registered on the graph before the transaction
                is appended.
            payload (dict): The signal fields, mapping field name to value, e.g.
                {"data": Logic.parse("8'd3")}.
        """
        self.itf = itf
        self.payload = payload

    ###########
    # __str__ #
    ###########
    def __str__(self):
        """
        Returns a readable form, e.g. req{addr = 8'h03}.

        Payload values are formatted with str(), so a Logic appears as hex. That
        is lossy for x and z, which is fine here: this is for error messages and
        debugging, and anything compared must use bin() explicitly.

        Returns:
            str: The readable form.
        """
        txt = ""

        for field in self.payload:
            if txt != "":
                txt += ", "

            txt += f"{field} = {self.payload[field]}"

        return f"{self.itf}{{{txt}}}"

    ############
    # __repr__ #
    ############
    def __repr__(self):
        """
        Returns an unambiguous representation shaped like the constructor call,
        e.g. Transaction('req', {'addr': Logic("00000011")}).
        """
        return f"Transaction({self.itf!r}, {self.payload!r})"


#########
# Delay #
#########
class Delay(Transaction):

    ############
    # __init__ #
    ############
    def __init__(self, n):
        """
        Constructs a delay.

        A delay occupies time without driving anything. It belongs to no
        interface, so it never chains, and any number of delays can be counting
        down at once. What separates it from an ordinary transaction is when it
        retires: a transaction retires when the design accepts it, a delay retires
        after its cycles have elapsed.

        Its payload is empty because a delay has no signal fields. The cycle count
        is not one, so it is an attribute of its own.

        Args:
            n (int): Number of idle cycles to insert before whatever depends on
                this delay can fire.
        """
        super().__init__(None, {})

        self.n = n

    ###########
    # __str__ #
    ###########
    def __str__(self):
        """
        Returns a readable form, e.g. delay(3).
        """
        return f"delay({self.n})"

    ############
    # __repr__ #
    ############
    def __repr__(self):
        """
        Returns an unambiguous representation shaped like the constructor call,
        e.g. Delay(3).
        """
        return f"Delay({self.n!r})"
