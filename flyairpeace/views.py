from django.shortcuts import render
from selenium import webdriver
import time
import json
from django.contrib import messages
from webdriver_manager.chrome import ChromeDriverManager


def form_data(request):
    if request.method == 'POST':
        name = request.POST['Name']
        reference = request.POST['RF']
        detail, data_show = scraper_form(request, name, reference)
        compress_data = json.dumps(detail)
        web = 'airpeace'
        data = {'Details': detail, 'Compress_data': compress_data, 'web': web, 'data_show': data_show}
        return render(request, 'wakanow/Details.html', data)
    data = {'Details': ''}
    return render(request, 'wakanow/Index.html', data)


def scraper_form(request, name, reference):
    options = webdriver.ChromeOptions()

    options.add_argument("--disable-notifications")
    options.add_argument("headless")
    options.add_argument("disable-gpu")
    options.add_argument("log-level=3")
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
    try:
        driver.get("https://www.flyairpeace.com/managebooking.php")

        while True:
            try:
                iframe_tag = driver.find_elements_by_tag_name('iframe')[0]
                break
            except Exception as e:
                print("iframe_tag Exception", e)
                time.sleep(5)

        driver.switch_to.frame(iframe_tag)
        while True:
            try:
                inputs_tags = driver.find_elements_by_tag_name('input')
                break
            except Exception as e:
                print("input_tag Exception", e)
                time.sleep(5)

        inputs_tags[4].send_keys(name)
        inputs_tags[5].send_keys(reference)
        inputs_tags[7].click()
    except Exception as e:
        print("whole scraper Exception", e)
        messages.success(request, 'Wrong Login Info')
        driver.close()
        return ['Wrong Login Info  Try  Again!!', 0]

    try:
        name, data_show = data_scraper(driver)
        return name, data_show
    except Exception as e:
        print("Data Scraper Exception", e)
        messages.success(request, 'No Data Found')
        driver.close()
        return ['No Data Found', 0], []


def data_scraper(driver):
    while True:
        try:
            time.sleep(5)
            ul_tag = driver.find_elements_by_tag_name('ul')
            break
        except Exception as e:
            time.sleep(5)
            print("ul_tag Exception", e)

    try:
        div_tag = ul_tag[2].find_elements_by_tag_name('div')
        name = str(div_tag[1].text)

        while True:
            try:
                ul_tag[0].find_elements_by_tag_name('li')[3].click()
                break
            except Exception as e:
                time.sleep(5)
                print(e)
        while True:
            try:
                main_data_tag = driver.find_elements_by_class_name('panel-body')[0].find_elements_by_tag_name('div')
                break
            except Exception as e:
                print(e)

        try:
            adult = str(main_data_tag[2].text)
        except Exception as e:
            print(e)
            adult = 0
        try:
            child = str(main_data_tag[5].text)
        except Exception as e:
            print(e)
            child = 0

        flight = str(main_data_tag[4].text)
        flight_no = str(main_data_tag[7].text)
        departure_time = str(main_data_tag[13].text)
        arrival_time = str(main_data_tag[14].text)
        fare_type = str(main_data_tag[14].text)
        net_fare = str(main_data_tag[19].text)
        tax = str(main_data_tag[22].text)
        all_text = main_data_tag[-1].text
        all_text = all_text[:-3]
        total_amount_pay = ''

        for i in all_text.split(','):
            total_amount_pay += i
        try:
            total_amount_pay = int(float(total_amount_pay))
        except Exception as e:
            print(e)
            total_amount_pay = float(total_amount_pay)
        main = [name, adult, child, flight, flight_no, departure_time, arrival_time,
                fare_type, net_fare, tax, total_amount_pay]
        data_show = ["Passenger Name:\t" + name, "Bill:\t"+all_text]
        return main, data_show
    except Exception as e:
        print(e)
        raise Exception('No Data found In this Account')
