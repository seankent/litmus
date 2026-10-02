###########
# imports #
###########
import cocotb
from cocotb.binary import BinaryValue
from litmus import utils
from litmus.logic import Logic


###############
# Coordinator #
###############
class Coordinator:

    ############
    # __init__ #
    ############
    def __init__(self):
        """
        """
        self.workers = {}

        self.init()

    ########
    # init #
    ########
    def init(self):
        """
        """
        pass

    ############
    # register #
    ############
    def register(self, worker):
        """
        """
        self.workers[worker.name] = worker 

    ########
    # args #
    ########
    def args(self, test):
        """
        """
        return {}

    #######
    # run #
    #######
    async def run(self, test):
        """
        """
        args = self.args(test)

        tasks = []

        for name in self.workers:
            tasks.append(cocotb.start_soon(self.workers[name].run(**args.get(name, {}))))

        await cocotb.triggers.First(*[task.join() for task in tasks])

        for task in tasks:
            if not task.done():
                task.kill()
