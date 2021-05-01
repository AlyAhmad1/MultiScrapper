from django.shortcuts import render, redirect
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from . import login_required
from django.http import HttpResponse
from .models import WakanowScrape, BeforePaymentData
from arikair.models import ArikData
from flyairpeace.models import AirpeaceScraper
from jumaia.models import JumaiaScraper
from selenium import webdriver
import time
from django.contrib import messages
from arikair.models import RegisteredUsers, MailOTP
from MultiS.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
import random
import datetime
from urllib.parse import unquote
from django.utils import timezone
import json
import requests

Details = []

# these variables will be used to save information of scraper and account
ALLDATA, ACCOUNT, WEB = [], {}, ''


def form_data(request):
    if request.method == 'POST':
        name = request.POST['Name']
        email = request.POST['Email']
        reference = request.POST['RF']
        e = email.strip()
        n = name.strip()
        r = reference.strip()
        Details, data_show = scraper_form(request, e, n, r)
        Compress_data = json.dumps(Details)
        web = 'WAKANOW'
        data = {'Details': Details, 'Compress_data': Compress_data, 'web': web, 'data_show':data_show}
        return render(request, 'wakanow/Details.html', data)
    data = {'Details': ''}
    return render(request, 'wakanow/Index.html', data)


def scraper_form(request, email, name, reference):
    global Details
    Details.clear()
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    options.add_argument("window-size=1500,1200")
    options.add_argument("no-sandbox")
    options.add_argument("disable-dev-shm-usage")
    options.add_argument("disable-gpu")
    options.add_argument("log-level=3")
    options.add_argument("--disable-xss-auditor")
    options.add_argument("--disable-web-security")
    options.add_argument("--allow-running-insecure-content")
    options.add_argument("--disable-setuid-sandbox")
    options.add_argument("--disable-webgl")
    options.add_argument("--disable-popup-blocking")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(chrome_options=options)
    # driver = webdriver.Chrome()
    try:
        driver.get("https://www.wakanow.com/en-ng/manage-booking")
        try:
            data = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "main")))
        except:
            data = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "main")))

        try:
            link = driver.find_elements(By.TAG_NAME, 'div')[21]
        except:
            try:
                time.sleep(5)
                link = driver.find_elements(By.TAG_NAME, 'div')[21]
            except:
                try:
                    time.sleep(5)
                    link = driver.find_elements(By.TAG_NAME, 'div')[21]
                except:
                    try:
                        time.sleep(5)
                        link = driver.find_elements(By.TAG_NAME, 'div')[21]
                    except:
                        messages.error(request, 'ERRORR')
                        ame = ['Wrong Login Info  Try  Again!!', 0]
                        return ame
        try:
            link.click()
        except:
            time.sleep(5)
            link.click()

        try:
            f = driver.find_element(By.TAG_NAME, 'form')
        except:
            time.sleep(5)
            f = driver.find_element(By.TAG_NAME, 'form')

        input_list = f.find_elements(By.TAG_NAME, 'input')

        input_list[0].send_keys(reference)
        input_list[1].send_keys(name)
        input_list[2].send_keys(email)
        f.find_element(By.TAG_NAME, 'button').click()

    except:
        messages.error(request, 'Wrong Login Information Try  Again!!')
        ame = ['Wrong Login Info  Try  Again!!', 0]
        return ame

    try:
        ame,data_show = data_scraper(request, driver)
        return ame,data_show
    except:
        messages.error(request, 'No Data Found')
        ame = ['No Data Found', 0]
        data_show = []
        return ame, data_show


def data_scraper(request, driver):
    try:
        all_data = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "cards")))
    except:
        all_data = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "cards")))
    try:
        n = all_data.find_element(By.TAG_NAME,'app-passenger-details').find_elements(By.TAG_NAME, 'p')
    except:
        time.sleep(5)
        n = all_data.find_element(By.TAG_NAME,'app-passenger-details').find_elements(By.TAG_NAME, 'p')

    name = str(n[1].text)
    email = str(n[2].text)
    contact = str(n[3].text)
    details = str(n[5].text)

    driver.maximize_window()
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="confirm-payment"]/div/i')))
    except:
        try:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="confirm-payment"]/div/i')))
        except Exception as e:
            raise e

    data = driver.find_elements(By.TAG_NAME, 'i')
    try:
        data[8].click()
        data[9].click()
        # data[10].click()
        # data[11].click()
    except Exception as E:
        print('---')
        print(E)
        print('-------')
        raise E
    try:
        ff = all_data.find_element(By.TAG_NAME, 'app-mbb-flight-details').find_elements(By.TAG_NAME, 'p')
        location = str(ff[3].text)
        date = str(ff[1].text)
        t = str(ff[2].text)
        flight = str(ff[4].text) + str(ff[5].text)
        t_time = str(ff[6].text)
        p = all_data.find_element(By.TAG_NAME, 'app-payment-details').find_elements(By.TAG_NAME, 'p')
        total = str(p[1].text)
        amount_paid = str(p[3].text)
        outstanding = str(p[5].text)
        tt = outstanding[1:]
        total_amount_pay = ''
        for i in tt.split(','):
            total_amount_pay += i
        try:
            total_amount_pay = int(float(total_amount_pay))
        except:
            total_amount_pay = float(total_amount_pay)

        d = [name, email, contact, details, location, date, t, flight, t_time, total, amount_paid, outstanding,
             total_amount_pay]

        data_show = ['Passenger:\t' + name,'Passenger Email:\t'+email,'Details:\t'+details,
                     'Travel:\t'+location, "Date:\t" + date, "Time:\t" +t, "Bill:\t" + total,
                     "Amount Pay:\t" + amount_paid, "Outstanding:\t" + outstanding]

        return d, data_show
    except Exception as E:
        print(E)


