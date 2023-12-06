#imports needed
import sqlite3
import json
import smtplib
import os
from email.mime.text import MIMEText

#connects to SQLite3 details database
#the Details database has one table 
#the column is emails, while the rows are 
#the newsletter tier, the recipients, the subject, and  the body
  
conn=sqlite3.connect("details.db")
cur=conn.cursor()
if os.path.getsize('details.db') == 0: #makes sure that the database is there
  cur.execute("CREATE TABLE emails(tier, recipients, subject, body"), this is the line that made the table

while True:
  choice=int(input(("Would you like to \n1.Add an email tier\n2.Edit the contents of an email tier\n3.Remove an email tier\n4.View all tiers\n5.Send all emails\n6.Quit")))
  match choice:
    case 1:#To add a tier
      #Gets input for the tier, and sets up the recipients and email 
      tier=input("What is the name of the tier?")
      recipients=[]
      email=""
      while True:
        email=input("Enter an email here. Type STOP when you are done.")#Gets emails for the tier recipients
        if email=="STOP":
          break
        recipients.append(email) #Gets the list of recipients until user inputs "STOP"
        
      subject=input("What is the subject of the email?")
      body=input("What is the body of the email?")
      recipients_str=json.dumps(recipients)#turns recipients into json string to support SQLITE
      cur.execute("INSERT INTO emails(tier, recipients, subject, body) VALUES (?, ?, ?, ?)", (tier, recipients_str, subject, body))
      conn.commit()#To add a tier
      print("Tier added")    
    case 2:#To edit a tier
      tier=input("What is the name of the tier?")
      cur.execute("SELECT * FROM emails WHERE tier = ?", (tier,))
      row = cur.fetchone()
      if row is not None:
        recipients=[]
        email=""
        while True:
          email=input("Enter an email here. Type STOP when you are done.")#Gets emails for the tier recipients
          if email=="STOP":
            break
          recipients.append(email) #Gets the list of recipients until user inputs "STOP"
        subject=input("What is the subject of the email?")
        body=input("What is the body of the email?")
        recipients_str=json.dumps(recipients)#turns recipients into json string to support SQLITE
        cur.execute("UPDATE emails SET recipients = ?, subject =?, body=? WHERE tier = ?", (recipients_str,subject, body, tier))
        conn.commit()
        print("Values in the 'recipients' column for tier '{tier}' updated.")
      else:
        print("No row found with tier '{tier}'.")
    case 3:#To remove a tier
       tier=input("What tier will you remove?")
       cur.execute("SELECT * FROM emails WHERE tier = ?", (tier,))
       row = cur.fetchone()
       if row is not None:
         # Delete the entire row which the tier is in
         cur.execute("DELETE FROM emails WHERE tier = ?", (tier,))
         conn.commit()
         print(f"Tier '{tier}' removed successfully")
    case 4:#To view all tiers
      cur.execute("SELECT * FROM emails")
      rows = cur.fetchall()
      for row in rows:
        print(row)
    case 5:#To send an email
      #try statement to catch errors if SMTP fails
      try:
        email=input("What is your email")
        password=input("What is the password for your email?")
        mail= smtplib.SMTP('smtp.gmail.com', 587) #sets up the SMTP connection
        mail.starttls()  # Use TLS
        mail.login(email, password) #log in and get the rows of database
        cur.execute("SELECT * FROM emails")
        rows=cur.fetchall()
        for row in rows: #to send the emails
          try:#try catch statement if there are errors sending email
            msg = MIMEText(row[3])#column 3 holds the body
            msg['from']=email
            receivers=json.loads(row[1])#column 1 holds the list of recipients, in a json list
            msg['to']=",".join(receivers)
            msg['subject']=row[2]#column 2 holds the subject of email
            mail.sendmail(msg['from'],msg['to'],msg.as_string())#SMTP connection sends the email being set up
          except Exception as e:
           print(f"Error sending email: {e}")
           mail.close()
        mail.close()
        
      except Exception as e:
        print(f"SMTP Connection Error: {e}")
        mail.close()
    case 6: #to close the app
      conn.close()
      print("App closed")
      exit()
    case other:
      print("Invalid choice")



