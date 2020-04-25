class GenotypeModel:
    class SingleParentOperatorStrategy:
        def Apply(self, in_Chromosome):
            raise NotImplementedError
            return None

    class DualParentOperatorStrategy:
        def Apply(self, in_Chromosome1, in_Chromosome2):
            raise NotImplementedError
            return None

    class ChromosomeObjectCreatorStrategy:
        def CreateRandom(self, in_FitnessFunctionStrategy):
            raise NotImplementedError
            return None

        def Create(self, in_Chromosome, in_RawFitness):
            raise NotImplementedError
            return None

    class FitnessFunctionStrategy:
        def Calculate(self, in_Chromosome):
            raise NotImplementedError
            return None

    class ChromosomeObject:
        def __init__(self, in_Chromosome):
            self.TheChromosome = in_Chromosome

        def GetChromosome(self):
            return self.TheChromosome

        def GetRawFitness(self):
            raise NotImplementedError
            return None

        def DeepCopy(self):
            raise NotImplementedError
            return None
            
    def __init__(self, in_ChromosomeObjectCreator, in_FitnessFunction, in_MutationOperator, in_CrossoverOperator):
        self.TheChromosomeObjectCreatorStrategy = in_ChromosomeObjectCreator
        self.TheFitnessFunctionStrategy = in_FitnessFunction
        self.TheMutationOperatorStrategy = in_MutationOperator
        self.TheCrossoverOperatorStrategy = in_CrossoverOperator

    # Generates a new chromosome using the generator.
    def CreateRandomizedChromosomeObject(self):
        return self.TheChromosomeObjectCreatorStrategy.CreateRandom(self.TheFitnessFunctionStrategy)

    # Calculates the raw fitness value and returns it.
    def CalculateFitness(self, in_ChromosomeObject):
        return self.TheFitnessFunctionStrategy.Calculate(in_ChromosomeObject.GetChromosome())

    def ApplyMutationOperator(self, in_ChromosomeObject):
        chrom = self.TheMutationOperatorStrategy.Apply(in_ChromosomeObject.GetChromosome())
        return self.TheChromosomeObjectCreatorStrategy.Create( chrom , self.TheFitnessFunctionStrategy.Calculate(chrom) )

    def ApplyCrossoverOperator(self, in_ChromosomeObject1, in_ChromosomeObject2):
        chrom1, chrom2 = self.TheCrossoverOperatorStrategy.Apply(in_ChromosomeObject1.GetChromosome(), in_ChromosomeObject2.GetChromosome())
        return self.TheChromosomeObjectCreatorStrategy.Create(chrom1, self.TheFitnessFunctionStrategy.Calculate(chrom1)) , self.TheChromosomeObjectCreatorStrategy.Create(chrom2, self.TheFitnessFunctionStrategy.Calculate(chrom2))
