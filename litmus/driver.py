###########
# imports #
###########
from litmus.logic import Logic
from litmus.worker import Worker
import cocotb

##########
# Driver #
##########
class Driver(Worker):

    #######
    # run #
    #######
    async def run(self, task_graph):
        """
        """
        pass


###############
# LevelDriver #
###############
class LevelDriver(Driver):

    #######
    # run #
    #######
    async def run(self, task_graph):
        """
        """
        while True:
            await cocotb.triggers.RisingEdge(self.handles["clk"])
            await cocotb.triggers.ReadWrite()

            u = None
            us = task_graph.ready(self.name)

            if len(us) > 0:
                u = us[0]

                for sig in self.handles:
                    if sig != "clk":
                        self.set(self.handles[sig], u.sigs[sig])

            await cocotb.triggers.ReadOnly()

            if u is not None:
                task_graph.retire(u)


###################
# ValidOnlyDriver #
###################
class ValidOnlyDriver(Driver):

    #######
    # run #
    #######
    async def run(self, task_graph):
        """
        """
        while True:
            await cocotb.triggers.RisingEdge(self.handles["clk"])
            await cocotb.triggers.ReadWrite()

            u = None
            us = task_graph.ready(self.name)

            if len(us) > 0:
                u = us[0]

            if u is not None:
                self.set(self.handles["valid"], Logic("1"))

                for sig in self.handles:
                    if sig not in {"clk", "valid"}:
                        self.set(self.handles[sig], u.sigs[sig])
            else:
                self.set(self.handles["valid"], Logic("0"))

            await cocotb.triggers.ReadOnly()

            if u is not None:
                task_graph.retire(u)


####################
# ValidReadyDriver #
####################
class ValidReadyDriver(Driver):

    #######
    # run #
    #######
    async def run(self, task_graph):
        """
        """
        u = None

        while True:
            await cocotb.triggers.RisingEdge(self.handles["clk"])
            await cocotb.triggers.ReadWrite()

            if u is None:
                us = task_graph.ready(self.name)

                if len(us) > 0:
                    u = us[0]

            if u is not None:
                self.set(self.handles["valid"], Logic("1"))

                for sig in self.handles:
                    if sig not in {"clk", "valid", "ready"}:
                        self.set(self.handles[sig], u.sigs[sig])
            else:
                self.set(self.handles["valid"], Logic("0"))

            await cocotb.triggers.ReadOnly()

            if u is not None:
                ready = self.get(self.handles["ready"])

                if ready.undef():
                    print("[ERROR] 'ready' is undefined.")
                    break

                if ready:
                    task_graph.retire(u)
                    u = None
