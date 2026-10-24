###########
# imports #
###########
from litmus import utils
from litmus.logic import Logic
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
    def append(self, entry):
        """
        Adds an entry.

        Args:
            entry (dict): The fields to record.
        """
        self.entries.append(entry)

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
        Returns an entry, or a log holding a range of them.

        Args:
            index (int | slice): An entry position, or a slice of them.

        Returns:
            dict | Log: The entry at that position, or a log holding the sliced entries.
        """
        if isinstance(index, slice):
            log = Log()
            log.entries = self.entries[index]

            return log

        return self.entries[index]

    ############
    # __iter__ #
    ############
    def __iter__(self):
        """
        Returns an iterator over the entries.

        Returns:
            iterator: An iterator over the entries.
        """
        return iter(self.entries)

    ##########
    # lookup #
    ##########
    def lookup(self, entry, path):
        """
        Returns whether an entry holds a path, and the value it holds there.

        Args:
            entry (dict): The entry to read.
            path (object | list): The key to read, or the keys to follow in turn.

        Returns:
            tuple: True and the value if the entry holds the path, False and None if not.
        """
        if not isinstance(path, list):
            path = [path]

        value = entry

        for key in path:
            if not isinstance(value, dict) or key not in value:
                return False, None

            value = value[key]

        return True, value

    #########
    # where #
    #########
    def where(self, path, values):
        """
        Returns a log holding every entry that holds a value at a path.

        Args:
            path (object | list): The key to read, or the keys to follow in turn.
            values (object | set): The value an entry must hold, or a set of values it
                must hold one of.

        Returns:
            Log: The matching entries, in the order they were logged.
        """
        log = Log()

        if isinstance(values, set):
            values = list(values)
        else:
            values = [values]

        for entry in self.entries:
            found, value = self.lookup(entry, path)

            if found and value in values:
                log.append(entry)

        return log

    ########
    # only #
    ########
    def only(self, path, values):
        """
        Returns the one entry that holds a value at a path.

        Args:
            path (object | list): The key to read, or the keys to follow in turn.
            values (object | set): The value an entry must hold, or a set of values it
                must hold one of.

        Returns:
            dict: The matching entry, or None if no entry matches.

        Raises:
            ValueError: More than one entry matches.
        """
        log = self.where(path, values)

        if len(log) > 1:
            raise ValueError(f"{len(log)} entries hold {values} at {path}, expected one.")

        if len(log) == 0:
            return None

        return log[0]

    ##########
    # select #
    ##########
    def select(self, path):
        """
        Returns the value every entry holds at a path.

        Args:
            path (object | list): The key to read, or the keys to follow in turn.

        Returns:
            list: The value at that path from each entry that holds one.
        """
        values = []

        for entry in self.entries:
            found, value = self.lookup(entry, path)

            if found:
                values.append(value)

        return values

    ############
    # distinct #
    ############
    def distinct(self, path):
        """
        Returns each value held at a path, once.

        Args:
            path (object | list): The key to read, or the keys to follow in turn.

        Returns:
            list: Each distinct value at that path, in the order it was first logged.
        """
        values = []

        for value in self.select(path):
            if value not in values:
                values.append(value)

        return values

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
        Returns a Verilog literal as a Logic, leaving any other value alone.

        Args:
            value (object): The value to convert.

        Returns:
            object: The value, shaped like the value, with every literal parsed.
        """
        if isinstance(value, dict):
            values = {}

            for key in value:
                values[key] = self.unjsonify(value[key])

            return values

        if isinstance(value, list):
            values = []

            for v in value:
                values.append(self.unjsonify(v))

            return values

        if isinstance(value, str):
            try:
                return Logic.from_literal(value)
            except ValueError:
                return value

        return value

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
            Log: The log, with every Verilog literal parsed back into Logic.
        """
        log = cls()

        for entry in json.loads(utils.read(path)):
            log.append(log.unjsonify(entry))

        return log
