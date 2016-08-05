#! python2

from GainString import *
from ImportData import *
'''
tba: It's much better if a signal match a value, delete the value from the list of sv.
'''
desFile = r'e:/ks.c'
# desFile = r'/Users/caopengkun/python/Gener/ks.c'

ecu = 'VCU'

def GenerateCode(db, sv):
	reStr = ''
	for fr in db._fl._list:
		if len(sv._list) == 0:
			break
		
		# genFlag: 0: recieve; 1: transmit; 2: generate code for ecu reference
		genFlag = 0
		msgStr = ''
		# whether there is a signal required
		if ecu in fr._Transmitter:
			genFlag = 1

		if genFlag == 0:	# recieve
			msgStr = '\n\n' + GetUnpackCommStr(fr._Id) + ', Trans ECU(s) is(are): '

			for tr in fr._Transmitter:
				msgStr += tr + ' '
			msgStr += '\n' + GetUnpackMsgHeadStr(fr._Id) + '\n'

			for sgl in fr._signals:

				# if sgl in sv file
				sglInfo = sv.getSignalInfo(sgl._name)

				if sglInfo[0]:
					genFlag = 2
					msgStr  += '\n' + GetSglCommStr(sglInfo[1], sgl._startbit, sgl._signalsize, sgl._factor, sgl._offset)
					msgStr  += '\n' + GetUnpackSglStr(sglInfo[1], sglInfo[2], 'data', sgl._startbit, sgl._signalsize, sgl._factor, sgl._offset)
					msgStr  += '\n'
			msgStr += GetUnpackMsgFootStr(fr._Id)

			if genFlag == 2:		
				reStr += msgStr
		else:
			# tba pack message comment

			for sgl in fr._signals:
				for ma in sv._list:
					if ma._signal == sgl._name:
						genFlag = 2

						#tba pack sgl code

			if genFlag == 2:
				print '// Pack message, tba, ID: ', fr._Id

	return reStr

def generateFile(desfile):
	# try:
	db = importDBC(dbcFile)
	sv = importSV(svFile)
	# print GenerateCode(db, sv)
	try:
		fi = open(desfile, 'w')
		fi.write(GenerateCode(db, sv))
		fi.close()
		print 'success for generated!'
	except:
		print 'error'

def test():
	# db = importDBC(dbcFile)
	# sv = importSV(svFile)
	# print GenerateCode(db, sv)
	generateFile(desFile)

if __name__ == '__main__':
    test()