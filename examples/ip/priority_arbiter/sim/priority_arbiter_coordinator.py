###########
# imports #
###########
import cocotb
import litmus


##############################
# PriorityArbiterCoordinator #
##############################
class PriorityArbiterCoordinator(litmus.Coordinator):

    ########
    # init #
    ########
    def init(self):
        """
        Registers the workers.
        """
        self.register(litmus.Clocker(
            name = "clocker",
            handles = {
                "clk": cocotb.top.clk,
            },
        ))

        self.register(litmus.LevelDriver(
            name = "req_driver",
            handles = {
                "clk": cocotb.top.clk,
                "req": cocotb.top.req,
            },
        ))

        self.register(litmus.LevelMonitor(
            name = "monitor",
            handles = {
                "clk": cocotb.top.clk,
                "req": cocotb.top.req,
                "gnt": cocotb.top.gnt,
            },
        ))

        self.register(litmus.Finisher(
            name = "finisher",
            handles = {
                "clk": cocotb.top.clk,
            },
        ))

        self.register(litmus.Watchdog(
            name = "watchdog",
            handles = {
                "clk": cocotb.top.clk,
            },
        ))
