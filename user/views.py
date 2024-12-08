"""
This is the views.py file where all the logis of the application view is places
"""
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from .models import Profile, Match, Ball, Scoreboard
from . forms import CreateUserForm, LoginForm, UpdateUserForm, UpdateProfileForm, AddMatchForm


@require_http_methods(["GET"])
def homepage(request):
    """
    This is the homepage view and landing page of the application
    """
    return render(request, 'user/index.html')


@csrf_protect
@require_http_methods(["GET", "POST"])
def register(request):
    """
    This is the regster page which uses create user form from forms.py
    """

    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)

        if form.is_valid():
            current_user = form.save(commit=False)
            form.save()

            send_mail("Welcome to ScoreCricket",
            "All the best to save your memorable innings",
            settings.DEFAULT_FROM_EMAIL, [current_user.email])
            #profile = Profile.objects.create(user=current_user) # pylint: disable=no-member
            Profile.objects.create(user=current_user)
            messages.success(request, "User created!")
            return redirect ('my-login')

    context = {'RegistrationForm': form}
    return render(request, 'user/register.html', context)



@csrf_protect
@require_http_methods(["GET", "POST"])
def my_login(request):
    """
    This is the loginpage which uses loginform from forms.py
    """
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)

        if form.is_valid():

            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth.login(request, user)
                return redirect('dashboard')

    context = {'LoginForm' : form}
    return render(request, 'user/my-login.html', context)




@require_http_methods(["GET"])
def user_logout(request):
    """
    This is the logout function to redirect to homepage
    """
    auth.logout(request)
    return redirect("")


@csrf_protect
@require_http_methods(["GET", "POST"])
def update_scoreboard(request, match_id):
    """
    This is the scoreboard update function which updates the match detail page 
    """
    if request.method == "POST":
        match = get_object_or_404(Match, id=match_id)
        scoreboard, _ = Scoreboard.objects.get_or_create(match=match) # pylint: disable=no-member
        # Ball details
        teamname = request.POST.get("teamname")
        runs = int(request.POST.get("runs"))
        is_wicket = request.POST.get("is_wicket") == "on"

        # Create the ball entry
        Ball.objects.create( # pylint: disable=no-member
            match=match,
            teamname=teamname,
            runs=runs,
            is_wicket=is_wicket,
        )

        # Update the scoreboard
        team1_score = team2_score = team1_wickets = team2_wickets = 0
        team1_balls = Ball.objects.filter(match=match, teamname=match.team1).count() # pylint: disable=no-member
        team2_balls = Ball.objects.filter(match=match, teamname=match.team2).count() # pylint: disable=no-member
        balls = Ball.objects.filter(match=match)  # pylint: disable=no-member

        for ball in balls:
            if ball.teamname == match.team1:
                team1_score += ball.runs
                if ball.is_wicket:
                    team1_wickets += 1
            elif ball.teamname == match.team2:
                team2_score += ball.runs
                if ball.is_wicket:
                    team2_wickets += 1
        # Update the scoreboard model
        scoreboard.team1_score = team1_score
        scoreboard.team2_score = team2_score
        scoreboard.team1_wickets = team1_wickets
        scoreboard.team2_wickets = team2_wickets
        scoreboard.team1_balls = team1_balls
        scoreboard.team2_balls = team2_balls
        scoreboard.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)

@csrf_protect
@require_http_methods(["GET", "POST"])
@login_required(login_url='my-login')
def match_detail(request, match_id):
    """
    This is the match detail view where we show the scoreboard of the application
    """
    match = get_object_or_404(Match, id=match_id)
    scoreboard = Scoreboard.objects.filter(match=match).first() # pylint: disable=no-member
    return render(request, 'user/match_detail.html', {
        'match': match,
        'scoreboard': scoreboard,
    })

@csrf_protect
@require_http_methods(["GET", "POST"])
@login_required(login_url='my-login')
def dashboard(request):
    """
    This is the dashboard page where the user lands once logged in 
    """
    profile_pic = Profile.objects.get(user=request.user) # pylint: disable=no-member
    if request.method == "POST":
        match1 = AddMatchForm(request.POST)
        if match1.is_valid():
            matchitem = match1.save(commit=False)
            matchitem.user = request.user
            matchitem.save()

            return redirect('match_detail', match_id=matchitem.id)
    else:
        match1 = AddMatchForm()


    current_user = request.user.id
    user_matches = Match.objects.all().filter(user = current_user) # pylint: disable=no-member

    context = {
        'AddMatchForm': match1,
        'profilePic': profile_pic,
        'matches': user_matches
    }
    return render(request, 'user/dashboard.html', context)

@csrf_protect
@require_http_methods(["GET", "POST"])
@login_required(login_url ='my-login')
def profile_management(request):
    """
    This is the profile management section used to update profile details of a user
    """
    form = UpdateUserForm( instance= request.user)

    profile = Profile.objects.get(user = request.user) # pylint: disable=no-member
    form_2 = UpdateProfileForm(instance=profile)
    if request.method =="POST":
        form = UpdateUserForm(request.POST, instance = request.user)
        form_2 = UpdateProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('dashboard')

        if form_2.is_valid():
            form_2.save()
            return redirect('dashboard')

    context = {'UserUpdateForm': form, 'ProfileUpdateForm': form_2}

    return render(request, 'user/profile-management.html', context)



@csrf_protect
@require_http_methods(["GET", "POST"])
@login_required(login_url ='my-login')
def delete_account(request):
    """
    This is the view used to delete the account details from the database 
    """
    if request.method == 'POST':
        deleteuser = User.objects.get(username=request.user)
        deleteuser.delete()
        return redirect("")

    return render(request, 'user/delete-account.html')
