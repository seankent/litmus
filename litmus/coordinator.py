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

    ############
    # register #
    ############
    def register(self, worker):
        """
        """
        self.workers[worker.name] = worker 

    #######
    # run #
    #######
    async def run(self, test):
        """
        """
        tasks = []

        for name in self.workers:
            tasks.append(cocotb.start_soon(self.workers[name].run(**test["kwargs"].get(name, {}))))

        await cocotb.triggers.First(*[task.join() for task in tasks])

        for task in tasks:
            if not task.done():
                task.kill()

        print("[INFO] The End.")


class ExampleCoordinator(Coordinator):
    
    ########
    # init #
    ########
    def init(self):
        """
        """
        self.register(Driver(
            name = "drv",
            handles = {
                "clk": cocotb.top.clk,
                "valid": cocotb.top.valid,
                "ready": cocotb.top.ready,
                "data": cocotb.top.data,
            }
        ))

        self.register(Monitor(
            name = "mon",
            handles = {
                "clk": cocotb.top.clk,
                "valid": cocotb.top.valid,
                "ready": cocotb.top.ready,
                "data": cocotb.top.data,
            }
        ))


