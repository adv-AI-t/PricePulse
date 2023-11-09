import pandas as pd
from ModelCode.WebData.sentiment_analysis import sentiment_analysis
from flask import Flask, render_template, request
from ModelCode.WebData.contact_mail import send_mail
from ModelCode.WebData.Database import area_data
import datetime
import pywhatkit
import csv

from ModelCode.Rent.Hinjewadi_Magicbricks import hinjewadi_model
from ModelCode.Rent.Kharadi_Magicbricks import kharadi_model
from ModelCode.Rent.Baner_Magicbricks import baner_model
from ModelCode.Rent.Hadapsar_Magicbricks import hadapsar_model
from ModelCode.Rent.Wagholi_Magicbricks import wagholi_model
from ModelCode.Rent.Wakad_Magicbricks import wakad_model

from ModelCode.Purchase.Hinjewadi_purchase import hinjewadi_purchase
from ModelCode.Purchase.Baner_purchase import baner_purchase
from ModelCode.Purchase.Wakad_purchase import wakad_purchase
from ModelCode.Purchase.Kharadi_purchase import kharadi_purchase
from ModelCode.Purchase.Wagholi_purchase import wagholi_purchase
from ModelCode.Purchase.Hadapsar_purchase import hadapsar_purchase



prices = {}
prices_buy = []

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")


@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == "POST":
        contact_us = {
            'email' : request.form['email'],
            'name' : request.form['name'],
            'phone_num' : request.form['phone_num'],
            'message': request.form['message']

        }
        print(contact_us)

        current_time = datetime.datetime.now()

        # Extract hours, minutes, and seconds
        current_hour = current_time.hour
        current_minute = current_time.minute

        message_to_send = f"Hi *{contact_us['name']}*,\nThank you for reaching out to us! We've received your message and appreciate your interest in PricePulse. \n\nOur team is on it and will get back to you shortly."

        if(sentiment_analysis(contact_us['message']) < 0):
            message_to_send = f"Hi *{contact_us['name']}*,\nThank you for reaching out to us! We've received your message. \nSorry for the inconvenience caused. \n\nOur team is on it and will get back to you shortly."

        pywhatkit.sendwhatmsg_instantly(f"+91{contact_us['phone_num']}", message_to_send)

        send_mail(recipient_email=contact_us['email'],subject=f"Response to {contact_us['name']}",message=message_to_send)
        return render_template('/contact.html')
    return render_template("contact.html")

@app.route('/area/<int:num>',  methods=['GET', 'POST'])
def area(num):
    area = area_data[num]
    current_area = area[0]
    global prices

    if request.method == 'POST':

        form_data = {


            # 'amount': int(request.form['Amount']),
            'Unfurnished': int(((request.form['furniture'])[4])),
            'Semi-Furnished': int(((request.form['furniture'])[2])),
            'Furnished': int(((request.form['furniture'])[0])),
            # 'Furnishing' : int((request.form['furniture'])[0]),
            'Area_sqft': int(request.form['SquareFeet']),
            'BHK': int(request.form['Bedrooms'])


            # 'floor': int(request.form['Floor']),
            # 'parking': int(request.form['Parking']),
            # 'propertyage': int(request.form['PropertyAge']),

        }
        form = {

            # 'BHK': int(request.form['Bedrooms']),
            'Area_sqft': int(request.form['SquareFeet']),
            # 'amount': int(request.form['Amount']),
            'Unfurnished': int(((request.form['furniture'])[4])),
            'Semi-Furnished': int(((request.form['furniture'])[2])),
            'Furnished': int(((request.form['furniture'])[0])),
            'BHK': int(request.form['Bedrooms']),
            # 'floor': int(request.form['Floor']),
            # 'parking': int(request.form['Parking']),
            # 'propertyage': int(request.form['PropertyAge']),
            'email' : request.form['email']
        }



        price = 0
        with open("Data/Rent Data/test.csv", 'w', newline='') as csvfile:

            fieldnames = form_data.keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()

            writer.writerow(form_data)
        test = pd.read_csv("Data/Rent Data/test.csv")

        if(current_area == "Hinjewadi"):
            price = int((hinjewadi_model.predict(test))[0])

        elif (current_area == "Kharadi"):
            price = int((kharadi_model.predict(test))[0])

        elif (current_area == "Baner"):
            price = int((baner_model.predict(test))[0])

        elif (current_area == "Hadapsar"):
            price = int((hadapsar_model.predict(test))[0])

        elif (current_area == "Wagholi"):
            price = int((wagholi_model.predict(test))[0])

        elif (current_area == "Wakad"):
            price = int((wakad_model.predict(test))[0])

        prices = {
                  "Hinjewadi": int((hinjewadi_model.predict(test))[0]),
                  "Kharadi": int((kharadi_model.predict(test))[0]),
                  "Baner": int((baner_model.predict(test))[0]),
                  "Hadapsar": int((hadapsar_model.predict(test))[0]),
                  "Wagholi": int((wagholi_model.predict(test))[0]),
                  "Wakad": int((wakad_model.predict(test))[0])
                }


        send_mail(form['email'],f"Rent price for {current_area}",message=f"Choice Summary\nNo. of Bedrooms : {form['BHK']}\nArea : {form['Area_sqft']}\nRent : ₹{price}\n\nThank you visit us again")
        return render_template('result.html', area=area, area_data=area_data, price =price,num=num, form_data=form_data, form = form)
    return render_template('area_rent.html', area = area, area_data = area_data, num=num)


