from enum import Enum


class SaqaQualificationLevel(Enum):

    LEVEL_1 = 'Grade 9'
    LEVEL_2 = 'Grade 10 and National (vocational) Certificates level 2'
    LEVEL_3 = 'Grade 11 and National (vocational) Certificates level 3'
    LEVEL_4 = (
        'Grade 12 (National Senior Certificate) and National '
        '(vocational) Cert.'
    )
    LEVEL_5 = 'Higher Certificates and Advanced National (vocational) Cert.'
    LEVEL_6 = 'National Diploma and Advanced certificates'
    LEVEL_7 = (
        'Bachelor\'s degree, Advanced Diplomas, '
        'Post Graduate Certificate and B-tech'
    )
    LEVEL_8 = (
        'Honours degree, Post Graduate diploma and Professional Qualifications'
    )
    LEVEL_9 = 'Master\'s degree'
    LEVEL_10 = 'Doctor\'s degree'
