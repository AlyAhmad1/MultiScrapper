from django.shortcuts import render, redirect
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from . import login_required
from selenium import webdriver
import time
from django.contrib import messages
import requests
from arikair.models import RegisteredUsers, MailOTP
from MultiS.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
import random
import datetime
from urllib.parse import unquote
from django.utils import timezone
import json
import _pickle as pickle

Details = []

def form_data(request):
    if request.method == 'POST':
        Name = request.POST['Name']
        Email = request.POST['Email']
        Reference = request.POST['RF']
        E=Email.strip()
        N=Name.strip()
        R=Reference.strip()
        Details = scraper_form(request,E,N,R)
        Compress_data = json.dumps(Details)
        Data = {'Details': Details, 'Compress_data': Compress_data}
        return render(request, 'wakanow/Details.html', Data)
    Data = {'Details':''}
    return render(request, 'wakanow/Index.html', Data)


def scraper_form(request, Email, Name, Reference):
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
            link = driver.find_elements(By.TAG_NAME,'div')[21]
        except:
            try:
                time.sleep(5)
                link = driver.find_elements(By.TAG_NAME,'div')[21]
            except:
                try:
                    time.sleep(5)
                    link = driver.find_elements(By.TAG_NAME,'div')[21]
                except:
                    try:
                        time.sleep(5)
                        link = driver.find_elements(By.TAG_NAME,'div')[21]
                    except:
                        messages.error(request, 'ERRORR')
                        Name = ['Wrong Login Info  Try  Again!!', 0]
                        return Name
        try:
            link.click()
        except:
            time.sleep(5)
            link.click()

        try:
            FORM = driver.find_element(By.TAG_NAME,'form')
        except:
            time.sleep(5)
            FORM = driver.find_element(By.TAG_NAME,'form')

        input_list = FORM.find_elements(By.TAG_NAME, 'input')

        input_list[0].send_keys(Reference)
        input_list[1].send_keys(Name)
        input_list[2].send_keys(Email)
        FORM.find_element(By.TAG_NAME,'button').click()

    except:
        messages.error(request, 'Wrong Login Information Try  Again!!')
        Name = ['Wrong Login Info  Try  Again!!', 0]
        return Name

    try:
        Name=data_scraper(request,driver)
        return Name
    except:
        messages.error(request, 'No Data Found')
        Name = ['No Data Found',0]
        return Name


def data_scraper(request, driver):
    try:
        All_data = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "cards")))
    except:
        All_data = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "cards")))

    # All_data = driver.find_element(By.ID,'cards')

    try:
        N = All_data.find_element(By.TAG_NAME,'app-passenger-details').find_elements(By.TAG_NAME, 'p')
    except:
        time.sleep(5)
        N = All_data.find_element(By.TAG_NAME,'app-passenger-details').find_elements(By.TAG_NAME, 'p')


    Name = str(N[1].text)
    Email = str(N[2].text)
    Contact = str(N[3].text)

    driver.maximize_window()
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="confirm-payment"]/div/i')))
    except:
        try:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="confirm-payment"]/div/i')))
        except Exception as e:
            raise e

    data = driver.find_elements(By.TAG_NAME,'i')
    try:
        data[9].click()
        data[10].click()
        data[11].click()
    except Exception as E:
        raise E

    F = All_data.find_element(By.TAG_NAME,'app-mbb-flight-details').find_elements(By.TAG_NAME, 'p')
    Location = str(F[3].text)
    Date = str(F[1].text)
    Time = str(F[2].text)
    Flight = str(F[4].text) + str(F[5].text)
    T_Time = str(F[6].text)


    P = All_data.find_element(By.TAG_NAME,'app-pss-details').find_elements(By.TAG_NAME, 'p')
    Total= str(P[1].text)
    Paid= str(P[3].text)
    Outstanding= str(P[5].text)
    T = P[5].text
    T = T[1:]

    Total_Amout_pay = ''
    for i in T.split(','):
        Total_Amout_pay += i
    try:
        Total_Amout_pay = int(float(Total_Amout_pay))
    except:
        Total_Amout_pay = float(Total_Amout_pay)

    All = [Name,Email,Contact,Location,Date,Time,Flight,T_Time,Total,Paid,Outstanding, T, Total_Amout_pay]
    return All

@login_required
def home(request):
    return render(request, 'wakanow/Index.html')


def sign_in(request):
    if request.method == 'POST':
        email = request.POST['Email']
        password = request.POST['Password']
        all_users = RegisteredUsers.objects.all()
        for i in range(0, len(all_users)):
            if all_users[i].Email != email or all_users[i].Password != password :
                messages.error(request, 'Incorrect Email')
                return render(request, 'wakanow/login.html')
            if all_users[i].Email == email and all_users[i].Password != password :
                messages.error(request, 'Incorrect Password')
                return render(request, 'wakanow/login.html')
            if all_users[i].Email == email and all_users[i].Password == password:
                request.session['user'] = str(email).split('@')[0]
                request.session['email'] = email
                return redirect('home')
    return render(request, 'wakanow/login.html')


def register_user(request):
    if request.method == 'POST':
        email = request.POST['Email']
        password = request.POST['Password']

        # email Checking
        api_key = "f4bbfa4a-a896-4ddc-9e2d-10ae1cb45775"
        response = requests.get("https://isitarealemail.com/api/email/validate", params={'email': email},
                                headers = {'Authorization': "Bearer " + api_key })
        status = response.json()['status']
        if status == "invalid":
            messages.error(request, 'Invalid Email')
            return render(request, 'wakanow/Signup.html')
        all_users = RegisteredUsers.objects.all()
        for i in range(0, len(all_users)):
            if all_users[i].Email==request.POST['Email']:
                messages.error(request, 'Email Already Exists')
                return render(request, 'wakanow/Signup.html')
        data = RegisteredUsers(Email=email, Password=password)
        RegisteredUsers.save(data)
        request.session['email'] = email
        request.session['user'] = str(email).split('@')[0]
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
        check_email_exists =RegisteredUsers.objects.filter(Email__iexact=email)
        if check_email_exists.exists():
            key = genotp(email)
            if key:
                # Set Token Expiry
                two_minute = datetime.timedelta(minutes=2)
                now = timezone.now()
                expiry = (now + two_minute)


                subject = 'Reset Password'
                message = f'Below is your reset password pin {key}'
                recepient = email

                Add_otp=MailOTP(
                    Email=email,
                    OTP=key,
                    timestamp=expiry)
                MailOTP.save(Add_otp)
                cofirmed_email = RegisteredUsers.objects.get(Email=email)
                email=cofirmed_email.id
                send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently = False)
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
        key = random.randint(9999,999999)
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
                verify =MailOTP.objects.get(Email=email)
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


def payment(requests,Amount,ALLData,Temp):
    # Temp =1 Jumaia/details.html
    # Temp =0 wakanow/Details.html
    ALLData = unquote(ALLData).strip('[]').split(',')
    # Data = []

    # ALLData = str(ALLData).strip("'<>() ").replace('\'', '\"')
    ALLData = str(ALLData)
    Data = json.loads(ALLData)

    print('----------------------------')
    print(Data)
    print('----------------------------')

    # Main = [Name, Details, Flight,Flight_No, Departure_Time, Arrival_time, Fare_Type,Net_fare, Tax, Total,T]
    # All = [Name,Email,Contact,Location,Date,Time,Flight,T_Time,Total,Paid,Outstanding, T]

    return render(requests,'wakanow/Payment.html')
