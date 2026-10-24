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
            name = "init_driver",
            handles = {
                "clk": cocotb.top.clk,
                "wr_stall_prob": cocotb.top.u_rand_stall_wr.stall_prob,
                "wr_stall_min": cocotb.top.u_rand_stall_wr.stall_min,
                "wr_stall_max": cocotb.top.u_rand_stall_wr.stall_max,
                "rd_stall_prob": cocotb.top.u_rand_stall_rd.stall_prob,
                "rd_stall_min": cocotb.top.u_rand_stall_rd.stall_min,
                "rd_stall_max": cocotb.top.u_rand_stall_rd.stall_max,
            },
        ))

        self.register(litmus.LevelDriver(
            name = "rst_driver",
            handles = {
                "clk": cocotb.top.clk,
                "rst": cocotb.top.rst,
            },
        ))

        self.register(litmus.ValidReadyDriver(
            name = "wr_driver",
            handles = {
                "clk": cocotb.top.clk,
                "valid": cocotb.top.tb_wr_valid,
                "ready": cocotb.top.tb_wr_ready,
                "wr_data": cocotb.top.tb_wr_data,
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