@login_required
def home(request):
    if request.session['user'] == 'Admin12345678910!':
        return render(request, 'manager/manager_index.html')

    return render(request, 'wakanow/Index.html')


def sign_in(request):
    if request.method == 'POST':
        email = request.POST['Email']
        password = request.POST['Password']
        all_users = RegisteredUsers.objects.filter(Email=email,Password=password)
        if all_users:
            request.session['user'] = all_users[0].FName
            request.session['email'] = email
            return redirect('home')
        else:
            messages.error(request, 'Invalid Email or Password')
            return render(request, 'wakanow/login.html')
    return render(request, 'wakanow/login.html')


def register_user(request):
    if request.method == 'POST':
        email = request.POST['Email']
        password = request.POST['Password']
        fname = request.POST['fname']
        lname = request.POST['lname']

        # email Checking
        api_key = "996ad77f-aeb0-478b-936c-5c0ee5838da5"
        response = requests.get("https://isitarealemail.com/api/email/validate", params={'email': email},
                                headers = {'Authorization': "Bearer " + api_key })
        status = response.json()['status']
        if status == "invalid":
            messages.error(request, 'Invalid Email')
            return render(request, 'wakanow/Signup.html')
        all_users = RegisteredUsers.objects.filter(Email=email)
        if all_users:
            messages.error(request, 'Email Already Exists')
            return render(request, 'wakanow/Signup.html')
        data = RegisteredUsers(Email=email, Password=password, FName=fname, LName=lname)
        RegisteredUsers.save(data)
        request.session['email'] = email
        request.session['user'] = fname
        messages.error(request, 'Successfully Register')
        return redirect('home')
    return render(request, 'wakanow/Signup.html')


def logout(request):
    del request.session['user']
    del request.session['email']
    return redirect('login')


def reset_password_email(request):
    if request.method == 'POST':
        email = request.POST['Email']
        check_email_exists = RegisteredUsers.objects.filter(Email__iexact=email)
        if check_email_exists.exists():
            key = genotp(email)
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
                cofirmed_email = RegisteredUsers.objects.get(Email=email)
                email = cofirmed_email.id
                send_mail(subject, message, EMAIL_HOST_USER, [receiver], fail_silently=False)
                return redirect('reset_pass', email=email)
        else:
            messages.error(request, "Email Not registered")
            return render(request, 'wakanow/reset_password_enter_email.html')
    return render(request, 'wakanow/reset_password_enter_email.html')


def genotp(email):
    if email:
        try:
            MailOTP.objects.filter(Email=email).delete()
        except:
            pass
        key = random.randint(9999, 999999)
        return key
    else:
        return False


def reset_password(request, email):
    EE = RegisteredUsers.objects.get(id=email)
    id = email
    email = EE.Email
    if request.method == 'POST':
        otp = request.POST['otp']
        if otp:
            otp_confirmation = MailOTP.objects.filter(Email=email, OTP=otp)
            if otp_confirmation.exists():
                verify = MailOTP.objects.get(Email=email)
                if timezone.now() < verify.timestamp:
                    verify.delete()
                    request.session['email'] = email
                    request.session['user'] = str(EE.Email).split('@')[0]

                    return redirect('set_new_pass', id=id)
                else:
                    verify.delete()
                    messages.error(request,'Token Expire')
                    return render(request, 'wakanow/reset_pass_code.html')
            else:
                messages.error(request,'Invalid Token')
                return render(request, 'wakanow/reset_pass_code.html')
    return render(request, 'wakanow/reset_pass_code.html')


