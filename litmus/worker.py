###########
# imports #
###########
from cocotb.binary import BinaryValue
from litmus.logic import Logic

##########
# Worker #
##########
class Worker:

    ############
    # __init__ #
    ############
    def __init__(self, name, handles):
        """
        Constructs a worker.

        Args:
            name (str): The name of the worker.
            handles (dict): Signal name mapped to cocotb handle.
        """
        self.name = name
        self.handles = handles or {}

    #######
    # set #
    #######
    def set(self, handle, value):
        """
        Drives a value onto a signal.

        Args:
            handle (SimHandle): The signal to drive.
            value (Logic): The value to drive onto it.
        """
        handle.setimmediatevalue(BinaryValue(value.binstr))

    #######
    # get #
    #######
    def get(self, handle):
        """
        Returns the current value of a signal.

        Args:
            handle (SimHandle): The signal to sample.

        Returns:
            Logic: The current value, including any x or z.
        """
        return Logic(handle.value.binstr.lower())

    #######
    # run #
    #######
    async def run(self):
        """
        Runs the worker, overridden by each subclass.
        """
        pass

