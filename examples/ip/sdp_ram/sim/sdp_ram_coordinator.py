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

        args["init_driver"] = {
            "task_graph": test["task_graph"],
            "log": test["log"],
        }

        args["wr_driver"] = {
            "task_graph": test["task_graph"],
            "log": test["log"],
        }

        args["rd_driver"] = {
            "task_graph": test["task_graph"],
        }

        args["rd_monitor"] = {
            "log": test["log"],
        }

        args["sampler"] = {
            "task_graph": test["task_graph"],
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
