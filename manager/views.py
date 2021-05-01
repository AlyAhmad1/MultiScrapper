from django.shortcuts import render, redirect
from django.shortcuts import render
from MultiS.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
import json
from wakanow.models import *
from arikair.models import *
from flyairpeace.models import *
from jumaia.models import *


# Create your views here.
def Home(request):
    return render(request, 'manager/manager_index.html')


def details(request, web):
    if web == 'WAKANOW':
        data = WakanowScrape.objects.all().order_by('id')

    elif web == 'airpeace':
        data = AirpeaceScraper.objects.all().order_by('id')

    elif web == 'arikair':
        data = ArikData.objects.all().order_by('id')

    elif web == 'jumaia':
        data = JumaiaScraper.objects.all().order_by('id')

    return render(request, 'manager/All_details.html', {'data': data, 'web': web})


def details_invoice(request, id, web):
    if web == 'arikair':
        data = ArikData.objects.get(id=id)
        return render(request, 'arikair/arikinvoice.html',{'data':data})
    elif web == 'WAKANOW':
        data = WakanowScrape.objects.get(id=id)
        return render(request, 'wakanow/wakinvoice.html', {'data': data})
    elif web == 'airpeace':
        data = AirpeaceScraper.objects.get(id=id)
        return render(request, 'flyairpeace/flyinvoice.html', {'data':data})
    elif web == 'jumaia':
        data = JumaiaScraper.objects.get(id=id)
        data_detail = json.loads(data.All_Data)
        return render(request, 'jumaia/jumaiainvoice.html', {'data':data,'data_detail':data_detail})
    else:
        data = PaymentTransfer.objects.get(id=id)
        return render(request, 'manager/payment_invoice.html', {'data': data})


def email(request):
    subject = 'Testing Email'
    message = 'Lets Start Buddy'
    recepient = 'aliahmad538404@gmail.com'
    send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently = False)
    return redirect('manager')
