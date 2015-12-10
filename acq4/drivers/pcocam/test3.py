import sys
sys.path.append('..\\..\\..\\')

import pcocam


paramValues = {}
## storage for local params and cache for remote params
## remote params must be cached because reading them can cause
## the camera to stop.
'''
paramValues = {  ## list of current values for parameters not handled by driver
'binningX': 1,
'binningY': 1,
'exposure': 0.001,
'framerate': 1,
'pixelrate': 1,			
'TriggerMode': 0,
'regionX': 0,
'regionY': 0, 
}

		
#print len(paramValues)
#print paramValues
i=0 
for i in paramValues:
	print i , paramValues[i]
	
print "\n"

for i in paramValues:
	paramValues[i] = int(paramValues[i]) + 99
	print i , paramValues[i]'''
	


pco = pcocam.PCODriverClass()
cam = pco.getCamera('pixelfly')
cam.close()






