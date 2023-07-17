from flask import request,Blueprint,render_template,jsonify
from datetime import datetime
import requests
from fit4life.mailProgram import mailProgram
from fit4life.Utility import changingTimeFormat24T12,changeDateFormatOnly
from fit4life import dataBaseUtilizes
from fit4life.whatsappTemplate import ApptCancelmessage,apptCancelByStaffMessage
from fit4life import Config

appFit4Apptcancel =  Blueprint('appFit4Apptcancel' , __name__)



@appFit4Apptcancel.route('/apptCancelByStaff')
def apptCancelByStaff():
  try:
    apptid = request.args.get('apptid')
    result = dataBaseUtilizes.cancelApptByStaff(apptid)
    #return str(result)

    fin_time_01 = changeDateFormatOnly(str(result['apppointmentdt']).split(' ')[0])
    FinalTimel = changingTimeFormat24T12(str(result['starttime'].split('.')[0]))
    #61e8d10a3a0948638364c96736d9994d
    mobileNumber = result['cusmobile']
    whatsUp_data = {'apikey': Config.WhatsApp.apiKey,
                            'mobile': mobileNumber,
                            'msg':apptCancelByStaffMessage.format(result['cusname'],fin_time_01,FinalTimel)
                            }
    service = Config.WhatsApp.service
    responce = requests.post(url=service, params=whatsUp_data)

    message = ' !!Appt cancelled!!'
    #customerMail
    cancelTemplate = render_template("apptCancelStaffForClient.html",Name = result['cusname'] , date = fin_time_01 , time = FinalTimel,imglogo1=Config.fit4lifeLogo.image1)
    mailProgram(result['cusemail'], cancelTemplate,'','','',message)
    #staffMail
    cancelTemplateforStaff = render_template("apptcancelledINApplicationMailForStaff.html",Customer = result['cusname'] , d1 = fin_time_01 , sl1sT = FinalTimel,Name =result['staffname'],imglogo1=Config.fit4lifeLogo.image1)
    mailProgram(result['staffemail'], cancelTemplateforStaff,'','','',message)


    return jsonify({"status":True})
  except Exception as e:
        #return {'Status' :False,'Message' :str(e),'ResultData':[]}
        return render_template("somethingwentwrong.html",f4lLogo2 = Config.fit4lifeLogo.image2)




@appFit4Apptcancel.route('/F4LApptcancel')
def Fit4LApptcancel():
  try:
    id = request.args.get('rmd')
    present_time_to_send_template = request.args.get('date')

    templatTime = datetime.strptime(present_time_to_send_template, '%Y-%m-%d %H:%M:%S.%f')
    diff = datetime.utcnow()-templatTime
    days, seconds = diff.days, diff.seconds
    hours = days * 24 + seconds // 3600

    if Config.ApptReminderCancelationLinkExpireTime.hours > hours:
        result = dataBaseUtilizes.cancelappt(id)
       # return result
        if result == False:
            return render_template("YouDontAppt.html",f4lLogo2 = Config.fit4lifeLogo.image2)

        fin_time_01 = changeDateFormatOnly(result['apptDate'])
        FinalTimel = changingTimeFormat24T12(result['starttime'])

        # for  whatsup
        mobileNumber = result['cusmobile']
        whatsUp_data = {'apikey': Config.WhatsApp.apiKey,
                            'mobile': mobileNumber,
                            'msg':ApptCancelmessage.format(result['cusname'],fin_time_01,FinalTimel)
                            }
        service = Config.WhatsApp.service
        responce = requests.post(url=service, params=whatsUp_data)
        message = ' !!Appt cancelled!!'

        cancelTemplate = render_template("appt Cancel.html",Name = result['cusname'] , ApptDate = fin_time_01 , ApptTime = FinalTimel,f4lLogo1 = Config.fit4lifeLogo.image1)
        mailProgram(result['cusEmail'], cancelTemplate,'','','',message)
        stafftemplate = render_template("apptcancelledtemplateStaff.html",Name = result['staffName'] , ApptDate = fin_time_01 , ApptTime = FinalTimel,customername=result['cusname'],f4lLogo1 = Config.fit4lifeLogo.image1)
        mailProgram(result['staffmail'], stafftemplate,'','','',message)

        return cancelTemplate
    return render_template("Link Expired.html",f4lLogo2 = Config.fit4lifeLogo.image2)
  except Exception as e:
        #return {'Status' :False,'Message' :str(e),'ResultData':[]}
        return render_template("somethingwentwrong.html",f4lLogo2 = Config.fit4lifeLogo.image2)


