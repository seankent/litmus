###########
# imports #
###########
import sys
import litmus


#####
# N #
#####
N = 4


###########################
# PriorityArbiterChecker #
###########################
class PriorityArbiterChecker(litmus.Checker):

    #########
    # check #
    #########
    def check(self, log):
        """
        Returns the failures found in a log, which passes when every grant goes to the
        highest requester.

        Args:
            log (Log): The log to check.

        Returns:
            list: A description of each failure, empty if the log passes.
        """
        failures = []

        for entry in log.where("name", "monitor"):
            req = entry["sigs"]["req"]
            gnt = entry["sigs"]["gnt"]

            if req.undef():
                continue

            if gnt.undef():
                failures.append(f"monitor @ {entry['time']} ns (req {req}): gnt is undefined")
                continue

            if int(req) == 0:
                gnt_expected = litmus.Logic.from_int(0, N)
            else:
                gnt_expected = litmus.Logic.from_int(1 << (int(req).bit_length() - 1), N)

            if gnt != gnt_expected:
                failures.append(f"monitor @ {entry['time']} ns (req {req}): expected {gnt_expected}, got {gnt}")

        return failures


########
# main #
########
if __name__ == "__main__":
    log = litmus.Log.load(sys.argv[1] if len(sys.argv) > 1 else "gen/log.json")

    checker = PriorityArbiterChecker()
    failures = checker.check(log)

    checker.report(failures)

    sys.exit(1 if failures else 0)
