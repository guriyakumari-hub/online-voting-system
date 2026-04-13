from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import CandidateForm, ElectionForm, UserRegisterForm, UserUpdateForm
from .models import Candidate, Election, Vote


def home(request):
    return redirect('core:election_list')


def register(request):
    if request.user.is_authenticated:
        return redirect('core:election_list')
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Your account was created successfully. You can now log in.')
            return redirect('core:login')
    else:
        form = UserRegisterForm()
    return render(request, 'core/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('core:election_list')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('core:election_list')
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('core:login')


@login_required
def profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was updated.')
            return redirect('core:profile')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'core/profile.html', {'form': form})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password has been updated.')
            return redirect('core:profile')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'core/change_password.html', {'form': form})


@login_required
def election_list(request):
    elections = Election.objects.all()
    ongoing = [e for e in elections if e.is_ongoing]
    expired = [e for e in elections if e.is_expired]
    return render(request, 'core/election_list.html', {
        'ongoing': ongoing,
        'expired': expired,
    })


@login_required
def election_detail(request, pk):
    election = get_object_or_404(Election, pk=pk)
    user_vote = Vote.objects.filter(voter=request.user, election=election).first()
    return render(request, 'core/election_detail.html', {
        'election': election,
        'user_vote': user_vote,
    })


@login_required
def cast_vote(request, pk):
    election = get_object_or_404(Election, pk=pk)
    if not election.is_ongoing:
        messages.error(request, 'This election is not open for voting.')
        return redirect('core:election_detail', pk=pk)
    if request.method == 'POST':
        candidate_id = request.POST.get('candidate')
        candidate = get_object_or_404(Candidate, pk=candidate_id, election=election)
        vote, created = Vote.objects.get_or_create(
            voter=request.user,
            election=election,
            defaults={'candidate': candidate},
        )
        if not created:
            vote.candidate = candidate
            vote.save()
            messages.success(request, 'Your vote was updated.')
        else:
            messages.success(request, 'Your vote has been recorded.')
        return redirect('core:election_detail', pk=pk)
    return redirect('core:election_detail', pk=pk)


def is_admin(user):
    return user.is_staff


@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    elections = Election.objects.all()
    total_votes = Vote.objects.count()
    return render(request, 'core/admin_dashboard.html', {
        'elections': elections,
        'total_votes': total_votes,
    })


@login_required
@user_passes_test(is_admin)
def election_create(request):
    if request.method == 'POST':
        form = ElectionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Election created successfully.')
            return redirect('core:admin_dashboard')
    else:
        form = ElectionForm()
    return render(request, 'core/election_form.html', {'form': form, 'title': 'Create Election'})


@login_required
@user_passes_test(is_admin)
def election_edit(request, pk):
    election = get_object_or_404(Election, pk=pk)
    if request.method == 'POST':
        form = ElectionForm(request.POST, instance=election)
        if form.is_valid():
            form.save()
            messages.success(request, 'Election updated successfully.')
            return redirect('core:admin_dashboard')
    else:
        form = ElectionForm(instance=election)
    return render(request, 'core/election_form.html', {'form': form, 'title': 'Edit Election'})


@login_required
@user_passes_test(is_admin)
def election_delete(request, pk):
    election = get_object_or_404(Election, pk=pk)
    if request.method == 'POST':
        election.delete()
        messages.success(request, 'Election deleted successfully.')
        return redirect('core:admin_dashboard')
    return render(request, 'core/confirm_delete.html', {'object': election, 'title': 'Delete Election'})


@login_required
@user_passes_test(is_admin)
def candidate_list(request):
    candidates = Candidate.objects.select_related('election', 'user').all()
    return render(request, 'core/candidate_list.html', {'candidates': candidates})


@login_required
@user_passes_test(is_admin)
def candidate_create(request):
    if request.method == 'POST':
        form = CandidateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Candidate added successfully.')
            return redirect('core:candidate_list')
    else:
        form = CandidateForm()
    return render(request, 'core/candidate_form.html', {'form': form, 'title': 'Add Candidate'})


@login_required
@user_passes_test(is_admin)
def candidate_edit(request, pk):
    candidate = get_object_or_404(Candidate, pk=pk)
    if request.method == 'POST':
        form = CandidateForm(request.POST, instance=candidate)
        if form.is_valid():
            form.save()
            messages.success(request, 'Candidate updated successfully.')
            return redirect('core:candidate_list')
    else:
        form = CandidateForm(instance=candidate)
    return render(request, 'core/candidate_form.html', {'form': form, 'title': 'Edit Candidate'})


@login_required
@user_passes_test(is_admin)
def candidate_delete(request, pk):
    candidate = get_object_or_404(Candidate, pk=pk)
    if request.method == 'POST':
        candidate.delete()
        messages.success(request, 'Candidate removed successfully.')
        return redirect('core:candidate_list')
    return render(request, 'core/confirm_delete.html', {'object': candidate, 'title': 'Delete Candidate'})
