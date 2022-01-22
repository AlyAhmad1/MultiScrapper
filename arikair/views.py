from django.shortcuts import render
from selenium import webdriver
import time
import json
from django.contrib import messages
from webdriver_manager.chrome import ChromeDriverManager


def form_data(request):
    if request.method == 'POST':
        name = request.POST.get('Name').strip()
        reference = request.POST.get('RF').strip()
        details, data_show = scraper_form(request, name, reference)
        compress_data = json.dumps(details)
        web = 'arikair'
        data = {'Details': details, 'Compress_data': compress_data,
                'web': web, 'data_show': data_show}
        return render(request, 'wakanow/Details.html', data)
    data = {'Details': ''}
    return render(request, 'wakanow/Index.html', data)


def scraper_form(request, name, reference):
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-notifications")
    # options.add_argument("headless")
    # options.add_argument("disable-gpu")
    # options.add_argument("log-level=3")
    # options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
    try:
        driver.get("https://arikair.com/")

        counter = 1
        while counter < 5:
            model_footer_tags = driver.find_elements_by_class_name('modal-footer')
            if len(model_footer_tags) == 2:
                model_footer_tags[1].find_elements_by_tag_name('button')[0].click()
                break
            else:
                counter += 1
                continue
        while True:
            try:
                bar = driver.find_elements_by_tag_name('ul')[1]
                break
            except Exception as e:
                print("---------", e)
                time.sleep(3)

        bar.find_elements_by_tag_name('li')[1].click()
        form = driver.find_elements_by_tag_name('form')[0]
        form_input = form.find_elements_by_tag_name('input')
        time.sleep(5)
        form_input[0].send_keys(reference)
        form_input[1].send_keys(name)
        form_input[2].click()
    except Exception as e:
        print("---------", e)
        messages.success(request, 'Wrong Login Info \n Try  Again!!')
        name = ['Wrong Login Information Try Again!!', 0]
        return name
    name, data_show = data_scraper(driver)
    if not name:
        messages.success(request, 'error in Page loading check your internet connection')
        driver.close()
        name = ['No Data Found', 0]
        data_show = []
        return name, data_show
    return name, data_show


def data_scraper(driver):
    while True:
        try:
            table_data = driver.find_elements_by_tag_name('table')
            break
        except Exception as e:
            print(e)
            time.sleep(5)

    try:
        # Passenger Details
        try:
            name_detail = table_data[0].find_elements_by_tag_name('tr')[1].find_elements_by_tag_name('td')
        except Exception as e:
            print(e)
            time.sleep(5)
            name_detail = table_data[0].find_elements_by_tag_name('tr')[1].find_elements_by_tag_name('td')

        try:
            flight = str(name_detail[0].text)
        except Exception as e:
            print(e)
            time.sleep(5)
            flight = str(name_detail[0].text)

        passenger = str(name_detail[1].text)

        # Flight Details
        flight_detail = table_data[1].find_elements_by_tag_name('tr')[1].find_elements_by_tag_name('td')
        going_from = str(flight_detail[0].text)
        to = str(flight_detail[1].text)
        date = str(flight_detail[3].text)
        time_ = str(flight_detail[4].text)
        total_baggage = str(flight_detail[7].text)

        # Payment Details
        payment_detail = table_data[-3].find_elements_by_tag_name('tr')
        ticket_fare = str(payment_detail[0].find_elements_by_tag_name('td')[1].text)
        tax = str(payment_detail[1].find_elements_by_tag_name('td')[1].text)
        surcharge = str(payment_detail[2].find_elements_by_tag_name('td')[1].text)
        service = str(payment_detail[3].find_elements_by_tag_name('td')[1].text)
        insurance_fee = str(payment_detail[4].find_elements_by_tag_name('td')[1].text)

        # Total = 'Total_Amount:\t' + str(Payment_detail[5].find_elements_by_tag_name('td')[1].text)
        total_payment_details = payment_detail[5].find_elements_by_tag_name('td')[1].text
        total_payment_details = total_payment_details[:-3]
        total_amount_pay = ''
        for i in total_payment_details.split(','):
            total_amount_pay += i
        try:
            total_amount_pay = int(float(total_amount_pay))
        except Exception as e:
            print("------", e)
            total_amount_pay = float(total_amount_pay)

        da = [passenger, flight, going_from, to, date, time_,
              total_baggage, ticket_fare, tax, surcharge, service,
              insurance_fee, total_amount_pay]
        data_show = ['Passenger:\t'+passenger, 'Flight No:\t', 'Starting:\t'+going_from,
                     "Destination\t"+to,
                     "Date:\t"+date, "Time:\t"+time_, "Bagage:\t"+total_baggage,
                     "Ticket Fare:\t"+ticket_fare, "Tax:\t"+tax, "Surcharge:\t"+surcharge,
                     "Service:\t"+service, "Insurance Fee:\t"+insurance_fee,
                     "Total Bill:\t"+total_payment_details]
    except Exception as e:
        print(e)
        da = False
        data_show = []
    return da, data_show
