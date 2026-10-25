###########
# imports #
###########
from litmus import Delay
from litmus import TaskGraph
from litmus import Transaction

#########
# graph #
#########
graph = TaskGraph()

graph.chain([
    [
        Transaction("wr_rst_driver", {"wr_rst": "1'b1"}),
        Transaction("rd_rst_driver", {"rd_rst": "1'b1"}),
    ],
    [
        Delay("wr_delayer", 5),
        Delay("rd_delayer", 5),
    ],
    [
        Transaction("wr_rst_driver", {"wr_rst": "1'b0"}),
        Transaction("rd_rst_driver", {"rd_rst": "1'b0"}),
    ],
    [
        Delay("wr_delayer", 5),
        Delay("rd_delayer", 5),
    ],

    Transaction("wr_driver", {"wr_data": "8'ha0"}),
    Transaction("wr_driver", {"wr_data": "8'ha1"}),
    Transaction("wr_driver", {"wr_data": "8'ha2"}),
    Transaction("wr_driver", {"wr_data": "8'ha3"}),
    Delay("wr_delayer", 1),
    Transaction("wr_driver", {"wr_data": "8'ha4"}),
    Transaction("wr_driver", {"wr_data": "8'ha5"}),
    Transaction("wr_driver", {"wr_data": "8'ha6"}),
    Transaction("wr_driver", {"wr_data": "8'ha7"}),
    Delay("wr_delayer", 2),
    Transaction("wr_driver", {"wr_data": "8'ha8"}),
    Transaction("wr_driver", {"wr_data": "8'ha9"}),
    Transaction("wr_driver", {"wr_data": "8'haa"}),
    Transaction("wr_driver", {"wr_data": "8'hab"}),
    Delay("wr_delayer", 1),
    Transaction("wr_driver", {"wr_data": "8'hac"}),
    Transaction("wr_driver", {"wr_data": "8'had"}),
    Transaction("wr_driver", {"wr_data": "8'hae"}),
    Transaction("wr_driver", {"wr_data": "8'haf"}),
])
