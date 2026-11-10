"""
views for the tracker app.
"""

import csv
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.timezone import localtime
from django.views.decorators.http import require_POST

from tracker.forms import UserSettingsForm, WeightEntryForm

from .models import UserSettings, WeightEntry

KG_PER_LB = Decimal("0.45359237")


def _format_weight(weight: Decimal) -> str:
    """Show at most two decimals, without trailing zeros."""
    return f"{weight:.2f}".rstrip("0").rstrip(".")


def _entry_saved_message(entry: WeightEntry, previous: WeightEntry | None) -> str:
    """
    Build the short confirmation shown after a reading is saved.
    """
    message = f"saved {_format_weight(entry.weight)} {entry.unit}"
    if previous is None:
        return message

    previous_weight = previous.weight
    if previous.unit != entry.unit:
        if entry.unit == "kg":
            previous_weight *= KG_PER_LB
        else:
            previous_weight /= KG_PER_LB

    delta = entry.weight - previous_weight
    if abs(delta) < Decimal("0.05"):
        return f"{message} · no change since last entry"
    return f"{message} · {delta:+.1f} {entry.unit} since last entry"


@login_required
def index(request: HttpRequest) -> HttpResponse:
    """
    View for the index page. Displays the weight entry form, the weight
    history chart and handles form submissions.
    Requires user to be logged in.
    """
    user_settings, _ = UserSettings.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = WeightEntryForm(request.POST)
        if form.is_valid():
            previous_entry = (
                WeightEntry.objects.filter(user=request.user)
                .order_by("-timestamp")
                .first()
            )
            weight_entry = form.save(commit=False)
            weight_entry.user = request.user
            weight_entry.save()

            messages.success(
                request,
                _entry_saved_message(weight_entry, previous_entry),
            )
            return redirect("index")
    else:
        form = WeightEntryForm(initial={"unit": user_settings.preferred_unit})

    all_entries = WeightEntry.objects.filter(user=request.user).only(
        "weight", "unit", "timestamp"
    )
    all_entries_serialized = [
        {
            "weight": float(entry.weight),
            "unit": entry.unit,
            "timestamp": localtime(entry.timestamp).isoformat(),
        }
        for entry in all_entries
    ]
    last_entry = (
        WeightEntry.objects.filter(user=request.user).order_by("-timestamp").first()
    )
    context = {
        "form": form,
        "all_entries": all_entries_serialized,
        "last_entry": last_entry,
        "preferred_unit": user_settings.preferred_unit,
    }

    return render(request, "tracker/index.html", context)


@login_required
def all_entries(request: HttpRequest) -> HttpResponse:
    """
    View to show all weight entries for the logged-in user.
    """
    entry_list = WeightEntry.objects.filter(user=request.user).order_by("-timestamp")
    paginator = Paginator(entry_list, 10)
    page_obj = paginator.get_page(request.GET.get("page"))
    page_range = list(
        paginator.get_elided_page_range(page_obj.number, on_each_side=2, on_ends=1)
    )

    context = {
        "page_obj": page_obj,
        "page_range": page_range,
    }
    return render(request, "tracker/all_entries.html", context)


@login_required
@require_POST
def delete_entry(request: HttpRequest, entry_id: int) -> HttpResponse:
    """
    View to delete a specific weight entry.
    """
    entry = get_object_or_404(WeightEntry, id=entry_id, user=request.user)
    entry.delete()
    return redirect("all_entries")


@login_required
def edit_entry(request: HttpRequest, entry_id: int) -> HttpResponse:
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
    }

    return render(request, "tracker/edit_entry.html", context)


@login_required
def export_entries_csv(request: HttpRequest) -> HttpResponse:
    """
    view to export all weight entries as a csv file.
    """
    response = HttpResponse(content_type="text/csv")
    now = timezone.now()
    filename = f"wait_{now.strftime('%Y-%m-%d_%H%M%S')}.csv"
    response["Content-Disposition"] = f'attachment; filename="{filename}"'

    writer = csv.writer(response)
    writer.writerow(["timestamp", "weight", "unit"])  # CSV header

    # Fetch all entries and write them to the CSV
    entries = WeightEntry.objects.filter(user=request.user).order_by("timestamp")
    for entry in entries:
        writer.writerow(
            [localtime(entry.timestamp).isoformat(), entry.weight, entry.unit]
        )

    return response


@login_required
def settings_view(request: HttpRequest) -> HttpResponse:
    """
    view to load and update user preferences.
    """
    user_settings, _ = UserSettings.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = UserSettingsForm(request.POST, instance=user_settings)
        if form.is_valid():
            form.save()
            return redirect("index")
    else:
        form = UserSettingsForm(instance=user_settings)
    return render(request, "tracker/settings.html", {"form": form})
