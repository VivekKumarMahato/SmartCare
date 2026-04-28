from enum import Enum

class RequestStatus(str, Enum):
    pending = "pending"
    accepted = "accepted"
    completed = "completed"

class UserRole(str, Enum):
    patient = "patient"
    donor = "donor"
    admin = "admin"

class BloodGroup(str, Enum):
    A_POS = "A+"
    A_NEG = "A-"
    O_POS = "O+"
    O_NEG = "O-"
    B_POS = "B+"
    B_NEG = "B-"
    AB_POS = "AB+"
    AB_NEG = "AB-"

