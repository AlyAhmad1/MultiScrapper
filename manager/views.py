from django.shortcuts import render, redirect
from django.shortcuts import render
from MultiS.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from jumaia.views import D
from arikair.views import Details as D1
from flyairpeace.views import Details as D2
from wakanow.views import Details as D3
import _pickle as pickle
from .models import ManagerData1
from django.contrib import messages


# Create your views here.
def Home(request):

    # for i in Data:
    #     print('Name-----------------')
    #     print(i.website)
    #     print('Form Data-----------------')
    #     Un = pickle.loads(i.form_data)
    #     for j in Un:
    #         print(j)
    #     print('Scrape-----------------')
    #     Un = pickle.loads(i.Scrape_Data)
    #     for j in Un:
    #         for i in j:
    #             print(i)


    return render(request, 'manager/manager_index.html')


def details(request):
    return render(request, 'manager/manager_details.html')


def email(request):
    subject = 'Testing Email'
    message = 'Lets Start Buddy'
    recepient = 'aliahmad538404@gmail.com'
    send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently = False)
    return redirect('manager')


class Output:
    def others(self, request):
        if request.method == 'POST':
            amount = request.POST.get('amount')
            name = request.POST.get('name')
            receiver = request.POST.get('receiver')
            bank = request.POST.get('bank')
            account = request.POST.get('account')
            ccv = request.POST.get('ccv')
            web = request.POST.get('website')
            pay_form = [amount,name,receiver,bank,account,ccv]
            pay_form1 = pickle.dumps(pay_form)
            if web == 'ARIKAIR':
                data = pickle.dumps(D1)
            elif web == 'FLYAIRPEACE':
                data = pickle.dumps(D2)
            elif web == 'WAKANOW':
                data = pickle.dumps(D3)
            else:
                data = pickle.dumps(D)
            s = ManagerData1(website=web, Email=request.session['email'], form_data=pay_form1, Scrape_Data=data)
            s.save()
            messages.error(request, 'Transaction Successful Thank You For Choosing Our Services.')
            return redirect('home')
        messages.error(request, 'Error Try Again')
        return redirect('home')

class IndexDetail:
    def website_filter(self, request, web):
        retrieve_data = ManagerData1.objects.filter(website=web)
        data = {'retrieve_data': retrieve_data}
        return render(request, 'manager/manager_details.html', data)

