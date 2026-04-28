from app.models.enums import BloodGroup

COMPATIBILITY_MAP = {
    BloodGroup.O_NEG: [
        BloodGroup.O_NEG, BloodGroup.O_POS,
        BloodGroup.A_NEG, BloodGroup.A_POS,
        BloodGroup.B_NEG, BloodGroup.B_POS,
        BloodGroup.AB_NEG, BloodGroup.AB_POS
    ],
    BloodGroup.O_POS: [
        BloodGroup.O_POS, BloodGroup.A_POS,
        BloodGroup.B_POS, BloodGroup.AB_POS
    ],
    BloodGroup.A_NEG: [
        BloodGroup.A_NEG, BloodGroup.A_POS,
        BloodGroup.AB_NEG, BloodGroup.AB_POS
    ],
    BloodGroup.A_POS: [
        BloodGroup.A_POS, BloodGroup.AB_POS
    ],
    BloodGroup.B_NEG: [
        BloodGroup.B_NEG, BloodGroup.B_POS,
        BloodGroup.AB_NEG, BloodGroup.AB_POS
    ],
    BloodGroup.B_POS: [
        BloodGroup.B_POS, BloodGroup.AB_POS
    ],
    BloodGroup.AB_NEG: [
        BloodGroup.AB_NEG, BloodGroup.AB_POS
    ],
    BloodGroup.AB_POS: [
        BloodGroup.AB_POS
    ]
}

def get_compatible_recipients(donor_blood_group):
    return COMPATIBILITY_MAP.get(donor_blood_group, [])