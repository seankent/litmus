###########
# imports #
###########
import cocotb
from litmus.clocker import Clocker
from litmus.coordinator import Coordinator
from litmus.delayer import Delayer
from litmus.driver import ValidOnlyDriver
from litmus.finisher import Finisher
from litmus.monitor import LevelMonitor
from litmus.watchdog import Watchdog


#####
# N #
#####
N = 4


######################
# ArbiterCoordinator #
######################
class ArbiterCoordinator(Coordinator):

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

        for i in range(N):
            self.register(ValidOnlyDriver(
                name = f"req{i}_driver",
                handles = {
                    "clk": cocotb.top.clk,
                    "valid": cocotb.top.req[i],
                },
            ))

        self.register(LevelMonitor(
            name = "monitor",
            handles = {
                "clk": cocotb.top.clk,
                "req": cocotb.top.req,
                "gnt": cocotb.top.gnt,
            },
        ))

        self.register(Delayer(
            name = "delayer",
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

        for i in range(N):
            args[f"req{i}_driver"] = {
                "task_graph": test["task_graph"],
            }

        args["delayer"] = {
            "task_graph": test["task_graph"],
        }

        args["monitor"] = {
            "log": test["log"],
        }

        args["finisher"] = {
            "task_graph": test["task_graph"],
            "drain": test.get("drain", 2),
        }

        args["watchdog"] = {
            "timeout": test.get("timeout", 1000),
        }

        return args
