from django.shortcuts import render
from selenium import webdriver
import time, json
from django.contrib import messages

Details = []


def form_data(request):
    global Details
    if request.method == 'POST':
        Name = request.POST.get('Name')
        Reference = request.POST.get('RF')
        N=Name.strip()
        R=Reference.strip()
        Details, data_show = scraper_form(request, N, R)
        Compress_data = json.dumps(Details)
        web = 'arikair'
        Data = {'Details': Details, 'Compress_data': Compress_data, 'web': web, 'data_show':data_show}
        return render(request, 'wakanow/Details.html', Data)
    Data = {'Details': ''}
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
        driver.get("https://arikair.com/")
        try:
            bar = driver.find_elements_by_tag_name('ul')[1]
        except:
            try:
                time.sleep(5)
                bar = driver.find_elements_by_tag_name('ul')[1]
            except:
                try:
                    time.sleep(5)
                    bar = driver.find_elements_by_tag_name('ul')[1]
                except:
                    time.sleep(5)
                    bar = driver.find_elements_by_tag_name('ul')[1]
        manage_button = bar.find_elements_by_tag_name('li')[1].click()
        form = driver.find_elements_by_tag_name('form')[0]
        form_input = form.find_elements_by_tag_name('input')
        time.sleep(5)
        form_input[0].send_keys(Reference)
        form_input[1].send_keys(Name)
        form_input[2].click()
    except:
        messages.error(request, 'Wrong Login Info \n Try  Again!!')
        Name = ['Wrong Login Information Try Again!!', 0]
        return Name
    Name, data_Show = data_scraper(request, driver)
    if not Name:
        messages.error(request, 'error in Page loading check your internet connection')
        Name = ['No Data Found', 0]
        data_show = []
        return Name, data_show
    return Name,data_Show


def data_scraper(request, driver):
    try:
        Z = driver.find_elements_by_tag_name('table')
    except:
        try:
            time.sleep(5)
            Z = driver.find_elements_by_tag_name('table')
        except:
            time.sleep(5)
            Z = driver.find_elements_by_tag_name('table')

    try:
        # Passenger Details
        try:
            Name_detail = Z[0].find_elements_by_tag_name('tr')[1].find_elements_by_tag_name('td')
        except:
            time.sleep(5)
            Name_detail = Z[0].find_elements_by_tag_name('tr')[1].find_elements_by_tag_name('td')

        try:
            Flight = str(Name_detail[0].text)
        except:
            time.sleep(5)
            Flight = str(Name_detail[0].text)

        Passanger = str(Name_detail[1].text)

        # Flight Details
        Flight_detail = Z[1].find_elements_by_tag_name('tr')[1].find_elements_by_tag_name('td')
        From = str(Flight_detail[0].text)
        To = str(Flight_detail[1].text)
        Date = str(Flight_detail[3].text)
        Time = str(Flight_detail[4].text)
        Total_bagage = str(Flight_detail[7].text)

        # Payment Details
        Payment_detail = Z[-3].find_elements_by_tag_name('tr')
        Tiket_fare = str(Payment_detail[0].find_elements_by_tag_name('td')[1].text)
        Tax = str(Payment_detail[1].find_elements_by_tag_name('td')[1].text)
        Surcharge = str(Payment_detail[2].find_elements_by_tag_name('td')[1].text)
        service = str(Payment_detail[3].find_elements_by_tag_name('td')[1].text)
        insurance_fee = str(Payment_detail[4].find_elements_by_tag_name('td')[1].text)
        # Total = 'Total_Amount:\t' + str(Payment_detail[5].find_elements_by_tag_name('td')[1].text)
        T = Payment_detail[5].find_elements_by_tag_name('td')[1].text
        T = T[:-3]
        Total_Amout_pay = ''
        for i in T.split(','):
            Total_Amout_pay += i
        try:
            Total_Amout_pay = int(float(Total_Amout_pay))
        except:
            Total_Amout_pay = float(Total_Amout_pay)

        da = [Passanger, Flight, From, To, Date, Time, Total_bagage, Tiket_fare, Tax, Surcharge, service,
              insurance_fee, Total_Amout_pay]
        data_show = ['Passenger:\t'+Passanger, 'Flight No:\t', 'Starting:\t'+From, "Destination\t"+To,
                     "Date:\t"+Date, "Time:\t"+Time, "Bagage:\t"+Total_bagage,
                     "Ticket Fare:\t"+Tiket_fare, "Tax:\t"+Tax, "Surcharge:\t"+Surcharge,
                     "Service:\t"+service, "Insurance Fee:\t"+insurance_fee,
                     "Total Bill:\t"+T]

    except:
        da = False
        data_show = []
    return da,data_show
