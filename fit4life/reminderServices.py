from flask import  render_template,Blueprint,jsonify
from datetime import datetime
import requests
from fit4life.mailProgram import mailProgram
from fit4life.Utility import changeDateFormatOnly,changingTimeFormat24T12
from fit4life import dataBaseUtilizes
from fit4life.whatsappTemplate import reminder05MinMessage,reminder24HrMessage,reminder48HrMessage
import pyshorteners
from fit4life import Config

appFit4lifereminders =  Blueprint('appFit4lifereminders' , __name__)

@appFit4lifereminders.route('/reminders')
def hello_world():
    return 'Hello Reminder !!!!!!!!'


@appFit4lifereminders.route("/reminderDetailEvery-05-mins")
def reminderEvery5MinDetails():
    datailsOfActiveReminder= dataBaseUtilizes.reminders()

    if datailsOfActiveReminder == None:
        return "no active reminders"
    #return str(datails_of_active_reminder)
    for i in datailsOfActiveReminder:
        date = i['operatingdate']
        dateSplit = date.split()

        fin_time_01 = changeDateFormatOnly(dateSplit[0])
        FinalTimel = changingTimeFormat24T12(dateSplit[1])

        FillDetailsInTemplate = render_template("reminderBefore30Mins.html", Name=i['name'], ApptDate=fin_time_01, ApptTime=FinalTimel)

        message = ' !!  REMINDER 30Min BEFORE  !!'
        mailProgram(i['emailaddr'], FillDetailsInTemplate,'','','',message)

         #for  whatsup
        mobileNumber = i['mobile']
        whatsUp_data = {'apikey': Config.WhatsApp.apiKey,
            'mobile': mobileNumber,
            'msg':reminder05MinMessage.format(i['name'],fin_time_01,FinalTimel)
            }
        service = Config.WhatsApp.service
        responce = requests.post(url=service, params=whatsUp_data)

    return jsonify({"status":True})



@appFit4lifereminders.route('/dayBeforeReminder')
def day_before_remminder():
    datailsOfActiveReminder = dataBaseUtilizes.dayBeforeReminders()
    if datailsOfActiveReminder == None:
        return "no active reminders"

    for i in datailsOfActiveReminder:
        date = i['operatingdate']
        dateSplit = date.split()

        fin_time_01 = changeDateFormatOnly(dateSplit[0])
        FinalTimel = changingTimeFormat24T12(dateSplit[1])
        presenttime = datetime.utcnow()
        presenttimeforwhatsup = str(presenttime).replace(' ','%20')

        #FillDetailsInTemplate = render_template("EmailTemplate.html", Name=i['name'], ApptDate=fin_time_01, ApptTime=FinalTime)

        #"http://perennialcode.pythonanywhere.com/F4LApptcancel?rmd={{reminderid}}&date={{presenttime}}"
        url = Config.Domain.domainName
        cancelLink = f"""{url}F4LApptcancel?rmd={i["rmd"]}&date={presenttimeforwhatsup}"""
        FillDetailsInTemplate = render_template("ReminderOneDayBefore.html", Name=i['name'], ApptDate=fin_time_01, ApptTime=FinalTimel,link =cancelLink )

        #FillDetailsInTemplate = render_template("ReminderOneDayBefore.html", Name=i['name'], ApptDate=fin_time_01, ApptTime=FinalTimel,reminderid=i["rmd"],presenttime=presenttime)

        message = ' !!  REMINDER 24hr BEFORE  !!'

        mailProgram(i['emailaddr'], FillDetailsInTemplate,'','','',message)


        #tinyurl
        proposal_url = url+"F4LApptcancel?rmd={0}&date={1}".format(i["rmd"],presenttimeforwhatsup)

        def shortenurl(url):
            s = pyshorteners.Shortener()
            return s.tinyurl.short(url)

        urlt = shortenurl(proposal_url)
         #for  whatsup
        mobileNumber = i['mobile']
        whatsUp_data = {'apikey':  Config.WhatsApp.apiKey,
            'mobile': mobileNumber,
            'msg':reminder24HrMessage.format(i['name'],fin_time_01,FinalTimel,urlt)
            }
        service =  Config.WhatsApp.service
        responce = requests.post(url=service, params=whatsUp_data)

    return jsonify({"status":True})


@appFit4lifereminders.route('/twoBeforeReminder')
def twodays_before_remminder():
    datailsOfActiveReminder = dataBaseUtilizes.twoBeforeReminders()
    if datailsOfActiveReminder == None:
        return "no active reminders"
    #return str(datails_of_active_reminder)
    for i in datailsOfActiveReminder:
        date = i['operatingdate']
        dateSplit = date.split()

        fin_time_01 = changeDateFormatOnly(dateSplit[0])
        FinalTimel = changingTimeFormat24T12(dateSplit[1])
        presenttime = datetime.utcnow()
        presenttimeforwhatsup = str(presenttime).replace(' ','%20')

        #"http://perennialcode.pythonanywhere.com/F4LApptcancel?rmd={{reminderid}}&date={{presenttime}}"

        url = Config.Domain.domainName
        cancelLink = f"""{url}F4LApptcancel?rmd={i["rmd"]}&date={presenttimeforwhatsup}"""
        FillDetailsInTemplate = render_template("ReminderOneDayBefore.html", Name=i['name'], ApptDate=fin_time_01, ApptTime=FinalTimel,link =cancelLink )



        #FillDetailsInTemplate = render_template("ReminderOneDayBefore.html", Name=i['name'], ApptDate=fin_time_01, ApptTime=FinalTimel,reminderid=i["rmd"],presenttime=presenttime)

        message = ' !!  REMINDER 48Hr BEFORE  !!'

        mailProgram(i['emailaddr'], FillDetailsInTemplate,'','','',message)
        #tinyurl
        proposal_url = url+"F4LApptcancel?rmd={0}&date={1}".format(i["rmd"],presenttimeforwhatsup)

        def shortenurl(url):
            s = pyshorteners.Shortener()
            return s.tinyurl.short(url)

        urlt = shortenurl(proposal_url)
         #for  whatsup
        mobileNumber = i['mobile']
        whatsUp_data = {'apikey': Config.WhatsApp.apiKey,
            'mobile': mobileNumber,
            'msg':reminder48HrMessage.format(i['name'],fin_time_01,FinalTimel,urlt)
            }
        service = Config.WhatsApp.service
        responce = requests.post(url=service, params=whatsUp_data)

    return jsonify({"status":True})







