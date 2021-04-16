from django.shortcuts import render
from django.http import Http404
from selenium import webdriver
import time
from django.contrib import messages

Details = []

def form_data(request):
    global Details
    if request.method == 'POST':
        Name = request.POST['name']
        Reference = request.POST['RF']
        Details = scraper_form(request,Name,Reference)
        Data = {'Details':Details}
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
        time.sleep(15)
        A = driver.find_elements_by_tag_name('iframe')[0]
        driver.switch_to.frame(A)
        B = driver.find_elements_by_tag_name('input')
        B[4].send_keys(Name)
        B[5].send_keys(Reference)
        B[7].click()
        time.sleep(20)
    except:
        Name = ['Wrong Login Info  Try  Again!!', 0]
        return Name
    try:
        Name = data_scraper(request, driver)
        return Name
    except:
        Name = ['No Data Found', 0]
        return Name


def data_scraper(request, driver):
    try:
        Z = driver.find_elements_by_tag_name('ul')
    except:
        time.sleep(10)
        Z = driver.find_elements_by_tag_name('ul')
    try:
        # Name = Z[2].text
        N = Z[2].find_elements_by_tag_name('div')
        Name = 'Passenger\t'+ str(N[1].text)
        Details = 'Details\t'+ str(N[2].text)

        Z[0].find_elements_by_tag_name('li')[3].click()
        p = driver.find_elements_by_class_name('panel-body')[0].find_elements_by_tag_name('div')
        Flight = 'Flight From\t' + str(p[3].text)
        Flight_No = 'Flight No\t' + str(p[7].text)
        Departure_Time = 'Departure Time\t' + str(p[10].text)
        Arrival_time = 'Arrival Time\t'+ str(p[13].text)
        Fare_Type = 'Fare Type\t'+ str(p[14].text)
        Net_fare = 'Net Fare\t'+ str(p[19].text)
        Tax = 'Tax\t'+ str(p[22].text)
        Total = 'Total\t'+ str(p[25].text)
        T = p[25].text
        # Main = [str(Name) ,price_info[0].text]
        Main = [Name, Details, Flight,Flight_No, Departure_Time, Arrival_time, Fare_Type,Net_fare, Tax, Total,T]
        return Main
    except :
           raise Exception('No Data found In this Account')

