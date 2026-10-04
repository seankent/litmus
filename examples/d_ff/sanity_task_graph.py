###########
# imports #
###########
from litmus.logic import Logic
from litmus.task import Delay, Transaction
from litmus.task_graph import TaskGraph

##############
# task_graph #
##############
task_graph = TaskGraph()

task_graph.chain([
    Transaction("rst_driver", {"rst": Logic.from_literal("1'b1")}),
    [
        Transaction("rst_driver", {"rst": Logic.from_literal("1'b0")}),
        Transaction("d_driver", {"d": Logic.from_literal("8'h7")}),
    ],
    Transaction("d_driver", {"d": Logic.from_literal("8'h7")}),
    Transaction("d_driver", {"d": Logic.from_literal("8'h6")}),
    Transaction("d_driver", {"d": Logic.from_literal("8'h5")}),
    Transaction("d_driver", {"d": Logic.from_literal("8'h4")}),
    Delay("delayer", 1),
    Transaction("d_driver", {"d": Logic.from_literal("8'h3")}),
    Delay("delayer", 1),
    Transaction("d_driver", {"d": Logic.from_literal("8'h2")}),
    Transaction("d_driver", {"d": Logic.from_literal("8'h1")}),
    Transaction("d_driver", {"d": Logic.from_literal("8'h0")}),
    Delay("delayer", 2),
    Transaction("d_driver", {"d": Logic.from_literal("8'h1")}),
    Transaction("d_driver", {"d": Logic.from_literal("8'h2")}),
])
