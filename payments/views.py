from decimal import Decimal
import uuid
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction as db_transaction
from django.shortcuts import render, redirect
from django.utils import timezone

from .forms import DepositForm, WithdrawForm, TransferForm
from .models import Wallet, Transaction

@login_required
def dashboard(request):
    wallet = Wallet.objects.filter(user=request.user).first()
    txs = Transaction.objects.filter(user=request.user).order_by("-created_at")[:20]
    return render(request, "payments/dashboard.html", {"wallet": wallet, "transactions": txs})

@login_required
def deposit_view(request):
    if request.method == "POST":
        form = DepositForm(request.POST)
        if form.is_valid():
            amount: Decimal = form.cleaned_data["amount"]
            with db_transaction.atomic():
                wallet = Wallet.objects.select_for_update().get(user=request.user)
                wallet.balance += amount
                wallet.save()
                Transaction.objects.create(
                    user=request.user,
                    tx_type=Transaction.DEPOSIT,
                    amount=amount,
                    reference=uuid.uuid4().hex[:12].upper(),
                )
            messages.success(request, f"Dépôt de {amount} FCFA effectué.")
            return redirect("payments:dashboard")
    else:
        form = DepositForm()
    return render(request, "payments/deposit.html", {"form": form})

@login_required
def withdraw_view(request):
    if request.method == "POST":
        form = WithdrawForm(request.POST)
        if form.is_valid():
            amount: Decimal = form.cleaned_data["amount"]
            with db_transaction.atomic():
                wallet = Wallet.objects.select_for_update().get(user=request.user)
                if wallet.balance < amount:
                    form.add_error("amount", "Solde insuffisant.")
                else:
                    wallet.balance -= amount
                    wallet.save()
                    Transaction.objects.create(
                        user=request.user,
                        tx_type=Transaction.WITHDRAW,
                        amount=amount,
                        reference=uuid.uuid4().hex[:12].upper(),
                    )
                    messages.success(request, f"Retrait de {amount} FCFA effectué.")
                    return redirect("payments:dashboard")
    else:
        form = WithdrawForm()
    return render(request, "payments/withdraw.html", {"form": form})

@login_required
def transfer_view(request):
    if request.method == "POST":
        form = TransferForm(request.POST)
        if form.is_valid():
            recipient = form.cleaned_data["recipient"]
            amount: Decimal = form.cleaned_data["amount"]
            if recipient == request.user:
                form.add_error("recipient_username", "Vous ne pouvez pas vous transférer à vous-même.")
            else:
                with db_transaction.atomic():
                    sender_wallet = Wallet.objects.select_for_update().get(user=request.user)
                    if sender_wallet.balance < amount:
                        form.add_error("amount", "Solde insuffisant.")
                    else:
                        recipient_wallet = Wallet.objects.select_for_update().get(user=recipient)
                        ref = uuid.uuid4().hex[:12].upper()
                        # Débit expéditeur
                        sender_wallet.balance -= amount
                        sender_wallet.save()
                        Transaction.objects.create(
                            user=request.user,
                            tx_type=Transaction.TRANSFER_OUT,
                            amount=amount,
                            reference=ref,
                            related_user=recipient,
                        )
                        # Crédit destinataire
                        recipient_wallet.balance += amount
                        recipient_wallet.save()
                        Transaction.objects.create(
                            user=recipient,
                            tx_type=Transaction.TRANSFER_IN,
                            amount=amount,
                            reference=ref,
                            related_user=request.user,
                        )
                        messages.success(
                            request,
                            f"Transfert de {amount} FCFA envoyé à {recipient.username}."
                        )
                        return redirect("payments:dashboard")
    else:
        form = TransferForm()
    return render(request, "payments/transfer.html", {"form": form})
