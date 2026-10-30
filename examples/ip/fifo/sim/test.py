###########
# imports #
###########
import cocotb
import litmus
import os
import task_graph
from fifo_coordinator import FifoCoordinator
from fifo_checker import FifoChecker


########
# test #
########
@cocotb.test()
async def test(top):
    coordinator = FifoCoordinator()
    checker = FifoChecker()

    log = litmus.Log()
    graph = task_graph.graph.copy()

    await coordinator.run({
        "clocker": {"period": 10},
        "rst_driver": {"task_graph": graph},
        "delayer": {"task_graph": graph},
        "wr_driver": {"task_graph": graph},
        "rd_ready_randomizer": {
            "value_dist": litmus.dist.Choice({1: 30, 0: 70}),
            "duration_dist": litmus.dist.Uniform(1, 3),
        },
        "wr_monitor": {"log": log},
        "rd_monitor": {"log": log},
        "finisher": {"task_graph": graph, "drain": 50},
        "watchdog": {"timeout": 1000},
    })

    if "LITMUS_LOG_FILE" in os.environ:
        log.dump(os.environ["LITMUS_LOG_FILE"])

    failures = checker.check(log)
    checker.report(failures)

    assert failures == []
