from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required,user_passes_test

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.models import User

from django.utils import timezone
from django.db import IntegrityError
from django.contrib import messages

from .models import PollModel, PollOption, UserVote

import openpyxl
from django.http import HttpResponse

from django.utils import timezone
# Create your views here.



def MainPage(request):
    if request.user.is_authenticated:
        if request.user.is_superuser or request.user.is_staff:
            return redirect('create_poll')
        return redirect('poll_list')
    return render(request, 'main.html')
def UserRegister(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        User.objects.create_user(username=username, password=password)
        return redirect('login')
    return render(request, 'register.html')

def UserLogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser or user.is_staff:
                return redirect('create_poll')
            return redirect('poll_list')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')


def UserLogout(request):
    logout(request)
    return redirect('login')




def is_admin(user):
    return user.is_staff or user.is_superuser



@login_required
@user_passes_test(is_admin)
def create_poll(request):
    if request.method == "POST":
        question = request.POST.get("question")
        options = request.POST.getlist("options")  
        end_time = request.POST.get("end_time")

        if question and options:
            poll = PollModel.objects.create(
                user=request.user,
                question=question,
                pub_date=timezone.now(),
                end_time=parse_datetime(end_time) if end_time else None
            )
            for opt in options:
                if opt.strip():
                    PollOption.objects.create(poll=poll, option_text=opt)
            return redirect("poll_list")

    return render(request, "create_poll.html",{"now": timezone.now()})



@login_required
def poll_list(request):
    polls = PollModel.objects.all().order_by("-pub_date")
    return render(request, "poll_list.html", {"polls": polls,"is_admin": request.user.is_staff or request.user.is_superuser})



@login_required
def poll_detail(request, poll_id):
    poll = get_object_or_404(PollModel, id=poll_id)
    options = PollOption.objects.filter(poll=poll)

    if request.user.is_staff or request.user.is_superuser:
        return render(request, "poll_detail.html", {
            "poll": poll,
            "options": options,
            "is_admin": True,
            "has_voted": False
        })

    if poll.is_ended:
        return redirect("poll_results", poll_id=poll.id)

    # check if user already voted
    has_voted = UserVote.objects.filter(user=request.user, poll=poll).exists()

    if request.method == "POST" and not has_voted:
        option_id = request.POST.get("option")
        option = get_object_or_404(PollOption, id=option_id, poll=poll)

        try:
            UserVote.objects.create(user=request.user, poll=poll, option=option)
            option.votes += 1
            option.save()
            messages.success(request, "Your vote has been recorded!")
        except IntegrityError:
            messages.error(request, "You have already voted in this poll!")

        return redirect("poll_detail", poll_id=poll.id)

    return render(request, "poll_detail.html", {
        "poll": poll,
        "options": options,
        "is_admin": False,
        "has_voted": has_voted
    })




@login_required
def poll_results(request, poll_id):
    poll = get_object_or_404(PollModel, id=poll_id)
    options = PollOption.objects.filter(poll=poll)

    total_votes = sum(opt.votes for opt in options)

    # Add percentage calculation
    results = []
    for opt in options:
        percent = (opt.votes / total_votes * 100) if total_votes > 0 else 0
        results.append({
            "text": opt.option_text,
            "votes": opt.votes,
            "percent": round(percent, 2)
        })

    return render(request, "poll_results.html", {
        "poll": poll,
        "results": results,
        "total_votes": total_votes,
        "is_admin": request.user.is_staff or request.user.is_superuser
    })




@login_required
@user_passes_test(is_admin)
def admin_poll_list(request):
    polls = PollModel.objects.all().order_by("-pub_date")
    return render(request, "admin_poll_list.html", {"polls": polls})


@login_required
@user_passes_test(is_admin)
def end_poll(request, poll_id):
    poll = get_object_or_404(PollModel, id=poll_id)
    poll.is_ended = not poll.is_ended  
    poll.save()

    if poll.is_ended:
        messages.success(request, f"Poll '{poll.question}' has been ended.")
    else:
        messages.success(request, f"Poll '{poll.question}' has been reopened.")

    return redirect("admin_poll_list")

@login_required
def export_poll_excel(request, poll_id):
    if not request.user.is_staff:
        return HttpResponse("Unauthorized", status=403)

    poll = get_object_or_404(PollModel, id=poll_id)
    votes = UserVote.objects.filter(poll=poll).select_related("user", "option")

   
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Poll Results"

    
    ws.append(["Username", "Option Voted", "Poll Question", "Vote Date"])

   
    for v in votes:
        ws.append([
            v.user.username,
            v.option.option_text,
            poll.question,
            v.user.date_joined.strftime("%Y-%m-%d %H:%M:%S") 
        ])

   
    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"] = f'attachment; filename="poll_{poll_id}_results.xlsx"'
    wb.save(response)
    return response




@login_required
@user_passes_test(is_admin)
def delete_poll_votes(request, poll_id):
    poll = get_object_or_404(PollModel, id=poll_id)
    poll.delete()  # deletes poll + all related options + votes (cascade)

    messages.success(request, f"Poll '{poll.question}' has been deleted successfully.")
    return redirect("admin_poll_list")