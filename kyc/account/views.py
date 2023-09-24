from django.shortcuts import render, redirect
from account.models import KYC
from account.forms import KYCForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

# @login_required

def kyc_registration(request):
    user = request.user
    kyc = None 
    if request.user.is_authenticated:   
        try:
            kyc = KYC.objects.get(user=user)
        except KYC.DoesNotExist:
            kyc = None

    if request.method == "POST":
        form = KYCForm(request.POST, request.FILES, instance=kyc)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = user

        if request.method == "POST":
         form = KYCForm(request.POST, request.FILES, instance=kyc)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = user

            risk_rating = 'low'  # Initialize with the lowest risk rating

# Assess transaction history, location, and potential red flags
        transaction_history = new_form.transaction_history
        location = new_form.location
        red_flags = new_form.red_flags

        if transaction_history == 'high':
            risk_rating = 'high'  # High transaction history risk

        elif location == 'high_risk_area':
            risk_rating = 'high'  # High-risk location

        elif red_flags:
            risk_rating = 'high'  # Presence of red flags

        elif transaction_history == 'medium':
            risk_rating = 'medium'  # Medium transaction history risk

        # You can add more conditions based on your specific criteria

        # Update the KYC model instance with the calculated risk rating
        new_form.risk_rating = risk_rating
        new_form.save()
        new_form.save()

        messages.success(request, "KYC Form submitted successfully. Review pending.")
        return redirect("core:index")
    else:
        form = KYCForm(instance=kyc)

    context = {
        "form": form,
    }
    return render(request, "account/kyc-form.html", context)


