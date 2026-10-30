###########
# imports #
###########
import cocotb
import litmus
import os
from d_ff_checker import DffChecker
from d_ff_coordinator import DffCoordinator
import task_graph


########
# test #
########
@cocotb.test()
async def test(top):
    params = {"WIDTH": 8, "RESET_VALUE": 0}

    coordinator = DffCoordinator(params)
    checker = DffChecker(params)

    log = litmus.Log()
    graph = task_graph.graph.copy()

    await coordinator.run({
        "clocker": {"period": 10},
        "rst_driver": {"task_graph": graph},
        "d_driver": {"task_graph": graph},
        "monitor": {"log": log},
        "delayer": {"task_graph": graph},
        "finisher": {"task_graph": graph, "drain": 5},
        "watchdog": {"timeout": 1000},
    })

    if "LITMUS_LOG_FILE" in os.environ:
        log.dump(os.environ["LITMUS_LOG_FILE"])

    failures = checker.check(log)
    checker.report(failures)

    assert failures == []
