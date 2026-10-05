###########
# imports #
###########
from litmus.logic import Logic
from litmus.worker import Worker
import cocotb
from cocotb.clock import Clock

###########
# Clocker #
###########
class Clocker(Worker):

    #######
    # run #
    #######
    async def run(self, period = 2, unit = "ns"):
        """
        """
        await Clock(self.handles["clk"], period, unit = unit).start(start_high = False)
