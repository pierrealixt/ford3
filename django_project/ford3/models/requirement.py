from django.db import models
from ford3.enums.saqa_qualification_level import SaqaQualificationLevel


class Requirement(models.Model):
    qualification = models.ForeignKey(
        'ford3.qualification',
        on_delete=models.CASCADE,
        related_name='requirement_set')

    description = models.CharField(
        blank=True,
        null=True,
        help_text="A summary of the requirements and type of requirements "
                  "required for the assocaited qualification",
        max_length=255)
    assessment = models.BooleanField(
        blank=True,
        null=True,
        help_text="Is there an assessment as part of the application process?",
        default=False)
    assessment_comment = models.CharField(
        blank=True,
        null=True,
        unique=False,
        help_text='Additional information regarding the assessment involved.',
        max_length=255)

    interview = models.BooleanField(
        blank=True,
        null=True,
        help_text="Is there an interview as part of the application process?",
        default=False)
    admission_point_score = models.IntegerField(
        blank=True,
        null=True,
        help_text="The admission point score required for the qualification")
    min_nqf_level = models.CharField(
        blank=True,
        null=True,
        help_text="The minimum NQF level a person needs to have obtained to "
                  "apply for this qualification",
        max_length=120,
        choices=[(level, level.value) for level in SaqaQualificationLevel]
    )
    portfolio = models.BooleanField(
        blank=True,
        null=True,
        help_text="Does the applicant need to submit a portfolio as part of "
                  "the application process?",
        default=False)
    portfolio_comment = models.CharField(
        blank=True,
        null=True,
        help_text="Additional information regarding the portfolio to be "
                  "submitted",
        max_length=255)

    aps_calculator_link = models.URLField(
        blank=True,
        null=True,
        help_text="A link a calculator or the specifications for calculating"
                  " the required APS score.")
    require_aps_score = models.BooleanField(
        blank=True,
        null=True,
        help_text="Does the applicant need to acheive a certain APS score?",
        default=False)
    require_certain_subjects = models.BooleanField(
        blank=True,
        null=True,
        help_text="Are there specific subjects listed as a prerequisite for "
                  "this qualification",
        default=False)

    def __unicode__(self):
        return self.description
