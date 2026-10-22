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
    Transaction("rst_driver", {"rst": "1'b1"}),
    Transaction("rst_driver", {"rst": "1'b0"}),
    Transaction("d_driver", {"d": "8'ha0"}),
    Transaction("d_driver", {"d": "8'ha1"}),
    Transaction("d_driver", {"d": "8'ha2"}),
    Transaction("d_driver", {"d": "8'ha3"}),
    Delay("delayer", 1),
    Transaction("d_driver", {"d": "8'hb0"}),
    Delay("delayer", 1),
    Transaction("d_driver", {"d": "8'hb1"}),
    Delay("delayer", 1),
    Transaction("d_driver", {"d": "8'hb2"}),
    Delay("delayer", 1),
    Transaction("d_driver", {"d": "8'hb3"}),
])
