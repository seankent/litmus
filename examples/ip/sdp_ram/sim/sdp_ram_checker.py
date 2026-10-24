###########
# imports #
###########
import litmus


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

        memory = [litmus.Logic("x"*8)]*4

        for time in log.distinct("time"):
            timeslot_log = log.where("time", time)

            sampler_entry = timeslot_log.only("name", "sampler")
            wr_entry = timeslot_log.only("name", "wr_monitor")
            rd_entry = timeslot_log.only("name", "rd_monitor")

            if sampler_entry is not None:
                memory_actual = sampler_entry["sigs"]["memory"]

                if memory_actual != memory:
                    failures.append(f"sampler @ {time} ns: expected {memory}, got {memory_actual}")

            if rd_entry is not None:
                rd_data_expected = memory[int(rd_entry["sigs"]["rd_addr"])]
                rd_data_actual = rd_entry["sigs"]["rd_data"]

                if rd_data_actual != rd_data_expected:
                    failures.append(f"rd_monitor @ {time} ns: expected {rd_data_expected}, got {rd_data_actual}")

            if wr_entry is not None:
                memory[int(wr_entry["sigs"]["wr_addr"])] = wr_entry["sigs"]["wr_data"]

        return failures


