from ..state import StateEnum

LABEL_TEST_MAP = {
    StateEnum.UNCONFIGURED: '<span style="color: gray"><i>Unconfigured</i></span>',
    StateEnum.INACTIVE: '<span style="color: blue"><i>Inactive</i></span>',
    StateEnum.ACTIVE: '<span style="color: green"><b>Active</b></span>',
    StateEnum.FINALIZED: '<span style="color: black"><i>Finalised</i></span>',
    StateEnum.ERROR: '<span style="color: red"><b>Error</b></span>',
}


def get_state_label_text(state: StateEnum) -> str:
    return LABEL_TEST_MAP[state]
