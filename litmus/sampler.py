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
        Logs a snapshot of its signals for each Sample task.

        Args:
            task_graph (TaskGraph): The graph to claim tasks from.
            log (Log): The log to write to.
        """
        claimed = []

        while True:
            await cocotb.triggers.RisingEdge(self.handles["clk"])

            for u in claimed:
                sigs = {}

                for sig in self.handles:
                    if sig != "clk":
                        sigs[sig] = self.get(self.handles[sig])

                log.append(self.name, sigs)
                task_graph.retire(u)

            claimed = []

            await cocotb.triggers.ReadWrite()

            for u in task_graph.ready(self.name):
                claimed.append(u)
