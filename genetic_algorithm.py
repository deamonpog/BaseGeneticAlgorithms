from random_number_generator import RandomNumberGenerator as RNG
from output_processor import OutputProcessor

class GeneticAlgorithm:
    class SelectionStrategy:
        def __init__(self, in_GA):
            self.TheGA = in_GA

        def SelectChromosomeObject(self):
            raise NotImplementedError
            return None

    class Parameters:
        def __init__(self, in_ParameterDict):
            self.FromParamDict(in_ParameterDict)

        def ToParamDict(self):
            return {'NumRuns':self.NumberOfRuns,'NumGenerations':self.NumGenerations,'PopSize':self.PopSize,\
                    'ChildrenPerGeneration':self.ChildrenPerGeneration,'XoverProb':self.CrossoverProbability,'OutputFile':self.OutputFile}

        def FromParamDict(self,in_ParameterDict):
            self.NumberOfRuns = in_ParameterDict['NumRuns']
            self.NumGenerations = in_ParameterDict['NumGenerations']
            self.PopSize = in_ParameterDict['PopSize']
            self.ChildrenPerGeneration = in_ParameterDict['ChildrenPerGeneration'] if 'ChildrenPerGeneration' in in_ParameterDict.keys() else in_ParameterDict['PopSize']
            self.CrossoverProbability = in_ParameterDict['XoverProb']
            self.OutputFile = in_ParameterDict['OutputFile']

    def ComputeMaxMinMeanStdev(in_Population):
        for 


    def __init__(self, in_GenotypeModel, in_ParameterDict):
        self.TheGenotypeModel = in_GenotypeModel
        self.Parameters = GeneticAlgorithm.Parameters(in_ParameterDict)
        self.TheSelectionStrategy = None
        self.OutputProcessor = OutputProcessor(self.Parameters.OutputFile)
        self.Population = [] # population doesn't really belong here, should be moved to a run class? --> move to a data class instance

    def SelectRandomChromosomeObject(self):
        return self.Population[RNG.GetRandomIntValue(0,self.Parameters.PopSize)]

    def SetSelectionStrategy(self, in_SelectionStrategy):
        self.TheSelectionStrategy = in_SelectionStrategy

    def Run(self):
        # Initialization
        self.Population = [ self.TheGenotypeModel.CreateRandomizedChromosomeObject() for i in range(self.Parameters.PopSize) ]
        ExperimentData = {'GAParameters':self.Parameters.ToParamDict(),'Runs':[]}

        self.OutputProcessor.Record(0, self.Population)
        bestFitness = None
        avgFitness = None
        stdevFitness = None
        bestChromosome = []

        # Main Loop of Generations
        for runNo in range(self.Parameters.NumberOfRuns):
            RunData = []
            for currentGeneration in range(self.Parameters.NumGenerations):
                newPopulation = []
                for pairs in range(self.Parameters.ChildrenPerGeneration // 2):
                    # Selection of Parents
                    parentObject1 = self.TheSelectionStrategy.SelectChromosomeObject()
                    parentObject2 = self.TheSelectionStrategy.SelectChromosomeObject()
                    while parentObject1 == parentObject2:
                        parentObject2 = self.TheSelectionStrategy.SelectChromosomeObject()

                    childObject1 = parentObject1.DeepCopy()
                    childObject2 = parentObject2.DeepCopy()

                    # Crossover
                    if RNG.GetRandomProbabilityValue() < self.Parameters.CrossoverProbability:
                        childObject1, childObject2 = self.TheGenotypeModel.ApplyCrossoverOperator(childObject1,childObject2)

                    # Mutation
                    childObject1 = self.TheGenotypeModel.ApplyMutationOperator(childObject1)
                    childObject2 = self.TheGenotypeModel.ApplyMutationOperator(childObject2)

                    # Add to next generation
                    newPopulation.append(childObject1)
                    newPopulation.append(childObject2)

                    if bestFitness < childObject1.GetRawFitness():
                        bestFitness = childObject1.GetRawFitness()
                        bestChromosome = childObject1.DeepCopy()
                    if bestFitness < childObject2.GetRawFitness():
                        bestFitness = childObject2.GetRawFitness()
                        bestChromosome = childObject1.DeepCopy()
                self.Population = newPopulation
            # end of generations loop
        # end of runs loop
        print(bestFitness)
        print(bestChromosome.GetChromosome())
