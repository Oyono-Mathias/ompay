# accounts/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import KycRequestForm     # ← NE PAS commenter
from .models import KycRequest


@login_required
def kyc_status(request):
    last = KycRequest.objects.filter(user=request.user).order_by("-created_at").first()
    return render(request, "accounts/kyc_status.html", {"last": last})


@login_required
def kyc_submit(request):
    # Si une demande est en attente, on bloque la création d'une nouvelle
    pending = KycRequest.objects.filter(user=request.user, status=KycRequest.PENDING).exists()
    if pending:
        messages.warning(request, "Vous avez déjà une demande KYC en attente.")
        return redirect("accounts:kyc_status")

    if request.method == "POST":
        form = KycRequestForm(request.POST, request.FILES)
        if form.is_valid():
            kyc: KycRequest = form.save(commit=False)
            kyc.user = request.user
            kyc.status = KycRequest.PENDING
            kyc.reviewed_at = None
            kyc.reviewed_by = None
            kyc.save()
            messages.success(request, "Votre demande KYC a été soumise. Elle sera examinée par un administrateur.")
            return redirect("accounts:kyc_status")
    else:
        form = KycRequestForm()
    return render(request, "accounts/kyc_submit.html", {"form": form})
