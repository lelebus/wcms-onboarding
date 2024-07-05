def name_to_size():
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


def size_to_name():
    d = {v: k for k, v in name_to_size().items()}
    d[6] = "MATHUSALEM"
    return d


def size_to_name_alternate():
    d = {v: k for k, v in name_to_size().items()}
    d[6] = "IMPERIAL"
    return d
