from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm


def contact(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            subject = form.cleaned_data['subject']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            MAIL_TEMPLATE = f"From: {email}\nMessage:\n{message}"

            try:
                send_mail(subject, MAIL_TEMPLATE, email, ['havok_2004@hotmail.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')

            messages.success(request, f'Thank you {name}! We will get back to you as soon as possible.')
            return redirect('contact')

    context = {
        'page_title': 'Contact',
        'form': form
    }
    return render(request, "sendemail/contact.html", context)

