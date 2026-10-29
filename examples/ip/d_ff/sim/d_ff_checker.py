###########
# imports #
###########
import litmus


##############
# DffChecker #
##############
class DffChecker(litmus.Checker):

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

        q_expected = None

        for entry in log.where("name", "monitor"):
            rst = entry["sigs"]["rst"]
            en = entry["sigs"]["en"]
            d = entry["sigs"]["d"]
            q = entry["sigs"]["q"]

            if q_expected is not None and q != q_expected:
                failures.append(f"monitor @ {entry['time']} ns: expected {q_expected}, got {q}")

            if rst:
                q_expected = litmus.Logic.from_int(self.params["RESET_VALUE"], self.params["WIDTH"])
            elif en:
                q_expected = d

        return failures
