from src.tcas.state import State
from src.tcas.main import altitude_separation_test, non_crossing_biased_climb, non_crossing_biased_descend, positive_ra_alt_thresh


def test_positive_ra_alt_thresh():
    # Baseline state with zeroed thresholds and default layer
    baseline = State(
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

    # Verify each altitude threshold value is returned for valid layers
    assert positive_ra_alt_thresh(baseline, 0) == baseline.positive_ra_alt_thresh_0
    assert positive_ra_alt_thresh(baseline, 1) == baseline.positive_ra_alt_thresh_1
    assert positive_ra_alt_thresh(baseline, 2) == baseline.positive_ra_alt_thresh_2
    assert positive_ra_alt_thresh(baseline, 3) == baseline.positive_ra_alt_thresh_3

    # Verify invalid layer values return the default of 0
    assert positive_ra_alt_thresh(baseline, 99) == 0


def test_non_crossing_biased_climb_variant():
    # State where climb bias is expected to allow a climb advisory
    climb_state = State(
        current_vertical_sep=400,
        high_confidence=0,
        two_of_three_reports_valid=0,
        own_tracked_altitude=150,
        own_tracked_alt_rate=0,
        other_tracked_altitude=250,
        altitude_layer_value=0,
        up_separation=200,
        down_separation=100,
        other_rac=0,
        other_capability=0,
        climb_inhibit=0,
    )

    # State where climb advisory should be rejected because own is below and down separation is above alim
    no_climb_state = State(
        current_vertical_sep=200,
        high_confidence=0,
        two_of_three_reports_valid=0,
        own_tracked_altitude=1000,
        own_tracked_alt_rate=0,
        other_tracked_altitude=2000,
        altitude_layer_value=0,
        up_separation=17000,
        down_separation=17000,
        other_rac=0,
        other_capability=0,
        climb_inhibit=1,
    )

    assert non_crossing_biased_climb(climb_state) == True
    assert non_crossing_biased_climb(no_climb_state) == False


def test_non_crossing_biased_descend_variant():
    # State where descend advisory should be allowed by the logic
    descend_state = State(
        current_vertical_sep=350,
        high_confidence=0,
        two_of_three_reports_valid=0,
        own_tracked_altitude=300,
        own_tracked_alt_rate=0,
        other_tracked_altitude=100,
        altitude_layer_value=0,
        up_separation=0,
        down_separation=50,
        other_rac=0,
        other_capability=0,
        climb_inhibit=0,
    )

    # State where descend advisory should be rejected because the descend clause is not satisfied
    no_descend_state = State(
        current_vertical_sep=400,
        high_confidence=0,
        two_of_three_reports_valid=0,
        own_tracked_altitude=300,
        own_tracked_alt_rate=0,
        other_tracked_altitude=100,
        altitude_layer_value=0,
        up_separation=0,
        down_separation=400,
        other_rac=0,
        other_capability=0,
        climb_inhibit=1,
    )

    assert non_crossing_biased_descend(descend_state) == False
    assert non_crossing_biased_descend(no_descend_state) == False


def test_altitude_separation_variant():
    # State configured to produce an upward RA advisory
    up_state = State(
        current_vertical_sep=700,
        high_confidence=1,
        two_of_three_reports_valid=1,
        own_tracked_altitude=200,
        own_tracked_alt_rate=0,
        other_tracked_altitude=500,
        altitude_layer_value=0,
        up_separation=120,
        down_separation=10,
        other_rac=0,
        other_capability=1,
        climb_inhibit=0,
    )

    # Baseline state expected to return no advisory
    neutral_state = State(
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

    # State configured to produce a downward RA advisory
    down_state = State(
        current_vertical_sep=700,
        high_confidence=1,
        two_of_three_reports_valid=1,
        own_tracked_altitude=500,
        own_tracked_alt_rate=0,
        other_tracked_altitude=100,
        altitude_layer_value=1,
        up_separation=17000,
        down_separation=17000,
        other_rac=0,
        other_capability=1,
        climb_inhibit=0,
    )

    assert altitude_separation_test(up_state) == 1
    assert altitude_separation_test(neutral_state) == 0
    assert altitude_separation_test(down_state) == 2
