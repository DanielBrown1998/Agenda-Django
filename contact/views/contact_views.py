from django.shortcuts import render, get_object_or_404
from contact.models import Contact
# from django.http import Http404


# Create your views here.
def contact(re, contact_id):
    # single_contact = Contact.objects.filter(pk=contact_id, show=True).first()
    single_contact = get_object_or_404(
        Contact,
        pk=contact_id,
        show=True
    )

    # if single_contact is None:
    #     raise Http404()

    context = {
        'contact': single_contact,
        'site_title': f"{single_contact.first_name}: ",
    }
    return render(re,
                  'contact/contact.html', context=context)


def index(re):
    contacts = Contact.objects.filter(show=True).order_by('-id')[:10]

    context = {
        'contacts': contacts,
    }
    return render(re,
                  'contact/index.html', context=context)
