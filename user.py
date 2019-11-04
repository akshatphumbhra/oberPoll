class User():
	#base class -> pass in student or teacher, then the rest for account info. sets variables to them
	def __init__(self, account, name, email, password):
		self.accountType = account
		self.name = name
		self.email = email
		self.password = password
		
	def identity(self):
		print("Hey! I am " + self.name)
		
#testing to make sure the class is working		
#kobe = User("student", "Kobe Brooks", "kobe.brooks@yahoo.com", "hey")

#kobe.identity()
