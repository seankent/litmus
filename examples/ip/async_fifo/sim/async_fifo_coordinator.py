###########
# imports #
###########
import cocotb
import litmus


########################
# AsyncFifoCoordinator #
########################
class AsyncFifoCoordinator(litmus.Coordinator):

    ########
    # init #
    ########
    def init(self):
        """
        Registers the workers.
        """
        self.register(litmus.Clocker(
            name = "wr_clocker",
            handles = {
                "clk": cocotb.top.wr_clk,
            },
        ))

        self.register(litmus.Clocker(
            name = "rd_clocker",
            handles = {
                "clk": cocotb.top.rd_clk,
            },
        ))

        self.register(litmus.Delayer(
            name = "wr_delayer",
            handles = {
                "clk": cocotb.top.wr_clk,
            },
        ))

        self.register(litmus.Delayer(
            name = "rd_delayer",
            handles = {
                "clk": cocotb.top.rd_clk,
            },
        ))

        self.register(litmus.LevelDriver(
            name = "wr_rst_driver",
            handles = {
                "clk": cocotb.top.wr_clk,
                "wr_rst": cocotb.top.wr_rst,
            },
        ))

        self.register(litmus.LevelDriver(
            name = "rd_rst_driver",
            handles = {
                "clk": cocotb.top.rd_clk,
                "rd_rst": cocotb.top.rd_rst,
            },
        ))

        self.register(litmus.ValidReadyDriver(
            name = "wr_driver",
            handles = {
                "clk": cocotb.top.wr_clk,
                "valid": cocotb.top.wr_valid,
                "ready": cocotb.top.wr_ready,
                "wr_data": cocotb.top.wr_data,
            },
        ))

        self.register(litmus.Randomizer(
            name = "rd_ready_randomizer",
            handles = {
                "clk": cocotb.top.rd_clk,
                "sig": cocotb.top.rd_ready,
            },
        ))

        self.register(litmus.ValidReadyMonitor(
            name = "wr_monitor",
            handles = {
                "clk": cocotb.top.wr_clk,
                "valid": cocotb.top.wr_valid,
                "ready": cocotb.top.wr_ready,
                "wr_data": cocotb.top.wr_data,
            },
        ))

        self.register(litmus.ValidReadyMonitor(
            name = "rd_monitor",
            handles = {
                "clk": cocotb.top.rd_clk,
                "valid": cocotb.top.rd_valid,
                "ready": cocotb.top.rd_ready,
                "rd_data": cocotb.top.rd_data,
            },
        ))

        self.register(litmus.Finisher(
            name = "finisher",
            handles = {
                "clk": cocotb.top.rd_clk,
            },
        ))

        self.register(litmus.Watchdog(
            name = "watchdog",
            handles = {
                "clk": cocotb.top.wr_clk,
            },
        ))
