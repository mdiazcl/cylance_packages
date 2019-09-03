"""
CylanceOPTICS Refract Package Template
Use this file as a template to create custom code
to be executed by the CylanceOPTICS endpoint.

Most of your custom code will likely be in the
'execute' method of the CyInterface class.
"""

# Imports
# We must add the IronPython standard library in order to
# import python standard modules like 'os' and 'platform'
import clr
clr.AddReference('IronPython.StdLib')
import sys
import os
import platform

# Imports C# libraries
clr.AddReference('System.Core')
from System.Dynamic import ExpandoObject

# Custom Imports - Place any other modules to import below this line
import subprocess

class CyInterface:
	"""A simple interface class"""

	def __init__(self):
		"""
		Add initialization code here for the interface (likely very little)
		"""

		# This prints the name of the of the function in the log
		print sys._getframe().f_code.co_name
		self.package_output_directory = '.'  # output folder, to be populated in the initialize function

	def __del__(self):
		"""
		Add code to be executed when the instance is destroyed (also known as a destructor)
		"""
		print sys._getframe().f_code.co_name

	def initialize(self, param):
		print sys._getframe().f_code.co_name

		# param.print_message decides whether to print to the log or not
		if 'print_message' in param:
			print '  print_message: ', param.print_message
		else:
			print 'initialize() does not have print_message'

		# cache the param if needed for execute later.
		if "out" in param:
			self.package_output_directory = param.out

		self.package_source_directory = os.path.dirname(os.path.realpath(__file__))

		eo = ExpandoObject()  # prepare return value
		eo.status = 0  # success

		print "Initialization complete."
		return eo

	def execute(self):
		"""
		This is where most of your custom code should live.
		Note: you can use the 'self.package_output_directory' and 'self.package_source_directory' variables
		to reference the paths where a package is outputting to or executing from.
		"""
		print sys._getframe().f_code.co_name
		eo = ExpandoObject()  # prepare return value

		# Start of package code
		try:
			# if (param.ip != None):
			print("made it to execute")

			'''cmd_get_services = "Get-Service"
			process = subprocess.Popen(["powershell", cmd_get_services],stdout=subprocess.PIPE);
			service = process.communicate()[0]

			output_file = open(os.path.join(self.package_output_directory, "services.txt"), "w+")
			output_file.write(service)
			output_file.close()

			cmd_get_logs = 'Get-EventLog -LogName System | where-Object {$_.EventID -eq 7045} | Format-Table TimeGenerated, MachineName, UserName, Message -wrap'
			process = subprocess.Popen(["powershell", cmd_get_logs],stdout=subprocess.PIPE);
			service_logs = process.communicate()[0]

			output_file = open(os.path.join(self.package_output_directory, "services_log.txt"), "w+")
			output_file.write(service_logs)
			output_file.close()'''

			data = self.run_powershell("Get-WmiObject -Class Win32_UserAccount -Filter \"LocalAccount=True\" | Select PSComputername, Name, Status, Disabled, AccountType, Lockout, PasswordRequired, PasswordChangeable | Format-Table Status, PSComputername, Name, AccountType, Lockout, PasswordRequired  -wrap")
			self.write_output(data, "usuarios.txt")

			data = self.run_powershell("Get-EventLog -LogName System | where-Object {$_.EventID -eq 7045} | Format-Table TimeGenerated, MachineName, UserName, Message -wrap")
			self.write_output(data, "event_7045.txt")

			data = self.run_powershell("Get-Service")
			self.write_output(data, "installed_services.txt")


			eo.status = 0  # set the return code of the package either manually or as a result of how things went

		except Exception as e:
			eo.status = -1  # fail
			print("Excecution of package failed with error: {}".format( e.message))

		# End of package code

		print "Package execution completed."
		return eo

	def run_powershell(self, cmd):
		cmd_get_services = cmd
		process = subprocess.Popen(["powershell", cmd_get_services],stdout=subprocess.PIPE);
		return process.communicate()[0]

	def write_output(self, data, filename):
		output_file = open(os.path.join(self.package_output_directory, filename), "w+")
		output_file.write(data)
		output_file.close()
		return True

# End of interface API

# This is the 'runner' of the package
# It is used to get the location of the output directory and
# setup the interface. Consider this the "Main" function.
# This is also where you can check for and parse additional command line args.
def run_test(argv):
	import os
	print sys._getframe().f_code.co_name

	# Imports C# libraries
	import clr
	from System.Dynamic import ExpandoObject
	clr.AddReference('System.Core')

	interface = CyInterface()

	param = ExpandoObject()
	param.print_message = 1  # set print message to True so outputs are in log

	# get the output folder from the arguments
	# this is also where you would look for other custom arguments
	# (by searching for the argument name, incrementing i, and then grabbing that value)
	i = 0
	for arg in argv:
		print 'arg: ', arg
		i = i + 1
		if arg == "-out":
			param.out = argv[i]
		elif arg == "-ip":
			param.ip = argv[i]
		elif arg == "-net":
			param.net = argv[i]
		elif arg == "-url":
			param.url = argv[i]
		elif arg == "-dir":
			param.dir = argv[i]
	print "param.out: ", param.out
	print "param.ip: ", param.ip
	print "param.net: ", param.net
	print "param.url", param.url
	print "param.dir", param.dir

	# call interface's initialize
	result = interface.initialize(param)

	# call interface's Excute
	result = interface.execute()

	# call interface's delete
	del interface


if __name__ == "__main__":
	run_test(sys.argv)
