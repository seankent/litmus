###########
# imports #
###########
from litmus.logic import Logic
from litmus.task import Sample, Transaction
from litmus.task_graph import TaskGraph


######
# wr #
######
def wr(addr, data):
    return Transaction("ram_driver", {
        "we": Logic.from_literal("1'b1"),
        "addr": Logic.from_int(addr, 2),
        "wr_data": Logic.from_int(data, 8),
    })


######
# rd #
######
def rd(addr):
    return Transaction("ram_driver", {
        "we": Logic.from_literal("1'b0"),
        "addr": Logic.from_int(addr, 2),
        "wr_data": Logic.from_int(0, 8),
    })


##############
# task_graph #
##############
task_graph = TaskGraph()

task_graph.chain([
    Transaction("init_driver", {
        "memory": [
            Logic.from_int(0x01, 8),
            Logic.from_int(0x02, 8),
            Logic.from_int(0x03, 8),
            Logic.from_int(0x04, 8),
        ],
    }),
    Sample("sampler"),
    rd(0),
    rd(1),
    rd(2),
    rd(3),
    wr(0, 0xaa),
    wr(1, 0xbb),
    wr(2, 0xcc),
    wr(3, 0xdd),
    rd(0),
    rd(1),
    rd(2),
    rd(3),
    Sample("sampler"),
])
