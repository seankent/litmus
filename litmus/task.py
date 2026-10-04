
########
# Task #
########
class Task:

    ############
    # __init__ #
    ############
    def __init__(self, name):
        """
        Constructs a task.

        Args:
            name (str): The name of the worker that should process the task.
        """
        self.name = name

    ###########
    # __str__ #
    ###########
    def __str__(self):
        """
        Returns the readable form, which is the name.

        Returns:
            str: The name of the worker that should process the task.
        """
        return self.name

    ############
    # __repr__ #
    ############
    def __repr__(self):
        """
        Returns the constructor call, e.g. Task('rst').

        Returns:
            str: The constructor call.
        """
        return f"{type(self).__name__}({self.name!r})"

###############
# Transaction #
###############
class Transaction(Task):

    ############
    # __init__ #
    ############
    def __init__(self, name, sigs):
        """
        """
        super().__init__(name)

        self.sigs = sigs

    ###########
    # __str__ #
    ###########
    def __str__(self):
        """
        Returns the readable form, e.g. d{d = 8'h07}.

        Returns:
            str: The name and signal values.
        """
        txt = ""

        for sig in self.sigs:
            if txt != "":
                txt += ", "

            txt += f"{sig} = {self.sigs[sig]}"

        return f"{self.name}{{{txt}}}"

    ############
    # __repr__ #
    ############
    def __repr__(self):
        """
        Returns the constructor call, e.g. Transaction('d', {'d': 8'h07}).

        Returns:
            str: The constructor call.
        """
        return f"Transaction({self.name!r}, {self.sigs!r})"


#########
# Delay #
#########
class Delay(Task):

    ############
    # __init__ #
    ############
    def __init__(self, name, cycles):
        """
        """
        super().__init__(name)

        self.cycles = cycles

    ###########
    # __str__ #
    ###########
    def __str__(self):
        """
        Returns the readable form, e.g. delay(3).

        Returns:
            str: The name and cycle count.
        """
        return f"{self.name}({self.cycles})"

    ############
    # __repr__ #
    ############
    def __repr__(self):
        """
        Returns the constructor call, e.g. Delay('delay', 3).

        Returns:
            str: The constructor call.
        """
        return f"Delay({self.name!r}, {self.cycles!r})"


##########
# Sample #
##########
class Sample(Task):
    pass


