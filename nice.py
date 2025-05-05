# -*- coding: utf-8 -*-
"""
NICEpy SDK - Conceptual Implementation (Single File)

A Python SDK structure based on medical guidelines, focusing on explicit function
parameters for core logic while using dataclasses for structured data handling.
Includes complex, branching management algorithms.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Optional, Dict, Union, Tuple, Any
from datetime import datetime
import math

# ---------------------------------------------
# Section 1: Enums
# ---------------------------------------------

# --- General ---
class Sex(Enum): MALE = auto(); FEMALE = auto()
class BooleanStatus(Enum): YES = auto(); NO = auto(); UNKNOWN = auto()
class DiseaseSeverity(Enum): MILD = auto(); MODERATE = auto(); SEVERE = auto(); LIFE_THREATENING = auto()

# --- Cardiology ---
class ACSType(Enum): STEMI = auto(); NSTEMI = auto(); UNSTABLE_ANGINA = auto()
class KillipClass(Enum): CLASS_I = auto(); CLASS_II = auto(); CLASS_III = auto(); CLASS_IV = auto()
class RhythmType(Enum): SHOCKABLE = auto(); NON_SHOCKABLE = auto()
class AxisDeviation(Enum): NORMAL = auto(); LEFT = auto(); RIGHT = auto(); EXTREME_RIGHT = auto()

# --- Vascular ---
class WellsScoreRiskPE(Enum): PE_LIKELY = auto(); PE_UNLIKELY = auto()

# --- Respiratory ---
class COPDExacerbationSeverity(Enum): MILD = auto(); MODERATE = auto(); SEVERE = auto(); LIFE_THREATENING = auto() # For COPD

# --- Endocrinology ---
class HypertensionStage(Enum): STAGE_1 = auto(); STAGE_2 = auto(); SEVERE = auto()
class DKASeverity(Enum): MILD = auto(); MODERATE = auto(); SEVERE = auto() # Based on pH/Bicarb/Ketones

# --- Rheumatology ---
class RAActivityLevel(Enum): LOW = auto(); MODERATE = auto(); HIGH = auto()
class UCExtent(Enum): PROCTITIS = auto(); PROCTOSIGMOIDITIS = auto(); LEFT_SIDED_COLITIS = auto(); EXTENSIVE_COLITIS = auto(); PANCŌLITIS = auto()
class UCSeverity(Enum): MILD = auto(); MODERATE = auto(); SEVERE = auto() # Truelove & Witts simplified

# --- Neurology ---
class StrokeType(Enum): ISCHAEMIC = auto(); HAEMORRHAGIC = auto()

# --- Drug Classes ---
class DrugClass(Enum): ACE_INHIBITOR = auto(); ARB = auto(); BETA_BLOCKER = auto(); CALCIUM_CHANNEL_BLOCKER = auto(); THIAZIDE_DIURETIC = auto(); LOOP_DIURETIC = auto(); STATIN = auto(); ANTIPLATELET = auto(); ANTICOAGULANT = auto(); FIBRINOLYTIC = auto(); DOAC = auto(); LMWH = auto(); UFH = auto(); PPI = auto(); ANTIBIOTIC = auto(); STEROID = auto(); SABA = auto(); SAMA = auto(); LAMA = auto(); LABA = auto(); INSULIN = auto(); DMARD_CONVENTIONAL = auto(); DMARD_BIOLOGIC_TNF = auto(); DMARD_BIOLOGIC_OTHER = auto(); DMARD_JAK_INHIBITOR = auto(); AMINOSALICYLATE = auto(); NITRATE = auto(); OPIOID = auto(); ANTITHROMBIN = auto(); GPIIbIIIa_INHIBITOR = auto(); DOPAMINE_ANTAGONIST = auto(); # Added more

# --- Investigations ---
class InvestigationType(Enum): ECG = auto(); TROPONIN = auto(); CHEST_XRAY = auto(); CTPA = auto(); VQ_SCAN = auto(); D_DIMER = auto(); BLOOD_CULTURE = auto(); ABG = auto(); U_AND_E = auto(); FBC = auto(); LIPIDS = auto(); GLUCOSE_HBA1C = auto(); KETONES_BLOOD_URINE = auto(); SPUTUM_MC_S = auto(); BLOOD_GAS = auto(); CRP = auto(); ESR = auto(); CT_HEAD_NON_CONTRAST = auto(); CT_ANGIOGRAM = auto(); MRI_BRAIN = auto(); COLONOSCOPY = auto(); ENDOSCOPY = auto(); SIGMOIDOSCOPY = auto(); DAS28_ASSESSMENT = auto(); LFT = auto(); # Added more

# ... Add other enums as needed ...

# ---------------------------------------------
# Section 2: Data Models
# ---------------------------------------------

@dataclass
class DrugRecommendation:
    name: str
    drug_class: Optional[DrugClass] = None
    dosage_recommendation: Optional[str] = None
    route: Optional[str] = None # e.g., "PO", "IV", "Nebulised", "Rectal", "SC"
    rationale: Optional[str] = None
    duration: Optional[str] = None
    warnings: List[str] = field(default_factory=list)

@dataclass
class InvestigationRecommendation:
    investigation_type: InvestigationType
    details: Optional[str] = None
    rationale: Optional[str] = None
    urgency: Optional[str] = "Routine" # e.g., "Immediate", "Urgent", "Routine"

@dataclass
class ActionRecommendation:
    description: str
    details: Optional[str] = None

@dataclass
class AlgorithmStep:
    step_id: str # Unique ID for referencing steps
    description: str # Description of the step/decision point
    condition: Optional[str] = None # Condition triggering this specific step (if part of a branch)
    recommended_actions: List[ActionRecommendation] = field(default_factory=list)
    investigation_recommendations: List[InvestigationRecommendation] = field(default_factory=list)
    drug_recommendations: List[DrugRecommendation] = field(default_factory=list)
    # For branching logic: Key = condition/result string, Value = next step ID
    conditional_next_step_ids: Optional[Dict[str, str]] = None
    default_next_step_id: Optional[str] = None # Step to go to if no conditions met or branching not applicable

@dataclass
class AlgorithmPlan:
    condition: str
    start_step_id: str # ID of the first step
    steps: Dict[str, AlgorithmStep] = field(default_factory=dict) # All steps keyed by ID
    warnings: List[str] = field(default_factory=list)
    required_referrals: List[str] = field(default_factory=list)
    final_diagnosis_recommendation: Optional[str] = None
    stop_condition: Optional[str] = None

@dataclass
class RiskFactors:
    modifiable: List[str] = field(default_factory=list)
    non_modifiable: List[str] = field(default_factory=list)

@dataclass
class PatientData: # Keep for caller's convenience - Example fields
    # --- Demographics ---
    age: Optional[int] = None
    sex: Optional[Sex] = None
    weight_kg: Optional[float] = None
    is_pregnant: Optional[bool] = None
    # --- History / Clinical State ---
    # Shared
    smoker: Optional[bool] = None
    has_hypertension: Optional[bool] = None
    has_diabetes: Optional[bool] = None
    known_diabetes_type: Optional[int] = None # 1 or 2
    has_heart_failure: Optional[bool] = None
    has_active_infection: Optional[bool] = None
    has_malignancy: Optional[bool] = None
    is_renal_impaired: Optional[bool] = None # Simplified
    high_bleeding_risk: Optional[bool] = None
    # ACS
    has_chest_pain_suspicious_for_acs: Optional[bool] = None
    symptom_onset_hours_acs: Optional[float] = None
    # PE
    has_clinical_signs_dvt: Optional[bool] = None
    is_pe_most_likely_diagnosis: Optional[bool] = None
    had_immobilisation_or_surgery_last_4_weeks: Optional[bool] = None
    has_previous_dvt_or_pe: Optional[bool] = None
    has_haemoptysis: Optional[bool] = None
    # COPD
    known_copd_patient: Optional[bool] = None
    sputum_purulent: Optional[bool] = None
    # DKA
    # diabetes type above
    # RA
    ra_das28_score: Optional[float] = None
    ra_failed_dmards: List[DrugClass] = field(default_factory=list)
    has_active_tb: Optional[bool] = None
    # UC
    uc_disease_extent: Optional[UCExtent] = None
    uc_severity: Optional[UCSeverity] = None
    # Stroke
    stroke_symptom_onset_hours: Optional[float] = None
    stroke_nihss_score: Optional[int] = None
    stroke_has_intracranial_haemorrhage: Optional[bool] = None
    stroke_has_large_established_infarct: Optional[bool] = None
    stroke_has_thrombectomy_target_vessel: Optional[bool] = None
    # --- Vitals ---
    heart_rate: Optional[int] = None
    systolic_bp: Optional[int] = None
    diastolic_bp: Optional[int] = None
    respiratory_rate: Optional[int] = None
    oxygen_saturation: Optional[float] = None
    temperature_celsius: Optional[float] = None
    gcs: Optional[int] = None
    killip_class: Optional[KillipClass] = None # Cardiology specific state
    had_cardiac_arrest: Optional[bool] = None
    # --- Labs ---
    is_troponin_raised: Optional[bool] = None
    d_dimer_positive: Optional[bool] = None
    creatinine_umol_l: Optional[float] = None
    potassium_mmol_l: Optional[float] = None
    blood_glucose_mmol_l: Optional[float] = None
    blood_ketones_mmol_l: Optional[float] = None
    ph_level: Optional[float] = None
    bicarbonate_mmol_l: Optional[float] = None
    wcc_x10e9_l: Optional[float] = None
    haemoglobin_g_dl: Optional[float] = None
    esr_mm_hr: Optional[int] = None
    # --- ECG ---
    has_st_elevation: Optional[bool] = None
    has_st_depression_or_twi: Optional[bool] = None
    # --- Scores ---
    grace_score: Optional[int] = None # Often calculated, not input directly
    wells_score_pe: Optional[float] = None # Raw score
    # --- Imaging ---
    ctpa_result_positive: Optional[bool] = None
    # ... other relevant fields ...

# ---------------------------------------------
# Section 3: Base Condition Class
# ---------------------------------------------

class MedicalCondition(ABC):
    name: str
    description: str
    @abstractmethod
    def get_definition(self) -> str: pass
    @abstractmethod
    def get_aetiology(self) -> List[str]: pass
    @abstractmethod
    def get_risk_factors(self) -> RiskFactors: pass
    @abstractmethod
    def get_signs_symptoms(self) -> List[str]: pass
    @abstractmethod
    def get_complications(self) -> List[str]: pass

# ---------------------------------------------
# Section 4: Utility / Scoring Functions
# ---------------------------------------------

# --- Wells Score for PE ---
def calculate_wells_score_pe(
    has_clinical_signs_dvt: bool, is_pe_most_likely_diagnosis: bool, heart_rate: int,
    had_immobilisation_or_surgery_last_4_weeks: bool, has_previous_dvt_or_pe: bool,
    has_haemoptysis: bool, has_malignancy: bool
) -> float:
    score = 0.0
    if has_clinical_signs_dvt: score += 3.0
    if is_pe_most_likely_diagnosis: score += 3.0
    if heart_rate > 100: score += 1.5
    if had_immobilisation_or_surgery_last_4_weeks: score += 1.5
    if has_previous_dvt_or_pe: score += 1.5
    if has_haemoptysis: score += 1.0
    if has_malignancy: score += 1.0
    return score

def interpret_wells_score_pe(score: float) -> WellsScoreRiskPE:
     return WellsScoreRiskPE.PE_LIKELY if score > 4 else WellsScoreRiskPE.PE_UNLIKELY

# --- Killip Class ---
def determine_killip_class(
    has_lung_crackles: bool, has_s3_gallop: bool, has_frank_pulmonary_oedema: bool, is_in_cardiogenic_shock: bool
) -> KillipClass:
    if is_in_cardiogenic_shock: return KillipClass.CLASS_IV
    if has_frank_pulmonary_oedema: return KillipClass.CLASS_III
    if has_lung_crackles or has_s3_gallop: return KillipClass.CLASS_II
    return KillipClass.CLASS_I

# --- GRACE Score Placeholder ---
def calculate_grace_score(
    age: int, heart_rate: int, systolic_bp: int, creatinine: float,
    killip_class: KillipClass, had_cardiac_arrest: bool,
    has_st_deviation: bool, is_troponin_raised: bool
) -> Optional[int]:
    print("Warning: GRACE score calculation logic is complex and not fully implemented here.")
    return None

# --- DKA Severity ---
def determine_dka_severity(
    ph_level: Optional[float],
    bicarbonate_mmol_l: Optional[float],
    blood_ketones_mmol_l: Optional[float]
) -> Optional[DKASeverity]:
    if ph_level is None or bicarbonate_mmol_l is None or blood_ketones_mmol_l is None:
        return None # Cannot determine severity
    if ph_level < 7.0 or bicarbonate_mmol_l < 5.0:
        return DKASeverity.SEVERE
    elif ph_level < 7.3 or bicarbonate_mmol_l < 15.0:
         # Assuming ketones > 3 already met for DKA diagnosis
        return DKASeverity.MODERATE
    else:
        return DKASeverity.MILD

# --- DAS28 Calculation Placeholder ---
def calculate_das28(
    tender_joint_count_28: int, swollen_joint_count_28: int, esr_or_crp_value: float,
    patient_global_assessment_vas_100mm: int
) -> Optional[float]:
    print("Warning: DAS28 calculation logic is complex and not implemented here.")
    return None

def interpret_das28(das28_score: Optional[float]) -> Optional[RAActivityLevel]:
    if das28_score is None: return None
    if das28_score <= 3.2: return RAActivityLevel.LOW
    if das28_score <= 5.1: return RAActivityLevel.MODERATE
    return RAActivityLevel.HIGH

# --- UC Severity Placeholder ---
def assess_uc_severity(
    stools_per_day: int, has_blood_in_stool: bool, temperature_celsius: float,
    heart_rate: int, haemoglobin_g_dl: float, esr_mm_hr: int
) -> UCSeverity:
    print("Warning: UC severity assessment logic is simplified based on Truelove & Witts.")
    severe_criteria_count = 0
    if stools_per_day >= 6: severe_criteria_count += 1
    if has_blood_in_stool: severe_criteria_count += 1
    if temperature_celsius > 37.8: severe_criteria_count += 1
    if heart_rate > 90: severe_criteria_count += 1
    if haemoglobin_g_dl < 10.5: severe_criteria_count += 1
    if esr_mm_hr > 30: severe_criteria_count += 1
    if severe_criteria_count >= 2: return UCSeverity.SEVERE # Simplified rule
    if stools_per_day > 4: return UCSeverity.MODERATE
    return UCSeverity.MILD


# ---------------------------------------------
# Section 5: Condition Implementations
# ---------------------------------------------

# --- Cardiology: ACS ---
class AcuteCoronarySyndrome(MedicalCondition):
    name = "Acute Coronary Syndrome"
    description = "Umbrella term: STEMI, NSTEMI, Unstable Angina."
    def get_definition(self) -> str: return self.description
    def get_aetiology(self) -> List[str]: return ["Coronary artery disease", "Plaque rupture"]
    def get_risk_factors(self) -> RiskFactors: return RiskFactors(modifiable=["Smoking", "Hypertension", "Diabetes", "Obesity", "Hypercholesterolaemia"], non_modifiable=["Age", "Male sex", "Family history"])
    def get_signs_symptoms(self) -> List[str]: return ["Chest pain (crushing, radiating)", "Dyspnoea", "Sweating", "Nausea"]
    def get_complications(self) -> List[str]: return ["Arrhythmias", "Heart failure", "Cardiogenic shock", "Rupture"]

    def diagnose_acs_type(self, has_st_elevation: bool, is_troponin_raised: bool, has_st_depression_or_twi: bool, has_chest_pain_suspicious_for_acs: bool) -> Optional[ACSType]:
        if not has_chest_pain_suspicious_for_acs: return None
        if has_st_elevation: return ACSType.STEMI
        if is_troponin_raised: return ACSType.NSTEMI
        if has_st_depression_or_twi or has_chest_pain_suspicious_for_acs: return ACSType.UNSTABLE_ANGINA # Treat as NSTEMI/UA
        return None

    def get_stemi_management_plan(self, symptom_onset_hours: float, hospital_can_pci_within_120m: bool) -> AlgorithmPlan:
        # Implementation from previous example... (simplified for brevity)
        plan = AlgorithmPlan(condition="STEMI", start_step_id="INITIAL")
        steps = {}
        steps["INITIAL"] = AlgorithmStep(step_id="INITIAL", description="Initial Management (MONA-B style)", default_next_step_id="REPERFUSION")
        steps["REPERFUSION"] = AlgorithmStep(step_id="REPERFUSION", description="Reperfusion Strategy")
        steps["PCI"] = AlgorithmStep(step_id="PCI", description="Primary PCI preferred", default_next_step_id="SECONDARY")
        steps["LYSIS"] = AlgorithmStep(step_id="LYSIS", description="Fibrinolysis indicated", default_next_step_id="SECONDARY")
        steps["LATE"] = AlgorithmStep(step_id="LATE", description="Late Presentation management", default_next_step_id="SECONDARY")
        steps["SECONDARY"] = AlgorithmStep(step_id="SECONDARY", description="Secondary Prevention") # End step

        if symptom_onset_hours <= 12 and hospital_can_pci_within_120m:
            steps["REPERFUSION"].default_next_step_id = "PCI"
        elif symptom_onset_hours <= 12:
            steps["REPERFUSION"].default_next_step_id = "LYSIS"
        else:
            steps["REPERFUSION"].default_next_step_id = "LATE"

        plan.steps = steps
        return plan

    def get_nstemi_ua_management_plan(self, grace_score: Optional[int], high_bleeding_risk: bool) -> AlgorithmPlan:
        # Implementation from previous example... (simplified for brevity)
        plan = AlgorithmPlan(condition="NSTEMI/Unstable Angina", start_step_id="INITIAL")
        steps = {}
        steps["INITIAL"] = AlgorithmStep(step_id="INITIAL", description="Initial Management (Aspirin, Fondaparinux/UFH, Anti-anginal)", default_next_step_id="RISK_STRAT")
        steps["RISK_STRAT"] = AlgorithmStep(step_id="RISK_STRAT", description="Risk Stratification (GRACE Score)")
        steps["INVASIVE"] = AlgorithmStep(step_id="INVASIVE", description="Intermediate/High Risk: Invasive Strategy", default_next_step_id="SECONDARY")
        steps["CONSERVATIVE"] = AlgorithmStep(step_id="CONSERVATIVE", description="Low Risk: Conservative Strategy", default_next_step_id="SECONDARY")
        steps["SECONDARY"] = AlgorithmStep(step_id="SECONDARY", description="Secondary Prevention") # End step

        if grace_score is None or grace_score > 3:
            steps["RISK_STRAT"].default_next_step_id = "INVASIVE"
        else:
            steps["RISK_STRAT"].default_next_step_id = "CONSERVATIVE"

        plan.steps = steps
        return plan

# --- Vascular/Respiratory: PE ---
class PulmonaryEmbolism(MedicalCondition):
    name = "Pulmonary Embolism"
    description = "Obstruction of pulmonary arteries."
    def get_definition(self) -> str: return self.description
    def get_aetiology(self) -> List[str]: return ["Deep vein thrombosis (DVT)"]
    def get_risk_factors(self) -> RiskFactors: return RiskFactors(modifiable=["Immobility", "Surgery", "OCP/HRT"], non_modifiable=["Previous VTE", "Malignancy"])
    def get_signs_symptoms(self) -> List[str]: return ["Dyspnoea", "Pleuritic chest pain", "Tachypnoea", "Tachycardia"]
    def get_complications(self) -> List[str]: return ["Right heart strain", "Collapse", "Death"]

    def get_investigation_management_plan(
        self, has_clinical_signs_dvt: bool, is_pe_most_likely_diagnosis: bool, heart_rate: int,
        had_immobilisation_or_surgery_last_4_weeks: bool, has_previous_dvt_or_pe: bool,
        has_haemoptysis: bool, has_malignancy: bool, is_renal_impaired: bool,
        ctpa_contraindicated: bool = False
    ) -> AlgorithmPlan:
        """Provides the investigation and initial management algorithm for suspected PE."""
        plan = AlgorithmPlan(condition=self.name, start_step_id="ASSESS_RISK")
        steps = {}

        # Calculate Wells score and risk
        wells_score = calculate_wells_score_pe(has_clinical_signs_dvt, is_pe_most_likely_diagnosis, heart_rate, had_immobilisation_or_surgery_last_4_weeks, has_previous_dvt_or_pe, has_haemoptysis, has_malignancy)
        pe_risk = interpret_wells_score_pe(wells_score)

        # Step 1: Assess Risk
        steps["ASSESS_RISK"] = AlgorithmStep(step_id="ASSESS_RISK", description="Assess Pre-test Probability (Wells Score)", details=f"Score: {wells_score}, Risk: {pe_risk.name}")
        steps["ASSESS_RISK"].conditional_next_step_ids = {
            WellsScoreRiskPE.PE_LIKELY.name: "PE_LIKELY_PATH",
            WellsScoreRiskPE.PE_UNLIKELY.name: "PE_UNLIKELY_PATH"
        }

        # --- PE Likely Pathway ---
        steps["PE_LIKELY_PATH"] = AlgorithmStep(step_id="PE_LIKELY_PATH", description="PE Likely Pathway (Wells > 4)")
        steps["PE_LIKELY_PATH"].drug_recommendations.append(DrugRecommendation(name="Apixaban / Rivaroxaban", drug_class=DrugClass.DOAC, rationale="Offer interim therapeutic anticoagulation"))
        if ctpa_contraindicated or is_renal_impaired:
            steps["PE_LIKELY_PATH"].investigation_recommendations.append(InvestigationRecommendation(investigation_type=InvestigationType.VQ_SCAN, urgency="Immediate"))
        else:
            steps["PE_LIKELY_PATH"].investigation_recommendations.append(InvestigationRecommendation(investigation_type=InvestigationType.CTPA, urgency="Immediate"))
        steps["PE_LIKELY_PATH"].default_next_step_id = "AWAIT_IMAGING_LIKELY" # Wait for results

        steps["AWAIT_IMAGING_LIKELY"] = AlgorithmStep(step_id="AWAIT_IMAGING_LIKELY", description="Await Imaging Result")
        steps["AWAIT_IMAGING_LIKELY"].conditional_next_step_ids = {
            "IMAGING_POSITIVE": "PE_CONFIRMED",
            "IMAGING_NEGATIVE": "PE_RULED_OUT_CONSIDER_DVT"
        }

        # --- PE Unlikely Pathway ---
        steps["PE_UNLIKELY_PATH"] = AlgorithmStep(step_id="PE_UNLIKELY_PATH", description="PE Unlikely Pathway (Wells <= 4)")
        steps["PE_UNLIKELY_PATH"].investigation_recommendations.append(InvestigationRecommendation(investigation_type=InvestigationType.D_DIMER, urgency="Immediate"))
        steps["PE_UNLIKELY_PATH"].default_next_step_id = "AWAIT_DDIMER"

        steps["AWAIT_DDIMER"] = AlgorithmStep(step_id="AWAIT_DDIMER", description="Await D-Dimer Result")
        steps["AWAIT_DDIMER"].conditional_next_step_ids = {
            "D-Dimer Positive": "DDIMER_POS_PATH",
            "D-Dimer Negative": "PE_RULED_OUT"
        }

        steps["DDIMER_POS_PATH"] = AlgorithmStep(step_id="DDIMER_POS_PATH", description="D-Dimer Positive - Proceed as PE Likely", drug_recommendations=[DrugRecommendation(name="Apixaban / Rivaroxaban", drug_class=DrugClass.DOAC, rationale="Start interim anticoagulation")])
        # Re-use imaging recommendations from PE Likely path
        if ctpa_contraindicated or is_renal_impaired:
            steps["DDIMER_POS_PATH"].investigation_recommendations.append(InvestigationRecommendation(investigation_type=InvestigationType.VQ_SCAN, urgency="Immediate"))
        else:
             steps["DDIMER_POS_PATH"].investigation_recommendations.append(InvestigationRecommendation(investigation_type=InvestigationType.CTPA, urgency="Immediate"))
        steps["DDIMER_POS_PATH"].default_next_step_id = "AWAIT_IMAGING_UNLIKELY" # Wait for results

        steps["AWAIT_IMAGING_UNLIKELY"] = AlgorithmStep(step_id="AWAIT_IMAGING_UNLIKELY", description="Await Imaging Result (after positive D-Dimer)")
        steps["AWAIT_IMAGING_UNLIKELY"].conditional_next_step_ids = {
             "IMAGING_POSITIVE": "PE_CONFIRMED",
             "IMAGING_NEGATIVE": "PE_RULED_OUT_CONSIDER_DVT" # May need DVT scan
        }

        # --- End States ---
        steps["PE_CONFIRMED"] = AlgorithmStep(step_id="PE_CONFIRMED", description="PE Confirmed", final_diagnosis_recommendation="PE Confirmed. Continue/Start therapeutic anticoagulation.")
        steps["PE_RULED_OUT"] = AlgorithmStep(step_id="PE_RULED_OUT", description="PE Ruled Out", stop_condition="PE Ruled Out. Stop anticoagulation. Consider alternative diagnoses.")
        steps["PE_RULED_OUT_CONSIDER_DVT"] = AlgorithmStep(step_id="PE_RULED_OUT_CONSIDER_DVT", description="PE Ruled Out, Consider DVT", stop_condition="PE Ruled Out based on imaging. Stop anticoagulation. Consider proximal leg vein ultrasound if DVT suspected despite negative imaging.")

        plan.steps = steps
        return plan

# --- Respiratory: Acute Exacerbation of COPD ---
class AcuteExacerbationCOPD(MedicalCondition):
    # ... (Static methods like get_definition, get_aetiology etc. remain the same) ...
    name = "Acute Exacerbation of COPD"
    description = "Acute worsening of respiratory symptoms requiring change in regular medication."
    def get_definition(self) -> str: return self.description
    def get_aetiology(self) -> List[str]: return ["Infection (Bacterial/Viral)", "Pollution", "Non-adherence"]
    def get_risk_factors(self) -> RiskFactors: return RiskFactors(modifiable=["Smoking"], non_modifiable=["Alpha-1 antitrypsin def.", "Age"])
    def get_signs_symptoms(self) -> List[str]: return ["Increased dyspnoea", "Increased cough", "Sputum change", "Wheeze"]
    def get_complications(self) -> List[str]: return ["Respiratory failure", "Pneumonia", "Cor pulmonale"]

    def get_management_plan(
        self, oxygen_saturation: Optional[float], sputum_purulent: bool,
        resp_acidosis_present: Optional[bool], ph_level: Optional[float]
    ) -> AlgorithmPlan:
        """Provides management algorithm for Acute Exacerbation of COPD."""
        # Implementation from previous example... (simplified for brevity)
        plan = AlgorithmPlan(condition=self.name, start_step_id="INITIAL_ASSESSMENT")
        steps = {}
        steps["INITIAL_ASSESSMENT"] = AlgorithmStep(step_id="INITIAL_ASSESSMENT", description="Initial Assessment & Oxygen Therapy", default_next_step_id="BRONCHODILATORS")
        steps["BRONCHODILATORS"] = AlgorithmStep(step_id="BRONCHODILATORS", description="Bronchodilator Therapy (Nebulised SABA + SAMA)", default_next_step_id="STEROIDS")
        steps["STEROIDS"] = AlgorithmStep(step_id="STEROIDS", description="Corticosteroid Therapy (Oral/IV)", default_next_step_id="ANTIBIOTICS")
        steps["ANTIBIOTICS"] = AlgorithmStep(step_id="ANTIBIOTICS", description="Antibiotic Therapy")
        steps["ASSESS_NIV"] = AlgorithmStep(step_id="ASSESS_NIV", description="Assess Need for NIV based on ABG")
        steps["CONSIDER_ICU"] = AlgorithmStep(step_id="CONSIDER_ICU", description="Consider Invasive Ventilation/ICU")
        steps["CONTINUE_MEDICAL"] = AlgorithmStep(step_id="CONTINUE_MEDICAL", description="Continue Medical Management") # End step (simplified)

        if sputum_purulent:
            steps["ANTIBIOTICS"].recommended_actions.append(ActionRecommendation("Antibiotics indicated"))
        else:
            steps["ANTIBIOTICS"].recommended_actions.append(ActionRecommendation("Antibiotics not routinely indicated"))
        steps["ANTIBIOTICS"].default_next_step_id = "ASSESS_NIV"

        if resp_acidosis_present and ph_level is not None:
            if 7.25 <= ph_level < 7.35:
                steps["ASSESS_NIV"].recommended_actions.append(ActionRecommendation("NIV Indicated"))
                steps["ASSESS_NIV"].default_next_step_id = "CONTINUE_MEDICAL" # Assume NIV started elsewhere
            elif ph_level < 7.25:
                steps["ASSESS_NIV"].default_next_step_id = "CONSIDER_ICU"
            else: # pH >= 7.35
                steps["ASSESS_NIV"].default_next_step_id = "CONTINUE_MEDICAL"
        else: # No acidosis or pH unknown
            steps["ASSESS_NIV"].default_next_step_id = "CONTINUE_MEDICAL"

        plan.steps = steps
        return plan

# --- Endocrinology: Diabetic Ketoacidosis (DKA) ---
class DiabeticKetoacidosis(MedicalCondition):
    # ... (Static methods like get_definition, get_aetiology etc. remain the same) ...
    name = "Diabetic Ketoacidosis (DKA)"
    description = "Life-threatening complication of diabetes."
    def get_definition(self) -> str: return self.description
    def get_aetiology(self) -> List[str]: return ["Missed insulin", "Infection", "New T1DM"]
    def get_risk_factors(self) -> RiskFactors: return RiskFactors(non_modifiable=["Type 1 Diabetes"])
    def get_signs_symptoms(self) -> List[str]: return ["Polyuria/Polydipsia", "Nausea/Vomiting", "Abdo pain", "Kussmaul breathing", "Acetone breath"]
    def get_complications(self) -> List[str]: return ["Cerebral oedema", "Hypokalaemia", "ARDS", "Thromboembolism"]

    def get_management_plan(
        self, weight_kg: float, blood_glucose_mmol_l: float, ph_level: float,
        bicarbonate_mmol_l: float, blood_ketones_mmol_l: float, potassium_mmol_l: float,
        systolic_bp: int
    ) -> AlgorithmPlan:
        """Provides management algorithm for DKA based on UK guidelines (JBDS)."""
        # Implementation from previous example... (simplified for brevity)
        plan = AlgorithmPlan(condition=self.name, start_step_id="CONFIRM_INITIAL")
        steps = {}
        steps["CONFIRM_INITIAL"] = AlgorithmStep(step_id="CONFIRM_INITIAL", description="Confirmation and Initial Actions", default_next_step_id="FLUIDS")
        steps["FLUIDS"] = AlgorithmStep(step_id="FLUIDS", description="IV Fluid Replacement", default_next_step_id="INSULIN")
        steps["INSULIN"] = AlgorithmStep(step_id="INSULIN", description="Insulin Therapy (FRIII)", default_next_step_id="POTASSIUM")
        steps["POTASSIUM"] = AlgorithmStep(step_id="POTASSIUM", description="Potassium Replacement (based on initial K+)")
        steps["MONITOR_RESOLVE"] = AlgorithmStep(step_id="MONITOR_RESOLVE", description="Monitoring and DKA Resolution")
        steps["TRANSITION"] = AlgorithmStep(step_id="TRANSITION", description="Transition to Subcutaneous Insulin") # End step

        # Basic Potassium logic linking
        if potassium_mmol_l < 3.5:
             steps["POTASSIUM"].warnings.append("SEVERE HYPOKALAEMIA - Seek senior help BEFORE starting insulin")
             steps["POTASSIUM"].default_next_step_id = "MONITOR_RESOLVE"
        elif 3.5 <= potassium_mmol_l <= 5.5:
             steps["POTASSIUM"].default_next_step_id = "MONITOR_RESOLVE"
        else: # > 5.5
             steps["POTASSIUM"].default_next_step_id = "MONITOR_RESOLVE"

        # Resolution logic placeholder
        steps["MONITOR_RESOLVE"].default_next_step_id = "TRANSITION" # Assume resolution criteria met

        plan.steps = steps
        return plan

# --- Rheumatology: RA Management (already implemented with complexity) ---
class RheumatoidArthritis(MedicalCondition):
    # Implementation from previous example...
    name = "Rheumatoid Arthritis"
    description = "Chronic autoimmune disease causing joint inflammation."
    def get_definition(self) -> str: return self.description
    def get_aetiology(self) -> List[str]: return ["Autoimmune", "Genetics", "Environment"]
    def get_risk_factors(self) -> RiskFactors: return RiskFactors(modifiable=["Smoking"], non_modifiable=["Female sex", "Family history"])
    def get_signs_symptoms(self) -> List[str]: return ["Symmetrical polyarthritis", "Morning stiffness"]
    def get_complications(self) -> List[str]: return ["Joint destruction", "Vasculitis", "Lung disease"]

    def get_management_plan(
        self, das28_score: Optional[float], failed_conventional_dmards: int,
        failed_biologic_tnfi: bool, tb_screening_done_and_negative: bool,
        has_active_infection: bool, has_severe_heart_failure_for_tnfi: bool,
        patient_preference_biologic: bool = True
    ) -> AlgorithmPlan:
        # Implementation from previous example...
        plan = AlgorithmPlan(condition=self.name, start_step_id="START")
        steps = {}
        steps["START"] = AlgorithmStep(step_id="START", description="Initial Diagnosis/Assessment", default_next_step_id="FIRST_LINE_DMARD")
        steps["FIRST_LINE_DMARD"] = AlgorithmStep(step_id="FIRST_LINE_DMARD", description="Initiate First-Line Conventional DMARD", default_next_step_id="ASSESS_RESPONSE_DMARD")
        steps["ASSESS_RESPONSE_DMARD"] = AlgorithmStep(step_id="ASSESS_RESPONSE_DMARD", description="Assess Response after ~3-6 months")
        steps["OPTIMIZE_DMARD"] = AlgorithmStep(step_id="OPTIMIZE_DMARD", description="Optimize/Switch Conventional DMARDs", default_next_step_id="ASSESS_RESPONSE_DMARD")
        steps["CONSIDER_BIOLOGIC"] = AlgorithmStep(step_id="CONSIDER_BIOLOGIC", description="Consider Biologic/Targeted Synthetic DMARD Therapy")
        steps["ADD_ANTI_TNF"] = AlgorithmStep(step_id="ADD_ANTI_TNF", description="Add Anti-TNF Biologic", default_next_step_id="ASSESS_RESPONSE_BIOLOGIC")
        steps["SWITCH_BIOLOGIC"] = AlgorithmStep(step_id="SWITCH_BIOLOGIC", description="Switch Biologic or JAK inhibitor", default_next_step_id="ASSESS_RESPONSE_BIOLOGIC")
        steps["ASSESS_RESPONSE_BIOLOGIC"] = AlgorithmStep(step_id="ASSESS_RESPONSE_BIOLOGIC", description="Assess Response to Biologic/tsDMARD", default_next_step_id="CONTINUE_MONITOR")
        steps["CONTINUE_MONITOR"] = AlgorithmStep(step_id="CONTINUE_MONITOR", description="Continue Current Therapy and Monitor")

        # Simplified conditional logic for demonstration
        activity_level = interpret_das28(das28_score)
        steps["ASSESS_RESPONSE_DMARD"].conditional_next_step_ids = {
             RAActivityLevel.HIGH.name: "CONSIDER_BIOLOGIC",
             RAActivityLevel.MODERATE.name: "OPTIMIZE_DMARD",
             RAActivityLevel.LOW.name: "CONTINUE_MONITOR"
        }
        steps["ASSESS_RESPONSE_DMARD"].default_next_step_id = "CONTINUE_MONITOR"

        can_start_biologic = tb_screening_done_and_negative and not has_active_infection
        eligibility_met = (das28_score or 0) > 5.1 and failed_conventional_dmards >= 2

        if eligibility_met and can_start_biologic:
            if failed_biologic_tnfi:
                 steps["CONSIDER_BIOLOGIC"].default_next_step_id = "SWITCH_BIOLOGIC"
            elif not has_severe_heart_failure_for_tnfi:
                 steps["CONSIDER_BIOLOGIC"].default_next_step_id = "ADD_ANTI_TNF"
            else: # Severe HF is contraindication for Anti-TNF
                 steps["CONSIDER_BIOLOGIC"].warnings.append("Anti-TNF contraindicated due to severe HF. Consider alternative biologic/JAKi.")
                 steps["CONSIDER_BIOLOGIC"].default_next_step_id = "SWITCH_BIOLOGIC" # Assume switch path if anti-TNF CI
        else:
             steps["CONSIDER_BIOLOGIC"].default_next_step_id = "OPTIMIZE_DMARD" # Not eligible or unsafe for biologic

        plan.steps = steps
        return plan

# --- Gastroenterology: Ulcerative Colitis Induction (already implemented with complexity) ---
class UlcerativeColitis(MedicalCondition):
    # Implementation from previous example...
    name = "Ulcerative Colitis"
    description = "Chronic inflammatory bowel disease affecting colon/rectum."
    def get_definition(self) -> str: return self.description
    def get_aetiology(self) -> List[str]: return ["Unknown"]
    def get_risk_factors(self) -> RiskFactors: return RiskFactors(non_modifiable=["Family history", "Ethnicity"])
    def get_signs_symptoms(self) -> List[str]: return ["Bloody diarrhoea", "Urgency", "Tenesmus"]
    def get_complications(self) -> List[str]: return ["Toxic megacolon", "Perforation", "Cancer"]

    def induce_remission_plan(
        self, disease_extent: UCExtent, severity: UCSeverity,
        # Add flags for response to previous steps if needed for navigation
        current_treatment_step_id: str = "START", # To track progress
        response_to_last_step: Optional[BooleanStatus] = None
    ) -> AlgorithmPlan:
        """Generates plan for inducing remission in Ulcerative Colitis."""
        plan = AlgorithmPlan(condition=f"{self.name} - Induce Remission ({severity.name}, {disease_extent.name})", start_step_id="START")
        steps = {}

        # --- Define Steps ---
        steps["START"] = AlgorithmStep(step_id="START", description=f"Initial treatment for {severity.name} {disease_extent.name}")
        # Maintenance step placeholder
        steps["CONSIDER_MAINTENANCE"] = AlgorithmStep(step_id="CONSIDER_MAINTENANCE", description="Remission Achieved - Consider Maintenance Therapy")
        # Severe pathway steps
        steps["ADMIT_SEVERE"] = AlgorithmStep(step_id="ADMIT_SEVERE", description="Admit to hospital for Severe UC", recommended_actions=[ActionRecommendation("Assess VTE risk + LMWH")])
        steps["IV_STEROIDS"] = AlgorithmStep(step_id="IV_STEROIDS", description="IV Corticosteroids", drug_recommendations=[DrugRecommendation(name="IV Hydrocortisone / Methylprednisolone")], default_next_step_id="ASSESS_RESPONSE_SEVERE")
        steps["ASSESS_RESPONSE_SEVERE"] = AlgorithmStep(step_id="ASSESS_RESPONSE_SEVERE", description="Assess response after 72 hours")
        steps["SWITCH_ORAL_STEROIDS"] = AlgorithmStep(step_id="SWITCH_ORAL_STEROIDS", description="Switch to Oral Steroids", default_next_step_id="CONSIDER_MAINTENANCE")
        steps["SECOND_LINE_SEVERE"] = AlgorithmStep(step_id="SECOND_LINE_SEVERE", description="Add IV Ciclosporin OR Biologic (Infliximab)", default_next_step_id="ASSESS_RESPONSE_RESCUE")
        steps["ASSESS_RESPONSE_RESCUE"] = AlgorithmStep(step_id="ASSESS_RESPONSE_RESCUE", description="Assess response to rescue therapy (4-7 days)")
        steps["SURGERY_COLECTOMY"] = AlgorithmStep(step_id="SURGERY_COLECTOMY", description="Consider Colectomy")

        # --- Mild/Moderate Steps ---
        steps["TOPICAL_ASA_PROCTITIS"] = AlgorithmStep(step_id="TOPICAL_ASA_PROCTITIS", description="Topical 5-ASA (Suppository)", default_next_step_id="ASSESS_RESPONSE_PROCTITIS_1")
        steps["ASSESS_RESPONSE_PROCTITIS_1"] = AlgorithmStep(step_id="ASSESS_RESPONSE_PROCTITIS_1", description="Assess Proctitis response (4 weeks)")
        steps["ADD_ORAL_ASA_PROCTITIS"] = AlgorithmStep(step_id="ADD_ORAL_ASA_PROCTITIS", description="Add Oral 5-ASA to Topical 5-ASA", default_next_step_id="ASSESS_RESPONSE_PROCTITIS_2")
        steps["ASSESS_RESPONSE_PROCTITIS_2"] = AlgorithmStep(step_id="ASSESS_RESPONSE_PROCTITIS_2", description="Assess Proctitis response (4 weeks)")
        steps["ADD_TOPICAL_STEROID_PROCTITIS"] = AlgorithmStep(step_id="ADD_TOPICAL_STEROID_PROCTITIS", description="Add Topical Steroid (or switch Oral 5-ASA to Oral Steroid)", default_next_step_id="ASSESS_RESPONSE_PROCTITIS_3")
        steps["ASSESS_RESPONSE_PROCTITIS_3"] = AlgorithmStep(step_id="ASSESS_RESPONSE_PROCTITIS_3", description="Assess Proctitis response (4 weeks)") # -> Refer if fails?

        steps["TOPICAL_ASA_LEFTEXT"] = AlgorithmStep(step_id="TOPICAL_ASA_LEFTEXT", description="Topical 5-ASA (Enema)", default_next_step_id="ADD_ORAL_ASA_LEFTEXT")
        steps["ADD_ORAL_ASA_LEFTEXT"] = AlgorithmStep(step_id="ADD_ORAL_ASA_LEFTEXT", description="Add High-Dose Oral 5-ASA", default_next_step_id="ASSESS_RESPONSE_LEFTEXT_1")
        steps["ASSESS_RESPONSE_LEFTEXT_1"] = AlgorithmStep(step_id="ASSESS_RESPONSE_LEFTEXT_1", description="Assess Left-Sided/Extensive response (4 weeks)")
        steps["ADD_ORAL_STEROID_LEFTEXT"] = AlgorithmStep(step_id="ADD_ORAL_STEROID_LEFTEXT", description="Add Oral Corticosteroid", default_next_step_id="ASSESS_RESPONSE_LEFTEXT_2")
        steps["ASSESS_RESPONSE_LEFTEXT_2"] = AlgorithmStep(step_id="ASSESS_RESPONSE_LEFTEXT_2", description="Assess Left-Sided/Extensive response (4 weeks)") # -> Refer if fails?

        # --- Branching Logic from START ---
        if severity == UCSeverity.SEVERE:
             steps["START"].default_next_step_id = "ADMIT_SEVERE"
             steps["ADMIT_SEVERE"].default_next_step_id = "IV_STEROIDS"
             steps["ASSESS_RESPONSE_SEVERE"].conditional_next_step_ids = {"IMPROVED": "SWITCH_ORAL_STEROIDS", "NO_IMPROVEMENT": "SECOND_LINE_SEVERE"}
             steps["ASSESS_RESPONSE_RESCUE"].conditional_next_step_ids = {"IMPROVED": "CONSIDER_MAINTENANCE", "NO_RESPONSE": "SURGERY_COLECTOMY"}
        elif severity in [UCSeverity.MILD, UCSeverity.MODERATE]:
            if disease_extent == UCExtent.PROCTITIS:
                steps["START"].default_next_step_id = "TOPICAL_ASA_PROCTITIS"
                steps["ASSESS_RESPONSE_PROCTITIS_1"].conditional_next_step_ids = {"REMISSION": "CONSIDER_MAINTENANCE", "NO_RESPONSE": "ADD_ORAL_ASA_PROCTITIS"}
                steps["ASSESS_RESPONSE_PROCTITIS_2"].conditional_next_step_ids = {"REMISSION": "CONSIDER_MAINTENANCE", "NO_RESPONSE": "ADD_TOPICAL_STEROID_PROCTITIS"}
                steps["ASSESS_RESPONSE_PROCTITIS_3"].conditional_next_step_ids = {"REMISSION": "CONSIDER_MAINTENANCE"} # Add failure -> referral path
            else: # Left-sided / Extensive
                steps["START"].default_next_step_id = "TOPICAL_ASA_LEFTEXT"
                steps["ASSESS_RESPONSE_LEFTEXT_1"].conditional_next_step_ids = {"REMISSION": "CONSIDER_MAINTENANCE", "NO_RESPONSE": "ADD_ORAL_STEROID_LEFTEXT"}
                steps["ASSESS_RESPONSE_LEFTEXT_2"].conditional_next_step_ids = {"REMISSION": "CONSIDER_MAINTENANCE"} # Add failure -> referral path

        plan.steps = steps
        return plan

# --- Neurology: Acute Ischaemic Stroke Reperfusion (already implemented with complexity) ---
class AcuteIschaemicStroke(MedicalCondition):
    # Implementation from previous example...
    name = "Acute Ischaemic Stroke"
    description = "Sudden neurological deficit from focal cerebral ischaemia."
    def get_definition(self) -> str: return self.description
    def get_aetiology(self) -> List[str]: return ["Thrombosis", "Embolism", "Small vessel disease"]
    def get_risk_factors(self) -> RiskFactors: return RiskFactors(modifiable=["Hypertension", "Smoking", "Diabetes", "AF"], non_modifiable=["Age", "Family history"])
    def get_signs_symptoms(self) -> List[str]: return ["Unilateral weakness", "Facial droop", "Dysphasia", "Visual defects"]
    def get_complications(self) -> List[str]: return ["Haemorrhagic transformation", "Cerebral oedema", "Aspiration"]

    def get_reperfusion_plan(
        self, time_since_onset_hours: float, nihss_score: int, bp_systolic: int, bp_diastolic: int,
        ct_shows_haemorrhage: bool, ct_shows_large_established_infarct: bool,
        thrombolysis_contraindicated: bool, thrombectomy_possible: bool,
        thrombectomy_target_vessel_present: bool
    ) -> AlgorithmPlan:
        """Determines eligibility for thrombolysis and/or thrombectomy."""
        plan = AlgorithmPlan(condition=f"{self.name} - Reperfusion", start_step_id="START")
        steps = {}

        steps["START"] = AlgorithmStep(step_id="START", description="Assess Reperfusion Eligibility", investigation_recommendations=[InvestigationRecommendation(InvestigationType.CT_HEAD_NON_CONTRAST, urgency="Immediate"), InvestigationRecommendation(InvestigationType.CT_ANGIOGRAM, urgency="Immediate")], default_next_step_id="CHECK_HAEMORRHAGE")
        steps["CHECK_HAEMORRHAGE"] = AlgorithmStep(step_id="CHECK_HAEMORRHAGE", description="Check for Intracranial Haemorrhage (ICH)")
        steps["MANAGE_HAEMORRHAGE"] = AlgorithmStep(step_id="MANAGE_HAEMORRHAGE", description="Manage Haemorrhagic Stroke") # End state
        steps["CHECK_THROMBOLYSIS_TIME"] = AlgorithmStep(step_id="CHECK_THROMBOLYSIS_TIME", description="Assess Thrombolysis Eligibility (Time < 4.5 hours?)")
        steps["CHECK_THROMBOLYSIS_CONTRA"] = AlgorithmStep(step_id="CHECK_THROMBOLYSIS_CONTRA", description="Check Thrombolysis Contraindications")
        steps["OFFER_THROMBOLYSIS"] = AlgorithmStep(step_id="OFFER_THROMBOLYSIS", description="Offer IV Thrombolysis (Alteplase)", default_next_step_id="CHECK_THROMBECTOMY_TIME")
        steps["CHECK_THROMBECTOMY_TIME"] = AlgorithmStep(step_id="CHECK_THROMBECTOMY_TIME", description="Assess Thrombectomy Eligibility (Time/Target Vessel?)")
        steps["OFFER_THROMBECTOMY"] = AlgorithmStep(step_id="OFFER_THROMBECTOMY", description="Offer Mechanical Thrombectomy", default_next_step_id="POST_REPERFUSION_CARE")
        steps["NO_REPERFUSION"] = AlgorithmStep(step_id="NO_REPERFUSION", description="No Acute Reperfusion Therapy Indicated") # End state
        steps["POST_REPERFUSION_CARE"] = AlgorithmStep(step_id="POST_REPERFUSION_CARE", description="Post-Reperfusion Care") # End state

        # Define branching logic
        steps["CHECK_HAEMORRHAGE"].conditional_next_step_ids = {"ICH_PRESENT": "MANAGE_HAEMORRHAGE", "ICH_ABSENT": "CHECK_THROMBOLYSIS_TIME"}
        if time_since_onset_hours <= 4.5:
            steps["CHECK_THROMBOLYSIS_TIME"].default_next_step_id = "CHECK_THROMBOLYSIS_CONTRA"
        else:
            steps["CHECK_THROMBOLYSIS_TIME"].default_next_step_id = "CHECK_THROMBECTOMY_TIME" # Skip lysis check

        if thrombolysis_contraindicated or ct_shows_large_established_infarct:
            steps["CHECK_THROMBOLYSIS_CONTRA"].default_next_step_id = "CHECK_THROMBECTOMY_TIME"
        else:
            steps["CHECK_THROMBOLYSIS_CONTRA"].default_next_step_id = "OFFER_THROMBOLYSIS"

        # Simplified thrombectomy time/criteria check
        if time_since_onset_hours <= 24 and thrombectomy_possible and thrombectomy_target_vessel_present:
             steps["CHECK_THROMBECTOMY_TIME"].default_next_step_id = "OFFER_THROMBECTOMY"
        else:
             steps["CHECK_THROMBECTOMY_TIME"].default_next_step_id = "NO_REPERFUSION"

        plan.steps = steps
        return plan

# ---------------------------------------------
# Section 6: Example Usage (Conceptual - showing some of the classes)
# ---------------------------------------------

# --- Data Setup ---
print("--- Setting up Example Patient Contexts ---")
# ACS Patient
patient_acs = PatientData(age=55, sex=Sex.MALE, is_troponin_raised=True, has_st_elevation=True, has_chest_pain_suspicious_for_acs=True)
# PE Patient
patient_pe = PatientData(has_clinical_signs_dvt=True, is_pe_most_likely_diagnosis=False, heart_rate=105, had_immobilisation_or_surgery_last_4_weeks=False, has_previous_dvt_or_pe=True, has_haemoptysis=False, has_malignancy=False, is_renal_impaired=False)
# COPD Patient
patient_copd = PatientData(oxygen_saturation=90.0, sputum_purulent=True, resp_acidosis_present=True, ph_level=7.28)
# DKA Patient
patient_dka = PatientData(weight_kg=70.0, blood_glucose_mmol_l=30.0, ph_level=7.1, bicarbonate_mmol_l=10.0, blood_ketones_mmol_l=5.0, potassium_mmol_l=3.8, systolic_bp=100)
# RA Patient
patient_ra = PatientData(ra_das28_score=5.5, failed_conventional_dmards=2, failed_biologic_tnfi=False, tb_screening_done_and_negative=True, has_active_infection=False, has_severe_heart_failure_for_tnfi=False)
# UC Patient
patient_uc = PatientData(uc_disease_extent=UCExtent.LEFT_SIDED_COLITIS, uc_severity=UCSeverity.MODERATE)
# Stroke Patient
patient_stroke = PatientData(stroke_symptom_onset_hours=3.0, stroke_nihss_score=15, stroke_bp_systolic=170, stroke_bp_diastolic=90, ct_shows_haemorrhage=False, ct_shows_large_established_infarct=False, thrombolysis_contraindicated=False, thrombectomy_possible=True, thrombectomy_target_vessel_present=True)

# --- Instantiating Handlers ---
print("--- Instantiating Condition Handlers ---")
acs_handler = AcuteCoronarySyndrome()
pe_handler = PulmonaryEmbolism()
copd_handler = AcuteExacerbationCOPD() # Assumes class exists
dka_handler = DiabeticKetoacidosis() # Assumes class exists
ra_handler = RheumatoidArthritis()
uc_handler = UlcerativeColitis() # Assumes class exists
stroke_handler = AcuteIschaemicStroke() # Assumes class exists

# --- Function to Print Plan (Simplified Navigation) ---
def print_plan_path(plan: AlgorithmPlan):
    print(f"\n--- Plan for: {plan.condition} ---")
    current_step_id = plan.start_step_id
    step_count = 0
    max_steps_to_print = 6 # Limit output length

    while current_step_id and step_count < max_steps_to_print:
        step = plan.steps.get(current_step_id)
        if not step:
            print(f"Error: Step ID '{current_step_id}' not found in plan.")
            break

        print(f"\nStep {step_count+1} ({step.step_id}): {step.description}")
        if step.details: print(f"  Details: {step.details}")
        # ... (add printing for actions, investigations, drugs, warnings) ...
        if step.drug_recommendations:
            print("  Drugs:")
            for drug in step.drug_recommendations: print(f"    - {drug.name}")


        # Simplified navigation: just follow default path for demonstration
        next_step_id = step.default_next_step_id
        if not next_step_id and not step.conditional_next_step_ids:
            print("  (End of this path)")
            break

        current_step_id = next_step_id
        step_count += 1
    if step_count == max_steps_to_print:
        print("  ...")


# --- Generating and Printing Plans ---

# ACS Plan
print("\n--- Generating ACS Plan ---")
acs_type = acs_handler.diagnose_acs_type(
    has_st_elevation=patient_acs.has_st_elevation or False,
    is_troponin_raised=patient_acs.is_troponin_raised or False,
    has_st_depression_or_twi=patient_acs.has_st_depression_or_twi or False,
    has_chest_pain_suspicious_for_acs=patient_acs.has_chest_pain_suspicious_for_acs or False
)
if acs_type == ACSType.STEMI:
    acs_plan = acs_handler.get_stemi_management_plan(patient_acs.symptom_onset_hours_acs or 1.0, True) # Assume PCI available
    print_plan_path(acs_plan)
elif acs_type in [ACSType.NSTEMI, ACSType.UNSTABLE_ANGINA]:
    # Need GRACE score calculated (using placeholder function)
    grace_score = calculate_grace_score(patient_acs.age or 55, patient_acs.heart_rate or 90, patient_acs.systolic_bp or 140, patient_acs.creatinine_umol_l or 90, patient_acs.killip_class or KillipClass.CLASS_I, patient_acs.had_cardiac_arrest or False, patient_acs.has_st_depression_or_twi or False, patient_acs.is_troponin_raised or False)
    acs_plan = acs_handler.get_nstemi_ua_management_plan(grace_score or 5, patient_acs.high_bleeding_risk or False) # Assume high risk if score unknown
    print_plan_path(acs_plan)

# PE Plan
print("\n--- Generating PE Plan ---")
pe_plan = pe_handler.get_investigation_management_plan(
    has_clinical_signs_dvt=patient_pe.has_clinical_signs_dvt or False,
    is_pe_most_likely_diagnosis=patient_pe.is_pe_most_likely_diagnosis or False,
    heart_rate=patient_pe.heart_rate or 90,
    had_immobilisation_or_surgery_last_4_weeks=patient_pe.had_immobilisation_or_surgery_last_4_weeks or False,
    has_previous_dvt_or_pe=patient_pe.has_previous_dvt_or_pe or False,
    has_haemoptysis=patient_pe.has_haemoptysis or False,
    has_malignancy=patient_pe.has_malignancy or False,
    is_renal_impaired=patient_pe.is_renal_impaired or False
)
print_plan_path(pe_plan) # This will show the start and conditional possibilities

# COPD Plan
print("\n--- Generating COPD Exacerbation Plan ---")
copd_plan = copd_handler.get_management_plan(
    oxygen_saturation=patient_copd.oxygen_saturation,
    sputum_purulent=patient_copd.sputum_purulent or False,
    resp_acidosis_present=patient_copd.resp_acidosis_present,
    ph_level=patient_copd.ph_level
)
print_plan_path(copd_plan)

# DKA Plan
print("\n--- Generating DKA Plan ---")
dka_plan = dka_handler.get_management_plan(
    weight_kg=patient_dka.weight_kg or 70.0,
    blood_glucose_mmol_l=patient_dka.blood_glucose_mmol_l or 99.0,
    ph_level=patient_dka.ph_level or 7.0,
    bicarbonate_mmol_l=patient_dka.bicarbonate_mmol_l or 5.0,
    blood_ketones_mmol_l=patient_dka.blood_ketones_mmol_l or 99.0,
    potassium_mmol_l=patient_dka.potassium_mmol_l or 3.0,
    systolic_bp=patient_dka.systolic_bp or 90
)
print_plan_path(dka_plan)

# RA Plan
print("\n--- Generating RA Plan ---")
ra_plan = ra_handler.get_management_plan(
    das28_score=patient_ra.ra_das28_score,
    failed_conventional_dmards=len(patient_ra.ra_failed_dmards),
    failed_biologic_tnfi=DrugClass.DMARD_BIOLOGIC_TNF in patient_ra.ra_failed_dmards, # Example check
    tb_screening_done_and_negative=patient_ra.has_active_tb == False, # Example check
    has_active_infection=patient_ra.has_active_infection or False,
    has_severe_heart_failure_for_tnfi=patient_ra.has_heart_failure or False # Example mapping
)
print_plan_path(ra_plan)

# UC Plan
print("\n--- Generating UC Induction Plan ---")
uc_plan = uc_handler.induce_remission_plan(
    disease_extent=patient_uc.uc_disease_extent or UCExtent.LEFT_SIDED_COLITIS, # Provide default if needed
    severity=patient_uc.uc_severity or UCSeverity.MODERATE # Provide default if needed
)
print_plan_path(uc_plan)

# Stroke Plan
print("\n--- Generating Stroke Reperfusion Plan ---")
stroke_plan = stroke_handler.get_reperfusion_plan(
    time_since_onset_hours=patient_stroke.stroke_symptom_onset_hours or 3.0,
    nihss_score=patient_stroke.stroke_nihss_score or 10,
    bp_systolic=patient_stroke.stroke_bp_systolic or 170,
    bp_diastolic=patient_stroke.stroke_bp_diastolic or 90,
    ct_shows_haemorrhage=patient_stroke.stroke_has_intracranial_haemorrhage or False,
    ct_shows_large_established_infarct=patient_stroke.stroke_has_large_established_infarct or False,
    thrombolysis_contraindicated=False, # Assuming false for example
    thrombectomy_possible=True, # Assuming capable centre
    thrombectomy_target_vessel_present=patient_stroke.stroke_has_thrombectomy_target_vessel or False
)
print_plan_path(stroke_plan)
