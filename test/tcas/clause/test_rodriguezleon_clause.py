from src.tcas.state import State
from src.tcas.main import altitude_separation_test, alim, inhibit_biased_climb, non_crossing_biased_climb, non_crossing_biased_descend, own_above_threat, own_below_threat, positive_ra_alt_thresh



def test_own_below_threat_true_and_false():
    state_below = State(
        current_vertical_sep=0,
        high_confidence=0,
        two_of_three_reports_valid=0,
        own_tracked_altitude=1000,
        own_tracked_alt_rate=0,
        other_tracked_altitude=2000,
        altitude_layer_value=0,
        up_separation=0,
        down_separation=0,
        other_rac=0,
        other_capability=0,
        climb_inhibit=0,
    )
    assert own_below_threat(state_below) is True

    state_equal = State(
        current_vertical_sep=0,
        high_confidence=0,
        two_of_three_reports_valid=0,
        own_tracked_altitude=2000,
        own_tracked_alt_rate=0,
        other_tracked_altitude=2000,
        altitude_layer_value=0,
        up_separation=0,
        down_separation=0,
        other_rac=0,
        other_capability=0,
        climb_inhibit=0,
    )
    assert own_below_threat(state_equal) is False


def test_own_above_threat_true_and_false():
    state_above = State(
        current_vertical_sep=0,
        high_confidence=0,
        two_of_three_reports_valid=0,
        own_tracked_altitude=3000,
        own_tracked_alt_rate=0,
        other_tracked_altitude=2000,
        altitude_layer_value=0,
        up_separation=0,
        down_separation=0,
        other_rac=0,
        other_capability=0,
        climb_inhibit=0,
    )
    assert own_above_threat(state_above) is True

    state_equal = State(
        current_vertical_sep=0,
        high_confidence=0,
        two_of_three_reports_valid=0,
        own_tracked_altitude=2000,
        own_tracked_alt_rate=0,
        other_tracked_altitude=2000,
        altitude_layer_value=0,
        up_separation=0,
        down_separation=0,
        other_rac=0,
        other_capability=0,
        climb_inhibit=0,
    )
    assert own_above_threat(state_equal) is False


def test_positive_ra_alt_thresh_and_alim_values():
    state = State(
        current_vertical_sep=0,
        high_confidence=0,
        two_of_three_reports_valid=0,
        own_tracked_altitude=0,
        own_tracked_alt_rate=0,
        other_tracked_altitude=0,
        altitude_layer_value=0,
        up_separation=0,
        down_separation=0,
        other_rac=0,
        other_capability=0,
        climb_inhibit=0,
    )

    assert positive_ra_alt_thresh(state, 0) == state.positive_ra_alt_thresh_0
    assert positive_ra_alt_thresh(state, 1) == state.positive_ra_alt_thresh_1
    assert positive_ra_alt_thresh(state, 2) == state.positive_ra_alt_thresh_2
    assert positive_ra_alt_thresh(state, 3) == state.positive_ra_alt_thresh_3
    assert positive_ra_alt_thresh(state, 999) == 0
    assert alim(state) == state.positive_ra_alt_thresh_0


def test_inhibit_biased_climb_behavior():
    state = State(
        current_vertical_sep=0,
        high_confidence=0,
        two_of_three_reports_valid=0,
        own_tracked_altitude=0,
        own_tracked_alt_rate=0,
        other_tracked_altitude=0,
        altitude_layer_value=0,
        up_separation=400,
        down_separation=0,
        other_rac=0,
        other_capability=0,
        climb_inhibit=0,
    )
    assert inhibit_biased_climb(state) == 400

    state.climb_inhibit = 1
    assert inhibit_biased_climb(state) == 500


def test_non_crossing_biased_climb_clauses():
    # Case 1: inhibit bias greater than down separation, own not below threat => True
    state1 = State(
        current_vertical_sep=0,
        high_confidence=0,
        two_of_three_reports_valid=0,
        own_tracked_altitude=3000,
        own_tracked_alt_rate=0,
        other_tracked_altitude=2000,
        altitude_layer_value=0,
        up_separation=500,
        down_separation=400,
        other_rac=0,
        other_capability=0,
        climb_inhibit=1,
    )
    assert non_crossing_biased_climb(state1) is True

    # Case 2: inhibit bias greater than down separation, own below threat and down separation >= alim => False
    state2 = State(
        current_vertical_sep=0,
        high_confidence=0,
        two_of_three_reports_valid=0,
        own_tracked_altitude=1000,
        own_tracked_alt_rate=0,
        other_tracked_altitude=3000,
        altitude_layer_value=0,
        up_separation=500,
        down_separation=17000,
        other_rac=0,
        other_capability=0,
        climb_inhibit=1,
    )
    assert non_crossing_biased_climb(state2) is False

    # Case 3: inhibit bias less than or equal down separation and climb conditions met => True
    state3 = State(
        current_vertical_sep=400,
        high_confidence=0,
        two_of_three_reports_valid=0,
        own_tracked_altitude=3000,
        own_tracked_alt_rate=0,
        other_tracked_altitude=2000,
        altitude_layer_value=0,
        up_separation=17000,
        down_separation=600,
        other_rac=0,
        other_capability=0,
        climb_inhibit=0,
    )
    assert non_crossing_biased_climb(state3) is True

    # Case 4: inhibit bias greater than down separation, own above threat => True because the climb clause short-circuits
    state4 = State(
        current_vertical_sep=200,
        high_confidence=0,
        two_of_three_reports_valid=0,
        own_tracked_altitude=3000,
        own_tracked_alt_rate=0,
        other_tracked_altitude=2000,
        altitude_layer_value=0,
        up_separation=1000,
        down_separation=600,
        other_rac=0,
        other_capability=0,
        climb_inhibit=0,
    )
    assert non_crossing_biased_climb(state4) is True


