from .state import State


# --- threat checks ---
def own_below_threat(state: State) -> bool:
    return state.own_tracked_altitude < state.other_tracked_altitude
#predicate w/ 1 clause

def own_above_threat(state: State) -> bool:
    return state.other_tracked_altitude < state.own_tracked_altitude
#predicate w/ 1 clause

# --- RA threshold logic ---
def positive_ra_alt_thresh(state: State, layer: int) -> int:
    if layer == 0:
        return state.positive_ra_alt_thresh_0
    elif layer == 1:
        return state.positive_ra_alt_thresh_1
    elif layer == 2:
        return state.positive_ra_alt_thresh_2
    elif layer == 3:
        return state.positive_ra_alt_thresh_3
    return 0
#4 predicates w/ 1 clause

def alim(state: State) -> int:
    return positive_ra_alt_thresh(state, state.altitude_layer_value)
#neither

def inhibit_biased_climb(state: State) -> int:
    return state.up_separation + 100 if state.climb_inhibit else state.up_separation
#1 predicate & 1 clause

def non_crossing_biased_climb(state: State) -> bool:
    if inhibit_biased_climb(state) > state.down_separation:
        return (not own_below_threat(state)) or (
            own_below_threat(state) and not (state.down_separation >= alim(state))
        )
    else:
        return (
            own_above_threat(state)
            and (state.current_vertical_sep >= 300)
            and (state.up_separation >= alim(state))
        )
#predicate w/ 1 clause


def non_crossing_biased_descend(state: State) -> bool:
    if inhibit_biased_climb(state) > state.down_separation:
        return (
            own_below_threat(state)
            and (state.current_vertical_sep >= 300)
            and (state.down_separation >= alim(state))
        )
    else:
        return (not own_above_threat(state)) or (
            own_above_threat(state) and (state.up_separation >= alim(state))
        )


def altitude_separation_test(state: State) -> int:
    alt_sep = 0

    if (
        state.high_confidence
        and (state.own_tracked_alt_rate <= 600)
        and (state.current_vertical_sep > 600)
    ) and (
        (
            (state.other_capability == 1)
            and (state.two_of_three_reports_valid and state.other_rac == 0)
        )
        or not (state.other_capability == 1)
    ):
        need_upward_RA = non_crossing_biased_climb(state) and own_below_threat(state)
        need_downward_RA = non_crossing_biased_descend(state) and own_above_threat(
            state
        )

        if need_upward_RA and need_downward_RA:
            alt_sep = 0  # No advisory
        elif need_upward_RA:
            alt_sep = 1  # Upward RA
        elif need_downward_RA:
            alt_sep = 2  # Downward RA
        else:
            alt_sep = 0

    return alt_sep
