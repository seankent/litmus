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
    async def run(self, tg):
        """
        """
        u = None

        while True:
            await cocotb.triggers.RisingEdge(self.handles["clk"])
            await cocotb.triggers.ReadWrite()

            if u is None:
                us = tg.ready(self.name)

                if len(us) > 0:
                    u = us[0]

            if u is not None:
                if "valid" in self.handles:
                    self.set(self.handles["valid"], Logic("1"))

                for sig in self.handles:
                    if sig not in {"clk", "valid", "ready"}:
                        self.set(self.handles[sig], u.sigs[sig])
            else:
                if "valid" in self.handles:
                    self.set(self.handles["valid"], Logic("0"))

            await cocotb.triggers.ReadOnly()

            if u is not None:
                
                if "ready" in self.handles:
                    ready = self.get(self.handles["ready"])

                    if ready.undef():
                        print("[ERROR] 'ready' is undefined.")
                        break
                else:
                    ready = Logic("1")

                if ready: 
                    tg.retire(u)
                    u = None





