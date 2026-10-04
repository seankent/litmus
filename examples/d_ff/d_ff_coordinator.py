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
            name = "q_monitor",
            handles = {
                "clk": cocotb.top.clk,
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

        args["d_driver"] = {
            "task_graph": test["task_graph"],
        }

        args["q_monitor"] = {
            "log": test["log"],
        }

        args["delayer"] = {
            "task_graph": test["task_graph"],
        }

        args["finisher"] = {
            "task_graph": test["task_graph"],
            "drain": test.get("drain", 5),
        }

        args["watchdog"] = {
            "timeout": test.get("timeout", 1000),
        }

        return args

