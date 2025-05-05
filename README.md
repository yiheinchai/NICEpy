# NICEpy 🐍🩺

**A Python SDK for Clinical Guideline Implementation**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
<!-- Add other badges like build status, coverage, PyPI version when applicable -->
<!-- [![Build Status](...)](...) -->
<!-- [![Coverage Status](...)](...) -->
<!-- [![PyPI version](...)](...) -->

`NICEpy` is a conceptual Python library designed to represent and execute logic based on clinical guidelines (inspired by NICE and others). It aims to provide a structured, type-safe, and developer-friendly way to interact with clinical algorithms for educational, research, or decision-support prototyping purposes.

**Core Philosophy:**

*   **Clarity via Explicit Parameters:** Core diagnostic, scoring, and management functions declare their *exact* data requirements as parameters. This avoids passing large, opaque patient data objects, making dependencies clear directly from the function signature.
*   **Type Safety & Enums:** Leverages Python's type hinting and Enumerations (`Enum`) extensively to reduce errors, improve code clarity, and enhance developer experience through autocompletion.
*   **Structured Output:** Returns management plans and recommendations in well-defined data classes (`AlgorithmPlan`, `AlgorithmStep`, `DrugRecommendation`, etc.).
*   **Modularity:** Organized by medical specialty (`cardiology`, `respiratory`, `neurology`, etc.) for better maintainability.

---

**🚨 VERY IMPORTANT DISCLAIMER 🚨**

**`NICEpy` is a conceptual library and is intended STRICTLY for educational, research, and informational purposes ONLY.**

*   **DO NOT USE THIS SDK FOR ACTUAL CLINICAL DECISION-MAKING.**
*   Clinical guidelines are complex and constantly updated. This SDK may not reflect the most current or complete guidelines.
*   The implemented logic is based on the provided text examples and may be simplified or incomplete.
*   It is NOT a substitute for professional medical advice, diagnosis, or treatment provided by qualified healthcare professionals.
*   Always consult with a qualified healthcare provider for any health concerns or before making any decisions related to your health or treatment.
*   The creators and contributors of `NICEpy` assume NO responsibility for any clinical decisions or outcomes based on the use of this software. **Use entirely at your own risk.**

---

## Features (Conceptual Implementation)

This SDK provides classes and functions to model:

*   **Medical Conditions:** Base structure and specific implementations for:
    *   **Cardiology:**
        *   Acute Coronary Syndrome (ACS): Diagnosis (STEMI/NSTEMI/UA), Management Plans (STEMI reperfusion, NSTEMI/UA risk stratification).
    *   **Vascular / Respiratory:**
        *   Pulmonary Embolism (PE): Investigation and initial management algorithm based on Wells score.
    *   **Respiratory:**
        *   Acute Exacerbation of COPD: Management algorithm (Oxygen, Bronchodilators, Steroids, Antibiotics, NIV criteria).
    *   **Endocrinology:**
        *   Diabetic Ketoacidosis (DKA): Management algorithm (Fluids, Insulin, Potassium replacement).
    *   **Rheumatology:**
        *   Rheumatoid Arthritis (RA): Management algorithm (Step-up from cDMARDs to Biologics/tsDMARDs based on activity).
    *   **Gastroenterology:**
        *   Ulcerative Colitis (UC): Induction of remission algorithm based on severity and extent.
    *   **Neurology:**
        *   Acute Ischaemic Stroke: Reperfusion decision algorithm (Thrombolysis, Thrombectomy).
*   **Clinical Scoring:** Utility functions for calculating scores (with explicit parameters):
    *   Wells Score (PE)
    *   Killip Class Determination
    *   DKA Severity Assessment (Conceptual)
    *   DAS28 Interpretation (Conceptual - calculation placeholder)
    *   UC Severity Assessment (Conceptual - calculation placeholder)
    *   *Note: Complex scores like GRACE are only represented by function signatures.*
*   **Data Models:** Dataclasses for structuring inputs (optional `PatientData` for callers) and outputs (`AlgorithmPlan`, `DrugRecommendation`, etc.).
*   **Enums:** Type-safe enumerations for clinical concepts (e.g., `ACSType`, `Sex`, `DrugClass`).

