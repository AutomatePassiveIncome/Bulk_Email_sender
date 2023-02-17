import smtplib, ssl, csv, random
from email.message import EmailMessage

replyto = 'Your Reaply to Email Id'
subject = 'Subject Of your Email'
name = 'Email Name'

counter = {}

with open("user.csv") as f:
    data = [row for row in csv.reader(f)]

# file_list = ['emails/message' + str(i) + '.txt' for i in range(1,11)] # Multipale Files
file_list = ['emails/message1.txt'] #Singale Email

with open('mails.csv', 'r') as csvfile:
    datareader = csv.reader(csvfile)
    for row in datareader:
        random_user = random.choice(data)
        sender = random_user[0]
        password = random_user[1]
        
        if sender not in counter:
            counter[sender] = 0
        
        if counter[sender] >= 500:
            continue
        
        try:
            context = ssl.create_default_context()
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context)
            server.login(sender, password)
            em =EmailMessage()
            em['from'] = f'{name} <{sender}>'
            em['Reply-To'] = replyto
            em['To'] = row
            em['subject'] = subject
            random_file = random.choice(file_list)
            with open(random_file, 'r') as file:
                html_msg = file.read()
            em.add_alternative(html_msg, subtype='html')
            server.send_message(em)
            counter[sender] += 1
            print(counter[sender], " emails sent", "From ", sender,  "To ", row ,"File ", random_file)
            with open("mails.csv", "r") as file:
                reader = csv.reader(file)
                rows = list(reader)
                rows = rows[1:]
            if rows:
                with open("mails.csv", "w", newline='') as file:
                    writer = csv.writer(file)
                    writer.writerows(rows)
            server.close()
        except Exception as e:
            print(f"Error sending email From {sender} to {row}:", e )
            with open("mails.csv", "r") as file:
                reader = csv.reader(file)
                rows = list(reader)
                rows = rows[1:]
            if rows:
                with open("mails.csv", "w", newline='') as file:
                    writer = csv.writer(file)
                    writer.writerows(rows)

print("Emails Sent")
for sender, count in counter.items():
    print(f"{sender}: {count}")
