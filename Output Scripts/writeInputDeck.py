# writeInputDeck.py
# 2014-01-17 Ebbe Smith - PLM Tech AS 
#
# Dumps condenced inputdecks for all models in the CAE (same as shown in keyword editor)
#
#--------------------------------------------------

from abaqus import *
from abaqusConstants import *

for modelKey in mdb.models.keys():
	m = mdb.models[modelKey]
	block = m.keywordBlock.sieBlocks

	outputfile = open(modelKey+'.txt', 'w')
	for line in block:
		print line
		outputfile.write(line)
		outputfile.write('\n')
	outputfile.close()

