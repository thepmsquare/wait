# Create your views here.
import csv
from datetime import datetime, time

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.utils.timezone import localtime
from django.views.generic.edit import CreateView

from tracker.forms import WeightEntryForm
from .models import WeightEntry  # Assuming WeightEntry is your model


@login_required
def index(request):
    """
    View for the index page. Displays the weight entry form,
    the last 10 weight entries for the logged-in user,
    and handles form submissions.
    Requires user to be logged in.
    """

    if request.method == "POST":
        form = WeightEntryForm(request.POST)
        if form.is_valid():
            weight_entry = form.save(commit=False)
            weight_entry.user = request.user
            weight_entry.save()

            return redirect(reverse("index"))
    else:
        form = WeightEntryForm()
    latest_entries = WeightEntry.objects.filter(user=request.user)[:10]
    latest_entries_serialized = [
        {"weight": entry.weight, "timestamp": localtime(entry.timestamp).isoformat()}
        for entry in latest_entries
    ]
    context = {
        "form": form,
        "latest_entries": latest_entries_serialized,
        "todaymax": datetime.combine(timezone.now(), time.max),
    }

    return render(request, "tracker/index.html", context)


@login_required
def all_entries(request):
    """
    View to show all weight entries for the logged-in user.
    """
    entry_list = WeightEntry.objects.filter(user=request.user).order_by("-timestamp")
    paginator = Paginator(entry_list, 10)
    page_number = request.GET.get("page")

    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        page_obj = paginator.get_page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        page_obj = paginator.get_page(paginator.num_pages)

    context = {
        "page_obj": page_obj,
    }
    return render(request, "tracker/all_entries.html", context)


@login_required
def delete_entry(request, entry_id):
    """
    View to delete a specific weight entry.
    """
    entry = get_object_or_404(WeightEntry, id=entry_id, user=request.user)
    entry.delete()
    return redirect("all_entries")


@login_required
def edit_entry(request, entry_id):
    """
    View to edit a specific weight entry.
    """
    entry = get_object_or_404(WeightEntry, id=entry_id, user=request.user)
    if request.method == "POST":
        form = WeightEntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            return redirect("all_entries")
    else:
        form = WeightEntryForm(instance=entry)

    context = {
        "form": form,
        "entry": entry,
        "todaymax": datetime.combine(timezone.now(), time.max),
    }

    return render(request, "tracker/edit_entry.html", context)


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


def export_entries_csv(request):
    response = HttpResponse(content_type="text/csv")
    now = datetime.now()
    filename = f"wait_{now.strftime('%Y-%m-%d_%H%M%S')}.csv"
    response["Content-Disposition"] = f'attachment; filename="{filename}"'

    writer = csv.writer(response)
    writer.writerow(["Timestamp", "Weight"])  # CSV header

    # Fetch all entries and write them to the CSV
    entries = WeightEntry.objects.filter(user=request.user).order_by("timestamp")
    for entry in entries:
        writer.writerow([entry.timestamp, entry.weight])

    return response
