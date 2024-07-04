import re


class Formula(object):
    """
    IMPORTANT NOTE: The formula object currently does no validation on the formula that you supply and it assumes
    you will supply it with a valid formula.

    For this reason, it's important that you: use . (point, full stop, period) as the decimal separator and ; as the
    argument separator.

    It is strongly recommended that you test your generated spreadsheets in LibreOffice because odswriter will not
    warn you of formula related mistakes.
    """

    def __init__(self, s):
        self.formula_string = s

    def __str__(self):
        s = self.formula_string
        # Remove = sign if present
        if s.startswith("="):
            s = s[1:]
        # Wrap cell refs in square brackets.
        s = re.sub(r"([A-Z]+[0-9]+(:[A-Z]+[0-9]+)?)", r"[\1]", s)
        # Place a . before cell references, so for example . A2 becomes .A2
        s = re.sub(r"([A-Z]+[0-9]+)(?!\()", r".\1", s)
        return "of:={}".format(s)
