from utils import Utilities

class OutputWriter:
    def __init__(self, in_FilePath):
        self.FilePath = in_FilePath

        # RunData must be a list of lists. Each sublist contains [ RunNumber, GenerationNumber, MinFitness, MaxFitness, AvgFitness, StdevFitness ]
        self.RunData = []

        # State is defined as follows:
        #    NW : Not Writing - Have not started writing the file or have finished writing the file.
        #    HW : Header Written - Have wirtten the header part of the file.
        #    DW : Data Written - Have written some RunData to the file and ready to write more RunData.
        #    DF : Data Finished - Finished writing data and ready to write summary section.
        #    
        self.State = 'NW'

    def Initialize(self, in_ExpDataStr):
        if self.State != 'NW':
            print('Warning: called Init at state {}'.format(self.State))
        with open(self.FilePath, 'w') as f:
            f.write('{\n"ExperimentData":' + in_ExpDataStr + ',\n"RunData":{\n\t"Columns":["RunNumber","GenerationNumber","MinFitness","MaxFitness","AvgFitness","StdevFitness"],\n\t"Data":[\n')
        self.State = 'HW'

    def CollectData(self, in_RunNo, in_CurrentGeneration, in_GenMin, in_GenMax, in_GenMean, in_GenStdev):
        if self.State != 'HW' and self.State != 'DW':
            print('Warning: called CollectData at state {}'.format(self.State))
        self.RunData.append( (in_RunNo, in_CurrentGeneration, in_GenMin, in_GenMax, in_GenMean, in_GenStdev) )
        if 100 < len(self.RunData):
            self.__writeRunData()

    def WriteSummary(self, in_OverallMinMaxCalculator):
        if self.State != 'DW':
            print('Warning: called WriteSummary at state {}'.format(self.State))
        self.__writeRunData(True)
        minChromObj = in_OverallMinMaxCalculator.GetMinObject()
        maxChromObj = in_OverallMinMaxCalculator.GetMaxObject()
        with open(self.FilePath,'a') as f:
            f.write('\t\t]\n\t}},\n"Summary":{{\n\t"OverallMinFitness":{},\n\t"OverallMaxChromosome":{},\n\t"OverallMaxFitness":{},\n\t"OverallMinChromosome":{}\n\t}}\n}}\n'.format(minChromObj.GetRawFitness(),minChromObj.GetChromosome(),maxChromObj.GetRawFitness(),maxChromObj.GetChromosome()))
        self.State = 'NW'

    def __writeRunData(self, in_Finish = False):
        with open(self.FilePath,'a') as f:
            hasData = 0 < len(self.RunData)
            if hasData and 'DW' == self.State :
                print('newline')
                f.write(',\n')
            if hasData:
                for data in self.RunData[:-1]:
                    f.write('\t\t\t[{},{},{},{},{},{}],\n'.format(data[0],data[1],data[2],data[3],data[4],data[5]))
                data = self.RunData[-1]
                f.write('\t\t\t[{},{},{},{},{},{}]'.format(data[0],data[1],data[2],data[3],data[4],data[5]))
                self.State = 'DW'
            if in_Finish:
                f.write('\n')
                self.State = 'DF'
        self.RunData = []

    
