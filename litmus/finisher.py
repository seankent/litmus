###########
# imports #
###########
from litmus.logic import Logic
from litmus.worker import Worker 
import cocotb

############
# Finisher #
############
class Finisher(Worker):

    #######
    # run #
    #######
    async def run(self, task_graph, drain = 0):
        """
        Ends the test once every task has retired.

        Args:
            task_graph (TaskGraph): The graph to wait on.
            drain (int): Extra cycles to run after the graph empties.
        """
        while True:
            await cocotb.triggers.RisingEdge(self.handles["clk"])

            if task_graph.empty():
                break

        for _ in range(drain):
            await cocotb.triggers.RisingEdge(self.handles["clk"])
