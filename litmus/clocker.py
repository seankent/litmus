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
    async def run(self, period = 2, units = "ns"):
        """
        """
        await Clock(self.handles["clk"], period, units = units).start(start_high = False)
