###########
# imports #
###########
import cocotb
import litmus
import os
import task_graph
from sdp_ram_checker import SdpRamChecker
from sdp_ram_coordinator import SdpRamCoordinator


########
# test #
########
@cocotb.test()
async def test(top):
    params = {"WIDTH": 8, "DEPTH": 4}

    coordinator = SdpRamCoordinator(params)
    checker = SdpRamChecker(params)

    log = litmus.Log()
    graph = task_graph.graph.copy()

    await coordinator.run({
        "clocker": {"period": 10},
        "preloader": {"task_graph": graph},
        "wr_driver": {"task_graph": graph},
        "rd_driver": {"task_graph": graph},
        "wr_monitor": {"log": log},
        "rd_monitor": {"log": log},
        "sampler": {"task_graph": graph, "log": log},
        "finisher": {"task_graph": graph, "drain": 5},
        "watchdog": {"timeout": 1000},
    })

    if "LITMUS_LOG_FILE" in os.environ:
        log.dump(os.environ["LITMUS_LOG_FILE"])

    failures = checker.check(log)
    checker.report(failures)

    assert failures == []
