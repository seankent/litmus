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
        """
        self.entries = []

    ##########
    # append #
    ##########
    def append(self, name, sigs):
        """
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
        """
        return len(self.entries)

    ###############
    # __getitem__ #
    ###############
    def __getitem__(self, index):
        """
        """
        return self.entries[index]

    ##########
    # filter #
    ##########
    def filter(self, name):
        """
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
