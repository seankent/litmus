###########
# imports #
###########
from litmus.logic import Logic
from litmus.worker import Worker 
import cocotb

###########
# Monitor #
###########
class Monitor(Worker):

    #######
    # run #
    #######
    async def run(self, log):
        """
        """
        while True:
            await cocotb.triggers.RisingEdge(self.handles["clk"])
            await cocotb.triggers.ReadOnly()

            if "valid" in self.handles:
                valid = self.get(self.handles["valid"])

                if valid.undef():
                    print("[ERROR] 'valid' is undefined.")
                    break 
            else:
                valid = Logic("1")

            if "ready" in self.handles:
                ready = self.get(self.handles["ready"])

                if ready.undef():
                    print("[ERROR] 'ready' is undefined.")
                    break 
            else:
                ready = Logic("1")


            if valid and ready: 
                sigs = {}

                for sig in self.handles:
                    if sig not in {"clk", "valid", "ready"}:
                        sigs[sig] = self.get(self.handles[sig])

                log.append(self.name, sigs)








