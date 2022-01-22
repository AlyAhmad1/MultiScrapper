from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth import logout as log_out
from django.shortcuts import render, redirect
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from . import login_required
from django.http import HttpResponse
from .models import WakanowScrape, BeforePaymentData, Payment
from arikair.models import ArikData
from flyairpeace.models import AirpeaceScraper
from jumaia.models import JumaiaScraper
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
from django.contrib import messages
from arikair.models import MailOTP
from MultiS.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
import random
import datetime
from django.utils import timezone
import json
import requests

RegisteredUsers = get_user_model()


def form_data(request):
    if request.method == 'POST':
        name = request.POST['Name'].strip()
        email = request.POST['Email'].strip()
        reference = request.POST['RF'].strip()
        details, data_show = scraper_form(request, email, name, reference)
        compress_data = json.dumps(details)
        web = 'WAKANOW'
        data = {'Details': details, 'Compress_data': compress_data, 'web': web, 'data_show': data_show}
        return render(request, 'wakanow/Details.html', data)
    data = {'Details': ''}
    return render(request, 'wakanow/Index.html', data)


def scraper_form(request, email, name, reference):
    options = webdriver.ChromeOptions()
    # options.add_argument("headless")
    # options.add_argument("disable-gpu")
    # options.add_argument("log-level=3")
    options.add_argument("--disable-notifications")
    # options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
    try:
        driver.get("https://www.wakanow.com/en-ng/manage-booking")
        try:
            WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.TAG_NAME, "main")))
        except Exception as e:
            print("------------", e)
            WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.TAG_NAME, "main")))
        count = 1
        while count < 5:
            try:
                link = driver.find_elements(By.TAG_NAME, 'div')[21]
                link.click()
                break
            except Exception as e:
                print("----------", e)
                time.sleep(3)
                count += 1

        if count == 4:
            messages.success(request, 'Error!!!!')
            return ['Wrong Login Info  Try  Again!!', 0]

        while True:
            try:
                form_tag = driver.find_element(By.TAG_NAME, 'form')
                break
            except Exception as e:
                print("-----------", e)
                time.sleep(2)

        input_list = form_tag.find_elements(By.TAG_NAME, 'input')
        input_list[0].send_keys(reference)
        input_list[1].send_keys(name)
        input_list[2].send_keys(email)
        form_tag.find_element(By.TAG_NAME, 'button').click()

    except Exception as e:
        print("----------", e)
        messages.success(request, 'Wrong Login Information Try  Again!!')
        driver.close()
        return ['Wrong Login Info  Try  Again!!', 0]

    try:
        ame, data_show = data_scraper(driver)
        return ame, data_show
    except Exception as e:
        print("----------", e)
        driver.close()
        messages.success(request, 'No Data Found')
        return ['No Data Found', 0], []


def data_scraper(driver):
    try:
        all_data = WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.ID, "cards")))
    except Exception as e:
        print(e)
        all_data = WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.ID, "cards")))

    while True:
        try:
            passenger_detail = all_data.find_element(By.TAG_NAME, 'app-passenger-details').find_elements(By.TAG_NAME,
                                                                                                         'p')
            break
        except Exception as e:
            print("----------", e)
            time.sleep(2)

    name = str(passenger_detail[1].text)
    email = str(passenger_detail[2].text)
    contact = str(passenger_detail[3].text)
    details = str(passenger_detail[5].text)

    driver.maximize_window()

    for i in range(0, 2):
        try:
            WebDriverWait(driver, 10).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="confirm-payment"]/div/i')))
            break
        except Exception as f:
            print(f)
            time.sleep(3)

    data = driver.find_elements(By.TAG_NAME, 'i')
    try:
        data[8].click()
        data[9].click()
    except Exception as E:
        raise E
    try:
        flight_details = all_data.find_element(By.TAG_NAME, 'app-mbb-flight-details').find_elements(By.TAG_NAME, 'p')
        location = str(flight_details[3].text)
        date = str(flight_details[1].text)
        t = str(flight_details[2].text)
        flight = str(flight_details[4].text) + str(flight_details[5].text)
        t_time = str(flight_details[6].text)

        payment_detail = all_data.find_element(By.TAG_NAME, 'app-payment-details').find_elements(By.TAG_NAME, 'p')
        total = str(payment_detail[1].text)
        amount_paid = str(payment_detail[3].text)
        outstanding = str(payment_detail[5].text)
        tt = outstanding[1:]

        total_amount_pay = ''
        for i in tt.split(','):
            total_amount_pay += i

        try:
            total_amount_pay = int(float(total_amount_pay))
        except Exception as e:
            print(e)
            total_amount_pay = float(total_amount_pay)

        d = [name, email, contact, details, location, date, t, flight, t_time, total, amount_paid, outstanding,
             total_amount_pay]

        data_show = ['Passenger:\t' + name, 'Passenger Email:\t'+email, 'Details:\t'+details,
                     'Travel:\t'+location, "Date:\t" + date, "Time:\t"+t, "Bill:\t" + total,
                     "Amount Pay:\t" + amount_paid, "Outstanding:\t" + outstanding]

        return d, data_show
    except Exception as E:
        raise E


