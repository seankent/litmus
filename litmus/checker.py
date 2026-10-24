###########
# Checker #
###########
class Checker:

    #########
    # check #
    #########
    def check(self, *args, **kwargs):
        """
        Returns the failures found, overridden by each subclass.

        Returns:
            list: A description of each failure, empty if nothing failed.
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
