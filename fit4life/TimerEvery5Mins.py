import requests

responce_30  = requests.get('https://perennialcode.pythonanywhere.com/reminderDetailEvery-05-mins')
responce_day= requests.get('https://perennialcode.pythonanywhere.com/dayBeforeReminder')
twoBeforeReminder = requests.get('https://perennialcode.pythonanywhere.com/twoBeforeReminder')
