import math

class Utilities:
    class NoSamplesGatheredError(Exception):
        """Raised when the number of collected samples are zero"""
        pass

    @staticmethod
    def ComputeStats(in_Values):
        n = len(in_Values)
        vMin = float('inf')
        vMinIdx = 0
        vMax = float('-inf')
        vMaxIdx = 0
        vSum = 0
        vSumOfSquares = 0
        for i in range(len(in_Values)):
            v = in_Values[i]
            if v < vMin:
                vMin = v
                minidx = i
            if vMax < v:
                vMax = v
                maxidx = i
            vSum += v
            vSumOfSquares += (v * v)
        vmean = (vSum / n)
        vvar = (vSumOfSquares / n) - (vmean * vmean)
        vstdev = math.sqrt(vvar)
        return vMin, vMinIdx, vMax, vMaxIdx, vmean, vstdev

    class StatCalculator:
        def __init__(self):
            self.Reset()

        def Reset(self):
            self.Min = float('inf')
            self.MinObject = None
            self.Max = float('-inf')
            self.MaxObject = None
            self.Sum = 0
            self.SumOfSquares = 0
            self.NumOfSamples = 0

        def AddRecordsBatch(self, in_ValueFunction, in_EnumerableObjects):
            for obj in in_EnumerableObjects:
                self.AddRecord(in_ValueFunction(obj), obj)

        def AddRecord(self, in_Value, in_Object):
            self.Sum += in_Value
            self.SumOfSquares += (in_Value * in_Value) 
            self.NumOfSamples += 1
            if in_Value < self.Min:
                self.Min = in_Value
                self.MinObject = in_Object
            if self.Max < in_Value:
                self.Max = in_Value
                self.MaxObject = in_Object

        def GetStats(self):
            if self.NumOfSamples <= 0:
                raise NoSamplesGatheredError
            mean = self.Sum / self.NumOfSamples
            var = (self.SumOfSquares / self.NumOfSamples) - (mean * mean)
            stdev = math.sqrt(var)
            return self.NumOfSamples, self.Min, self.MinObject, self.Max, self.MaxObject, mean, stdev

        def GetMinObject(self):
            return self.MinObject

        def GetMaxObject(self):
            return self.MaxObject

