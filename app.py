#import sys
#sys.path.append('/home/perennialcode/mysite/')

from flask import Flask,request
import requests

from flask_mail import Mail, Message
#from BookMyOT.Services import profile,Miscellaneous,Appointment,OTProcess,PaymentTransactions,Preferences,Schedule,PhysicianAvailability,more


app = Flask(__name__, template_folder='fit4life/templates/')

@app.route('/sendWhatsAppMessage')
def hello_world():
   number = request.args.get('number')
   message = request.args.get('message')
   whatsUp_data = {'apikey': '61e8d10a3a0948638364c96736d9994d', 'mobile': number,
                   'msg': message
                  }
   res = requests.post(url='http://bulkwhatsapp.live/wapp/api/send', params=whatsUp_data)
   return res.text



from fit4life import ServicesFit4life,reminderServices,ApptCancelServices
app.register_blueprint(ServicesFit4life.appFit4life)
app.register_blueprint(reminderServices.appFit4lifereminders)
app.register_blueprint(ApptCancelServices.appFit4Apptcancel)


if __name__ == "__main__":
    app.run()