def test_non_crossing_biased_descend_clauses():
    # Case 1: inhibit bias greater than down separation, own above threat but descend separation is too small => False
    state1 = State(
        current_vertical_sep=400,
        high_confidence=0,
        two_of_three_reports_valid=0,
        own_tracked_altitude=3000,
        own_tracked_alt_rate=0,
        other_tracked_altitude=2000,
        altitude_layer_value=0,
        up_separation=500,
        down_separation=400,
        other_rac=0,
        other_capability=0,
        climb_inhibit=1,
    )
    assert non_crossing_biased_descend(state1) is False

    # Case 2: same descent branch, but vertical separation still does not satisfy the alert condition => False
    state2 = State(
        current_vertical_sep=200,
        high_confidence=0,
        two_of_three_reports_valid=0,
        own_tracked_altitude=3000,
        own_tracked_alt_rate=0,
        other_tracked_altitude=2000,
        altitude_layer_value=0,
        up_separation=500,
        down_separation=400,
        other_rac=0,
        other_capability=0,
        climb_inhibit=1,
    )
    assert non_crossing_biased_descend(state2) is False

    # Case 3: inhibit bias less than or equal down separation, own not above threat => True
    state3 = State(
        current_vertical_sep=400,
        high_confidence=0,
        two_of_three_reports_valid=0,
        own_tracked_altitude=1000,
        own_tracked_alt_rate=0,
        other_tracked_altitude=2000,
        altitude_layer_value=0,
        up_separation=500,
        down_separation=600,
        other_rac=0,
        other_capability=0,
        climb_inhibit=0,
    )
    assert non_crossing_biased_descend(state3) is True

    # Case 4: inhibit bias less than or equal down separation, own above threat but up separation too small => False
    state4 = State(
        current_vertical_sep=400,
        high_confidence=0,
        two_of_three_reports_valid=0,
        own_tracked_altitude=3000,
        own_tracked_alt_rate=0,
        other_tracked_altitude=2000,
        altitude_layer_value=0,
        up_separation=1000,
        down_separation=600,
        other_rac=0,
        other_capability=0,
        climb_inhibit=0,
    )
    assert non_crossing_biased_descend(state4) is False


def test_altitude_separation_test_variants():
    # Upward advisory expected when climb conditions are met and own aircraft is below.
    up_state = State(
        current_vertical_sep=700,
        high_confidence=1,
        two_of_three_reports_valid=1,
        own_tracked_altitude=1000,
        own_tracked_alt_rate=500,
        other_tracked_altitude=2000,
        altitude_layer_value=0,
        up_separation=17000,
        down_separation=1000,
        other_rac=0,
        other_capability=1,
        climb_inhibit=0,
    )
    assert altitude_separation_test(up_state) == 1

    # No advisory expected if the system lacks high confidence.
    neutral_state = State(
        current_vertical_sep=700,
        high_confidence=0,
        two_of_three_reports_valid=0,
        own_tracked_altitude=1000,
        own_tracked_alt_rate=500,
        other_tracked_altitude=2000,
        altitude_layer_value=0,
        up_separation=17000,
        down_separation=17000,
        other_rac=0,
        other_capability=1,
        climb_inhibit=0,
    )
    assert altitude_separation_test(neutral_state) == 0

    # Downward advisory expected when own aircraft is above and descend conditions are met.
    down_state = State(
        current_vertical_sep=700,
        high_confidence=1,
        two_of_three_reports_valid=1,
        own_tracked_altitude=3000,
        own_tracked_alt_rate=500,
        other_tracked_altitude=2000,
        altitude_layer_value=0,
        up_separation=17000,
        down_separation=17000,
        other_rac=0,
        other_capability=1,
        climb_inhibit=0,
    )
    assert altitude_separation_test(down_state) == 2
