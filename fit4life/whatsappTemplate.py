sendBookingProposalDetails = """Hi {0},

Trust you’re doing well. Your Nutritionist “{1}” has proposed an appointment slot for your review call with Ms. Deepika Chalasani.

Please click the below  link to select your appointment - {2}

Please do reach out to us if you have any questions.

Thanks & Regards,

Fit4life India Team.
"""


#---------------------------------------------------------------------------------------------------------------------------------

ProposalAccept =  """Hi {0},

Thank you for confirming your appointment.

Your review call with Ms. Deepika Chalasani
is scheduled on {1} at {2}.

The Zoom link for your review call will be
shared in your WhatsApp group, kindly join the call on time.

If you are not available for the review call as selected by you,
you can cancel the appointment by clicking on the below mentioned link – {3}

Please contact your Nutritionist to reschedule your appointment as per availability of slots.


Thanks & Regards,

Fit4life India Team.
"""



#---------------------------------------------------------------------------------------------------------------------------------
ApptCancelmessage = """Hi {0},

Thanks for informing us about your appointment cancellation. We’ve noted the same.

Please contact your Nutritionist to reschedule your appointment depending on the available slots.

Thanks & Regards,

Fit4life India Team.
"""

#-----------------------------------------------------------------------------------------------------------------------------------
reminder05MinMessage = """Hi {0},

This message is to remind you that your appointment for a review call with Ms. Deepika Chalasani is on {1} at {2}. You will get the zoom link in your WhatsApp group, kindly join on time.

If you are not available at the scheduled time, please contact your Nutritionist to reschedule your appointment.

Thanks & Regards,

Fit4life India Team.
"""

#-----------------------------------------------------------------------------------------------------------------------------------
reminder24HrMessage = """Hi {0},

This message is to remind you that your appointment for a review call with Ms. Deepika Chalasani is on {1} at {2}. You will get the zoom link in your WhatsApp group, kindly join on time.

If you are not available for the review call as selected by you,
you can cancel the appointment by clicking on the below mentioned link – {3}

Please contact your Nutritionist to reschedule your appointment as per availability of slots.

Thanks & Regards,

Fit4life India Team."""

#-----------------------------------------------------------------------------------------------------------------------------------
reminder48HrMessage = """Hi {0},

This message is to remind you that your appointment for a review call with Ms. Deepika Chalasani is on {1} at {2}. You will get the zoom link in your WhatsApp group, kindly join on time.

If you are not available for the review call as selected by you,
you can cancel the appointment by clicking on the below mentioned link – {3}

Please contact your Nutritionist to reschedule your appointment as per availability of slots.

Thanks & Regards,

Fit4life India Team.
"""

#------------------------------

apptCancelByStaffMessage = """Hi {0},

This is to confirm that your appointment on {1} at {2} is cancelled by your Nutritionist on your behalf as requested by you.

Thanks & Regards,

Fit4life India Team"""






#-----------------------------------------------------------------------------------------------------------------------------------
l06 = """Hi {i['name']},
Thank You For Contacting Us.

!!!!!!!!⚕️ REMINDER 48 hours Before !!!!!!
-----------------------------
This is a reminder that your appointment is confirmed for:
{fin_time_01} at {FinalTimel} .
--------------------------------------
Request you to be there for the appointment as scheduled. You will receive a zoom link via your WhatsApp group.
--------------------------------------
if you are not availble at schedule time you can cancel appt using this link : http://perennialcode.pythonanywhere.com/F4LApptcancel?rmd={i["rmd"]}&date={presenttimeforwhatsup}

Thanks & Regards,

Fit4life India Team"""

l05 = """Hi {i['name']},
Thank You For Contacting Us.

!!!!!!!!⚕️ REMINDER 24 hours Before !!!!!!
-----------------------------
This is a reminder that your appointment is confirmed for:
{fin_time_01} at {FinalTimel} .
--------------------------------------
Request you to be there for the appointment as scheduled. You will receive a zoom link via your WhatsApp group.
--------------------------------------
if you are not availble at schedule time you can cancel appt using this link : http://perennialcode.pythonanywhere.com/F4LApptcancel?rmd={i["rmd"]}&date={presenttimeforwhatsup}

Thanks & Regards,

Fit4life India Team"""

l04 = """Hi {i['name']},
Thank You For Contacting Us.

!!!!!!!!⚕️ REMINDER 30 mins Before !!!!!!
-----------------------------
This is a reminder that your appointment is confirmed for:
{fin_time_01} at {FinalTimel} .
--------------------------------------
Request you to be there for the appointment as scheduled. You will receive a zoom link via your WhatsApp group.

Thanks & Regards,

Fit4life India Team"""



l03 ="""Hi {result['cusname']},


!!!!!!!!⚕️ Appt cancelled !!!!!!
-----------------------------
your appointment is cancelled :
{fin_time_01} at {FinalTimel} .
--------------------------------------
Thanks & Regards,

Fit4life India Team"""

l02 =  """Hi {detailsForConfirmationMail['name']},

-----------------------------
This is to confirm that your appointment is scheduled on
{final_date} at {finallTime}
--------------------------------------
We look forward to connecting with you.

Thanks & Regards,
Fit4life India Team"""




l01 = """Hello {customerName},

{doctorName} proposed appointment dates for you to Opt.

Please Select One of the dates using below Link.

https://perennialcode.pythonanywhere.com/whats_up_message/template/{str(date)}/data/{str(bookingId)}

Feel free to reach out to us with any questions.



Thanks.
Fit4Life """