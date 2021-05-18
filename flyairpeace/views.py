from django.shortcuts import render
from selenium.webdriver.common.by import By
from selenium import webdriver
import time, json
from django.contrib import messages

Details = []


def form_data(request):
    global Details
    if request.method == 'POST':
        Name = request.POST['Name']
        Reference = request.POST['RF']
        Detail, data_show = scraper_form(request,Name,Reference)
        Compress_data = json.dumps(Detail)
        web = 'airpeace'
        Data = {'Details': Detail, 'Compress_data': Compress_data, 'web': web, 'data_show': data_show}
        return render(request, 'wakanow/Details.html', Data)
    Data = {'Details':''}
    return render(request, 'wakanow/Index.html', Data)


def scraper_form(request, Name, Reference):
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
    driver = webdriver.Chrome(chrome_options=options)
    # driver = webdriver.Chrome()
    try:
        driver.get("https://www.flyairpeace.com/managebooking.php")
        # time.sleep(15)
        try:
            A = driver.find_elements_by_tag_name('iframe')[0]
        except:
            try:
                time.sleep(5)
                A = driver.find_elements_by_tag_name('iframe')[0]
            except:
                try:
                    time.sleep(5)
                    A = driver.find_elements_by_tag_name('iframe')[0]
                except:
                    time.sleep(5)
                    A = driver.find_elements_by_tag_name('iframe')[0]

        driver.switch_to.frame(A)
        try:
            B = driver.find_elements_by_tag_name('input')
        except:
            try:
                time.sleep(5)
                B = driver.find_elements_by_tag_name('input')
            except:
                time.sleep(5)
                B = driver.find_elements_by_tag_name('input')

        B[4].send_keys(Name)
        B[5].send_keys(Reference)
        B[7].click()
    except:
        messages.success(request, 'Wrong Login Info')
        Name = ['Wrong Login Info  Try  Again!!', 0]
        return Name
    try:
        Name,data_show = data_scraper(request, driver)

        return Name,data_show
    except:
        messages.success(request,'No Data Found')
        Name = ['No Data Found', 0]
        data_show = []
        return Name,data_show


def data_scraper(request, driver):
    try:
        time.sleep(5)
        Z = driver.find_elements_by_tag_name('ul')
    except:
        try:
            time.sleep(5)
            Z = driver.find_elements_by_tag_name('ul')
        except:
            time.sleep(5)
            Z = driver.find_elements_by_tag_name('ul')

    try:
        N = Z[2].find_elements_by_tag_name('div')
        Name = str(N[1].text)

        try:
            Z[0].find_elements_by_tag_name('li')[3].click()
        except:
            try:
                time.sleep(5)
                Z[0].find_elements_by_tag_name('li')[3].click()
            except:
                time.sleep(5)
                Z[0].find_elements_by_tag_name('li')[3].click()
        try:
            p = driver.find_elements_by_class_name('panel-body')[0].find_elements_by_tag_name('div')
        except:
            try:
                time.sleep(5)
                p = driver.find_elements_by_class_name('panel-body')[0].find_elements_by_tag_name('div')
            except:
                try:
                    p = driver.find_elements_by_class_name('panel-body')[0].find_elements_by_tag_name('div')
                except:
                    time.sleep(5)
                    p = driver.find_elements_by_class_name('panel-body')[0].find_elements_by_tag_name('div')
        try:
            Adult = str(p[2].text)
        except:
            Adult = 0
        try:
            child = str(p[5].text)
        except:
            child = 0
        Flight = str(p[4].text)
        Flight_No = str(p[7].text)
        Departure_Time = str(p[13].text)
        Arrival_time = str(p[14].text)
        Fare_Type = str(p[14].text)
        Net_fare = str(p[19].text)
        Tax = str(p[22].text)
        T = p[-1].text
        print('---------')
        T = T[:-3]
        print(T)
        Total_Amout_pay = ''

        for i in T.split(','):
            Total_Amout_pay += i
        try:
            Total_Amout_pay = int(float(Total_Amout_pay))
        except:
            Total_Amout_pay = float(Total_Amout_pay)
        Main = [Name, Adult, child, Flight,Flight_No, Departure_Time, Arrival_time, Fare_Type, Net_fare, Tax, Total_Amout_pay]
        # data_show = ["Passenger Name:\t" + Name, "Flight Name:\t"+Flight,
        #              "Flight No:\t" + Flight_No, "Fare Type:\t"+Fare_Type, "Net Fare:\t"+Net_fare,
        #              "Tax:\t"+Tax, "Bill:\t"+T]
        data_show = ["Passenger Name:\t" + Name, "Bill:\t"+T]
        return Main,data_show
    except Exception as E:
        print(E)
        raise Exception('No Data found In this Account')

