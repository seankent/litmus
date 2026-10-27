###########
# imports #
###########
import cocotb
import litmus


#####################
# SdpRamCoordinator #
#####################
class SdpRamCoordinator(litmus.Coordinator):

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
            name = "preloader",
            handles = {
                "clk": cocotb.top.clk,
                "memory": cocotb.top.u_dut.memory,
            },
        ))

        self.register(litmus.ValidOnlyDriver(
            name = "wr_driver",
            handles = {
                "clk": cocotb.top.clk,
                "valid": cocotb.top.we,
                "wr_addr": cocotb.top.wr_addr,
                "wr_data": cocotb.top.wr_data,
            },
        ))

        self.register(litmus.ValidOnlyDriver(
            name = "rd_driver",
            handles = {
                "clk": cocotb.top.clk,
                "valid": cocotb.top.re,
                "rd_addr": cocotb.top.rd_addr,
            },
        ))

        self.register(litmus.ValidOnlyMonitor(
            name = "wr_monitor",
            handles = {
                "clk": cocotb.top.clk,
                "valid": cocotb.top.we,
                "wr_addr": cocotb.top.wr_addr,
                "wr_data": cocotb.top.wr_data,
            },
        ))

        self.register(litmus.ValidOnlyMonitor(
            name = "rd_monitor",
            handles = {
                "clk": cocotb.top.clk,
                "valid": cocotb.top.re,
                "rd_addr": cocotb.top.rd_addr,
                "rd_data": cocotb.top.rd_data,
            },
        ))

        self.register(litmus.Sampler(
            name = "sampler",
            handles = {
                "clk": cocotb.top.clk,
                "memory": cocotb.top.u_dut.memory,
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
