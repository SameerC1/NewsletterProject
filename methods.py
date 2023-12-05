#imports needed
import smtplib
from email.message import EmailMessage
#function to prepare the email for the newsletter
def makemail():
  with open('recipients.txt', 'r') as file:
        mailList = [line.strip() for line in file]
  msg=EmailMessage()

  msg['To'] = mailList  # Join recipient emails with a comma and space
  
  with open('maildetails.txt', 'r') as file: #gets the subject and body of the email from lines 1  & 2 of the maildetails file
    msg['Subject']=file.readline()
    msg['From']=file.readline()
    msg.set_content(file.readline())
  return msg



def sendmail(msg,connection):
  connection.send_message(msg)#sends the message
  connection.quit()#ends the connection to smtplib
