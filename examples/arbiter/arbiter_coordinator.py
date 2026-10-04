###########
# imports #
###########
import cocotb
import litmus


#####
# N #
#####
N = 4


######################
# ArbiterCoordinator #
######################
class ArbiterCoordinator(litmus.Coordinator):

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

        for i in range(N):
            self.register(litmus.ValidOnlyDriver(
                name = f"req{i}_driver",
                handles = {
                    "clk": cocotb.top.clk,
                    "valid": cocotb.top.req[i],
                },
            ))

        self.register(litmus.LevelMonitor(
            name = "monitor",
            handles = {
                "clk": cocotb.top.clk,
                "req": cocotb.top.req,
                "gnt": cocotb.top.gnt,
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