@login_required
def home(request):
    if request.session['user'] == 'Admin12345678910!':
        return render(request, 'manager/manager_index.html')
    return render(request, 'wakanow/Index.html')


def sign_in(request):
    if request.method == 'POST':
        email = request.POST['Email']
        password = request.POST['Password']
        try:
            user = authenticate(Email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "welcome:{}".format(request.user.FName))
                request.session['user'] = request.user.FName
                request.session['email'] = email
                return redirect('home')
            else:
                messages.success(request, 'Invalid Email or Password')
                return render(request, 'wakanow/login.html')
        except Exception as e:
            print(e)
            messages.success(request, 'Invalid Email or Password')
            return render(request, 'wakanow/login.html')
    return render(request, 'wakanow/login.html')


def register_user(request):
    if request.method == 'POST':
        email = request.POST['Email']
        password = request.POST['Password']
        f_name = request.POST['fname']
        l_name = request.POST['lname']

        # email Checking
        api_key = "996ad77f-aeb0-478b-936c-5c0ee5838da5"
        response = requests.get("https://isitarealemail.com/api/email/validate", params={'email': email},
                                headers={'Authorization': "Bearer " + api_key})
        status = response.json()['status']
        if status == "invalid":
            messages.success(request, 'Invalid Email')
            return render(request, 'wakanow/Signup.html')
        all_users = RegisteredUsers.objects.filter(Email=email)
        try:
            if all_users:
                messages.success(request, 'Email Already Exists')
                return render(request, 'wakanow/Signup.html')
        except Exception as e:
            print(e)
            pass
        data = RegisteredUsers(Email=email, FName=f_name, LName=l_name)
        data.set_password(password)
        RegisteredUsers.save(data)
        request.session['email'] = email
        request.session['user'] = f_name
        user = authenticate(Email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Successfully Register')
            return redirect('home')
    return render(request, 'wakanow/Signup.html')


def logout(request):
    del request.session['user']
    del request.session['email']
    log_out(request)
    return redirect('login')


def reset_password_email(request):
    if request.method == 'POST':
        email = request.POST['Email']
        check_email_exists = RegisteredUsers.objects.filter(Email__iexact=email)
        if check_email_exists.exists():
            key = gen_otp(email)
            if key:
                # Set Token Expiry
                two_minute = datetime.timedelta(minutes=2)
                now = timezone.now()
                expiry = (now + two_minute)

                subject = 'Reset Password'
                message = f'Below is your reset password pin {key}'
                receiver = email

                add_otp = MailOTP(
                    Email=email,
                    OTP=key,
                    timestamp=expiry)
                MailOTP.save(add_otp)
                confirmed_email = RegisteredUsers.objects.get(Email=email)
                email = confirmed_email.id
                send_mail(subject, message, EMAIL_HOST_USER, [receiver], fail_silently=False)
                return redirect('reset_pass', email=email)
        else:
            messages.success(request, "Email Not registered")
            return render(request, 'wakanow/reset_password_enter_email.html')
    return render(request, 'wakanow/reset_password_enter_email.html')


def gen_otp(email):
    if email:
        try:
            MailOTP.objects.filter(Email=email).delete()
        except Exception as e:
            print(e)
            pass
        key = random.randint(9999, 999999)
        return key
    else:
        return False


def reset_password(request, email):
    user = RegisteredUsers.objects.get(id=email)
    user_id = email
    email = user.Email
    if request.method == 'POST':
        otp = request.POST['otp']
        if otp:
            otp_confirmation = MailOTP.objects.filter(Email=email, OTP=otp)
            if otp_confirmation.exists():
                verify = MailOTP.objects.get(Email=email)
                if timezone.now() < verify.timestamp:
                    verify.delete()
                    request.session['email'] = email
                    request.session['user'] = str(user.Email).split('@')[0]

                    return redirect('set_new_pass', id=user_id)
                else:
                    verify.delete()
                    messages.success(request, 'Token Expire')
                    return render(request, 'wakanow/reset_pass_code.html')
            else:
                messages.success(request, 'Invalid Token')
                return render(request, 'wakanow/reset_pass_code.html')
    return render(request, 'wakanow/reset_pass_code.html')


def set_new_password(request, user_id):
    try:
        if request.session['user']:
            if request.method == 'POST':
                password = request.POST['Password']
                if password:
                    ee = RegisteredUsers.objects.get(id=user_id)
                    ee.Password = password
                    ee.save()
                    request.session['email'] = ee.Email
                    request.session['user'] = str(ee.Email).split('@')[0]
                    messages.success(request, 'Password Changed')
                    return redirect('home')

            return render(request, 'wakanow/set_password.html')
    except Exception:
        raise Exception('No OTP Provide')


def payment(request, amount, all_data, web):
    BeforePaymentData.objects.filter(email=request.session['email']).delete()
    BeforePaymentData(email=request.session['email'],
                      web=web, ALL_data=all_data, Amount=amount).save()
    return render(request, 'wakanow/Payment.html', {'Amount': amount, 'email': request.session['email']})


def money_transfer(request):
    if request.method == 'POST':
        account = request.POST['acc_no']
        purpose = request.POST['purpose']
        pay = request.POST['pay']
        data = requests.get(url=f'https://app.nuban.com.ng/api/NUBAN-TKLGONRH525?acc_no={account}')
        data_output = data.json()
        print(data_output)

        try:
            if data_output['error']:
                return HttpResponse(False)
        except Exception as e:
            print(e)
            data_output = data.json()[0]
            data_output['purpose'] = purpose
            data_output['PAY'] = pay
            dumps_data_output = json.dumps(data_output)
            # BeforePaymentData.objects.filter(email=request.session['email']).delete()
            # BeforePaymentData(email=request.session['email'],
            #                   web='Direct_Payment', ALL_data=dumps_data_output, Amount=pay).save()
            return render(request, 'wakanow/pay_money.html', data_output)


def success_pay(request):
    data = BeforePaymentData.objects.filter(email=request.session['email'])[0]
    all_data = json.loads(data.ALL_data)
    web = data.web

    if web == 'WAKANOW':
        wak = WakanowScrape(user_email=request.session['email'], passenger=all_data[0], passenger_email=all_data[1],
                            details=all_data[3], flight=all_data[7], Total_Bill=all_data[9], Amount_Paid=all_data[10],
                            Bill=all_data[11],)
        WakanowScrape.save(wak)
    elif web == 'airpeace':
        air_peace = AirpeaceScraper(user_email=request.session['email'], passenger=all_data[0], Bill=all_data[10])
        AirpeaceScraper.save(air_peace)

    elif web == 'arikair':
        arik = ArikData(user_email=request.session['email'],
                        Pessenger=all_data[0], Flight=all_data[1],
                        Departure=all_data[2], Destination=all_data[3],
                        Date=all_data[4], Time=all_data[5], Total_bagage=all_data[6],
                        Tiket_fare=all_data[7], Tax=all_data[8], Surcharge=all_data[9],
                        service=all_data[10], insurance_fee=all_data[11], Bill=all_data[12],
                        )
        ArikData.save(arik)

    elif web == 'jumaia':
        new_data = json.dumps(all_data)
        jum = JumaiaScraper(user_email=request.session['email'], All_Data=new_data, Bill=str(data.Amount),)
        JumaiaScraper.save(jum)

    else:
        new_data = all_data
        d, status = transfer('', data.Amount)
        while True:
            if status == 200:
                if d['response_description'] == 'REQUEST ID ALREADY EXIST':
                    d, status = transfer(data.Account, data.Amount)
                    continue
                break
            else:
                break

        p = Payment(user_email=request.session['email'], Bill=str(data.Amount),
                    bank_name=new_data['bank_name'],
                    account_name=new_data['account_name'],
                    account_number=new_data['account_number'],
                    bank_code=new_data['bank_code'],
                    purpose=new_data['purpose'])
        Payment.save(p)
    messages.success(request, 'Successfully transfer')
    BeforePaymentData.objects.filter(email=request.session['email']).delete()
    return redirect('home')


def transfer(account_number, amount):
    api_link = 'https://sandbox.vtpass.com/api/pay'
    key = random.randint(9999, 999999)
    a = random.randint(1, 10)
    random_id = a * key
    par = {'request_id': f'{random_id}',
           'serviceID': 'bank-deposit',
           'billersCode': '1234567890',
           'variation_code': 'gtb',
           'amount': f'{amount}',
           'phone': '+923076463373'}
    d = requests.post(url=api_link, auth=('aliahmad538404@gmail.com', 'damit786'), data=par)
    status = d.status_code
    return d.json(), status
