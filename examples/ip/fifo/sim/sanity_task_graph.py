###########
# imports #
###########
import litmus


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
    litmus.Transaction("rst_driver", {"rst": litmus.Logic.from_literal("1'b1")}),
    litmus.Transaction("rst_driver", {"rst": litmus.Logic.from_literal("1'b0")}),
])

task_graph.chain([
    wr(0xa0),
    wr(0xa1),
    wr(0xa2),
    wr(0xa3),
    wr(0xa4),
    wr(0xa5),
])

task_graph.then(task_graph.tail("rst_driver"), task_graph.head("wr_driver"))
