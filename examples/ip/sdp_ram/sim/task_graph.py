###########
# imports #
###########
from litmus import Sample
from litmus import TaskGraph
from litmus import Transaction

#########
# graph #
#########
graph = TaskGraph()

graph.chain([
    Sample("sampler"),
    Transaction("wr_driver", {"wr_addr": "2'h0", "wr_data": "8'haa"}),
    Transaction("wr_driver", {"wr_addr": "2'h1", "wr_data": "8'hbb"}),
    Transaction("wr_driver", {"wr_addr": "2'h2", "wr_data": "8'hcc"}),
    Transaction("wr_driver", {"wr_addr": "2'h3", "wr_data": "8'hdd"}),
    Transaction("rd_driver", {"rd_addr": "2'h0"}),
    Transaction("rd_driver", {"rd_addr": "2'h1"}),
    Transaction("rd_driver", {"rd_addr": "2'h2"}),
    Transaction("rd_driver", {"rd_addr": "2'h3"}),
    Transaction("wr_driver", {"wr_addr": "2'h0", "wr_data": "8'h01"}),
    [
        Transaction("wr_driver", {"wr_addr": "2'h1", "wr_data": "8'h23"}),
        Transaction("rd_driver", {"rd_addr": "2'h0"}),
    ],
    [
        Transaction("wr_driver", {"wr_addr": "2'h2", "wr_data": "8'h45"}),
        Transaction("rd_driver", {"rd_addr": "2'h1"}),
    ],
    [
        Transaction("wr_driver", {"wr_addr": "2'h3", "wr_data": "8'h67"}),
        Transaction("rd_driver", {"rd_addr": "2'h2"}),
    ],
    Transaction("rd_driver", {"rd_addr": "2'h3"}),
    Sample("sampler"),
])
