from django.shortcuts import render, redirect, get_object_or_404
from . forms import CreateUserForm, LoginForm, UpdateUserForm, UpdateProfileForm, AddMatchForm 
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required
from . models import Profile, Match, Ball, Scoreboard
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.contrib import messages



def homepage(request):
    return render(request, 'user/index.html')




def register(request):
    
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)

        if form.is_valid():
            current_user = form.save(commit=False)
            form.save()

            send_mail("Welcome to TrackYourEuro", "All the best to track and Save ur leaking euros", settings.DEFAULT_FROM_EMAIL, [current_user.email])
            profile = Profile.objects.create(user=current_user)
            
            messages.success(request, "User created!")
            return redirect ('my-login')

    
    context = {'RegistrationForm': form}
    return render(request, 'user/register.html', context)





def my_login(request):
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





def user_logout(request):
    auth.logout(request)
    
    return redirect("")




def update_scoreboard(request, match_id):
    if request.method == "POST":
        match = get_object_or_404(Match, id=match_id)
        scoreboard, created = Scoreboard.objects.get_or_create(match=match)

        # Ball details
        teamname = request.POST.get("teamname")
        runs = int(request.POST.get("runs"))
        is_wicket = request.POST.get("is_wicket") == "on"

        # Create the ball entry
        Ball.objects.create(
            match=match,
            teamname=teamname,
            runs=runs,
            is_wicket=is_wicket,
        )

        # Update the scoreboard
        team1_score = team2_score = team1_wickets = team2_wickets = 0
    
        team1_balls = Ball.objects.filter(match=match, teamname=match.team1).count()
        team2_balls = Ball.objects.filter(match=match, teamname=match.team2).count()

        balls = Ball.objects.filter(match=match)
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



@login_required(login_url='my-login')
def match_detail(request, match_id):
    match = get_object_or_404(Match, id=match_id)
    current_user = request.user.id
    #user_expenses = Expense.objects.all().filter(user = current_user)
    #total_expenses = user_expenses.aggregate(Sum('amount'))
    scoreboard = Scoreboard.objects.filter(match=match).first()
    # Fetch players for each team
    #team1_players = Player.objects.filter(team=match.team1)
    #team2_players = Player.objects.filter(team=match.team2)
    #'team1_players': team1_players,
    #    'team2_players': team2_players,
    return render(request, 'user/match_detail.html', {
        'match': match,
        'scoreboard': scoreboard,
        
    })


@login_required(login_url='my-login')
def dashboard(request):
    profile_pic = Profile.objects.get(user=request.user)  # Retrieve the user's profile

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
    user_matches = Match.objects.all().filter(user = current_user)

    context = {
        'AddMatchForm': match1,
        'profilePic': profile_pic,
        'matches': user_matches
    }
    return render(request, 'user/dashboard.html', context)


'''

@login_required(login_url='my-login')
def edit(request, id):
    expense = Expense.objects.get(id=id)
    expense_form = ExpenceForm(instance=expense)
    if request.method =="POST":
        expense = Expense.objects.get(id=id)
        form = ExpenceForm(request.POST, instance = expense)
        if form.is_valid():
            form.save()
            return redirect('dashboard')

    context = {'expense_form': expense_form}
    return render(request, 'user/edit.html', context)







def delete(request, id):
    if request.method =='POST' and 'delete' in request.POST:
        expense =Expense.objects.get(id=id)
        expense.delete()

    return redirect('dashboard')


'''


@login_required(login_url ='my-login')
def profile_management(request):
    form = UpdateUserForm( instance= request.user)

    profile = Profile.objects.get(user = request.user)
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





@login_required(login_url ='my-login')
def delete_account(request):
    
    if request.method == 'POST':
        deleteUser = User.objects.get(username=request.user)
        deleteUser.delete() 
        return redirect("")

    return render(request, 'user/delete-account.html')