def set_new_password(request, id):
    try:
        if request.session['user']:
            if request.method == 'POST':
                password = request.POST['Password']
                if password:
                    EE = RegisteredUsers.objects.get(id=id)
                    EE.Password = password
                    EE.save()
                    request.session['email'] = EE.Email
                    request.session['user'] = str(EE.Email).split('@')[0]
                    messages.error(request, 'Password Changed')
                    return redirect('home')

            return render(request, 'wakanow/set_password.html')
    except:
        raise Exception('No OTP Provide')


def payment(request, Amount, ALLData, web):
    if request.method == 'POST':
        account = request.POST['acc_no']
        purpose = request.POST['purpose']
        ACCOUNT = money_transfer(account, purpose)
        if ACCOUNT:
            ACCOUNT['Amount'] = Amount
            ACCOUNT = json.dumps(ACCOUNT)
            Data_Show = json.loads(ACCOUNT)
            BeforePaymentData.objects.filter(email=request.session['email']).delete()
            BeforePaymentData(email=request.session['email'],
                              web=web,
                              ALL_data=ALLData,Account_data=ACCOUNT,Amount=Amount, Account=account).save()
            return render(request, 'wakanow/Payment.html', {'ACCOUNT': Data_Show,'email': request.session['email']})
        else:
            messages.error(request,'Account not exist')
            return redirect('home')


def money_transfer(account,purpose):
    data = requests.get(url=f'https://app.nuban.com.ng/api/NUBAN-TKLGONRH525?acc_no={account}')
    d = data.json()
    try:
        if d['error']:
            return False
    except:
        d = data.json()[0]
        d['purpose'] = purpose
        return d


def success_pay(request):
    Data = BeforePaymentData.objects.filter(email=request.session['email'])[0]
    d, status = transfer(Data.Account, Data.Amount)
    while(True):
        if status == 200:
            if d['response_description'] == 'REQUEST ID ALREADY EXIST':
                d, status = transfer(Data.Account, Data.Amount)
                continue
            break
        else:
            break
    web = Data.web
    all_data = json.loads(Data.ALL_data)
    account_data = json.loads(Data.Account_data)

    if web == 'WAKANOW':
        wak = WakanowScrape(user_email=request.session['email'], passenger=all_data[0], passenger_email=all_data[1],
                            details=all_data[3], flight = all_data[7], Total_Bill=all_data[9], Amount_Paid=all_data[10],
                            Bill=all_data[11],bank_name = account_data['bank_name'],
                            account_name= account_data['account_name'],account_number = account_data['account_number'],
                            bank_code = account_data['bank_code'],purpose = account_data['purpose'],)
        WakanowScrape.save(wak)
    elif web == 'airpeace':
        Airpeace = AirpeaceScraper(user_email=request.session['email'], passenger=all_data[0],Bill=all_data[10],
                                   bank_name=account_data['bank_name'],
                                   account_name=account_data['account_name'],
                                   account_number=account_data['account_number'],
                                   bank_code=account_data['bank_code'],
                                   purpose=account_data['purpose']
                                   )
        AirpeaceScraper.save(Airpeace)

    elif web == 'arikair':
        Arik = ArikData(user_email=request.session['email'],
                        Pessenger=all_data[0], Flight=all_data[1],
                        Departure=all_data[2], Destination=all_data[3],
                        Date=all_data[4], Time=all_data[5], Total_bagage=all_data[6],
                        Tiket_fare=all_data[7], Tax=all_data[8], Surcharge=all_data[9],
                        service=all_data[10], insurance_fee=all_data[11], Bill=all_data[12],
                        bank_name=account_data['bank_name'],
                        account_name=account_data['account_name'],
                        account_number=account_data['account_number'],
                        bank_code=account_data['bank_code'],
                        purpose=account_data['purpose']
                        )
        ArikData.save(Arik)

    elif web == 'jumaia':
        new_data = json.dumps(all_data)
        jum = JumaiaScraper(user_email=request.session['email'], All_Data=new_data, Bill=str(Data.Amount),
                            bank_name=account_data['bank_name'],
                            account_name=account_data['account_name'],
                            account_number=account_data['account_number'],
                            bank_code=account_data['bank_code'],
                            purpose=account_data['purpose']
                            )
        JumaiaScraper.save(jum)
    messages.error(request, 'Successfully transfer')
    BeforePaymentData.objects.filter(email=request.session['email']).delete()
    return redirect('home')


def transfer(account_number, Amount):
    Api_link = 'https://sandbox.vtpass.com/api/pay'
    key = random.randint(9999, 999999)
    A = random.randint(1, 10)
    random_id = A * key
    par = {'request_id': f'{random_id}',
           'serviceID': 'bank-deposit',
           'billersCode': '1234567890',
           'variation_code': 'gtb',
           'amount': f'{Amount}',
           'phone': '+923076463373'}
    d = requests.post(url=Api_link,auth=('aliahmad538404@gmail.com', 'damit786'), data=par )
    status = d.status_code
    return d.json(), status
