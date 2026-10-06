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
        Constructs a coordinator, calling init() to register its workers.
        """
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

    ########
    # args #
    ########
    def args(self, test):
        """
        Returns the keyword arguments for each worker, overridden by each subclass.

        Args:
            test (dict): The test being run.

        Returns:
            dict: Worker name mapped to the keyword arguments for its run().
        """
        return {}

    #######
    # run #
    #######
    async def run(self, test):
        """
        Runs the test, ending when the first worker finishes and cancelling the rest.

        Args:
            test (dict): The test to run.
        """
        args = self.args(test)

        coros = []

        for name in self.workers:
            coros.append(self.workers[name].run(**args.get(name, {})))

        await cocotb.triggers.select(*coros)
