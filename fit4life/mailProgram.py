from flask_mail import Mail, Message
from flask import   current_app
#from configparser import ConfigParser
from fit4life.Utility import change_date_format_ical
from fit4life import Config

def mailProgram(userMailId, data ,attachICalender = '0',startDateTime = '0',EndDateTime = '0',message= 'Hello'):

    #config_details = ConfigParser()
    #config_details.read('/home/perennialcode/mysite/fit4life/Mailconfig.ini')
    #sendeMail = config_details['sender_details']['sender_mail']
    sendeMail = Config.mail.sender_mail


    current_app.config['MAIL_SERVER'] = Config.mail.server  #'mail.fit4lifeindia.in'
    current_app.config['MAIL_PORT'] = Config.mail.port
    current_app.config['MAIL_USERNAME'] = sendeMail
    current_app.config['MAIL_PASSWORD'] = Config.mail.sender_pasword
    current_app.config['MAIL_USE_TLS'] = False
    current_app.config['MAIL_USE_SSL'] = True
    mail = Mail(current_app)

    msg = Message(
        message,
        sender= sendeMail,

        recipients=[userMailId, ],cc=[sendeMail ]
    )

    if attachICalender == 'y':


        with open(f'{Config.fit4lifeFolderLocation.address}icalenderFileData.ics') as icalData:
            replaceApptDates = icalData.read()

            replaceApptDates = replaceApptDates.replace('ApptStartTime', change_date_format_ical(startDateTime))
            replaceApptDates = replaceApptDates.replace('ApptEndTime', change_date_format_ical(EndDateTime))

            msg.attach("fit4lifeical.ics", 'text/icas',replaceApptDates )

    msg.html = data
    mail.send(msg)

    #config remove later
    with open('maillog.txt', 'a') as log:
       log.write(str(userMailId) + message + '\n')

    return 'mail_Sent True'
