from django.shortcuts import render, redirect
from django.contrib import messages
import _pickle as pickle
import json

Total = 0
D = []
Check = []


def form_data(request):
    global Total,D, Check
    D.clear()
    if request.method == 'POST':
        website = request.POST.get('website')
        link = request.POST.get('Name')
        Amount = int(request.POST.get('RF'))
        Total += Amount
        A = [website, link, Amount]
        Check.append(A)
        messages.error(request, 'Item Added Click Submit button to check details')
        return redirect('home')


def All_data(request):
    global Total, D, Check
    for i in Check:
        D.append(i)
    Items = json.dumps(D)
    Data = {'D': D, 'Total':Total,'Items':Items}
    Check.clear()
    Total = 0
    return render(request, 'jumaia/details.html', Data)


def data_update(request,index, whole, T):
    global Total, Check, D
    whole = str(whole).strip("'<>() ").replace('\'', '\"')
    whole = json.loads(whole)
    index = (int(index)-1)
    A = whole[index]
    T = int(T) - int(A[2])
    del whole[index]
    Total,Check,D = 0, [],[]
    Check = whole
    Total = T

    return redirect('jumaia_scraper1')
