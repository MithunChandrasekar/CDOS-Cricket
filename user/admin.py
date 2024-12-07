from django.contrib import admin

from .models import Match, Profile, Ball, Scoreboard

admin.site.register(Match)
admin.site.register(Ball)
admin.site.register(Profile)
admin.site.register(Scoreboard)