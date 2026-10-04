###########
# imports #
###########
import litmus


######
# wr #
######
def wr(addr, data):
    return litmus.Transaction("ram_driver", {
        "we": litmus.Logic.from_literal("1'b1"),
        "addr": litmus.Logic.from_int(addr, 2),
        "wr_data": litmus.Logic.from_int(data, 8),
    })


######
# rd #
######
def rd(addr):
    return litmus.Transaction("ram_driver", {
        "we": litmus.Logic.from_literal("1'b0"),
        "addr": litmus.Logic.from_int(addr, 2),
        "wr_data": litmus.Logic.from_int(0, 8),
    })


##############
# task_graph #
##############
task_graph = litmus.TaskGraph()

task_graph.chain([
    litmus.Transaction("init_driver", {
        "memory": [
            litmus.Logic.from_int(0x01, 8),
            litmus.Logic.from_int(0x02, 8),
            litmus.Logic.from_int(0x03, 8),
            litmus.Logic.from_int(0x04, 8),
        ],
    }),
    litmus.Sample("sampler"),
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
    litmus.Sample("sampler"),
])
