from django.shortcuts import render, redirect, get_object_or_404
from contact.forms import ContactForms
from django.urls import reverse
from contact.models import Contact


def create(request):
    form_action = reverse('contact:create')
    if request.method == 'POST':

        form = ContactForms(request.POST)

        context = {
            'form': form,
            'form_action': form_action,
            'mode': 'Create'
        }
        if form.is_valid():
            contact = form.save()
            return redirect(
                f'contact:update',
                contact_id=contact.pk)

        return render(
            request,
            'contact/create.html',
            context=context,
        )

    context = {
        'form': ContactForms(),
        'form_action': form_action,
        'mode': 'Create'
    }
    return render(request,
                  'contact/create.html',
                  context=context,
                  )


def update(request, contact_id):
    form_action = reverse('contact:update', args=(contact_id,))
    contact = get_object_or_404(
        Contact,
        pk=contact_id,
        show=True
    )
    if request.method == 'POST':

        form = ContactForms(request.POST, instance=contact)

        context = {
            'form': form,
            'form_action': form_action,
            "mode": "Update"
        }
        if form.is_valid():
            contact = form.save()
            return redirect(
                f'contact:update',
                contact_id=contact.pk)

        return render(
            request,
            'contact/create.html',
            context=context,
        )

    context = {
        'form': ContactForms(instance=contact),
        'form_action': form_action,
        "mode": 'Update'
    }
    return render(
        request,
        'contact/create.html',
        context=context,
    )


def delete(request, contact_id):
    # form_action = reverse('contact:update', args=(contact_id,))
    contact = get_object_or_404(
        Contact,
        pk=contact_id,
        show=True
    )
    confirmation = request.POST.get('confirmation', 'no')
    if confirmation == 'yes':
        contact.delete()
        return redirect("contact:index")

    return render(
        request,
        "contact/contact.html",
        {
            "contact": contact,
            "confirmation": confirmation,
        }
    )
