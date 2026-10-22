###########
# imports #
###########
from litmus import Delay
from litmus import TaskGraph
from litmus import Transaction

##############
# task_graph #
##############
task_graph = TaskGraph()

task_graph.chain([
    [
        Transaction("req3_driver", {}),
        Transaction("req0_driver", {}),
    ],
    [
        Transaction("req3_driver", {}),
        Transaction("req2_driver", {}),
        Transaction("req1_driver", {}),
        Transaction("req0_driver", {}),
    ],
    [
        Transaction("req1_driver", {}),
    ],
    Delay("delayer", 1),
    [
        Transaction("req2_driver", {}),
        Transaction("req1_driver", {}),
    ],
    [
        Transaction("req3_driver", {}),
        Transaction("req2_driver", {}),
        Transaction("req0_driver", {}),
    ],
])
