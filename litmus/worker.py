###########
# imports #
###########
from cocotb.binary import BinaryValue
from cocotb.handle import NonHierarchyIndexableObject
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
            value (Logic | list): The value to drive, shaped like the signal.
        """
        if type(handle) is NonHierarchyIndexableObject:
            for i in range(len(handle)):
                self.set(handle[i], value[i])
        else:
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
            Logic | list: The current value, shaped like the signal.
        """
        if type(handle) is NonHierarchyIndexableObject:
            values = []

            for i in range(len(handle)):
                values.append(self.get(handle[i]))

            return values
        else:
            return Logic(handle.value.binstr.lower())

    #######
    # run #
    #######
    async def run(self):
        """
        Runs the worker, overridden by each subclass.
        """
        pass

