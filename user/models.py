"""
    This is the models.py file where the database id defined
"""

from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """
    This is used to get th eprofile picture from the user
"""
    profile_pic = models.ImageField(null=True, blank = True, default = 'Default.png')
    user = models.ForeignKey(User, max_length=10, on_delete=models.CASCADE, null = True)


class Match(models.Model):
    """
    This is used to create the match table
"""
    team1 = models.CharField(max_length=50)
    team2 = models.CharField(max_length=50)
    venue = models.CharField(max_length=50, default = 'none')
    date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, max_length=10, on_delete=models.CASCADE, null = True)


class Scoreboard(models.Model):
    """
    each match wil have a scoreboard to write the scored 
"""
    match = models.OneToOneField(Match, on_delete=models.CASCADE)
    team1_score = models.IntegerField(default=0)
    team2_score = models.IntegerField(default=0)
    team1_wickets = models.IntegerField(default=0)
    team2_wickets = models.IntegerField(default=0)
    team1_balls = models.IntegerField(default=0)
    team2_balls = models.IntegerField(default=0)


    def __str__(self):
        return f"Scoreboard for {self.match}"



class Ball(models.Model):
    """
    the scoreboard is sum of the ball details 
"""
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    teamname = models.CharField(max_length=50, default = 'none')
    runs = models.IntegerField()
    is_wicket = models.BooleanField(default=False)
