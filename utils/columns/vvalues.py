class Size:
    """Possible values for the size of a bottle of wine."""

    @staticmethod
    def get_mapping_inverse():
        """Mapping from size name to size in liters."""
        return {
            "HALF_BOTTLE": 0.375,
            "HALF_LITER": 0.5,
            "BOTTLE": 0.75,
            "LITER": 1,
            "MAGNUM": 1.5,
            "JEROBOAM": 3,
            "REHOBOAM": 4.5,
            "BORDEAUX_JEROBOAM": 5,
            "MATHUSALEM": 6,
            "IMPERIAL": 6,
            "SALMANAZAR": 9,
            "BALTHAZAR": 12,
            "NEBUCHADNEZZAR": 15,
            "MELCHIOR": 18,
            "SOLOMON": 20,
            "SOVEREIGN": 25,
            "GOLIATH": 27,
            "MELCHIZEDEK": 30,
        }

    @classmethod
    def get(cls):
        """Get possible size names"""
        return list(cls.get_mapping_inverse().keys())

    @classmethod
    def get_values(cls):
        """Get possible sizes in liters"""
        return list(cls.get_mapping_inverse().values())

    @classmethod
    def get_mapping(cls):
        """Mapping from size in liters to size name."""
        d = {v: k for k, v in cls.get_mapping_inverse().items()}
        d[6] = "MATHUSALEM"
        return d

    @classmethod
    def get_mapping_alternate(cls):
        """Mapping from size in liters to size name.
        Alternative name for 6 liters bottle:
        IMPERIAL instead of MATHUSALEM
        """
        d = {v: k for k, v in cls.get_mapping_inverse().items()}
        d[6] = "IMPERIAL"
        return d


class Type:
    @staticmethod
    def get():
        return ["RED", "WHITE", "SPARKLING", "SPARKLING_ROSE", "ROSE", "DESSERT"]
