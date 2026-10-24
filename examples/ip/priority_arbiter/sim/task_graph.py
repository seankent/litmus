###########
# imports #
###########
from litmus import TaskGraph
from litmus import Transaction

#########
# graph #
#########
graph = TaskGraph()

graph.chain([
    Transaction("req_driver", {"req": "4'b1001"}),
    Transaction("req_driver", {"req": "4'b1111"}),
    Transaction("req_driver", {"req": "4'b0010"}),
    Transaction("req_driver", {"req": "4'b0000"}),
    Transaction("req_driver", {"req": "4'b0110"}),
    Transaction("req_driver", {"req": "4'b1101"}),
    Transaction("req_driver", {"req": "4'b0000"}),
])
