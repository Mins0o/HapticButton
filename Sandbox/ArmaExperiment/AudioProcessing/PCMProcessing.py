from os import listdir
from numpy import average
import csv
import random
	
def TruncateToMinLength(dataCollection):
	"""This method matches the length of the data by cutting off the tails of longer files"""
	# Get minimum length and file name of it
	minLength = 9999999
	fileName = ""
	for name in dataCollection:
		data = dataCollection[name][0]
		for singleDataStream in range(len(data)):
			if len(data[singleDataStream])<minLength:
				minLength = len(data[singleDataStream])
				fileName = "{0}, Line {1}".format(name, singleDataStream)
	
	# Confirm user action
	userAnswer = ""
	while not(userAnswer.lower() == "y" or userAnswer.lower() == "n"):
		userAnswer = input("The minimum length is {0} from {1}. Would you like to truncate the data?(Y/N)\n>>> ".format(minLength, fileName))
	
	# Slice and return
	if userAnswer.lower() == "y":
		output = ([], [])
		for dataFile in dataCollection:
			for i in range(len(dataCollection[dataFile][0])):
				output[0].append(dataCollection[dataFile][0][i][:minLength])
				output[1].append(dataCollection[dataFile][1][i])
	return output

def ElongateToMaxLength(dataCollection):
	"""This method matches the length of the data by inputing average value to the tails of shorter files"""
	maxLength = 0
	fileName = ""
	
	# Look for the max length
	for name in dataCollection:
		data = dataCollection[name][0]
		for singleDataStream in range(len(data)):
			if len(data[singleDataStream]) > maxLength:
				maxLength = len(data[singleDataStream])
				fileName = "{0}, Line {1}".format(name, singleDataStream)
				
	# User confirmation
	userAnswer = ""
	while not(userAnswer.lower() == "y" or userAnswer.lower() == "n"):
		userAnswer = input("The maximum length is {0} from {1}. Would you like to elongate the data?(Y/N)\n>>> ".format(maxLength, fileName))
	
	# Splice a fake tail to the data and return
	if userAnswer.lower() == "y":
		output = ([], [])
		for dataFile in dataCollection:
			for i in range(len(dataCollection[dataFile][0])):
				_data=dataCollection[dataFile][0][i]
				lastPoint=_data[-1]
				avg = average(_data)
				lenDiff = maxLength-len(_data)
				output[0].append(_data + [int(round((lastPoint * (lenDiff - i) + avg * i)/ lenDiff)) for i in range(lenDiff)])
				output[1].append(dataCollection[dataFile][1][i])
	return output


def MatchFrequency(dataCollection, originalF = 7840, targetF = 45000):
	"""This method compares the frequency difference and calls a data processing method accordingly"""
	output = ([], [])
	print("Processing frequency match from {0} Hz to {1} Hz.".format(originalF, targetF))
	if originalF > targetF:
		process = DecreaseFrequency
	elif originalF < targetF:
		process = IncreaseFrequency
	else:
		process = (lambda x, originalF, targetF : x)
	for dataFile in dataCollection:
		for i in range(len(dataCollection[dataFile][0])):
			processedData = process(dataCollection[dataFile][0][i], originalF, targetF)
			output[0].append(processedData)
			output[1].append(dataCollection[dataFile][1][i])
	return output

def IncreaseFrequency(data, originalF, targetF):
	"""This method uses interpolation to fill in the gaps"""
	baseStep = targetF // originalF
	randomAddPossibility = targetF % originalF
	returnData = []
	index = 0
	endOfList = False
	randAdd = [1 for i in range(randomAddPossibility)] + [0 for i in range(originalF - randomAddPossibility)]
	while not endOfList:
		random.shuffle(randAdd)
		for randomArrayIndex in range(originalF):
			try:
				returnData += interpolate(data[index], data[index + 1], baseStep + randAdd[randomArrayIndex])
			except IndexError:
				endOfList = True
				break
			index += 1
	return(returnData)
			
def interpolate(point1, point2, numberOfPoints, roundToInt = True):
	"""<numberOfPoints> should be greater or equal to 1.
	<numberOfPoints> is number of points from point1 until point2."""
	if numberOfPoints == 1:
		return([point1])
	interval = (point2 - point1) / numberOfPoints
	if roundToInt:
		return([int(round(point1 + i * interval)) for i in range(numberOfPoints)])
	return([point1 + i * interval for i in range(numberOfPoints)])
	
def DecreaseFrequency(data, originalF, targetF, avgOption = True):
	"""Decrease frequency by sampling from original data.
	This method uses psuedo random distribution to ensure it has rather uniform smapling rate match.
	With avgOption on(True), the sampling will use the average of the missed datapoints.
	If the option is False, it will sample from a single point.
	
	data: Numeric datapoints in list format
	originalF: integer value of the data's sample rate
	targetF: integer value of the target smple rate
	avgOption: boolean value to enable averaging
	"""
	baseStep = originalF // targetF
	randomAddPossibility = originalF % targetF
	returnData = []
	index = 0
	endOfList = False
	randAdd = list([1 for i in range(randomAddPossibility)] + [0 for i in range(targetF-randomAddPossibility)]) #create a list of 0 and 1 with fixed proportion
	if avgOption:
		prev = 0
		while not endOfList:
			random.shuffle(randAdd) # the list of 0 and 1 is mixed
			for randomArrayIndex in range(targetF):
				index += baseStep + randAdd[randomArrayIndex]
				slice = data[prev:index]
				if not slice == []:
					returnData.append(average(slice))
				else:
					endOfList = True
					break
				prev = index
				
	else:
		while not endOfList:
			random.shuffle(randAdd)
			for randomArrayIndex in range(targetF):
				try:
					returnData.append(data[index])
				except IndexError:
					endOfList = True
					break
				index += baseStep + randAdd[randomArrayIndex]
	return returnData
	
if (__name__ == "__main__"):
	print("The path may contain spaces and escape characters will not work.")
	filePath = input("What is the path of your data folder?\n>>> ")
	print("<<<MatchFrequency() in progress>>>")
	SaveData(MatchFrequency(LoadFiles(filePath)), filePath)
	print("<<<ElongateToMaxLength() in progress>>>")
	SaveData(ElongateToMaxLength(LoadFiles(filePath)), filePath)
	
	