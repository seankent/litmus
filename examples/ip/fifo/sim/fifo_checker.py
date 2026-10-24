###########
# imports #
###########
import sys
import litmus


###############
# FifoChecker #
###############
class FifoChecker(litmus.Checker):

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

        wr_log = log.where("name", "wr_monitor")
        rd_log = log.where("name", "rd_monitor")

        if len(wr_log) != len(rd_log):
            failures.append(f"rd_monitor: expected {len(wr_log)} entries, got {len(rd_log)}")

        for i in range(min(len(wr_log), len(rd_log))):
            wr_data = wr_log[i]["sigs"]["wr_data"]
            rd_data = rd_log[i]["sigs"]["rd_data"]

            if rd_data != wr_data:
                failures.append(f"rd_monitor[{i}] @ {rd_log[i]['time']} ns: expected {wr_data}, got {rd_data}")

        return failures


########
# main #
########
if __name__ == "__main__":
    log = litmus.Log.load(sys.argv[1] if len(sys.argv) > 1 else "gen/log.json")

    checker = FifoChecker()
    failures = checker.check(log)

    checker.report(failures)

    sys.exit(1 if failures else 0)
