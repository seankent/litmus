###########
# imports #
###########
from litmus import Sample
from litmus import TaskGraph
from litmus import Transaction

##############
# task_graph #
##############
task_graph = TaskGraph()

task_graph.chain([
    Transaction("init_driver", {"memory": ["8'h01", "8'h02", "8'h03", "8'h04"]}),
    Sample("sampler"),
    Transaction("rd_driver", {"rd_addr": "2'h0"}),
    Transaction("rd_driver", {"rd_addr": "2'h1"}),
    Transaction("rd_driver", {"rd_addr": "2'h2"}),
    Transaction("rd_driver", {"rd_addr": "2'h3"}),
    Transaction("wr_driver", {"wr_addr": "2'h0", "wr_data": "8'haa"}),
    [
        Transaction("wr_driver", {"wr_addr": "2'h1", "wr_data": "8'hbb"}),
        Transaction("rd_driver", {"rd_addr": "2'h0"}),
    ],
    [
        Transaction("wr_driver", {"wr_addr": "2'h2", "wr_data": "8'hcc"}),
        Transaction("rd_driver", {"rd_addr": "2'h1"}),
    ],
    [
        Transaction("wr_driver", {"wr_addr": "2'h3", "wr_data": "8'hdd"}),
        Transaction("rd_driver", {"rd_addr": "2'h2"}),
    ],
    Transaction("rd_driver", {"rd_addr": "2'h3"}),
    Sample("sampler"),
])
