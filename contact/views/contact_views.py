from django.shortcuts import render, get_object_or_404, redirect
from contact.models import Contact
from django.core.paginator import Paginator
from django.db.models import Q
# from django.http import Http404


# Create your views here.
def contact(request, contact_id):
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
        'site_title': f"{single_contact.first_name} {single_contact.last_name}: ",
    }
    return render(request,
                  'contact/contact.html', context=context)


# ATENÇÃO: essa view vai no action do form
def search(request):
    # "querry" é o name do form
    search_value = request.GET.get('querry', '').strip()

    if not search_value:
        return redirect("contact:index")

    # nome_do_campo__<método>
    contacts = Contact.objects \
        .filter(show=True) \
        .filter(
            Q(first_name__icontains=search_value) |
            Q(last_name__icontains=search_value) |
            Q(phone__icontains=search_value) |
            Q(email__icontains=search_value)
        ) \
        .order_by('-id')

    paginator = Paginator(contacts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search_value': search_value,
    }

    return render(request,
                  'contact/index.html', context=context)


def index(request):
    contacts = Contact.objects.filter(show=True).order_by('-id')

    paginator = Paginator(contacts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    return render(request,
                  'contact/index.html',
                  context=context,
                  )
