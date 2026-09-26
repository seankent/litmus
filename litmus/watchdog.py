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
        """
        cycle = 0

        while True:
            if timeout is not None and cycle >= timeout:
                print(f"[ERROR] Watchdog '{self.name}' timed out after {timeout} cycles.")
                break

            await cocotb.triggers.RisingEdge(self.handles["clk"])

            cycle += 1