## Installation

```bash
# Once packaged and published (conceptual)
pip install nicepy
```

*Requires Python 3.7+ (due to dataclasses)*

## Basic Usage: Pulmonary Embolism Investigation

This example demonstrates how to use the PE investigation algorithm, passing specific required parameters.

```python
from nicepy import vascular, enums, utils

# 1. Gather specific patient findings relevant to Wells score
signs_dvt = False
pe_most_likely = False
hr = 95
recent_immob_or_surgery = False
prev_vte = True
haemoptysis = False
malignancy = False
renal_impaired = False # Assume normal renal function

# 2. Instantiate the PE handler
pe_handler = vascular.pe.PulmonaryEmbolism()

# 3. Get the investigation plan
investigation_plan = pe_handler.get_investigation_management_plan(
    has_clinical_signs_dvt=signs_dvt,
    is_pe_most_likely_diagnosis=pe_most_likely,
    heart_rate=hr,
    had_immobilisation_or_surgery_last_4_weeks=recent_immob_or_surgery,
    has_previous_dvt_or_pe=prev_vte,
    has_haemoptysis=haemoptysis,
    has_malignancy=malignancy,
    is_renal_impaired=renal_impaired,
    # ctpa_contraindicated can also be passed if known
)

# 4. Print the initial recommended step and potential paths
print(f"--- PE Investigation Plan for {investigation_plan.condition} ---")
start_step = investigation_plan.steps.get(investigation_plan.start_step_id)

if start_step:
    print(f"Start Step ({start_step.step_id}): {start_step.description}")
    print(f"Details: {start_step.details}") # Shows Wells score and risk

    if start_step.conditional_next_step_ids:
        print("\nNext Steps Depend On:")
        for condition, next_step_id in start_step.conditional_next_step_ids.items():
            next_step_desc = investigation_plan.steps.get(next_step_id, "Unknown Step").description
            print(f" - If '{condition}': Go to step '{next_step_id}' ({next_step_desc})")

# Example: Manually following the 'PE_UNLIKELY' path
unlikely_step_id = start_step.conditional_next_step_ids.get(enums.WellsScoreRiskPE.PE_UNLIKELY.name)
if unlikely_step_id:
    unlikely_step = investigation_plan.steps.get(unlikely_step_id)
    print(f"\nFollowing PE Unlikely Path...")
    print(f"Next Step ({unlikely_step.step_id}): {unlikely_step.description}")
    print(f"  Recommended Investigation: {unlikely_step.investigation_recommendations[0].investigation_type.name}")
```

## Detailed Usage: DKA Management

This shows how a caller might use the `PatientData` class for convenience but still extracts specific values to call the SDK function.

