# ctim/ctim/ctia/models/threat_actor.py
from django.db import models
from django.utils import timezone


class ThreatActor(models.Model):
    """
    Represents a threat actor in the cybersecurity context, detailing their origin,
    period of activity, motivations, and the specific behaviors observed.
    """

    name = models.CharField(max_length=255)
    origin = models.TextField()
    activity_period = models.CharField(max_length=100)
    targets = models.TextField()
    motivation = models.TextField()
    notable_info = models.TextField()
    observed_behavior = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Mitigation(models.Model):
    threat_actor = models.ForeignKey(ThreatActor, related_name="mitigations", on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return f"Mitigation for {self.threat_actor.name}"


class RelatedThreatGroup(models.Model):
    main_group = models.ForeignKey(ThreatActor, related_name="related_groups", on_delete=models.CASCADE)
    related_group = models.ForeignKey(ThreatActor, related_name="+", on_delete=models.CASCADE)
    relation = models.CharField(
        max_length=100, null=True, blank=True  # Allows the owner to be null  # Optional in forms as well
    )

    def __str__(self):
        return f"{self.main_group.name} related to {self.related_group.name}"


class CVE(models.Model):
    threat_actor = models.ForeignKey(ThreatActor, related_name="cves", on_delete=models.CASCADE)
    cve_id = models.CharField(max_length=15)
    description = models.TextField()
    exploited_vulnerabilities = models.TextField()

    def __str__(self):
        return self.cve_id


class Risk(models.Model):
    threat_actor = models.ForeignKey(ThreatActor, related_name="risks", on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return f"Risk for {self.threat_actor.name}"
