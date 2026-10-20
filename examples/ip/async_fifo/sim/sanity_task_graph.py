###########
# imports #
###########
import litmus


########
# init #
########
def init(wr_prob, rd_prob, lo, hi):
    return litmus.Transaction("init_driver", {
        "wr_stall_prob": litmus.Logic.from_int(wr_prob, 32),
        "wr_stall_min": litmus.Logic.from_int(lo, 32),
        "wr_stall_max": litmus.Logic.from_int(hi, 32),
        "rd_stall_prob": litmus.Logic.from_int(rd_prob, 32),
        "rd_stall_min": litmus.Logic.from_int(lo, 32),
        "rd_stall_max": litmus.Logic.from_int(hi, 32),
    })


######
# wr #
######
def wr(data):
    return litmus.Transaction("wr_driver", {
        "wr_data": litmus.Logic.from_int(data, 8),
    })


##############
# task_graph #
##############
task_graph = litmus.TaskGraph()

task_graph.chain([
    init(50, 50, 1, 3),
    [
        litmus.Transaction("wr_rst_driver", {"wr_rst": litmus.Logic.from_literal("1'b1")}),
        litmus.Transaction("rd_rst_driver", {"rd_rst": litmus.Logic.from_literal("1'b1")}),
    ],
    [
        litmus.Delay("wr_delayer", 5),
        litmus.Delay("rd_delayer", 5),
    ],
    [
        litmus.Transaction("wr_rst_driver", {"wr_rst": litmus.Logic.from_literal("1'b0")}),
        litmus.Transaction("rd_rst_driver", {"rd_rst": litmus.Logic.from_literal("1'b0")}),
    ],
    [
        litmus.Delay("wr_delayer", 5),
        litmus.Delay("rd_delayer", 5),
    ],
    wr(0xa0),
    wr(0xa1),
    wr(0xa2),
    wr(0xa3),
    wr(0xa4),
    wr(0xa5),
])

