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
    async def run(self):
        """
        """
        self.log = []

        cycle = 0
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
                tr = {}

                for sig in self.handles:
                    if sig not in {"clk", "valid", "ready"}:
                        tr[sig] = self.get(self.handles[sig])

                self.log.append({"cycle": cycle, "tr": tr})

            cycle += 1








