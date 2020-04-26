
from random_number_generator import RandomNumberGenerator as RNG
from genotype_model import GenotypeModel
from genetic_algorithm import GeneticAlgorithm
import copy


# ------------------Test----------------------------

class BitStringChromosomeObject(GenotypeModel.ChromosomeObject):
    def __init__(self, in_Chromosome, in_RawFitness):
        super().__init__(in_Chromosome)
        self.RawFitness = in_RawFitness

    def GetRawFitness(self):
        return self.RawFitness

    def DeepCopy(self):
        return BitStringChromosomeObject(copy.deepcopy(self.TheChromosome), self.RawFitness)

class BitStringChromosomeObjectCreator(GenotypeModel.ChromosomeObjectCreatorStrategy):
    def __init__(self, in_Length):
        self.Length = in_Length

    def CreateRandom(self, in_FitnessFunctionStrategy):
        chrom = [ RNG.GetRandomIntValue(0, 2) for i in range(self.Length) ]
        return BitStringChromosomeObject(chrom, in_FitnessFunctionStrategy.Calculate(chrom))

    def Create(self, in_Chromosome, in_RawFitness):
        return BitStringChromosomeObject(in_Chromosome, in_RawFitness)

class OneMaxFitness(GenotypeModel.FitnessFunctionStrategy):
    def Calculate(self, in_Chromosome):
        return in_Chromosome.count(1)

class FlipMutation(GenotypeModel.SingleParentOperatorStrategy):
    def __init__(self, in_MutationProbability):
        self.MutProb = in_MutationProbability

    def Apply(self, in_Chromosome):
        return [ (1 - v) if RNG.GetRandomProbabilityValue() < self.MutProb else v for v in in_Chromosome ]

class OnePointCrossover(GenotypeModel.DualParentOperatorStrategy):
    def Apply(self, in_Chromosome1, in_Chromosome2):
        r = RNG.GetRandomIntValue(1, len(in_Chromosome1) ) # 1 <= r <= (n - 1) , n = len(Chromosome)
        childChromosome1 = in_Chromosome1[:r] + in_Chromosome2[r:]
        childChromosome2 = in_Chromosome2[:r] + in_Chromosome1[r:]
        return childChromosome1, childChromosome2

class TournamentOfTwoSelection(GeneticAlgorithm.SelectionStrategy):
    def __init__(self, in_GA, in_TournamentProbability):
        super().__init__(in_GA)
        self.TournamentProbability = in_TournamentProbability

    def SelectChromosomeObject(self):
        parentObject1 = self.TheGA.SelectRandomChromosomeObject()
        parentObject2 = self.TheGA.SelectRandomChromosomeObject()
        if RNG.GetRandomProbabilityValue() < self.TournamentProbability:
            if parentObject1.GetRawFitness() < parentObject2.GetRawFitness():
                return parentObject2
            else:
                return parentObject1
        else:
            if parentObject1.GetRawFitness() < parentObject2.GetRawFitness():
                return parentObject1
            else:
                return parentObject2

def main():
    print("hello world!")
    chromCreator = BitStringChromosomeObjectCreator(200)
    omf = OneMaxFitness()
    fmutOp = FlipMutation(0.001)
    opxover = OnePointCrossover()
    s = GenotypeModel(chromCreator, omf, fmutOp, opxover)
    p = {'NumRuns':5,'PopSize':50,'NumGenerations':180,'XoverProb':0.8,'OutputFile':'TestGAOutput.json'}
    ga = GeneticAlgorithm(s,p)
    ss = TournamentOfTwoSelection(ga, 1.0)
    ga.SetSelectionStrategy(ss)
    ga.Run()

if __name__ == "__main__":
    main()