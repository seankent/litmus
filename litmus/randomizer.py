###########
# imports #
###########
from litmus.logic import Logic
from litmus.worker import Worker
import cocotb

##############
# Randomizer #
##############
class Randomizer(Worker):

    #######
    # run #
    #######
    async def run(self, value_dist, duration_dist):
        """
        Drives a randomly chosen value, holding each one for a randomly chosen number
        of cycles.

        Args:
            value_dist (Distribution): Samples the value to drive, as an integer.
            duration_dist (Distribution): Samples the cycles to hold a value for.
        """
        cycles = 0

        await cocotb.triggers.ReadWrite()

        while True:
            if cycles <= 0:
                self.set(self.handles["sig"], Logic.from_int(value_dist.sample(), len(self.handles["sig"])))

                cycles = duration_dist.sample()

            await cocotb.triggers.RisingEdge(self.handles["clk"])

            cycles -= 1

            await cocotb.triggers.ReadWrite()
