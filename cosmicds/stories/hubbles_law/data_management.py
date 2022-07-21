STUDENT_MEASUREMENTS_LABEL = "student_measurements"
STUDENT_DATA_LABEL = "student_data"
CLASS_DATA_LABEL = "class_data"
ALL_DATA_LABEL = "all_measurements"
CLASS_SUMMARY_LABEL = "class_summary_data"
ALL_STUDENT_SUMMARIES_LABEL = "all_student_summaries"
ALL_CLASS_SUMMARIES_LABEL = "all_class_summaries"
SDSS_DATA_LABEL = "SDSS_all_sample_filtered"
SPECTRUM_DATA_LABEL = "spectrum_data"

def reverse(d):
    return { v : k for k, v in d.items() }

MEAS_TO_STATE = {
    "measwave": "obs_wave_value",
    "restwave": "rest_wave_value",
    "velocity": "velocity_value",
    "distance": "est_dist_value",
    "name": "galaxy_name",
    "student_id": "student_id",
    "angular_size" : "ang_size_value"
}

STATE_TO_MEAS = reverse(MEAS_TO_STATE)

SUMM_TO_STATE = {
    "H0": "hubble_fit_value",
    "age": "age_value"
}

STATE_TO_SUMM = reverse(SUMM_TO_STATE)

UNITS_TO_STATE = {
    "rest_wave_unit": "angstrom",
    "obs_wave_unit": "angstrom",
    "est_dist_unit": "Mpc",
    "velocity_unit": "km / s",
    "ang_size_unit": "arcsecond"
}
