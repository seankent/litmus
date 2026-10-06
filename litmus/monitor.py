###########
# imports #
###########
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
        Logs signal values sampled from the DUT. Overridden by each subclass.

        Args:
            log (Log): The log to write to.
        """
        pass


################
# LevelMonitor #
################
class LevelMonitor(Monitor):

    #######
    # run #
    #######
    async def run(self, log):
        """
        Logs signal values every cycle.

        Args:
            log (Log): The log to write to.
        """
        while True:
            await cocotb.triggers.RisingEdge(self.handles["clk"])
            await cocotb.triggers.ReadOnly()

            sigs = {}

            for sig in self.handles:
                if sig != "clk":
                    sigs[sig] = self.get(self.handles[sig])

            log.append(self.name, sigs)


####################
# ValidOnlyMonitor #
####################
class ValidOnlyMonitor(Monitor):

    #######
    # run #
    #######
    async def run(self, log):
        """
        Logs signal values in each cycle valid is high.

        Args:
            log (Log): The log to write to.
        """
        while True:
            await cocotb.triggers.RisingEdge(self.handles["clk"])
            await cocotb.triggers.ReadOnly()

            valid = self.get(self.handles["valid"])

            if valid.undef():
                print("[ERROR] 'valid' is undefined.")
                break

            if valid:
                sigs = {}

                for sig in self.handles:
                    if sig not in {"clk", "valid"}:
                        sigs[sig] = self.get(self.handles[sig])

                log.append(self.name, sigs)


#####################
# ValidReadyMonitor #
#####################
class ValidReadyMonitor(Monitor):

    #######
    # run #
    #######
    async def run(self, log):
        """
        Logs signal values in each cycle valid and ready are both high.

        Args:
            log (Log): The log to write to.
        """
        while True:
            await cocotb.triggers.RisingEdge(self.handles["clk"])
            await cocotb.triggers.ReadOnly()

            valid = self.get(self.handles["valid"])

            if valid.undef():
                print("[ERROR] 'valid' is undefined.")
                break

            ready = self.get(self.handles["ready"])

            if ready.undef():
                print("[ERROR] 'ready' is undefined.")
                break

            if valid and ready:
                sigs = {}

                for sig in self.handles:
                    if sig not in {"clk", "valid", "ready"}:
                        sigs[sig] = self.get(self.handles[sig])

                log.append(self.name, sigs)
