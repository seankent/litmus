###########
# imports #
###########
import cocotb
from litmus.clocker import Clocker
from litmus.coordinator import Coordinator
from litmus.delayer import Delayer
from litmus.driver import LevelDriver, ValidOnlyDriver
from litmus.finisher import Finisher
from litmus.monitor import LevelMonitor
from litmus.watchdog import Watchdog


##################
# DffCoordinator #
##################
class DffCoordinator(Coordinator):

    ########
    # init #
    ########
    def init(self):
        """
        """
        self.register(Clocker(
            name = "clocker",
            handles = {
                "clk": cocotb.top.clk,
            },
        ))

        self.register(LevelDriver(
            name = "rst",
            handles = {
                "clk": cocotb.top.clk,
                "rst": cocotb.top.rst,
            },
        ))

        self.register(ValidOnlyDriver(
            name = "d",
            handles = {
                "clk": cocotb.top.clk,
                "valid": cocotb.top.en,
                "d": cocotb.top.d,
            },
        ))

        self.register(LevelMonitor(
            name = "q",
            handles = {
                "clk": cocotb.top.clk,
                "q": cocotb.top.q,
            },
        ))

        self.register(Delayer(
            name = "delay",
            handles = {
                "clk": cocotb.top.clk,
            },
        ))

        self.register(Finisher(
            name = "finisher",
            handles = {
                "clk": cocotb.top.clk,
            },
        ))

        self.register(Watchdog(
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

        args["rst"] = {
            "task_graph": test["task_graph"],
        }

        args["d"] = {
            "task_graph": test["task_graph"],
        }

        args["q"] = {
            "log": test["log"],
        }

        args["delay"] = {
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

