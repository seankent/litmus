###########
# imports #
###########
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
