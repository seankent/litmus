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
        """
        self.name = name 
        self.handles = handles or {}

    #######
    # set #
    #######
    def set(self, handle, value):
        """
        """
        handle.setimmediatevalue(BinaryValue(value.binstr))

    #######
    # get #
    #######
    def get(self, handle):
        """
        """
        return Logic(handle.value.binstr.lower())

    #######
    # run #
    #######
    async def run(self):
        """
        """
        pass

