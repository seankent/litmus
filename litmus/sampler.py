###########
# imports #
###########
from litmus.worker import Worker
import cocotb

###########
# Sampler #
###########
class Sampler(Worker):

    #######
    # run #
    #######
    async def run(self, task_graph, log):
        """
        """
        while True:
            await cocotb.triggers.RisingEdge(self.handles["clk"])
            await cocotb.triggers.ReadOnly()

            for u in task_graph.ready(self.name):
                sigs = {}

                for sig in self.handles:
                    if sig != "clk":
                        sigs[sig] = self.get(self.handles[sig])

                log.append(self.name, sigs)
                task_graph.retire(u)
