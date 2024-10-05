import tkinter as tk
from tkinter import ttk  ### Kind of like the CSS for tkinter

email_font = ("Times", 12)
large_font = ("Verdana", 12)
norm_font = ("Verdana", 10)
small_font = ("Verdana", 8)

#####################################################################################################################################
def pop_up_msg(msg, title = "Warning"):
	"""Creates a pop up message for users when called. 
		The message is the argument you pass through."""
	### Creating an instance for pop up messsages
	pop_up = tk.Tk()
	pop_up.wm_title(title)
	label = ttk.Label(pop_up, text = msg, font = norm_font)
	label.pack(side = "top", padx = 30, pady = 10)

	### To ensure "Hopefully you didn't pick philly..." can be seen
	if "philly" in title: pop_up.geometry("350x75")

	## Creating exit options
	ttk.Button(pop_up, text = "Okay", command = pop_up.destroy).pack(pady = 5)
	pop_up.bind("<Return>", lambda e: pop_up.destroy())
	pop_up.mainloop()
	return

#####################################################################################################################################
def gamblingCal():
	"""Creates a calculator for calculating winning totals."""
	cal = tk.Tk()
	cal.wm_title("Gambling Calculator")

	### Creating labels and entry for number of players to be paid
	num_l = ttk.Label(cal, text = "Number of players to be paid?", font = ("Times", "12"), relief = "groove", anchor = "center")
	num_l.grid(row = 0, column = 0, padx = 10, ipady = 10, sticky = "nesw", ipadx = 10)

	num_e = ttk.Entry(cal)
	num_e.insert(0, 3)
	num_e.grid(row = 0, column = 1, padx = 10, ipady = 10, sticky = "nesw")

	## Creating labels for players, paid percent, and paid out
	per_l = ttk.Label(cal, text = "Enter the paid out percent:", font = ("Times", "12"), relief = "groove", anchor = "center")
	per_l.grid(row = 2, column = 1, padx = 10, ipady = 10, sticky = "nesw", ipadx = 10)

	results_l = ttk.Label(cal, text = "Each player should be paid:", font = ("Times", "12"), relief = "groove", anchor = "center")
	results_l.grid(row = 2, column = 2, padx = 10, ipady = 10, sticky = "nesw", ipadx = 10)

	### Creating total label/entry
	total_l = ttk.Label(cal, text = "Total Payout", font = ("Times", "12"), relief = "groove", anchor = "center")
	total_l.grid(row = 14, column = 0, padx = 10, ipady = 10, sticky = "nesw")
	total_e = ttk.Entry(cal)
	total_e.grid(row = 14, column = 1, padx = 10, ipady = 10, sticky = "nesw")

	def	num_player_ck():
		### Checking to make sure number of players is a whole number and falls between 2-10
		try: 
			if int(num_e.get()) > 10:
				pop_up_msg("Max number of players is 10... sorry, I'm not sorry...\nWhy are you trying to pay out so many people...")
				return "num_error"
			
			elif int(num_e.get()) == 1:
				pop_up_msg("There's only one player... why are you using this calculator?")
				return "num_error"

			elif int(num_e.get()) < 1:
				pop_up_msg("How can you have less than two players???... try again...")
				return "num_error"
		
		except ValueError:
			pop_up_msg("How can number of players not be a whole number? Try again...")
			return "num_error"
		return 

#####################################################################################################################################
	def num_players():
		"""Creates the inputs for number of players based out what is in the num_e entry."""
		cal.update()
		### creating players
		deValues = [60, 30, 10, 0, 0, 0, 0, 0, 0, 0]

		### Checking to make sure number of players is a whole number
		numPlayerCk = num_player_ck()
		if numPlayerCk == "num_error": return

		if int(num_e.get()) == 2:
			deValues = [70, 30]

		### Creating labels
		[items.grid_forget() for items in cal.grid_slaves() if 14>int(items.grid_info()["row"])>=6 and int(items.grid_info()["column"]) in [0,1,2]]
		for num in range(int(num_e.get())):
			player_l[num].grid(row = num+4, column = 0, padx = 10, ipady = 10, sticky = "nesw")

			### Creating entries
			player_e[num].delete(0, "end")
			player_e[num].insert(0, deValues[num])
			player_e[num].grid(row = num+4, column = 1, padx = 10, ipady = 10, sticky = "nesw")

			### Creating labels
			payOut[num].set("$ {}".format(player_e[num].get()))
			player_l2[num].grid(row = num+4, column = 2, ipadx = 10, ipady = 10, sticky = "nesw")

		### Creating total entry
		total_e.delete(0, "end")
		total_e.insert(0, 100)
		return

