###########
# imports #
###########
import litmus


###############
# SdpRamModel #
###############
class SdpRamModel:

    ############
    # __init__ #
    ############
    def __init__(self, params = None):
        """
        Constructs a model of the RAM.

        Args:
            params (dict): The WIDTH and DEPTH of the RAM.
        """
        self.params = params or {}

        self.init()

    ########
    # init #
    ########
    def init(self):
        """
        Resets every location to undefined.
        """
        self.memory = [litmus.Logic("x"*self.params["WIDTH"])]*self.params["DEPTH"]

    ########
    # load #
    ########
    def load(self, memory):
        """
        Replaces the whole memory.

        Args:
            memory (list): The value of each location.
        """
        self.memory = list(memory)

    #########
    # write #
    #########
    def write(self, addr, data):
        """
        Writes data to an address.

        Args:
            addr (Logic): The address to write.
            data (Logic): The data to write there.
        """
        self.memory[int(addr)] = data

    ########
    # read #
    ########
    def read(self, addr):
        """
        Returns the data a read from an address should return.

        Args:
            addr (Logic): The address to read.

        Returns:
            Logic: The data held at that address.
        """
        return self.memory[int(addr)]


#################
# SdpRamChecker #
#################
class SdpRamChecker(litmus.Checker):

    #########
    # check #
    #########
    def check(self, log):
        """
        Returns the failures found in a log.

        Args:
            log (Log): The log to check.

        Returns:
            list: A description of each failure, empty if the log passes.
        """
        failures = []

        model = SdpRamModel(self.params)

        sampler_entry = log.only("name", "sampler")

        if sampler_entry is not None:
            model.load(sampler_entry["sigs"]["memory"])

        for time in log.distinct("time"):
            timeslot_log = log.where("time", time)

            wr_entry = timeslot_log.only("name", "wr_monitor")
            rd_entry = timeslot_log.only("name", "rd_monitor")

            if rd_entry is not None:
                rd_data_expected = model.read(rd_entry["sigs"]["rd_addr"])
                rd_data_actual = rd_entry["sigs"]["rd_data"]

                if rd_data_actual != rd_data_expected:
                    failures.append(f"rd_monitor @ {time} ns: expected {rd_data_expected}, got {rd_data_actual}")

            if wr_entry is not None:
                model.write(wr_entry["sigs"]["wr_addr"], wr_entry["sigs"]["wr_data"])

        return failures
