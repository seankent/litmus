###########
# imports #
###########
from litmus.worker import Worker
import cocotb

############
# Gatherer #
############
class Gatherer(Worker):

    #######
    # run #
    #######
    async def run(self, tg, log):
        """
        """
        while True:
            await cocotb.triggers.RisingEdge(self.handles["clk"])
            await cocotb.triggers.ReadOnly()

            for u in tg.ready(self.name):
                sigs = {}

                for sig in self.handles:
                    if sig != "clk":
                        sigs[sig] = self.get(self.handles[sig])

                log.append(self.name, sigs)
                tg.retire(u)