```python
from nicepy import endocrinology # Assuming DKA is in this module
from nicepy import models, enums, utils

# 1. Populate patient data (e.g., from EMR)
patient_context = models.PatientData(
    age=25,
    sex=enums.Sex.FEMALE,
    weight_kg=60.0,
    known_diabetes_type=1,
    systolic_bp=95,
    heart_rate=115,
    respiratory_rate=28,
    gcs=14,
    ph_level=7.15,
    bicarbonate_mmol_l=8.0,
    blood_ketones_mmol_l=6.5,
    blood_glucose_mmol_l=28.0,
    potassium_mmol_l=5.8, # Initial potassium
    creatinine_umol_l=130.0
)

# 2. Instantiate the DKA handler (assuming class name is DiabeticKetoacidosis)
try:
    # Assuming DKA class is within an endocrinology module
    dka_handler = endocrinology.DiabeticKetoacidosis()
except AttributeError:
     print("NOTE: DiabeticKetoacidosis class needs to be defined within a module (e.g., endocrinology).")
     # Use the class defined directly in the single file for this example
     class DiabeticKetoacidosis(MedicalCondition): # Redefine locally for demo
         name = "DKA"; description = "DKA desc"
         def get_definition(self)->str: return ""
         def get_aetiology(self)->List[str]: return []
         def get_risk_factors(self)->RiskFactors: return RiskFactors()
         def get_signs_symptoms(self)->List[str]: return []
         def get_complications(self)->List[str]: return []
         def get_management_plan(self, weight_kg: float, blood_glucose_mmol_l: float, ph_level: float, bicarbonate_mmol_l: float, blood_ketones_mmol_l: float, potassium_mmol_l: float, systolic_bp: int) -> AlgorithmPlan:
             # Simplified placeholder - use full implementation from above code block
             plan = AlgorithmPlan(condition=self.name, start_step_id="CONFIRM_INITIAL")
             steps = {}
             steps["CONFIRM_INITIAL"] = AlgorithmStep(step_id="CONFIRM_INITIAL", description="Confirm DKA & Initial Actions")
             # ... add other steps based on full implementation ...
             plan.steps = steps
             return plan
     dka_handler = DiabeticKetoacidosis()


# 3. Extract specific parameters and call the management function
# Add error handling for missing essential data
if patient_context.weight_kg and patient_context.blood_glucose_mmol_l and \
   patient_context.ph_level and patient_context.bicarbonate_mmol_l and \
   patient_context.blood_ketones_mmol_l and patient_context.potassium_mmol_l and \
   patient_context.systolic_bp:

    dka_plan = dka_handler.get_management_plan(
        weight_kg=patient_context.weight_kg,
        blood_glucose_mmol_l=patient_context.blood_glucose_mmol_l,
        ph_level=patient_context.ph_level,
        bicarbonate_mmol_l=patient_context.bicarbonate_mmol_l,
        blood_ketones_mmol_l=patient_context.blood_ketones_mmol_l,
        potassium_mmol_l=patient_context.potassium_mmol_l,
        systolic_bp=patient_context.systolic_bp
    )

    # 4. Display the plan (using a helper function like print_plan_path from previous example)
    # print_plan_path(dka_plan) # Assuming print_plan_path is defined
    print(f"\nGenerated DKA plan starting with step: {dka_plan.start_step_id}")
    # Add logic here to navigate and display the plan steps as needed
else:
    print("Error: Missing essential data for DKA management plan generation.")

```

## SDK Structure Overview

*   **`enums.py`**: Defines enumerations for clinical concepts (e.g., `ACSType`, `WellsScoreRiskPE`, `DrugClass`, `InvestigationType`).
*   **`models.py`**: Contains dataclasses for structuring return types (e.g., `AlgorithmPlan`, `AlgorithmStep`, `DrugRecommendation`) and optionally for callers to organize input data (`PatientData`).
*   **`base_condition.py`**: Defines the abstract base class `MedicalCondition` for consistency.
*   **`utils/scoring.py`**: Includes functions for calculating clinical scores (e.g., `calculate_wells_score_pe`).
*   **Specialty Modules (e.g., `cardiology/`, `respiratory/`, `neurology/` etc.)**: Each module contains implementations for specific conditions inheriting from `MedicalCondition`, including their respective management algorithms.

## Contributing

Contributions are welcome! (Conceptual - If this were a real project):

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/your-feature-name`).
3.  Implement your changes, adding relevant conditions or refining algorithms.
4.  Add unit tests for your changes.
5.  Ensure code adheres to linting standards (e.g., Black, Flake8).
6.  Create a pull request with a clear description of your changes.
7.  Please report any issues or suggest features via the GitHub Issue Tracker.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details (A LICENSE file would need to be created).

## Future Work / Roadmap

*   Implement full logic for all algorithms based on detailed guidelines.
*   Complete implementations for scoring systems (GRACE, DAS28, etc.).
*   Add more medical conditions across various specialties.
*   Develop comprehensive unit tests.
*   Refine data models (`PatientData`) for greater detail and validation (potentially using Pydantic).
*   Add robust error handling for missing data or invalid inputs.
*   Improve documentation (docstrings, potentially Sphinx).
*   Consider adding interfaces for common data formats (e.g., FHIR).
*   Package for distribution via PyPI.
