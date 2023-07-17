from flask import  render_template , request,Blueprint
from fit4life.mailProgram import mailProgram
from fit4life.Utility import changingTimeFormat24T12,changeTimeFormat,changeDateFormatOnly
from fit4life import dataBaseUtilizes
#from fit4life.whatsappTemplate import sendBookingProposalDetails,ProposalAccept
from datetime import datetime,timezone,timedelta
from fit4life.sendWhatsappMessages import sendBookingDetailswhatsapp,apptComformation
#from configparser import ConfigParser
import pyshorteners
from fit4life import Config


appFit4life =  Blueprint('appFit4life' , __name__)

@appFit4life.route('/')
def hello_world():
    return 'Hello from PERENNIAL CODE !!!!!!!!'


@appFit4life.route('/sendBookingDetails/<int:bookingId>')
def BookingProposalId(bookingId):
    #it takes bookingId and returns bookingAppt details
    bookingDetails = dataBaseUtilizes.bookingApptDates(bookingId)

    present_time_to_send_template = (datetime.now(timezone.utc) + timedelta(hours = 5,minutes=30)).strftime("%Y-%m-%d %H:%M:%S")
    date= present_time_to_send_template.replace(' ','%20')

    #config_details = ConfigParser()
    #config_details.read('/home/perennialcode/mysite/rootDomain.ini')
    #url = config_details['domain']['domainName']

    url = Config.Domain.domainName
    data = render_template('UserConfirmPro2.html', PROPOSAL2=changeTimeFormat(str(bookingDetails['Sl1StartTime'])),
                           APPTHSTID=bookingId, APPURL=url, NAME=bookingDetails['custmerName'], DRNAME=bookingDetails['staffname'],
                           activatedTime= str(present_time_to_send_template),imglogo1=Config.fit4lifeLogo.image1)

    proposal_url = url+"Fit4LifeAppointment/{0}/{1}".format(str(date),str(bookingId))
    sendBookingDetailswhatsapp(bookingDetails['Mobile'],bookingDetails['custmerName'],bookingDetails['staffname'],proposal_url)

    return mailProgram(bookingDetails['customerMAIL'],data,'','','','Appointment slot for review call with Deepika Chalasani')


#for whatsup
@appFit4life.route('/Fit4LifeAppointment/<templateTime>/<bookingId>')
def whatsUp(templateTime,bookingId):
    try:

        bookingDetails = dataBaseUtilizes.bookingApptDates(bookingId)
        #config_details = ConfigParser()
        #config_details.read('/home/perennialcode/mysite/rootDomain.ini')

        #url = config_details['domain']['domainName']
        url = Config.Domain.domainName
        #url = 'http://perennialcode.pythonanywhere.com/'
        data = render_template('UserConfirmPro1.html', PROPOSAL2=changeTimeFormat(str(bookingDetails['Sl1StartTime'])),
                          APPTHSTID=bookingId, APPURL=url, NAME=bookingDetails['custmerName'], DRNAME=bookingDetails['staffname'],activatedTime= templateTime,f4lLogo2=Config.fit4lifeLogo.image2)

        return data
    except Exception:
        return render_template("somethingwentwrong.html",f4lLogo2=Config.fit4lifeLogo.image2)


