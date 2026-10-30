###########
# imports #
###########
import cocotb
import litmus
import os
from priority_arbiter_checker import PriorityArbiterChecker
from priority_arbiter_coordinator import PriorityArbiterCoordinator
import task_graph


########
# test #
########
@cocotb.test()
async def test(top):
    coordinator = PriorityArbiterCoordinator({"N": 4})
    checker = PriorityArbiterChecker({"N": 4})

    log = litmus.Log()
    graph = task_graph.graph.copy()

    await coordinator.run({
        "clocker": {"period": 10},
        "req_driver": {"task_graph": graph},
        "monitor": {"log": log},
        "finisher": {"task_graph": graph, "drain": 2},
        "watchdog": {"timeout": 1000},
    })

    if "LITMUS_LOG_FILE" in os.environ:
        log.dump(os.environ["LITMUS_LOG_FILE"])

    failures = checker.check(log)
    checker.report(failures)

    assert failures == []
