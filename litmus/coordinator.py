###########
# imports #
###########
import cocotb


###############
# Coordinator #
###############
class Coordinator:

    ############
    # __init__ #
    ############
    def __init__(self):
        """
        """
        self.workers = {}

        self.init()

    ########
    # init #
    ########
    def init(self):
        """
        """
        pass

    ############
    # register #
    ############
    def register(self, worker):
        """
        """
        self.workers[worker.name] = worker 

    ########
    # args #
    ########
    def args(self, test):
        """
        """
        return {}

    #######
    # run #
    #######
    async def run(self, test):
        """
        """
        args = self.args(test)

        coros = []

        for name in self.workers:
            coros.append(self.workers[name].run(**args.get(name, {})))

        await cocotb.triggers.select(*coros)
