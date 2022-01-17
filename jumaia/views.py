from django.shortcuts import render, redirect
from django.contrib import messages
import json
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


# def data_update(request, index, whole, T):
#     # whole = unquote(whole)               #for production
#     whole = json.loads(whole)
#     index = int(int(index)-1)
#     A = whole[index][-1]
#     T = int(T) - int(A)
#     del whole[index]
#     Total, Check, D = 0, [], []
#     Check = whole
#     Total = T
#     return redirect('jumaia_scraper1')


@never_cache
@csrf_exempt
def submit_data(request):
    if request.method == 'POST':
        print("---")
        request.session['list_data'] = request.POST.get('all_Data')
        print(request.session['list_data'])
        context = {'data_de': request.session['list_data'], 'Items': "Items", 'web': "web"}
        return render(request, 'jumaia/details.html', context)
    pass