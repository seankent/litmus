###########
# imports #
###########
from litmus.logic import Logic
from litmus.worker import Worker 
import cocotb

############
# Finisher #
############
class Finisher(Worker):

    #######
    # run #
    #######
    async def run(self, tg, drain = 0):
        """
        """
        while True:
            await cocotb.triggers.RisingEdge(self.handles["clk"])

            if tg.empty():
                break

        for _ in range(drain):
            await cocotb.triggers.RisingEdge(self.handles["clk"])
