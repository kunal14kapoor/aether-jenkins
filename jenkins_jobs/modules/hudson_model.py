# Representation of the hudson.model.Result class

SUCCESS = {"name": "SUCCESS", "ordinal": "0", "color": "BLUE", "complete": True}

UNSTABLE = {"name": "UNSTABLE", "ordinal": "1", "color": "YELLOW", "complete": True}

FAILURE = {"name": "FAILURE", "ordinal": "2", "color": "RED", "complete": True}

NOTBUILD = {"name": "NOT_BUILD", "ordinal": "3", "color": "NOTBUILD", "complete": False}

ABORTED = {"name": "ABORTED", "ordinal": "4", "color": "ABORTED", "complete": False}

THRESHOLDS = {
    "SUCCESS": SUCCESS,
    "UNSTABLE": UNSTABLE,
    "FAILURE": FAILURE,
    "NOT_BUILD": NOTBUILD,
    "ABORTED": ABORTED,
}
