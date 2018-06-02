# -*- coding: utf-8 -*-

from django.db import models
from django.utils import timezone

class Fixture(models.Model):
    status = models.CharField(max_length=200, null=True, blank=True)
    homeTeamName = models.CharField(max_length=200)
    awayTeamName = models.CharField(max_length=200)
    goalsAwayTeam = models.IntegerField(null=True, blank=True)
    goalsHomeTeam = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=200)
    competitionId = models.IntegerField(null=True, blank=True)
    opponent = models.CharField(max_length=200)
    gameType = models.CharField(max_length=200)
    result = models.CharField(max_length=200)
    created_date = models.DateTimeField(
        default=timezone.now)
    date = models.DateTimeField()
    matchday = models.IntegerField(null=True, blank=True)
    season = models.CharField(max_length=200)

    def publish(self):
        self.save()

    def __str__(self):
        return self.name


class Standing(models.Model):
    teamName = models.CharField(max_length=200)
    position = models.IntegerField(null=True, blank=True)
    goalDifference = models.IntegerField(null=True, blank=True)
    points = models.IntegerField(null=True, blank=True)
    crestURL = models.CharField(max_length=200)
    matchesPlayed = models.IntegerField(null=True, blank=True)

    def publish(self):
        self.save()

    def __str__(self):
        return self.teamName
