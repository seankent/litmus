###########
# imports #
###########
import cocotb
import os
from d_ff_coordinator import DffCoordinator
from litmus.log import Log
import sanity_task_graph


########
# test #
########
@cocotb.test()
async def test(top):
    coordinator = DffCoordinator()

    log = Log()
    task_graph = sanity_task_graph.task_graph.copy()

    test = {
        "name": "sanity",
        "task_graph": task_graph,
        "log": log,
    }

    await coordinator.run(test)

    if "LITMUS_LOG_FILE" in os.environ:
        log.dump(os.environ["LITMUS_LOG_FILE"])
