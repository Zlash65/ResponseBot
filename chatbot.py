import json

def gather_input():
	# pass the absolute path of file or just the name if in same directory
	path = take_input("Please provide the path of input file : ")

	with open(path, 'r') as file_data:
		input_data = json.loads(file_data.read())

	# call the conversation interpreter function
	eval("{0}({1})".format(scrub(input_data["function"]), input_data["questions"]))

def sample_text_function(question_matrix):
	''' loop through the input instruction '''
	# capture access to locals
	localVar = locals()

	for d in question_matrix:
		if d.get('instruction'):
			unpack_instrcution(d)
		elif d.get("text"):
			localVar[d["var"]] = get_var_input(d, localVar)

def get_var_input(data, localVar):
	''' store '''
	if not localVar.get(data["var"]):
		localVar[data["var"]] = None

	if data.get("conditions"):
		conditions = data.get("conditions")
		and_cond = ["(" + " and ".join(row) + ")" for row in conditions]
		cond = " or ".join(and_cond)

		while eval(cond, localVar):
			localVar[data["var"]] = take_input(data["text"], data.get("options"))
	else:
		# take input
		localVar[data["var"]] = take_input(data["text"], data.get("options"))

	return localVar[data["var"]]

def unpack_instrcution(data):
	print(data["instruction"])

def scrub(txt):
	''' return scrubbed name "XYZ-abc def" becomes "xyz_abc_def" '''
	return txt.replace(' ','_').replace('-', '_').lower()

def take_input(text, options=[]):
	inp, opt = "", ""
	if options:
		opt = "(" + " / ".join(options) + ")"

	# python 2 & 3 based input
	try:
		inp =  raw_input("{0} {1}: ".format(text, opt))
	except NameError:
		inp = input("{0} {1}: ".format(text, opt))

	if options and inp not in options:
		print("Invalid option. Please select one of these {0}".format(opt))
		inp = take_input(text, options)

	return inp

if __name__ == "__main__":
	gather_input()