###########
# imports #
###########
import litmus

##############
# task_graph #
##############
task_graph = litmus.TaskGraph()

task_graph.chain([
    litmus.Transaction("rst_driver", {"rst": litmus.Logic.from_literal("1'b1")}),
    [
        litmus.Transaction("rst_driver", {"rst": litmus.Logic.from_literal("1'b0")}),
        litmus.Transaction("d_driver", {"d": litmus.Logic.from_literal("8'h7")}),
    ],
    litmus.Transaction("d_driver", {"d": litmus.Logic.from_literal("8'h7")}),
    litmus.Transaction("d_driver", {"d": litmus.Logic.from_literal("8'h6")}),
    litmus.Transaction("d_driver", {"d": litmus.Logic.from_literal("8'h5")}),
    litmus.Transaction("d_driver", {"d": litmus.Logic.from_literal("8'h4")}),
    litmus.Delay("delayer", 1),
    litmus.Transaction("d_driver", {"d": litmus.Logic.from_literal("8'h3")}),
    litmus.Delay("delayer", 1),
    litmus.Transaction("d_driver", {"d": litmus.Logic.from_literal("8'h2")}),
    litmus.Transaction("d_driver", {"d": litmus.Logic.from_literal("8'h1")}),
    litmus.Transaction("d_driver", {"d": litmus.Logic.from_literal("8'h0")}),
    litmus.Delay("delayer", 2),
    litmus.Transaction("d_driver", {"d": litmus.Logic.from_literal("8'h1")}),
    litmus.Transaction("d_driver", {"d": litmus.Logic.from_literal("8'h2")}),
])
