###########
# imports #
###########
from litmus.logic import Logic
from litmus.worker import Worker 
import cocotb

############
# Watchdog #
############
class Watchdog(Worker):

    #######
    # run #
    #######
    async def run(self, timeout = None):
        """
        Fails the test if it runs longer than the timeout.

        Args:
            timeout (int): Cycles to allow, or None for no limit.
        """
        cycle = 0

        while True:
            if timeout is not None and cycle >= timeout:
                self.fail(f"timed out after {timeout} cycles")

            await cocotb.triggers.RisingEdge(self.handles["clk"])

            cycle += 1

