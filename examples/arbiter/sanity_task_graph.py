###########
# imports #
###########
from litmus.task import Transaction, Delay
from litmus.task_graph import TaskGraph


#######
# req #
#######
def req(i):
    return Transaction(f"req{i}_driver", {})


##############
# task_graph #
##############
task_graph = TaskGraph()

task_graph.chain([
    [
        req(3),
        req(0),
    ],
    [
        req(3),
        req(2),
        req(1),
        req(0),
    ],
    [
        req(1),
    ],
    Delay("delayer", 1),
    [
        req(2),
        req(1),
    ],
    [
        req(3),
        req(2),
        req(0),
    ],
])

