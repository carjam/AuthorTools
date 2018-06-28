import math
from bitarray import bitarray
from decimal import Decimal

# doesn't work for size 1
class BloomFilter(object):
        def getTrueBits(self):
            return self.trueBits

        def setTrueBits(self, trueBits):
            self.trueBits = trueBits

        def getBits(self):
            return self.bits

        def setBits(self, bits):
            self.bits = bits

        def getCount(self):
            return self.count

        def setCount(self, count):
            self.count = count

        def getArraySize(self):
            return self.arraySize

        def setArraySize(self, arraySize):
            self.arraySize = arraySize

        def getHashFunctionCount(self):
            return self.hashFunctionCount

        def setHashFunctionCount(self, count):
            self.hashFunctionCount = count

        def getSecondaryHashFunction(self):
            return self.secondaryHashFunction

        def setSecondaryHashFunction(self, secondaryHashFunction):
            self.secondaryHashFunction = secondaryHashFunction

        # <summary>
        # Initializes new filter with optimal parameters and populates it with given collection.
        # </summary>
        def __init__(self, items):
            self.count = 0
            self.trueBits = 0

            capacity = len(items)
            error = self.getOptimalError(capacity)
            arraySize = self.getOptimalArraySize(capacity, error)
            hashFunctionCount = self.getOptimalHashFunctions(capacity, error)

            self.arraySize = arraySize
            self.bits = bitarray(arraySize)
            self.bits.setall(0)

            self.hashFunctionCount = hashFunctionCount
            self.secondaryHashFunction = self.recommendedUInt32HashFunction #hashFunction

            self.addRange(items)

        @classmethod
        def getOptimalError(cls, capacity):
            # Starobinski, David; Trachtenberg, Ari; Agarwal, Sachin (2003), "Efficient PDA Synchronization", IEEE Transactions on Mobile Computing 2 (1): 40, doi:10.1109/TMC.2003.1195150
            return Decimal(1.0) / Decimal(capacity)

        @classmethod
        def getOptimalArraySize(cls, capacity, error):
            # Starobinski, David; Trachtenberg, Ari; Agarwal, Sachin (2003), "Efficient PDA Synchronization", IEEE Transactions on Mobile Computing 2 (1): 40, doi:10.1109/TMC.2003.1195150
            return int( math.ceil(capacity * math.log(error, (1.0 / math.pow(2, math.log(2.0))))) )

        @classmethod
        def getOptimalHashFunctions(cls, capacity, error):
            # Starobinski, David; Trachtenberg, Ari; Agarwal, Sachin (2003), "Efficient PDA Synchronization", IEEE Transactions on Mobile Computing 2 (1): 40, doi:10.1109/TMC.2003.1195150
            return int( round(math.log(2.0) * cls.getOptimalArraySize(capacity, error) / capacity) )

        def computeDoubleHash(self, primary, secondary, offset):
            # Dillinger-Manolios Formula
            compoundHash = (primary + offset * secondary) % self.arraySize
            return int( math.fabs(compoundHash) )

        # <summary>
        # Computes current probability of false positives.
        # </summary>
        # <returns>Zero means no false positives at all, one means false positives all the time.</returns>
        def getError(self):
            # Mitzenmacher, Michael; Upfal, Eli (2005), Probability and computing: Randomized algorithms and probabilistic analysis, Cambridge University Press, pp. 107–112, ISBN 9780521835404
            return math.pow(1.0 - math.pow(1.0 - 1.0 / Decimal(self.arraySize), Decimal(self.hashFunctionCount) * Decimal(self.count)), Decimal(self.hashFunctionCount))

        @classmethod
        def recommendedUInt32HashFunction(cls, x):
            # Integer hash function from http:#www.concentric.net/~Ttwang/tech/inthash.htm
            x = int(x)
            x = ~x + (x << 15) # x = (x << 15) - x- 1, as (~x) + y is equivalent to y - x - 1 in two's complement representation
            x = x ^ (x >> 12)
            x = x + (x << 2)
            x = x ^ (x >> 4)
            x = x * 2057 # x = (x + (x << 3)) + (x<< 11);
            x = x ^ (x >> 16)
            return int(x)

        # <summary>
        # Adds the item into the filter.
        # </summary>
        def add(self, item):
            ++self.count

            primary = hash(item)
            secondary = self.secondaryHashFunction(item)

            for i in range(self.hashFunctionCount):
                compoundHash = self.computeDoubleHash(primary, secondary, i)

                if (not self.bits[compoundHash]):
                    ++self.trueBits

                self.bits[compoundHash] = True

        # <summary>
        # Convenience method to add many items at once.
        # </summary>
        def addRange(self, items):
            for item in items:
                self.add(item)

        # <summary>
        # Checks whether the item is contained in the filter.
        # </summary>
        # <returns>False if the item is definitely not in the filter. True if the item might be in the filter.</returns>
        def contains(self, item):
            primary = hash(item)
            secondary = self.secondaryHashFunction(item)

            for i in range(self.hashFunctionCount):
                compoundHash = self.computeDoubleHash(primary, secondary, i)

                if (not self.bits[compoundHash]):
                    return False
            
            return True;

        # <summary>
        # The 'truthiness' of the filter.
        # </summary>
        # <returns>Ratio of bits with value 1 to the number of bits in the filter.</returns>
        def getRatio(self):
            return Decimal(self.trueBits) / Decimal(self.arraySize)
