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

        self.register(litmus.LevelDriver(
            name = "init_driver",
            handles = {
                "clk": cocotb.top.clk,
                "wr_stall_prob": cocotb.top.wr_rand_stall.stall_prob,
                "wr_stall_min": cocotb.top.wr_rand_stall.stall_min,
                "wr_stall_max": cocotb.top.wr_rand_stall.stall_max,
                "rd_stall_prob": cocotb.top.rd_rand_stall.stall_prob,
                "rd_stall_min": cocotb.top.rd_rand_stall.stall_min,
                "rd_stall_max": cocotb.top.rd_rand_stall.stall_max,
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
            name = "rd_monitor",
            handles = {
                "clk": cocotb.top.clk,
                "valid": cocotb.top.tb_rd_valid,
                "ready": cocotb.top.tb_rd_ready,
                "rd_data": cocotb.top.tb_rd_data,
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

    ########
    # args #
    ########
    def args(self, test):
        """
        """
        args = {}

        args["clocker"] = {
            "period": 2,
        }

        args["rst_driver"] = {
            "task_graph": test["task_graph"],
        }

        args["init_driver"] = {
            "task_graph": test["task_graph"],
        }

        args["wr_driver"] = {
            "task_graph": test["task_graph"],
            "log": test["log"],
        }

        args["rd_monitor"] = {
            "log": test["log"],
        }

        args["finisher"] = {
            "task_graph": test["task_graph"],
            "drain": test.get("drain", 5),
        }

        args["watchdog"] = {
            "timeout": test.get("timeout", 1000),
        }

        return args
