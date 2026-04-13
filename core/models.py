from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Election(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return self.title

    @property
    def is_ongoing(self):
        now = timezone.now()
        return self.start_date <= now <= self.end_date

    @property
    def is_expired(self):
        return timezone.now() > self.end_date

    def winner(self):
        candidate = (
            Candidate.objects.filter(election=self)
            .annotate(vote_count=models.Count('votes'))
            .order_by('-vote_count')
            .first()
        )
        return candidate


class Candidate(models.Model):
    election = models.ForeignKey(Election, on_delete=models.CASCADE, related_name='candidates')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    full_name = models.CharField(max_length=200)
    manifesto = models.TextField(blank=True)

    class Meta:
        ordering = ['full_name']

    def __str__(self):
        return self.full_name

    def vote_count(self):
        return self.votes.count()


class Vote(models.Model):
    voter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='votes')
    election = models.ForeignKey(Election, on_delete=models.CASCADE, related_name='votes')
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='votes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('voter', 'election')

    def __str__(self):
        return f'{self.voter.username} -> {self.candidate.full_name} ({self.election.title})'