#####################################################################################################################################
	### Calculates the outputs for the gmbling calculator
	def cal_results(event = None):
		"""Calculates how much each player should be  paid."""
		### Checking to make sure number of players is a whole number
		numPlayerCk = num_player_ck()
		if numPlayerCk == "num_error": return

		### Removing , for if some enters 1,000 or so
		tot_pot = total_e.get()
		if "," in tot_pot:
			tot_pot = tot_pot.replace(",", "")
	
		### Ensuring the total value is a float
		try: 
			if "." in tot_pot:
				tempPot = tot_pot.split(".", 1)
				for items in tempPot:
					if "." in items:
						pop_up_msg("Why do you have more than one decimal point???")
						return
				if len(tempPot[1]) > 2:
					pop_up_msg("How do you have a fraction of a penny?\nThat's impressive... try again...")
					return
			

		except TypeError:
			pop_up_msg("Total amount should probably be a number... try again...")
			return

		### Ensuring the total value is a float
		try:
			tot_pot = float(tot_pot)
		except ValueError:
			pop_up_msg("Total amount should probably be a number... try again...")
			return

		### Ensure the total pot is positive:
		if tot_pot < 0:
			pop_up_msg("A fantasy league where the winners lose money? I would have JJ Watt draft my team...")
			return
		elif tot_pot == 0:
			pop_up_msg("You really needed a calculator when the total payout is zero... here's the answer, everyone gets zero...")
			return

		### Checking to make sure winning percentage is a number and not negative
		try:
			total_per  = []
			for num_t in range(int(num_e.get())):
				total_per.append(float(player_e[num_t].get())) 
			
				### Check for negativies
				if float(player_e[num_t].get()) < 0:
					pop_up_msg("How can a winning percentage be negative?")	
					return

		except ValueError:
			pop_up_msg("How can percentage not be a number? Try again...")
			return

		### Checking percentage totals higher or lower than 100
		total_per = sum(total_per)
		if total_per > 100:
			pop_up_msg("Bro, {}%, that's more than 100%...".format(total_per))
			return
		elif total_per < 100: 
			pop_up_msg("{}%, that's less than 100%, trying to pocket a little?".format(total_per))
			return

		### Update labels to show the results
		[items.grid_forget() for items in cal.grid_slaves() if 14 > int(items.grid_info()["row"]) >= 6 and int(items.grid_info()["column"]) == 2]
		for num in range(int(num_e.get())):
					payOut[num].set("$ {}".format(round(float(player_e[num].get())/100*tot_pot, 2)))
					player_l2[num].grid(row = num+4, column = 2, ipadx = 10, ipady = 10, sticky = "snew")
		return

#####################################################################################################################################
	### Creating first labels
	payOut = {num : tk.StringVar(cal) for num in range(10)}
	player_l = {}
	player_l2 = {}
	player_e = {}
	for num in range(10):
		player_l.update({num:ttk.Label(cal, text = "Player {}".format(num+1), font = ("Times", "12"), relief = "groove", anchor = "center")})
		player_l2.update({num:ttk.Label(cal, textvariable = payOut[num], font=("Times", "12"), relief="sunken", anchor="center")})
		player_e.update({num:ttk.Entry(cal)})

	### Creating entry for inputs
	num_players()

	### submit button for number of players
	ttk.Button(cal, text = "Submit", command = num_players).grid(row = 1, column = 1)
	
	### Binding to calculate on enter
	cal.bind("<Return>", cal_results)

	### creating an buttons
	gamLabel = "*if gambling is illegal in your area, then this calculator is for hypothetical purposes only ;)"
	ttk.Label(cal, text=gamLabel, justify="left", anchor = "w").grid(row = 16, column = 0, columnspan = 2)
	ttk.Button(cal, text = "Calculate", command = cal_results).grid(row = 15, column = 0)
	ttk.Button(cal, text = "Exit", command = cal.destroy).grid(row = 15, column = 2)
	cal.mainloop()
	return

