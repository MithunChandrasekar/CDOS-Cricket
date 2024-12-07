from django.db import models
from django.contrib.auth.models import User

    

class Profile(models.Model):
    profile_pic = models.ImageField(null=True, blank = True, default = 'Default.png')
    user = models.ForeignKey(User, max_length=10, on_delete=models.CASCADE, null = True)


class Match(models.Model):
    team1 = models.CharField(max_length=50)
    team2 = models.CharField(max_length=50)
    venue = models.CharField(max_length=50, default = 'none')
    date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, max_length=10, on_delete=models.CASCADE, null = True)

    #def __str__(self):
     #   return f"{self.team1} vs {self.team2} ({self.date})"


class Scoreboard(models.Model):
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
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    teamname = models.CharField(max_length=50, default = 'none')
    runs = models.IntegerField()
    is_wicket = models.BooleanField(default=False)

    
