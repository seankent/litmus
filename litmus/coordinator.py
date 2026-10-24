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
    def __init__(self, params = None):
        """
        Constructs a coordinator, calling init() to register its workers.

        Args:
            params (dict): The parameters to register the workers from.
        """
        self.params = params or {}
        self.workers = {}

        self.init()

    ########
    # init #
    ########
    def init(self):
        """
        Registers the workers, overridden by each subclass.
        """
        pass

    ############
    # register #
    ############
    def register(self, worker):
        """
        Adds a worker, keyed by its name.

        Args:
            worker (Worker): The worker to add.
        """
        self.workers[worker.name] = worker 

    #######
    # run #
    #######
    async def run(self, args):
        """
        Runs the test, ending when the first worker finishes and cancelling the rest.

        Args:
            args (dict): Worker name mapped to the args for its run().
        """
        coros = []

        for name in self.workers:
            coros.append(self.workers[name].run(**args.get(name, {})))

        await cocotb.triggers.select(*coros)
