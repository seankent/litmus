###########
# imports #
###########
from litmus import utils
from litmus.logic import Logic
import cocotb


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
        Returns a Logic as its binary literal, for JSON to serialize.

        Args:
            value (Logic): The value to convert.

        Returns:
            str: The binary literal.
        """
        if isinstance(value, Logic):
            return value.bin()
        else:
            raise TypeError(f"Cannot serialize {type(value).__name__} to JSON.")

    ########
    # dump #
    ########
    def dump(self, path):
        """
        Writes the log to a JSON file.

        Args:
            path (str): Path to write to.
        """
        utils.write_json(path, self.entries, default = self.jsonify)