@appFit4life.route('/UserOption.aspx')
def selecting():
  try:
    proposalS = request.args.get('pr')
    apptiId = request.args.get('apid')

    template_time = request.args.get('activateTime')
    templateTimeConvertDatetime = datetime.strptime(template_time, '%Y-%m-%d %H:%M:%S')

    currentTime =  (datetime.now(timezone.utc) + timedelta(hours = 5,minutes=30)).strftime("%Y-%m-%d %H:%M:%S")
    currentTime_To_datetime_convert = datetime.strptime(currentTime, '%Y-%m-%d %H:%M:%S')

    timeDiff = (currentTime_To_datetime_convert-templateTimeConvertDatetime).total_seconds()
    timeDiff_hours =  timeDiff // (60 * 60)

    if timeDiff_hours > Config.ApptProposalDatesExpireHours.hours:
        return render_template("proDatesExpired.html",f4lLogo2=Config.fit4lifeLogo.image2)
        #return 'proposals invalid after 24 hours'
    #it require bookingApptId and return True or False
    checkingBokApptStatus = dataBaseUtilizes.checkBokApptActiveOrNot(apptiId)
    if checkingBokApptStatus[0] == True :

        date_startTime_endTime = dataBaseUtilizes.bookingapptSl1Sl2Proposals(apptiId,proposalS)
        check_dates = dataBaseUtilizes.compare_appt_date_time(date_startTime_endTime)

        if check_dates is not None :
            #config_details = ConfigParser()
            #config_details.read('/home/perennialcode/mysite/rootDomain.ini')

            #url = config_details['domain']['domainName']
            url = Config.Domain.domainName
            #url = 'http://perennialcode.pythonanywhere.com'
            return render_template("reschedule appointment.html",urls = url,id=apptiId,f4lLogo2=Config.fit4lifeLogo.image2 )

        """select cus.Name customername,staff.Name staffname,Staff.Emailid staffEmail from BookingAppt bokappt
inner join Customers cus on cus.id = bokappt.Customerid
inner join staff on staff.id = bokappt.staffid"""



        dataBaseUtilizes.updateStatusToinactive(apptiId)



        apptid = dataBaseUtilizes.insertIntoAppt(apptiId, proposalS)
        rmdid = dataBaseUtilizes.insertionDetailsReminder(apptiId, proposalS,apptid)
        detailsForConfirmationMail = dataBaseUtilizes.apptConfirmationMailDetails(apptiId, proposalS)

        if int(proposalS) == 1:
            date = detailsForConfirmationMail['Sl1StartTime']
            endtime = detailsForConfirmationMail['Sl1EndTime']
        elif int(proposalS) == 2:
            date = detailsForConfirmationMail['Sl2StartTime']
            endtime = detailsForConfirmationMail['Sl2EndTime']
        sp_date_time = str(date).split()
        #finalldate = sp_date_time[0]
        #finallTime = sp_date_time[1]


        attachICalender = 'y'
        final_date = changeDateFormatOnly(sp_date_time[0])

        finallTime = changingTimeFormat24T12(sp_date_time[1])

        confirmationSemplateForStaff = render_template('DrTemplate.html', Name=detailsForConfirmationMail['Name'],name = detailsForConfirmationMail['name'],
                                                      ApptDate=final_date, ApptTime=finallTime,f4lLogo1=Config.fit4lifeLogo.image1)

        mailProgram(detailsForConfirmationMail['staffEmail'], confirmationSemplateForStaff,'','','','Customer Accepted Dates')

        presenttime = datetime.utcnow()
        presenttimeforwhatsup = str(presenttime).replace(' ','%20')

        url = Config.Domain.domainName
        cancelLink = f"""{url}F4LApptcancel?rmd={rmdid}&date={presenttimeforwhatsup}"""

        confirmationTemplateCustomer = render_template('EmailTemplate.html', Name=detailsForConfirmationMail['name'],
                                                    ApptDate=final_date, ApptTime=finallTime,cancellink = cancelLink,f4lLogo1=Config.fit4lifeLogo.image1)

        mailProgram(detailsForConfirmationMail['customerEmail'], confirmationTemplateCustomer,attachICalender,date ,endtime,'Appt confirmation')

        def shortenurl(url):
            s = pyshorteners.Shortener()
            return s.tinyurl.short(url)

        urlt = shortenurl(cancelLink)

        apptComformation(detailsForConfirmationMail['mobile'],detailsForConfirmationMail['name'],final_date,finallTime,urlt)

        page = render_template('apptPage.html', Name=detailsForConfirmationMail['name'],
                                                    ApptDate=final_date, ApptTime=finallTime,f4lLogo2=Config.fit4lifeLogo.image2)


        return page
    return render_template("apptAlreadyConfirmed.html",f4lLogo2=Config.fit4lifeLogo.image2)
  except Exception :
      return render_template("somethingwentwrong.html",f4lLogo2=Config.fit4lifeLogo.image2)


@appFit4life.route('/rescheduleAppointment')
def rescheduleAppointment():
  try:
    bokapptid = request.args.get('bokaappt')
    checkingBokApptStatus = dataBaseUtilizes.checkBokApptActiveOrNot(bokapptid)
    if checkingBokApptStatus[0] == True :

        staffdetails = dataBaseUtilizes.dbrescheduleAppointment(bokapptid)

        templateforstaff = render_template("staffreschdMail.html",Name=staffdetails['staffname'],d1=staffdetails['sl1appointmentdt']
        ,sl1sT = staffdetails['sl1starttime'],sl1et=staffdetails['sl1endtime']
        ,Customer= staffdetails['customername'],f4lLogo1=Config.fit4lifeLogo.image1)

        mailProgram(staffdetails['staffemail'],templateforstaff,'','','','rescheduleproposalforcustomer')
        dataBaseUtilizes.updateStatusToinactive(bokapptid)
        return render_template("sendAnotherDatesMessage.html",f4lLogo1=Config.fit4lifeLogo.image1)

    return render_template("yourRequestReceived.html",f4lLogo2=Config.fit4lifeLogo.image2)
  except Exception as e:
        return render_template("somethingwentwrong.html",f4lLogo2=Config.fit4lifeLogo.image2)

