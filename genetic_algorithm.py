from random_number_generator import RandomNumberGenerator as RNG
from output_writer import OutputWriter
from utils import Utilities
import json

class GeneticAlgorithm:
    class SelectionStrategy:
        def __init__(self, in_GA):
            self.TheGA = in_GA

        def SelectChromosomeObject(self):
            raise NotImplementedError
            return None

    class Parameters:
        def __init__(self, in_ParameterDict):
            self.FromDict(in_ParameterDict)

        def ToDict(self):
            return {'NumRuns':self.NumberOfRuns,'NumGenerations':self.NumGenerations,'PopSize':self.PopSize,\
                    'ChildrenPerGeneration':self.ChildrenPerGeneration,'XoverProb':self.CrossoverProbability,'OutputFile':self.OutputFile}

        def FromDict(self,in_ParameterDict):
            self.NumberOfRuns = in_ParameterDict['NumRuns']
            self.NumGenerations = in_ParameterDict['NumGenerations']
            self.PopSize = in_ParameterDict['PopSize']
            self.ChildrenPerGeneration = in_ParameterDict['ChildrenPerGeneration'] if 'ChildrenPerGeneration' in in_ParameterDict.keys() else in_ParameterDict['PopSize']
            self.CrossoverProbability = in_ParameterDict['XoverProb']
            self.OutputFile = in_ParameterDict['OutputFile']

    def __init__(self, in_GenotypeModel, in_ParameterDict):
        self.TheGenotypeModel = in_GenotypeModel
        self.Parameters = GeneticAlgorithm.Parameters(in_ParameterDict)
        self.TheSelectionStrategy = None
        self.TheOutputWriter = OutputWriter(self.Parameters.OutputFile)
        self.Population = [] # population doesn't really belong here, should be moved to a run class? --> move to a data class instance

    def SelectRandomChromosomeObject(self):
        return self.Population[RNG.GetRandomIntValue(0,self.Parameters.PopSize)]

    def SetSelectionStrategy(self, in_SelectionStrategy):
        self.TheSelectionStrategy = in_SelectionStrategy

    def Run(self):
        # Initialization
        self.Population = [ self.TheGenotypeModel.CreateRandomizedChromosomeObject() for i in range(self.Parameters.PopSize) ]
        ExperimentData = {'GAParameters':self.Parameters.ToDict(),'Runs':[]}

        #self.OutputProcessor.Record(0, self.Population)
        self.TheOutputWriter.Initialize(json.dumps(self.Parameters.ToDict()))
        #RunData = []
        allRunsStats = Utilities.MinMaxCalculator()
        allRunsStats.AddRecordsBatch(lambda x: x.GetRawFitness(), self.Population)

        # Main Loop of Generations
        for runNo in range(self.Parameters.NumberOfRuns):
            generationStats = Utilities.StatCalculator()
            for currentGeneration in range(self.Parameters.NumGenerations):
                newPopulation = []
                generationStats.Reset()
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

                    # record stats of these children for this generation
                    generationStats.AddRecord(childObject1.GetRawFitness(), childObject1)
                    generationStats.AddRecord(childObject2.GetRawFitness(), childObject2)
                    allRunsStats.AddRecord(childObject1.GetRawFitness(), childObject1)
                    allRunsStats.AddRecord(childObject2.GetRawFitness(), childObject2)
                    # end for each children loop

                # generate summary for this generation
                _, genMin, _, genMax, _, genMean, genStdev = generationStats.GetStats()
                #RunData.append( (runNo, currentGeneration, genMin, genMax, genMean, genStdev) )
                self.TheOutputWriter.CollectData(runNo, currentGeneration, genMin, genMax, genMean, genStdev)
                self.Population = newPopulation
            # end of generations loop
        # end of runs loop
        self.TheOutputWriter.WriteSummary(allRunsStats)
        minChromObj = allRunsStats.GetMinObject()
        maxChromObj = allRunsStats.GetMaxObject()
        print('Min Fitness: ' + str(minChromObj.GetRawFitness()))
        print(minChromObj.GetChromosome())
        print('Max Fitness: ' + str(maxChromObj.GetRawFitness()))
        print(maxChromObj.GetChromosome())
