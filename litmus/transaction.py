
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

        Args:
            name (str): The name of the worker that should process the transaction.
            payload (dict): Signal name mapped to value.
        """
        self.name = name
        self.payload = payload

    ###########
    # __str__ #
    ###########
    def __str__(self):
        """
        Returns the readable form, e.g. req{addr = 8'h03}.

        Returns:
            str: The name and payload fields, with values formatted as hex.
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
        Returns the constructor call, e.g. Transaction('req', {'addr': Logic("00000011")}).

        Returns:
            str: The constructor call.
        """
        return f"Transaction({self.name!r}, {self.payload!r})"

