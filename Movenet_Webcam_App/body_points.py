from enum import Enum


class BodyPoint(Enum):
    nose = 0
    eye_left = 1
    eye_rite = 2
    ear_left = 3
    ear_rite = 4
    shoulder_left = 5
    shoulder_rite = 6
    elbow_left = 7
    elbow_rite = 8
    wrist_left = 9
    wrist_rite = 10
    waist_left = 11
    waist_rite = 12


class BodyPointColor(Enum):
    nose             = (255, 171, 0)    # FFAB00
    eye_left         = (33, 150, 243)   # 2196F3
    eye_rite         = (13, 71, 161)    # 0D47A1
    ear_left         = (255, 183, 77)   # FFB74D
    ear_rite         = (230, 81, 0)     # E65100
    shoulder_left    = (244, 143, 177)  # F48FB1
    shoulder_rite    = (194, 24, 91)    # C2185B
    elbow_left       = (244, 67, 54)    # F44336
    elbow_rite       = (183, 28, 28)    # B71C1C
    wrist_left       = (244, 255, 129)  # F4FF81
    wrist_rite       = (174, 234, 0)    # AEEA00
    waist_left       = (255, 241, 118)  # FFF176
    waist_rite       = (249, 168, 37)   # F9A825

    
color_array = [
    BodyPointColor.eye_left.value,
    BodyPointColor.eye_rite.value,
    BodyPointColor.ear_left.value,
    BodyPointColor.ear_rite.value,
    BodyPointColor.shoulder_left.value,
    BodyPointColor.shoulder_rite.value,
    BodyPointColor.elbow_left.value,
    BodyPointColor.elbow_rite.value,
    BodyPointColor.wrist_left.value,
    BodyPointColor.wrist_rite.value,
    BodyPointColor.waist_left.value,
    BodyPointColor.waist_rite.value]
