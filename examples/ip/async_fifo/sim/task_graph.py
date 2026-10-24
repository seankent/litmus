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
    Transaction("init_driver", {
        "wr_stall_prob": "32'd50",
        "wr_stall_min": "32'd1",
        "wr_stall_max": "32'd3",
        "rd_stall_prob": "32'd50",
        "rd_stall_min": "32'd1",
        "rd_stall_max": "32'd3",
    }),
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
    Transaction("wr_driver", {"wr_data": "8'ha4"}),
    Transaction("wr_driver", {"wr_data": "8'ha5"}),
])
