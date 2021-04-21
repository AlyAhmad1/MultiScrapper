from django.shortcuts import render
from selenium import webdriver
import time
from django.contrib import messages

Details = []

def form_data(request):
    global Details
    if request.method == 'POST':
        Name = request.POST.get('Name')
        Reference = request.POST.get('RF')
        print(Name, Reference)
        N=Name.strip()
        R=Reference.strip()
        Details = scraper_form(request,N,R)
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
    Name = data_scraper(request, driver)
    if not Name:
        messages.error(request, 'error in Page loading check your internet connection')
        Name = ['No Data Found', 0]
        return Name
    return Name


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
            Flight = 'Flight Number:\t' + str(Name_detail[0].text)
        except:
            time.sleep(5)
            Flight = 'Flight Number:\t' + str(Name_detail[0].text)

        Passanger = 'Passenger :\t' + str(Name_detail[1].text)

        # Flight Details
        Flight_detail = Z[1].find_elements_by_tag_name('tr')[1].find_elements_by_tag_name('td')
        From = 'Moving From:\t' + str(Flight_detail[0].text)
        To = 'Destination :\t' + str(Flight_detail[1].text)
        Date = 'Date:\t' + str(Flight_detail[3].text)
        Time = 'Time:\t' + str(Flight_detail[4].text)
        Seat = 'Seat Number:\t' + str(Flight_detail[6].text)
        Total_bagage = 'Baggage:\t'+ str(Flight_detail[7].text)
        # Payment Details
        Payment_detail = Z[3].find_elements_by_tag_name('tr')
        Tiket_fare = 'Ticket Fare:\t'+ str(Payment_detail[0].find_elements_by_tag_name('td')[1].text)
        Tax = 'Tax:\t' + str(Payment_detail[1].find_elements_by_tag_name('td')[1].text)
        Surcharge = 'Surcharge:\tt'+ str(Payment_detail[2].find_elements_by_tag_name('td')[1].text)
        service = 'Service:\t'+ str(Payment_detail[3].find_elements_by_tag_name('td')[1].text)
        insurance_fee = 'Insurance Fee:\t'+ str(Payment_detail[4].find_elements_by_tag_name('td')[1].text)
        Total = 'Total_Amount:\t' + str(Payment_detail[5].find_elements_by_tag_name('td')[1].text)
        T = Payment_detail[5].find_elements_by_tag_name('td')[1].text[:-3]
        Total_Amout_pay = ''
        for i in T.split(','):
            Total_Amout_pay += i
        print(Total_Amout_pay)
        try:
            Total_Amout_pay = int(float(Total_Amout_pay))
        except:
            Total_Amout_pay = float(Total_Amout_pay)
        WEBSITE = 'AIKAIRPEACE'
        All = [WEBSITE,Passanger,Flight,From,To,Date,Time,Seat,Total_bagage,Tiket_fare, Tax, Surcharge, service,insurance_fee,Total, Total_Amout_pay]

    except:
        All = False
    return All
