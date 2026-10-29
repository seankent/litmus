###########
# imports #
###########
import cocotb
import litmus


##################
# DffCoordinator #
##################
class DffCoordinator(litmus.Coordinator):

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
            name = "rst_driver",
            handles = {
                "clk": cocotb.top.clk,
                "rst": cocotb.top.rst,
            },
        ))

        self.register(litmus.ValidOnlyDriver(
            name = "d_driver",
            handles = {
                "clk": cocotb.top.clk,
                "valid": cocotb.top.en,
                "d": cocotb.top.d,
            },
        ))

        self.register(litmus.LevelMonitor(
            name = "monitor",
            handles = {
                "clk": cocotb.top.clk,
                "rst": cocotb.top.rst,
                "en": cocotb.top.en,
                "d": cocotb.top.d,
                "q": cocotb.top.q,
            },
        ))

        self.register(litmus.Delayer(
            name = "delayer",
            handles = {
                "clk": cocotb.top.clk,
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


