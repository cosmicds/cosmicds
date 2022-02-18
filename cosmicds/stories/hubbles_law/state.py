from pathlib import Path

from echo import DictCallbackProperty

from cosmicds.phases import Story
from cosmicds.registries import story_registry
import numpy as np
from glue.core import Data


@story_registry(name="hubbles_law")
class HubblesLaw(Story):
    measurements = DictCallbackProperty({
        "galax_id": 123,
        "rest_wave_value": 6563.0,
        "rest_wave_unit": "Angstrom",
        "obs_wave_value": 6863.0,
        "obs_wave_unit": "Angstrom",
        "velocity_value": 120.0,
        "velocity_unit": "km / s",
        "ang_size": 50,
        "est_dist_value": 100,
        "est_dist_unit": "lyr"
    })
    calculations = DictCallbackProperty({
        "hubble_value_fit_value": 65.0,
        "hubble_value_fit_unit": "km / s / Mpc",
        "hubble_value_guess_value": 80.0,
        "hubble_value_guess_unit": "km / s / Mpc",
        "age_value": 1.3e9,
        "age_unit": "Gyr"
    })
    validation_failure_counts = DictCallbackProperty({
        "doppler_equation": 1,
        "final_velocity": 3,
        "mc_q1": 2
    })
    responses = DictCallbackProperty({
        "dialog1": {
            "free_response": "I'm 90% confident about my answer.",
            "finished": True
        }
    })

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Load data needed for Hubble's Law
        data_dir = Path(__file__).parent / "data"
        output_dir = data_dir / "hubble_simulation" / "output"

        # Load some simulated measurements as summary data
        self.app.load_data([
            f"{dataset}.csv" for dataset in (
                data_dir / "galaxy_data",
                data_dir / "Hubble 1929-Table 1",
                data_dir / "HSTkey2001",
                data_dir / "SDSS_all_sample_filtered",
                data_dir / "dummy_student_data",
                output_dir / "HubbleData_ClassSample",
                output_dir / "HubbleData_All",
                output_dir / "HubbleSummary_ClassSample",
                output_dir / "HubbleSummary_Students",
                output_dir / "HubbleSummary_Classes",
            )
        ])

        # Compose empty data containers to be populated by user
        self.data_collection.append(Data(
            label='student_measurements',
            **{x: np.array([], dtype='float64')
               for x in ["ID", "RA", "DEC", "Z", "Type", "measwave",
                         "restwave", "student_id", "velocity", "distance",
                         "Element"]}))
