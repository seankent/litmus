###########
# imports #
###########
from litmus import utils
from litmus.logic import Logic
import cocotb
import json


#######
# Log #
#######
class Log:

    ############
    # __init__ #
    ############
    def __init__(self):
        """
        Constructs an empty log.
        """
        self.entries = []

    ##########
    # append #
    ##########
    def append(self, name, sigs):
        """
        Adds an entry, stamped with the current simulation time.

        Args:
            name (str): The name of the worker the entry came from.
            sigs (dict): Signal name mapped to value.
        """
        self.entries.append({
            "time": cocotb.utils.get_sim_time("ns"),
            "name": name,
            "sigs": sigs,
        })

    ###########
    # __len__ #
    ###########
    def __len__(self):
        """
        Returns the number of entries.

        Returns:
            int: The number of entries.
        """
        return len(self.entries)

    ###############
    # __getitem__ #
    ###############
    def __getitem__(self, index):
        """
        Returns an entry or a range of entries.

        Args:
            index (int | slice): An entry position, or a slice of them.

        Returns:
            dict | list: The selected entries.
        """
        return self.entries[index]

    ##########
    # filter #
    ##########
    def filter(self, name):
        """
        Returns every entry from a given worker.

        Args:
            name (str): The worker name to match.

        Returns:
            list: Every entry from that worker.
        """
        entries = []

        for entry in self.entries:
            if entry["name"] == name:
                entries.append(entry)

        return entries

    ###########
    # jsonify #
    ###########
    def jsonify(self, value):
        """
        Returns a Logic as its binary literal.

        Args:
            value (Logic | list): The value to convert.

        Returns:
            str | list: The literal, shaped like the value.
        """
        if isinstance(value, list):
            values = []

            for v in value:
                values.append(self.jsonify(v))

            return values
        else:
            return value.bin()

    #############
    # unjsonify #
    #############
    def unjsonify(self, value):
        """
        Returns a binary literal as a Logic.

        Args:
            value (str | list): The literal to convert.

        Returns:
            Logic | list: The value, shaped like the literal.
        """
        if isinstance(value, list):
            values = []

            for v in value:
                values.append(self.unjsonify(v))

            return values
        else:
            return Logic.from_literal(value)

    ########
    # dump #
    ########
    def dump(self, path):
        """
        Writes the log to a JSON file.

        Args:
            path (str): Path to write to.
        """
        utils.write(path, json.dumps(self.entries, indent = 4, default = self.jsonify))

    ########
    # load #
    ########
    @classmethod
    def load(cls, path):
        """
        Returns a Log read back from a JSON file.

        Args:
            path (str): Path to the file.

        Returns:
            Log: The log, with signal values parsed back into Logic.
        """
        log = cls()

        for entry in json.loads(utils.read(path)):
            sigs = {}

            for sig in entry["sigs"]:
                sigs[sig] = log.unjsonify(entry["sigs"][sig])

            log.entries.append({
                "time": entry["time"],
                "name": entry["name"],
                "sigs": sigs,
            })

        return log
