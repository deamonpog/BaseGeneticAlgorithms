class OutputProcessor:
    def __init__(self, in_OutputFileName):
        self.BestChromosome = None
        self.Records = []
        with open(in_OutputFileName, 'w') as file:
            file.write('GenNo,AvgRawFitness\n')

    def Record(self, in_GenerationNo, in_Population):
        if 0 < len(in_Population):
            bestObj = in_Population[0]
            avgRawFitness = in_Population[0].GetRawFitness()
            for chromObj in in_Population[1:]:
                if bestObj.GetRawFitness() < chromObj.GetRawFitness():
                    bestObj = chromObj
                avgRawFitness = avgRawFitness + chromObj.GetRawFitness()
            self.Records.append([ in_GenerationNo, avgRawFitness / len(in_Population)])
            with open('GAOutput.txt', 'a') as file:
                file.write('{},{}\n'.format(in_GenerationNo, avgRawFitness / len(in_Population)))

    def AppendStringToFile(self, in_String):
        with open('GAOutput.txt', 'a') as file:
            file.write(in_String)
