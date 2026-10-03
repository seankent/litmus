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
    Transaction("rst", {"rst": Logic.from_literal("1'b1")}),
    [
        Transaction("rst", {"rst": Logic.from_literal("1'b0")}),
        Transaction("d", {"d": Logic.from_literal("8'h7")}),
    ],
    Transaction("d", {"d": Logic.from_literal("8'h7")}),
    Transaction("d", {"d": Logic.from_literal("8'h6")}),
    Transaction("d", {"d": Logic.from_literal("8'h5")}),
    Transaction("d", {"d": Logic.from_literal("8'h4")}),
    Delay("delay", 1),
    Transaction("d", {"d": Logic.from_literal("8'h3")}),
    Delay("delay", 1),
    Transaction("d", {"d": Logic.from_literal("8'h2")}),
    Transaction("d", {"d": Logic.from_literal("8'h1")}),
    Transaction("d", {"d": Logic.from_literal("8'h0")}),
    Delay("delay", 2),
    Transaction("d", {"d": Logic.from_literal("8'h1")}),
    Transaction("d", {"d": Logic.from_literal("8'h2")}),
])