#####################################################################################################################################
def emailMe(whatKind = "General"):
	"""Sends emails: General, bugs, and ideas."""
	maxCharLen = 500

	def sendEmail():
		"""The function that actually sends the email"""

		if submit.get() == 0 and whatKind == "Idea":
			if "app" in subjectE.get().lower() or "app" in emailE.get("1.0", "end").lower():
				submit.set(1)
				pop_up_msg('You got this warning because you had "app" in your subject or email.\nIf your idea is a phone app, it\'s coming in due time...\nIf your idea is not a phone app, hit send again... ')
				return
		if len(subjectE.get()) > 50:
			pop_up_msg("Your Subject length is longer than 50 characters...\nLet's tone that down a little bit... ")
			return
		if len(emailE.get("1.0", "end")) > maxCharLen:
			pop_up_msg("Your email length is longer than 400 characters... Why????\nLet's tone that down a little bit... ")
			return
		
		import smtplib
		from email.mime.multipart import MIMEMultipart
		from email.mime.text import MIMEText
		from socket import gaierror
	 
		fromAddress = yourEmailE.get()
		emailAddress = "removed..."
		msg = MIMEMultipart()
		msg['From'] = fromAddress
		msg['Subject'] = whatSubject + subjectE.get()
		msg['Name'] = nameE.get()
		 
		body = "Email: " + yourEmailE.get() + '\n' + "Name: " + nameE.get() + '\n\n' + emailE.get("1.0", "end") 
		msg.attach(MIMEText(body, 'plain'))
		
		try:
			server = smtplib.SMTP('smtp.gmail.com', 587)
			server.starttls()
			server.login(emailAddress, "password removed...")
			text = msg.as_string()
			server.sendmail(fromAddress, emailAddress, text)
			server.quit()
			emailPopUp.destroy()
			pop_up_msg("Thank you for your email.\nI'll get to it, eventually,\nhopefully within some reasonable time frame...","Thank You")
		except gaierror:
			pop_up_msg("Dude, I got a socket error... Are you even connected to the internet?")

		return

	### String to show in email text box
	strEmail = "Text... ("+ str(maxCharLen) +" Characters Max)"

	if whatKind == "General":
		strEntry = "What's up?"
		strYourEmail = "ThisProgramIsAwesome@agreed.com"
		strName = "John Smith"
		strtitle = "Email Me or don't..."
		whatSubject = "General: "

	elif whatKind == "Idea":
		strEntry = "What's the idea?"
		strYourEmail = "IHaveGreatIdeas@maybe.com"
		strName = "Albert Einstein"
		strtitle = "Is this a good idea?"
		whatSubject = "Ideas: "

	elif whatKind == "Bug":
		strEntry = "What Kind of Bug?"
		strYourEmail = "IReportBugs@thankyou.com"
		strName = 'Joe "Bug Reporter" Schmo'
		strtitle = "Is it a bug or a feature?"
		strEmail = strEmail + "\nPlease include as much detail as possible.\nE.g: What were you doing?\n What button did you press?\netc..."
		whatSubject = "Bug: "

	emailPopUp = tk.Tk()
	emailPopUp.wm_title(strtitle)
	submit = tk.IntVar(emailPopUp)
	submit.set(0)

	### Creating your name information
	nameL = ttk.Label(emailPopUp, text = "Your Full Name:\n(optional)", font = email_font, relief = "groove", anchor = "center")
	nameL.grid(row = 0, column = 0, ipadx = 5, ipady = 5, sticky = "nesw")
	nameE = ttk.Entry(emailPopUp, font = email_font)
	nameE.insert(0, strName)
	nameE.grid(row = 0, column = 1, ipadx = 5, ipady = 5, sticky = "nesw")

	### Creating your email information
	yourEmailL = ttk.Label(emailPopUp, text = "Your Email:\n(optional)", font = ("Times", "12"), relief = "groove", anchor = "center")
	yourEmailL.grid(row = 1, column = 0, ipadx = 5, ipady = 5, sticky = "nesw")
	yourEmailE = ttk.Entry(emailPopUp, font = email_font)
	yourEmailE.insert(0, strYourEmail)
	yourEmailE.grid(row = 1, column = 1, ipadx = 5, ipady = 5, sticky = "nesw")
	
	### Creating subject informaion
	subjectL = ttk.Label(emailPopUp, text = "Subject:", font = ("Times", "12"), relief = "groove", anchor = "center")
	subjectL.grid(row = 2, column = 0, ipadx = 5, ipady = 5, sticky = "nesw")
	subjectE = ttk.Entry(emailPopUp, font = email_font)
	subjectE.insert(0, strEntry)
	subjectE.grid(row = 2, column = 1, ipadx = 5, ipady = 5, sticky = "nesw")

	### Creating subject informaion
	emailE = tk.Text(emailPopUp, bg = "white", font = email_font)
	emailE.insert("insert", strEmail)
	emailE.grid(row = 3, column = 0, rowspan = 2, columnspan = 2, ipadx = 5, ipady = 5, sticky = "nesw")

	ttk.Button(emailPopUp, text = "Send", command = sendEmail).grid(row = 15, column = 0, sticky = "nesw")
	ttk.Button(emailPopUp, text = "Exit", command = emailPopUp.destroy).grid(row = 15, column = 1, sticky = "nesw")
	emailPopUp.mainloop()
	return