@app.route('/area_buy/<int:num>',  methods=['GET', 'POST'])
def area_buy(num):
    area = area_data[num]
    current_area = area[0]
    global prices_buy

    if request.method == 'POST':

        form_data_buy = {

            # 'amount': int(request.form['Amount']),
            'Unfurnished': int(((request.form['furniture'])[4])),
            'Semi-Furnished': int(((request.form['furniture'])[2])),
            'Furnished': int(((request.form['furniture'])[0])),
            # 'Furnishing' : int((request.form['furniture'])[0]),
            'Area_sqft': int(request.form['SquareFeet']),
            'BHK': int(request.form['Bedrooms'])

            # 'floor': int(request.form['Floor']),
            # 'parking': int(request.form['Parking']),
            # 'propertyage': int(request.form['PropertyAge']),

        }
        form_buy = {

            # 'BHK': int(request.form['Bedrooms']),
            'Area_sqft': int(request.form['SquareFeet']),
            # 'amount': int(request.form['Amount']),
            'Unfurnished': int(((request.form['furniture'])[4])),
            'Semi-Furnished': int(((request.form['furniture'])[2])),
            'Furnished': int(((request.form['furniture'])[0])),
            'BHK': int(request.form['Bedrooms']),
            # 'floor': int(request.form['Floor']),
            # 'parking': int(request.form['Parking']),
            # 'propertyage': int(request.form['PropertyAge']),
            'email': request.form['email']
        }

        price_buy = 0
        with open("Data/Purchase Data/test_buy.csv", 'w', newline='') as csvfile:

            fieldnames = form_data_buy.keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()

            writer.writerow(form_data_buy)
        test = pd.read_csv("Data/Purchase Data/test_buy.csv")

        if (current_area == "Hinjewadi"):
            price_buy = int((hinjewadi_purchase.predict(test))[0])

        elif (current_area == "Kharadi"):
            price_buy = int((kharadi_purchase.predict(test))[0])

        elif (current_area == "Baner"):
            price_buy = int((baner_purchase.predict(test))[0])

        elif (current_area == "Hadapsar"):
            price_buy = int((hadapsar_purchase.predict(test))[0])

        elif (current_area == "Wagholi"):
            price_buy = int((wagholi_purchase.predict(test))[0])

        elif (current_area == "Wakad"):
            price_buy = int((wakad_purchase.predict(test))[0])


        prices_buy = [

            {
                "Hinjewadi": calc_buy_val(int((hinjewadi_purchase.predict(test))[0])),
                "post_fix" : calc_post_fix(int((hinjewadi_purchase.predict(test))[0]))
             },

            {
                "Kharadi": calc_buy_val(int((kharadi_purchase.predict(test))[0])),
                "post_fix" : calc_post_fix(int((kharadi_purchase.predict(test))[0]))
             },

            {
                "Baner": calc_buy_val(int((baner_purchase.predict(test))[0])),
                "post_fix" : calc_post_fix(int((baner_purchase.predict(test))[0]))
            },

            {
                "Hadapsar": calc_buy_val(int((hadapsar_purchase.predict(test))[0])),
                "post_fix": calc_post_fix(int((hadapsar_purchase.predict(test))[0]))
            },
            {
                "Wagholi": calc_buy_val(int((wagholi_purchase.predict(test))[0])),
                "post_fix": calc_post_fix(int((wagholi_purchase.predict(test))[0]))
            },

            {
                "Wakad": calc_buy_val(int((wakad_purchase.predict(test))[0])),
                "post_fix": calc_post_fix(int((wakad_purchase.predict(test))[0]))
            }
        ]
        post_fix = "Lakhs"
        if price_buy > 100 :
            price_buy = (price_buy / 100)
            post_fix = "Crore"

        print((prices_buy[0])['Hinjewadi'])

        send_mail(form_buy['email'], f"Buy price for {current_area}",
                  message=f"Choice Summary\nNo. of Bedrooms : {form_buy['BHK']}\nArea : {form_buy['Area_sqft']}\nRent : ₹{price_buy}\n\nThank you visit us again")
        return render_template('result_buy.html', area=area, area_data=area_data, price=price_buy, num=num, form_data=form_data_buy,
                               form=form_buy, post_fix = post_fix)
    return render_template('area_buy.html', area=area, area_data=area_data, num=num)



@app.route('/about')
def about_us():
    return render_template('about.html')

@app.route('/compare')
def compare():
    return render_template('compare.html', prices=prices)

@app.route('/compare_buy')
def compare_buy():
    return render_template('compare_buy.html', prices_buy=prices_buy)

def calc_post_fix(value):
    post_fix = "Lakhs"
    if value > 100:
        price_buy = (value / 100)
        post_fix = "Crore"

    return post_fix

def calc_buy_val(model_val):
    post_fix = "Lakhs"
    if model_val > 100:
        model_val = (model_val / 100)
        post_fix = "Crore"


    return model_val


if __name__ == "__main__":
    app.run(debug=True, port=5002)
