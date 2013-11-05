from LMIO.wrapper import LMIO

testLMIO = LMIO('swcFiles/HB060602_3ptSoma.swc')

failFile = open('functionFailures.txt', 'w')

#*********************************************************************************************************************
# Testing LMIO.getMeasure
#*********************************************************************************************************************
functionality = 'getMeasure:'
for func in testLMIO.functionRef:
    print 'Testing ' + functionality + func
    try:
        testLMIO.getMeasure(func)
    except Exception, exep:
        print 'error'
        failFile.write(functionality + func + '\n')
        failFile.write(str(exep) + '\n')

#*********************************************************************************************************************


#*********************************************************************************************************************
# Testing LMIO.getMeasureDistribution
#*********************************************************************************************************************
functionality = 'getMeasureDistribution:'
for func in testLMIO.functionRef:
    print 'Testing ' + functionality + func
    try:
        testLMIO.getMeasureDistribution(func)
    except Exception, exep:
        print 'error'
        failFile.write(functionality + func + '\n')
        failFile.write(str(exep) + '\n')

#*********************************************************************************************************************


#*********************************************************************************************************************
# Testing LMIO.getMeasureDependence
#*********************************************************************************************************************
functionality = 'getMeasureDependence:'
for func in testLMIO.functionRef:
    print 'Testing ' + functionality + func
    try:
        testLMIO.getMeasure('EucDistance', func)
    except Exception, exep:
        print 'error'
        failFile.write(functionality + func + '\n')
        failFile.write(str(exep) + '\n')

#*********************************************************************************************************************

failFile.close()