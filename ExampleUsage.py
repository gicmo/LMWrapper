from LMIO.wrapper import LMIO
import matplotlib.pyplot as plt

testLMIO = LMIO('swcFiles/HB060602_3ptSoma.swc')

# #*********************************************************************************************************************
# # Usage Example LMIO.getMeasureDistribution
# #*********************************************************************************************************************
# LMOutput = testLMIO.getMeasureDistribution('Diameter', nBins=50)
# plt.figure()
#
#
# print LMOutput['measure1BinCentres']
# print LMOutput['measure1BinCounts']
# plt.bar(LMOutput['measure1BinCentres'], LMOutput['measure1BinCounts'])
# plt.draw()
# plt.show(block=True)
#
# #*********************************************************************************************************************

#*********************************************************************************************************************
# # Usage Example LMIO.getMeasure
#*********************************************************************************************************************
LMOutput = testLMIO.getMeasure('Branch_Order')
print 'Neuron Surface is ' + str(LMOutput['Average'])

#*********************************************************************************************************************

# #*********************************************************************************************************************
# # Usage Example LMIO.getMeasureDependence
# #*********************************************************************************************************************
# LMOutput = testLMIO.getMeasureDependence('Bif_ampl_local', 'EucDistance', nBins=50)
# plt.figure()
# plt.bar(LMOutput['measure1BinCentres'], LMOutput['measure2BinAverages'])
# plt.draw()
# plt.show(block=True)
#
# #*********************************************************************************************************************