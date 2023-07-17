
import os
from datetime import datetime
from zoneinfo import ZoneInfo


import pyodbc
server = 'sql5050.site4now.net'
database_name = 'DB_A50D85_fit4life'
user_name = 'DB_A50D85_fit4life_admin'
password = 'p3r3nni@l'
forDbConnection = ('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database_name+';UID='+user_name+';PWD='+password)

def bookingApp():
    """ it takes requires bookingid,
        retuns appointment details"""

    quary = "select *  from reminders where  operatingdate = '2023-03-20 17:00:00' "
    quary = 'select *  from Appointments '
    db_connection = pyodbc.connect(forDbConnection)
    quary_execution = db_connection.execute(quary)
    total_data = quary_execution.fetchall()


    if len(total_data) == 0:
        return None
    total_data_to_list = []
    for j in range(len(total_data)):
        count = 0
        dict_data = {}

        for i in quary_execution.description:
            dict_data[str(i[0]).lower()] = total_data[j][count]
            count += 1

        total_data_to_list.append(dict_data)
    quary_execution.close()
    #total_data_to_list[0]["apppointmentdt"] = str(total_data_to_list[0]["apppointmentdt"])
    #total_data_to_list[0]["starttime"] = str(total_data_to_list[0]["starttime"])
    return total_data_to_list
#print(bookingApp())
#print(bookingApp())







"""
def compare_appt_date_time(date_startTime_endTime):
    quary = "SELECT * FROM appointments where apppointmentDt = '"+str(date_startTime_endTime[0])+"' and StartTime >= '"+str(date_startTime_endTime[1])+"'  and Endtime <= '"+str(date_startTime_endTime[2])+"' for json auto"
    #return quary
    quary_exe = db_connection.execute(quary)
    data = quary_exe.fetchone()
    return data

"""

def bookingApptDates(bookongid):
    """ it takes requires bookingid,
        retuns appointment details"""

    quary = 'select BookingAppt.* ,Customers.EmailAddr  customerMAIL, Customers.Name custmerName,Customers.Mobile,Staff.name staffname , Staff.EmailId staffMAILID from bookingappt  inner join Customers on Customers.Id = BookingAppt.CustomerId inner join Staff on Staff.Id = BookingAppt.StaffId where BookingAppt.id = '+str(bookongid)

    db_connection = pyodbc.connect(forDbConnection)
    data = db_connection.execute(quary)
    all_data = data.fetchall()
    e = {}
    lopp_details_count = 0
    for i in data.description:
        e[str(i[0])] = all_data[0][lopp_details_count]
        lopp_details_count += 1
    data.close()
    return e

#print(bookingApptDates(12))

def checkBokApptActiveOrNot(apptid):
    quary  = f"""select BookingAppt.isActive,Customers.name customername from BookingAppt
                inner join Customers on Customers.id = BookingAppt.customerid
                where BookingAppt.id = {apptid}"""

    """quary = select bok.isActive,appt.CustomerName from BookingAppt bok
                inner join Appointments appt on appt.customerid = bok.Customerid
                where bok.id = {apptid}"""
    db_connection = pyodbc.connect(forDbConnection)
    executionResult = db_connection.execute(quary)
    result = executionResult.fetchone()
    db_connection.close()
    return result
#print(checkBokApptActiveOrNot(321))

#print(checkBokApptActiveOrNot(12))
def updateStatusToinactive(apptid):
    quary = "update BookingAppt set isActive= 'False' where id = "+str(apptid)
    db_connection = pyodbc.connect(forDbConnection)
    db_connection.execute(quary)
    db_connection.commit()
    #db_connection.close()
    db_connection.close()
    return "updated"


def compare_appt_date_time(date_startTime_endTime):
    #quary = "SELECT * FROM appointments where apppointmentDt = '"+str(date_startTime_endTime[0])+"' and StartTime >= '"+str(date_startTime_endTime[1])+"'  and Endtime <= '"+str(date_startTime_endTime[2])+"' for json auto"
    #staff id
    quary = f"""SELECT * FROM appointments where isActive = 1 and staffid = {date_startTime_endTime[3]} and apppointmentDt = '{date_startTime_endTime[0]}' and
                ((StartTime between '{date_startTime_endTime[1]}' and '{date_startTime_endTime[2]}') or
                (Endtime between '{date_startTime_endTime[1]}' and '{date_startTime_endTime[2]}'))"""
    db_connection = pyodbc.connect(forDbConnection)
    quary_exe = db_connection.execute(quary)
    data = quary_exe.fetchone()
    db_connection.close()
    return data

#print(compare_appt_date_time(['2023-01-14', '15:20:00', '15:31:00',1]))
#['2023-01-14', '14:20:00', '15:21:00']
def bookingapptSl1Sl2Proposals(id,pro):
    quary = 'select Sl1StartTime,Sl1EndTime,Sl2StartTime,Sl2EndTime,staffid from BookingAppt where id ='+str(id) +'for json auto'
    db_connection = pyodbc.connect(forDbConnection)
    data = db_connection.execute(quary)
    all_data = data.fetchone()
    d =  eval(all_data[0])[0]
    staffid = d['staffid']

    if int(pro) == 1:
        #data = [d['Sl1StartTime'],d['Sl1EndTime']]
        startTime = d['Sl1StartTime'].split('T')
        EndTime = d['Sl1EndTime'].split('T')
        date_startTime_endTime = [startTime[0],startTime[1],EndTime[1],staffid]


    elif int(pro) == 2:
        #data = [d['Sl2StartTime'],d['Sl2EndTime']]
        startTime = d['Sl2StartTime'].split('T')
        EndTime = d['Sl2EndTime'].split('T')
        date_startTime_endTime = [startTime[0],startTime[1],EndTime[1],staffid]
    db_connection.close()
    return date_startTime_endTime

#print(bookingapptSl1Sl2Proposals(12,1))


def insertionDetailsReminder(bookingid,proposals,apptid):

    quary = "select Customers.OrgId,BookingAppt.CustomerId,BookingAppt.Sl1StartTime,BookingAppt.Sl1EndTime,BookingAppt.IsActive,BookingAppt.CreatedBy, GETDATE() dates,BookingAppt.Sl2StartTime,BookingAppt.Sl1EndTime from BookingAppt inner join Customers on Customers.id = BookingAppt.CustomerId where BookingAppt.id = "+str(bookingid)
    db_connection = pyodbc.connect(forDbConnection)
    remindersInsertDataExecution = db_connection.execute(quary)
    DataForReminders = remindersInsertDataExecution.fetchall()
    dictnary = {}
    count =0

    for tableHeaders in remindersInsertDataExecution.description:
        dictnary[str(tableHeaders[0])] = DataForReminders[0][count]
        count += 1

    Createdon = datetime.now(tz=ZoneInfo('Asia/Kolkata'))
    if int(proposals) == 1:
        AppointmentDt =  dictnary['Sl1StartTime']



    elif int(proposals) == 2:
        AppointmentDt = dictnary['Sl2StartTime']


    quary = "insert into reminders (OrgId,CustomerId,OperatingDate,IsActive,Createdby,Createdon,apptid) OUTPUT INSERTED.ID values(?,?,?,?,?,?,?)"
    values = (dictnary['OrgId'], dictnary['CustomerId'], AppointmentDt,'True', dictnary['CreatedBy'],Createdon,apptid)
    result = db_connection.execute(quary, values)
    id = list(result)
    db_connection.commit()
    db_connection.close()
    return id[0][0]






def insertIntoAppt(apptiId, proposalS):
    quary = 'select cust.OrgId,bok.CustomerId,cust.name ,bok.staffid ,bok.sl1AppointmentDt,bok.Sl1StartTime,bok.Sl1EndTime,BOK.Sl2AppointmentDt,bok.Sl2StartTime , bok.Sl2EndTime,bok.Status,cust.Address,cust.mobile,bok.createdby from BookingAppt bok inner join Customers cust on cust.id = bok.CustomerId  where bok.id ='+str(apptiId)
    db_connection = pyodbc.connect(forDbConnection)
    quaryExecution =db_connection.execute(quary)
    quaryDate = quaryExecution.fetchall()
    dictnary = {}
    count = 0
    for tableHeader in quaryExecution.description:
        dictnary[str(tableHeader[0])] = quaryDate[0][count]
        count +=1

    #return dictnary
    if int(proposalS) == 1:
        AppointmentDt =  dictnary['sl1AppointmentDt']
        StartTime =  dictnary['Sl1StartTime']
        EndTime = dictnary['Sl1EndTime']
    elif int(proposalS) == 2:
        AppointmentDt = dictnary['Sl2AppointmentDt']
        StartTime =  dictnary['Sl2StartTime']
        EndTime = dictnary['Sl2EndTime']
    Createdon = datetime.now(tz=ZoneInfo('Asia/Kolkata'))

    quary = 'insert into Appointments (OrgId,customerId,CustomerName,StaffId,ApppointmentDt,StartTime,Endtime,Location,Mobile,IsActive,CreatedBy,Createdon,Status) OUTPUT Inserted.ID values(?,?,?,?,?,?,?,?,?,?,?,?,?)'
    values = (dictnary['OrgId'], dictnary['CustomerId'], dictnary['name'], dictnary['staffid'], AppointmentDt, StartTime, EndTime, dictnary['Address'], dictnary['mobile'], 1, dictnary['createdby'], Createdon,1)
    data = db_connection.execute(quary, values)
    Id = data.fetchone()
    db_connection.commit()
    db_connection.close()
    return Id[0]



def apptConfirmationMailDetails(booking_id,pro):

    quary = 'select BookingAppt.Sl1StartTime,BookingAppt.Sl1EndTime,BookingAppt.Sl2StartTime,BookingAppt.Sl2EndTime,Customers.EmailAddr customerEmail,Customers.Mobile mobile, Staff.EmailId staffEmail ,Customers.name,staff.Name from BookingAppt  inner join staff on Staff.Id = BookingAppt.StaffId inner join Customers on Customers.id = BookingAppt.CustomerId where BookingAppt.id = '+str(booking_id)
    db_connection = pyodbc.connect(forDbConnection)
    quaryExecution = db_connection.execute(quary)
    quaryData = quaryExecution.fetchall()
    dicnary={}
    count = 0
    for tableHeaders in quaryExecution.description:
        dicnary[str(tableHeaders[0])] = quaryData[0][count]
        count += 1
    db_connection.close()
    return dicnary

#print(apptConfirmationMailDetails(12,1))





def reminders():
    quary = """
        select cus.Name,rem.OperatingDate ,cus.EmailAddr,cus.Mobile from Customers cus
        inner join reminders rem on rem.Customerid = cus.id
        where rem.IsActive = 'True' and rem.OperatingDate between  GETuTCDATE()+'6:20:00' and  GETuTCDATE()+'6:50:00' """
    db_connection = pyodbc.connect(forDbConnection)
    quary_execution = db_connection.execute(quary)
    total_data = quary_execution.fetchall()
    if len(total_data) == 0:
        return None
    total_data_to_list = []
    for j in range(len(total_data)):
        count = 0
        dict_data = {}

        for i in quary_execution.description:
            dict_data[str(i[0]).lower()] = total_data[j][count]
            count += 1
        dict_data['operatingdate'] = str(dict_data['operatingdate'])
        total_data_to_list.append(dict_data)
    db_connection.close()

    return total_data_to_list


def dayBeforeReminders():

    quary = """
        select cus.Name,rem.OperatingDate ,cus.EmailAddr,cus.Mobile,rem.id rmd from Customers cus
        inner join reminders rem on rem.Customerid = cus.id
        where rem.IsActive = 'True' and rem.OperatingDate between  GETuTCDATE()+1+'5:30:00' and  (GETuTCDATE()+1+'6:00:00')"""
    db_connection = pyodbc.connect(forDbConnection)
    quary_execution = db_connection.execute(quary)
    total_data = quary_execution.fetchall()
    if len(total_data) == 0:
        return None
    total_data_to_list = []
    for j in range(len(total_data)):
        count = 0
        dict_data = {}

        for i in quary_execution.description:
            dict_data[str(i[0]).lower()] = total_data[j][count]
            count += 1
        dict_data['operatingdate'] = str(dict_data['operatingdate'])
        total_data_to_list.append(dict_data)
    db_connection.close()
    return total_data_to_list

#print(dayBeforeReminders())

def twoBeforeReminders():

    quary = """
        select cus.Name,rem.OperatingDate ,cus.EmailAddr,cus.Mobile,rem.id rmd from Customers cus
        inner join reminders rem on rem.Customerid = cus.id
        where rem.IsActive = 'True' and rem.OperatingDate between  GETuTCDATE()+2+'5:30:00' and  (GETuTCDATE()+2+'6:00:00')"""
    db_connection = pyodbc.connect(forDbConnection)
    quary_execution = db_connection.execute(quary)
    total_data = quary_execution.fetchall()
    if len(total_data) == 0:
        return None
    total_data_to_list = []
    for j in range(len(total_data)):
        count = 0
        dict_data = {}

        for i in quary_execution.description:
            dict_data[str(i[0]).lower()] = total_data[j][count]
            count += 1
        dict_data['operatingdate'] = str(dict_data['operatingdate'])
        total_data_to_list.append(dict_data)
    db_connection.close()
    return total_data_to_list

def cancelApptByStaff(id):
    quary = f"""select staff.Emailid staffemail,staff.Name staffname,cus.name cusname,cus.mobile cusmobile,cus.emailaddr cusemail,
    appt.apppointmentdt,appt.starttime from Appointments appt
                inner join Staff on staff.id = appt.Staffid
                inner join customers cus on cus.id = appt.Customerid
                where  appt.id = {id} """
    db_connection = pyodbc.connect(forDbConnection)
    quary_execution = db_connection.execute(quary)
    total_data = quary_execution.fetchall()
    for j in range(len(total_data)):
        count = 0
        dict_data = {}

        for i in quary_execution.description:
            dict_data[str(i[0]).lower()] = total_data[j][count]
            count += 1

    """date = str(dict_data['apppointmentdt']).split(' ')[0]
    time = str(dict_data['starttime']).split('.')[0]
    appttime = date+' '+time"""
    updatequary = f"""update Appointments set Status = 4 , isActive = '0' where id = {id};
                        update Reminders set IsActive = 0 where apptid = {id} """
    db_connection.execute(updatequary)
    db_connection.commit()
    db_connection.close()
    return dict_data
#print(cancelApptByStaff(281))










def cancelappt(id):
    quary = f"""select rem.Customerid,rem.OperatingDate,rem.isActive,cus.Name,cus.Mobile,cus.EmailAddr,rem.apptid from reminders rem
                inner join customers cus on cus.id = rem.Customerid
                where rem.id = {id} """
    db_connection = pyodbc.connect(forDbConnection)
    quary_exe = db_connection.execute(quary)
    data = list(quary_exe)[0]

    #return data
    if data == []:
        return 'entered wrong reminder id'
    #data = data[0]
    if data[2] == False:
        return False
    Date = (str(data[1])).split(' ')
    apptDate,starttime = Date[0],Date[1]

    #quary = f"""select appt.id ,staff.Emailid,staff.Name from Appointments appt
               # inner join Staff on staff.id = appt.Staffid
               # where  appt.customerId = {data[0]} and appt.ApppointmentDt =  '{apptDate}' and appt.StartTime = '{starttime}'"""

    quary = f"""select appt.id ,staff.Emailid,staff.Name from Appointments appt
                inner join Staff on staff.id = appt.Staffid
                where  appt.id = {data[6]}"""

    quary_exeappt = db_connection.execute(quary)
    dataappt = list(quary_exeappt)
    if dataappt == []:
        return False
        #return 'reminders date not matching with appt dates'
    #print(list(quary_exeappt),dataappt)
    dataappt = dataappt[0]
    apptid = dataappt[0]
    staffmail = dataappt[1]
    staffName = dataappt[2]
    updatequary = f"""update reminders set isActive  = '0' where id = {id};
                        update Appointments set Status = 4 , isActive = '0' where id = {data[6]}"""
    db_connection.execute(updatequary)
    db_connection.commit()
    db_connection.close()


    return {"cusname": data[3], "cusmobile": data[4], "cusEmail": data[5], "apptDate": apptDate, "starttime": starttime,
            "staffmail":staffmail,"staffName":staffName}

#print(cancelappt(1))

def dbrescheduleAppointment(id):
    #updating bokappt status false
    updateStatusToinactive(id)


    quary = f"""select cus.Name customername,staff.Name staffname,Staff.Emailid staffEmail
                ,bokappt.Sl1AppointmentDt,bokappt.Sl1StartTime,bokappt.Sl1EndTime
                from BookingAppt bokappt
                inner join Customers cus on cus.id = bokappt.Customerid
                inner join staff on staff.id = bokappt.staffid where bokappt.id = {id} """
    db_connection = pyodbc.connect(forDbConnection)
    quary_execution = db_connection.execute(quary)
    total_data = quary_execution.fetchall()
    if len(total_data) == 0:
        return None

    for j in range(len(total_data)):
        count = 0
        dict_data = {}

        for i in quary_execution.description:
            dict_data[str(i[0]).lower()] = total_data[j][count]
            count += 1


    db_connection.close()
    return dict_data

#print(dbrescheduleAppointment(169))