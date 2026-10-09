###########
# imports #
###########
from litmus.logic import Logic
from litmus.worker import Worker 
import cocotb

###########
# Delayer #
###########
class Delayer(Worker):

    #######
    # run #
    #######
    async def run(self, task_graph):
        """
        Retires Delay tasks once their cycles have elapsed.

        Args:
            task_graph (TaskGraph): The graph to claim tasks from.
        """
        pending = {}

        while True:
            await cocotb.triggers.RisingEdge(self.handles["clk"])

            for u in list(pending):
                pending[u] -= 1

                if pending[u] <= 0:
                    del pending[u]
                    task_graph.retire(u)

            await cocotb.triggers.ReadWrite()

            for u in task_graph.ready(self.name):
                if u not in pending:
                    pending[u] = u.cycles
