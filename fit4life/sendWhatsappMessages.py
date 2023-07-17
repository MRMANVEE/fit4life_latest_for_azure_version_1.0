#import sys
#sys.path.append('/home/perennialcode/mysite/')
from fit4life.whatsappTemplate import sendBookingProposalDetails,ProposalAccept
import pyshorteners
import requests
from fit4life import Config

#from configparser import ConfigParser
#config_details = ConfigParser()
#config_details.read('/home/perennialcode/mysite/fit4life/WhatsAppConfig.ini')

def shortenurl(url):
    s = pyshorteners.Shortener()
    return s.tinyurl.short(url)

def sendBookingDetailswhatsapp(Mobile,custmerName,staffname,proposal_url):
    whatsUp_data = {'apikey': Config.WhatsApp.apiKey,'mobile': Mobile,'msg': sendBookingProposalDetails.format(custmerName,staffname,shortenurl(proposal_url)),'img1':Config.WhatsApp.imageLogo}
    return requests.post(url=Config.WhatsApp.service, params=whatsUp_data)

def apptComformation(mobile,name,final_date,finallTime,cancelLink):
    whatsUp_data = {'apikey': Config.WhatsApp.apiKey,'mobile': mobile,'msg':  ProposalAccept.format(name,final_date,finallTime,cancelLink)}
    return requests.post(url=Config.WhatsApp.service, params=whatsUp_data)
