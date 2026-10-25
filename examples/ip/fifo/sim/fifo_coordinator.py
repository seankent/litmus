###########
# imports #
###########
import cocotb
import litmus


###################
# FifoCoordinator #
###################
class FifoCoordinator(litmus.Coordinator):

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

        self.register(litmus.Delayer(
            name = "delayer",
            handles = {
                "clk": cocotb.top.clk,
            },
        ))

        self.register(litmus.ValidReadyDriver(
            name = "wr_driver",
            handles = {
                "clk": cocotb.top.clk,
                "valid": cocotb.top.wr_valid,
                "ready": cocotb.top.wr_ready,
                "wr_data": cocotb.top.wr_data,
            },
        ))

        self.register(litmus.Randomizer(
            name = "rd_ready_randomizer",
            handles = {
                "clk": cocotb.top.clk,
                "sig": cocotb.top.rd_ready,
            },
        ))

        self.register(litmus.ValidReadyMonitor(
            name = "wr_monitor",
            handles = {
                "clk": cocotb.top.clk,
                "valid": cocotb.top.wr_valid,
                "ready": cocotb.top.wr_ready,
                "wr_data": cocotb.top.wr_data,
            },
        ))

        self.register(litmus.ValidReadyMonitor(
            name = "rd_monitor",
            handles = {
                "clk": cocotb.top.clk,
                "valid": cocotb.top.rd_valid,
                "ready": cocotb.top.rd_ready,
                "rd_data": cocotb.top.rd_data,
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
