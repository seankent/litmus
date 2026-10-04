###########
# imports #
###########
import litmus


#######
# req #
#######
def req(i):
    return litmus.Transaction(f"req{i}_driver", {})


##############
# task_graph #
##############
task_graph = litmus.TaskGraph()

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
    litmus.Delay("delayer", 1),
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

