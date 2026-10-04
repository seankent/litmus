###########
# imports #
###########
import cocotb
import litmus


##################
# RamCoordinator #
##################
class RamCoordinator(litmus.Coordinator):

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

        self.register(litmus.ValidOnlyDriver(
            name = "ram_driver",
            handles = {
                "clk": cocotb.top.clk,
                "valid": cocotb.top.valid,
                "we": cocotb.top.we,
                "addr": cocotb.top.addr,
                "wr_data": cocotb.top.wr_data,
            },
        ))

        self.register(litmus.LevelDriver(
            name = "init_driver",
            handles = {
                "clk": cocotb.top.clk,
                "memory": cocotb.top.dut.memory,
            },
        ))

        self.register(litmus.ValidOnlyMonitor(
            name = "ram_monitor",
            handles = {
                "clk": cocotb.top.clk,
                "valid": cocotb.top.valid,
                "we": cocotb.top.we,
                "addr": cocotb.top.addr,
                "rd_data": cocotb.top.rd_data,
            },
        ))

        self.register(litmus.Sampler(
            name = "sampler",
            handles = {
                "clk": cocotb.top.clk,
                "memory": cocotb.top.dut.memory,
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

        args["ram_driver"] = {
            "task_graph": test["task_graph"],
        }

        args["init_driver"] = {
            "task_graph": test["task_graph"],
        }

        args["ram_monitor"] = {
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
