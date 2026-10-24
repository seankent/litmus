###########
# Checker #
###########
class Checker:

    #########
    # check #
    #########
    def check(self, log):
        """
        Returns the failures found in a log, overridden by each subclass.

        Args:
            log (Log): The log to check.

        Returns:
            list: A description of each failure, empty if the log passes.
        """
        return []

    ##########
    # report #
    ##########
    def report(self, failures):
        """
        Prints every failure and the verdict.

        Args:
            failures (list): A description of each failure.
        """
        for failure in failures:
            print(failure)

        if failures:
            print("FAIL")
        else:
            print("PASS")
