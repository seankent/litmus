###########
# imports #
###########
from litmus import TaskGraph
from litmus import Transaction
from litmus import Delay 

#########
# graph #
#########
graph = TaskGraph()

graph.chain([
    Transaction("rst_driver", {"rst": "1'b1"}),
    Transaction("rst_driver", {"rst": "1'b0"}),
    Transaction("wr_driver", {"wr_data": "8'ha0"}),
    Transaction("wr_driver", {"wr_data": "8'ha1"}),
    Transaction("wr_driver", {"wr_data": "8'ha2"}),
    Transaction("wr_driver", {"wr_data": "8'ha3"}),
    Delay("delayer", 1),
    Transaction("wr_driver", {"wr_data": "8'ha4"}),
    Transaction("wr_driver", {"wr_data": "8'ha5"}),
    Transaction("wr_driver", {"wr_data": "8'ha6"}),
    Transaction("wr_driver", {"wr_data": "8'ha7"}),
    Delay("delayer", 2),
    Transaction("wr_driver", {"wr_data": "8'ha8"}),
    Transaction("wr_driver", {"wr_data": "8'ha9"}),
    Transaction("wr_driver", {"wr_data": "8'haa"}),
    Transaction("wr_driver", {"wr_data": "8'hab"}),
    Delay("delayer", 1),
    Transaction("wr_driver", {"wr_data": "8'hac"}),
    Transaction("wr_driver", {"wr_data": "8'had"}),
    Transaction("wr_driver", {"wr_data": "8'hae"}),
    Transaction("wr_driver", {"wr_data": "8'haf"}),
])
