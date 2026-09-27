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
    async def run(self, tg):
        """
        """
        pending = {}

        while True:
            await cocotb.triggers.RisingEdge(self.handles["clk"])

            for u in tg.ready(self.name):
                if u not in pending:
                    pending[u] = u.cycles

            await cocotb.triggers.ReadOnly()

            for u in list(pending):
                pending[u] -= 1

                if pending[u] <= 0:
                    del pending[u]
                    tg.retire(u)
