###########
# imports #
###########
import cocotb
import litmus
import os
import sanity_task_graph
from sdp_ram_coordinator import SdpRamCoordinator


########
# test #
########
@cocotb.test()
async def test(top):
    coordinator = SdpRamCoordinator()

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
