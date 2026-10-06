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
        Generates a clock signal.

        Args:
            period (int): The clock period.
            unit (str): The time unit the period is given in.
        """
        await Clock(self.handles["clk"], period, unit = unit).start(start_high = False)
