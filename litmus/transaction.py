
###############
# Transaction #
###############
class Transaction:

    ############
    # __init__ #
    ############
    def __init__(self, name, payload):
        """
        Constructs a transaction.

        The name is what routes it: the worker registered under the same name
        is the one that services it. A Driver named "wr" claims transactions named
        "wr".

        The payload is a dict rather than keyword arguments so that a field can be
        named anything. Keywords would restrict field names to valid Python
        identifiers and let a field called "name" collide with the first argument.

        Transactions compare by identity, never by value: two transactions with
        the same name and the same payload are still different transactions. A
        TransactionGraph holds them as dict keys, so value equality would collapse
        repeats into a single vertex and silently drop stimulus. Do not give this
        class __eq__ or __hash__.

        Args:
            name (str): The worker this transaction routes to, e.g. "req" or
                "rst". It must be registered on the graph before the transaction
                is appended.
            payload (dict): The signal fields, mapping field name to value, e.g.
                {"data": Logic.parse("8'd3")}.
        """
        self.name = name
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

        return f"{self.name}{{{txt}}}"

    ############
    # __repr__ #
    ############
    def __repr__(self):
        """
        Returns an unambiguous representation shaped like the constructor call,
        e.g. Transaction('req', {'addr': Logic("00000011")}).
        """
        return f"Transaction({self.name!r}, {self.payload!r})"

