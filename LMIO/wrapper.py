import os
import subprocess
import platform
import pkgutil


class LMIO:
    """
    Wrapper class for using L-meausure via python scripting.
    """

    (bit, linkage) = platform.architecture()
    LMPath = 'Lm' + bit[:2] + '/'

    functionRef = ['Soma_Surface',
                   'N_stems',
                   'N_bifs',
                   'N_branch',
                   'N_tips',
                   'Width',
                   'Height',
                   'Depth',
                   'Type',
                   'Diameter',
                   'Diameter_pow',
                   'Length',
                   'Surface',
                   'SectionArea',
                   'Volume',
                   'EucDistance',
                   'PathDistance',
                   'Branch_Order',
                   'Terminal_degree',
                   'TerminalSegment',
                   'Taper_1',
                   'Taper_2',
                   'Branch_pathlength',
                   'Contraction',
                   'Fragmentation',
                   'Daughter_Ratio',
                   'Parent_Daughter_Ratio',
                   'Partition_asymmetry',
                   'Rall_Power',
                   'Pk',
                   'Pk_classic',
                   'Pk_2',
                   'Bif_ampl_local',
                   'Bif_ampl_remote',
                   'Bif_tilt_local',
                   'Bif_tilt_remote',
                   'Bif_torque_local',
                   'Bif_torque_remote',
                   'Last_parent_diam',
                   'Diam_threshold',
                   'HillmanThreshold',
                   'Hausdorff',
                   'Helix',
                   'Fractal_Dim']

    LMOutput = dict(rawData=[],
                    measure1BinCentres=[],
                    measure1BinCounts=[],
                    measure2BinAverages=[],
                    measure2BinStdDevs=[],
                    Minimum=None,
                    Maximum=None,
                    Average=None,
                    CompartmentsConsidered=None,
                    CompartmentsDiscarded=None,
                    TotalSum=None,
                    StdDev=None)
    outputFormat = None

    line1 = ""
    line2 = ""
    line3 = ""

    LMInputFName = 'tmp/LMInput.txt'
    LMOutputFName = 'tmp/LMOutput.txt'
    LMLogFName = 'tmp/LMLog.txt'

    rawDataOutputFlag = False

    packagePrefix = pkgutil.get_loader("LMIO").filename + '/'

    #*******************************************************************************************************************

    def resetOutputData(self):

        """
        Resets all the fields of the output dictionary LMOutput

        :argument   : None
        :returns    : None

        :rtype : None
        """
        self.LMOutput['rawData'] = []
        self.LMOutput['measure1BinCentres'] = []
        self.LMOutput['measure1BinCounts'] = []
        self.LMOutput['measure2BinAverages'] = []
        self.LMOutput['measure2BinStdDevs'] = []
        self.LMOutput['Minimum'] = None
        self.LMOutput['Maximum'] = None
        self.LMOutput['Average'] = None
        self.LMOutput['CompartmentsConsidered'] = None
        self.LMOutput['CompartmentsDiscarded'] = None
        self.LMOutput['TotalSum'] = None
        self.LMOutput['StdDev'] = None

        self.outputFormat = None

    #*******************************************************************************************************************

    def __init__(self, morphFile):

        """
        Initializes the object.

        :param morphFile    : string containing the path to the target SWC file.
        :rtype              : None.
        """
        self.rawDataOutputFlag = False

        self.resetOutputData()

        self.line1 = ""
        self.line2 = ""
        self.line3 = morphFile

        if not os.path.isdir('tmp'):
            os.mkdir('tmp')

    #*******************************************************************************************************************

    def writeLMIn(self, line1, line2, line3):
        """
        Write the input file for L-measure.

        :param line1: The string containing the first line of the input file to L-measure
        :param line2: The string containing the second line of the input file to L-measure
        :param line3: The string containing the third line of the input file to L-measure
        :rtype: None
        """

        LMIn = open(self.LMInputFName, 'w')

        if self.rawDataOutputFlag:
            line2 += '-R'

        LMIn.write(line1 + '\n' + line2 + '\n' + line3)
        LMIn.close()

    #*******************************************************************************************************************

    def runLM(self):
        """
        Runs the appropriate L-measure executable with the required arguments.

        """

        self.resetOutputData()
        if os.path.isfile(self.LMOutputFName):
            os.remove(self.LMOutputFName)
        if os.path.isfile(self.LMLogFName):
            os.remove(self.LMLogFName)

        LMLogFle = open(self.LMLogFName, 'w')
        subprocess.call([self.packagePrefix + self.LMPath + 'lmeasure', self.LMInputFName], \
                        stdout=LMLogFle, stderr=LMLogFle)

        try:
            LMOutputFile = open(self.LMOutputFName, 'r')
        except:
            print('No Output file created by Lmeasure. Check \'tmp/LMLog.txt\'')
            exit(1)

        LMLogFle.close()

    #*******************************************************************************************************************

    def readlineTrap(self, fle):
        """
        Reads a line from the specified 'fle' object and replaces all instances of '(0)' with 0.
        :param fle: file object
        :return:
        """

        tempStr = fle.readline()
        return tempStr.replace('(0)', '0')

    #*******************************************************************************************************************

    def readOutput(self):
        """
        Reads output from the L-measure output file according to the format specified in 'outputFormat' and fills in the structure LMOutput
        :return:
        """

        LMOutputFile = open(self.LMOutputFName, 'r')

        if self.rawDataOutputFlag:

            self.LMOutput['rawData'] = []
            prevLine = LMOutputFile.tell()
            tempStr = self.readlineTrap(LMOutputFile)

            while not tempStr.count('\t'):

                prevLine = LMOutputFile.tell()
                self.LMOutput['rawData'].append(float(tempStr))
                tempStr = self.readlineTrap(LMOutputFile)

            LMOutputFile.seek(prevLine)

        if self.outputFormat == 1:

            tempStr = self.readlineTrap(LMOutputFile)
            tempWords = tempStr.split('\t')
            self.LMOutput['TotalSum'] = float(tempWords[2])
            self.LMOutput['CompartmentsConsidered'] = float(tempWords[3])
            self.LMOutput['CompartmentsDiscarded'] = float(tempWords[4])
            self.LMOutput['Minimum'] = float(tempWords[5])
            self.LMOutput['Average'] = float(tempWords[6])
            self.LMOutput['Maximum'] = float(tempWords[7])
            self.LMOutput['StdDev'] = float(tempWords[8])

        elif self.outputFormat == 2:

            tempStr = self.readlineTrap(LMOutputFile)
            tempWords = tempStr.split('\t')
            tempWords = tempWords[2:len(tempWords) - 1]
            self.LMOutput['measure1BinCentres'] = [float(x) for x in tempWords]

            tempStr = self.readlineTrap(LMOutputFile)
            tempWords = tempStr.split('\t')
            tempWords = tempWords[2:len(tempWords) - 1]
            self.LMOutput['measure1BinCounts'] = [float(x) for x in tempWords]

        elif self.outputFormat == 3:

            tempStr = self.readlineTrap(LMOutputFile)
            tempWords = tempStr.split('\t')
            tempWords = tempWords[2:len(tempWords) - 1]
            self.LMOutput['measure1BinCentres'] = [float(x) for x in tempWords]

            tempStr = self.readlineTrap(LMOutputFile)
            tempWords = tempStr.split('\t')
            tempWords = tempWords[2:len(tempWords) - 1]
            self.LMOutput['measure2BinAverages'] = [float(x) for x in tempWords]

            tempStr = self.readlineTrap(LMOutputFile)
            tempWords = tempStr.split('\t')
            tempWords = tempWords[1:len(tempWords) - 1]
            self.LMOutput['measure2BinStdDevs'] = [float(x) for x in tempWords]

        LMOutputFile.close()

    #*******************************************************************************************************************

    def getMeasure(self, measure, Filter=False):

        """
        Runs L-measure on the SWC file in the initialized path to calculate the statistics of the measure specified. The fields 'CompartmentsConsidered', 'CompartmentsDiscarded', 'Minimum', 'Maximum', 'Average' and 'StdDev' of the LMOutput dictionary are filled in. The values of the remaining fields of the dictionary are not valid.

        :param measure: A string containing the measure required. Look at the different functions available in L-measure in 'help/index.html'. Examples: 'Diameter', 'N_tips'
        :param Filter: Not implemented
        :return:
        """
        self.line1 = '-f' + str(self.functionRef.index(measure)) + ',' + '0,0,10'

        self.line2 = '-s' + self.LMOutputFName

        self.writeLMIn(self.line1, self.line2, self.line3)

        self.runLM()

        self.outputFormat = 1
        self.readOutput()

        return self.LMOutput

    #*******************************************************************************************************************

    def getMeasureDistribution(self, measure, nBins=10, Filter=False):
        """
        Runs L-measure on the SWC file in the initialized path to calculate the distribution of the measure specified. The fields 'measure1BinCentres' and 'measure1BinCounts' of the LMOutput dictionary are filled in. The values of the remaining fields of the dictionary are not valid.

        :param measure:A string containing the measure required. Look at the different functions available in L-measure in 'help/index.html'. Examples: 'Diameter', 'N_tips'
        :param nBins: number of bins for the distribution
        :param Filter: Not implemented
        :return:
        """

        self.line1 = '-f' + str(self.functionRef.index(measure)) + ',' \
                     + 'f' + str(self.functionRef.index(measure)) + ',' + '0,0,' + str(nBins)

        self.line2 = '-s' + self.LMOutputFName

        self.writeLMIn(self.line1, self.line2, self.line3)

        self.runLM()

        self.outputFormat = 2
        self.readOutput()

        return self.LMOutput

    #*******************************************************************************************************************

    #*******************************************************************************************************************

    def getMeasureDependence(self, measure1, measure2, nBins=10, Filter=False):
        """
        Runs L-measure on the SWC file in the initialized path to calculate the averages and standard deviations of measure2 for different bins along the values of measure1.
        The fields 'measure1BinCentres', 'measure2BinAverages' and 'measure2BinStdDevs' of the LMOutput dictionary are filled in. The values of the remaining fields of the dictionary are not valid.

        :param measure1: A string containing the measure1 required. Look at the different functions available in L-measure in 'help/index.html'. Examples: 'Diameter', 'N_tips'
        :param measure2: A string containing the measure2 required. Look at the different functions available in L-measure in 'help/index.html'. Examples: 'Diameter', 'N_tips'
        :param nBins: number of bins for the distribution of measure1
        :param Filter: Not Implemented
        :return:
        """

        self.line1 = '-f' + str(self.functionRef.index(measure1)) + ',' \
                     + 'f' + str(self.functionRef.index(measure2)) + ',' + '1,0,' + str(nBins)

        self.line2 = '-s' + self.LMOutputFName

        self.writeLMIn(self.line1, self.line2, self.line3)

        self.runLM()

        self.outputFormat = 3
        self.readOutput()

        return self.LMOutput

    #*******************************************************************************************************************
#***********************************************************************************************************************