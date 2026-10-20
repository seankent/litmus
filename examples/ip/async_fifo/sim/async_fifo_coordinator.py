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

        self.register(litmus.LevelDriver(
            name = "init_driver",
            handles = {
                "clk": cocotb.top.wr_clk,
                "wr_stall_prob": cocotb.top.u_rand_stall_wr.stall_prob,
                "wr_stall_min": cocotb.top.u_rand_stall_wr.stall_min,
                "wr_stall_max": cocotb.top.u_rand_stall_wr.stall_max,
                "rd_stall_prob": cocotb.top.u_rand_stall_rd.stall_prob,
                "rd_stall_min": cocotb.top.u_rand_stall_rd.stall_min,
                "rd_stall_max": cocotb.top.u_rand_stall_rd.stall_max,
            },
        ))

        self.register(litmus.ValidReadyDriver(
            name = "wr_driver",
            handles = {
                "clk": cocotb.top.wr_clk,
                "valid": cocotb.top.tb_wr_valid,
                "ready": cocotb.top.tb_wr_ready,
                "wr_data": cocotb.top.tb_wr_data,
            },
        ))

        self.register(litmus.ValidReadyMonitor(
            name = "rd_monitor",
            handles = {
                "clk": cocotb.top.rd_clk,
                "valid": cocotb.top.tb_rd_valid,
                "ready": cocotb.top.tb_rd_ready,
                "rd_data": cocotb.top.tb_rd_data,
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

    ########
    # args #
    ########
    def args(self, test):
        """
        """
        args = {}

        args["wr_clocker"] = {
            "period": 2,
        }

        args["rd_clocker"] = {
            "period": 3,
        }

        args["wr_delayer"] = {
            "task_graph": test["task_graph"],
        }

        args["rd_delayer"] = {
            "task_graph": test["task_graph"],
        }

        args["wr_rst_driver"] = {
            "task_graph": test["task_graph"],
        }

        args["rd_rst_driver"] = {
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
            "drain": test.get("drain", 20),
        }

        args["watchdog"] = {
            "timeout": test.get("timeout", 1000),
        }

        return args
