from states import OppurtunityEvidenceStates, MotiveEvidenceStates, SpecialEvidenceStates

class Submit:
    # list of evidence that can be used to prove that the suspect had the oppurtunity to commit the crime
    oppurtunity_evidence = [
        OppurtunityEvidenceStates.LOCATION_DURING_CRIME,
        OppurtunityEvidenceStates.FINGERPRINTS,
        OppurtunityEvidenceStates.BLOOD,
        OppurtunityEvidenceStates.HAIR,
        OppurtunityEvidenceStates.FOOTPRINTS
    ]
    # list of evidence that can be used to prove that the suspect had a motive to commit the crime
    motive_evidence = [MotiveEvidenceStates.MURDER_MOTIVE]