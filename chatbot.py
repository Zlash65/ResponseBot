import json
import re

def gather_input():
	# pass the absolute path of file or just the name if in same directory
	path = take_input("Please provide the path of input file")

	with open(path, 'r') as file_data:
		input_data = json.loads(file_data.read())

	# call the conversation interpreter function
	eval("{0}({1})".format(scrub(input_data["function"]), input_data["questions"]))

def sample_text_function(question_matrix):
	''' loop through the input instruction '''
	# capture access to locals
	localVar = {}

	for d in question_matrix:
		if d.get('instruction'):
			unpack_instrcution(d, localVar)
		elif d.get("text"):
			list_instance = re.findall('.*(\[.*?\]).*', d["var"])
			if list_instance:
				temp_var = get_var_input(d, localVar)
				list_eval = "{0}.append('{1}')".format(d["var"].split("[")[0], temp_var)
				eval(list_eval, localVar)
			else:
				localVar[d["var"]] = get_var_input(d, localVar)
		elif d.get("calculated_variable"):
			localVar[d["var"]] = calculated_variable(d, localVar)

def get_var_input(data, localVar):
	''' store '''
	var = data["var"]

	if data.get("conditions"):
		conditions = data.get("conditions")
		and_cond = ["(" + " and ".join(row) + ")" for row in conditions]
		cond = " or ".join(and_cond)

		while eval(cond, localVar):
			localVar[var] = take_input(data["text"], data.get("options"))
	else:
		# take input
		temp_var = take_input(data["text"], data.get("options"))

	return localVar.get(var) or temp_var

def unpack_instrcution(data, localVar):
	output = data["instruction"]

	if data.get("list_var") and data.get("list_length"):
		for i in range(0, int(data["list_length"])):
			localVar["i"] = i
			args = [eval(x, localVar) for x in data["instruction_var"]]
			output = data["instruction"] % tuple(args)
			print(output)

		return
	elif data.get("instruction_var"):
		args = [localVar[d] for d in data["instruction_var"]]
		output = output % tuple(args)

	print(output)

def calculated_variable(d, localVar):
	return eval(d["formula"], localVar)

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