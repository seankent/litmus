###########
# imports #
###########
import cocotb
import litmus
import os
from ram_coordinator import RamCoordinator
import sanity_task_graph


########
# test #
########
@cocotb.test()
async def test(top):
    coordinator = RamCoordinator()

    log = litmus.Log()
    task_graph = sanity_task_graph.task_graph.copy()

    test = {
        "name": "sanity",
        "task_graph": task_graph,
        "log": log,
    }

    await coordinator.run(test)

    if "LITMUS_LOG_FILE" in os.environ:
        log.dump(os.environ["LITMUS_LOG_FILE"])
