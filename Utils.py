import math
import random
import errno, sys
import struct
class UArray:
    @staticmethod
    def ToDoubleArray(point, sourceIndex = 0, length = -1):
        if length == -1:
            result = [None] * len(point)
            for i in range(len(point)):
                result[i] = float(point[i])
            return result
        else:
            result = [None] * length
            for i in range(length):
                result[i] = float(point[i + sourceIndex])
            return result

    @staticmethod
    def ToFloatArray(point):
        result = [None] * len(point)
        for i in range(len(point)):
            result[i] = float(point[i])
        return result


    """
    // NB: Python and our script treat 'float' arrays as C  # doubles!
    // Hence 8 byte offets!
    """

    @staticmethod
    def ToDoubleArrayFromDoubleBytes(point):
        result = [None] * (len(point) / 8)

        for i in range(0, len(point), 8):
            result[n / 8] = (double)BitConverter.ToDouble(point, n);


        return result

    @staticmethod
    def ToDoubleArrayFromInt8Bytes(point):
        return UArray.ToDoubleArray(point)

    @staticmethod
    def ToByteArray(point):
        bytes = [None] * len(point)
        for i in range(len(point)):
            if point > 255:
                bytes[i] = 255
            elif point < 0:
                bytes[i] = 0
            else:
                bytes[i] = int(round(point))
        return bytes

    @staticmethod
    def ToIntArray(array):
        intArray = [None] * len(array)
        for i in range(len(array)):
            intArray[i] = int(array[i])
        return intArray

    """
    // / < summary >
    // / output[i] = input[i] * scale + offset
    // / < / summary >
    // / < param name = "array" > < / param >
    // / < param name = "scale" > < / param >
    // / < param name = "offset" > < / param >
    // / < returns > < / returns >
    """

    @staticmethod
    def ToRGBArray(array, scale, offset):
        result = [None] * len(array)
        for i in range(len(array)):
            result[i] = int(UMath.Clamp(array[i] * scale + offset, 0.0, 255.0))
        return result

    @staticmethod
    def InPlaceRoundDoubleArray(array):
        for i in range(len(array)):
            array[i] = int(round(array[i]))

    @staticmethod
    def ComputeRoundIdenticals(oldarr, newarr):
        samcount = 0
        for i in range(len(oldarr)):
            if int(round(oldarr[i])) == int(round(newarr[i])):
                samcount += 1
        return samcount



class UMath:

    """
    // / < summary >
    // / In - place
    soft
    max
    // / < / summary >
    // / < param
    name = "input" > < / param >"""

    @staticmethod
    def SoftMax(input):
        max = input[0]
        min = input[0]
        for i in range(0, len(input)):
            if input[i] > max:
                max = input[i]
        k = max - 4

        for i in range(0, len(input)):
            input[i] = math.exp(input[i] - k)
        sum = 0
        for i in range(0, len(input)):
            sum += input[i]
        for i in range(0, len(input)):
            input[i] /= sum

    """"
    // / < summary >
    // / Rounds a double and ensures it was an integer
    // / < / summary >
    // / < param name="value" > The double to be converted < / param >
    // / < returns > The integer represented by the double < / returns >
    """

    @staticmethod
    def EnsureInt(value):
        intValue = round(value)
        if value != intValue:
            raise FloatingPointError ("Invalid integer: " + `value`)
        return intValue

    """
    // / < summary >
    // / Converts
    an
    entire
    array
    to
    integers, ensuring
    their
    format
    // / < / summary >
    """

    @staticmethod
    def EnsureIntArray(array):
        integerArray = [None] * len(array)
        for i in range(0, len(array)):
            integerArray[i] = UMath.EnsureInt(array[i])
        return integerArray

    @staticmethod
    def Max(output):
        max = output[0]
        maxIndex = 0
        for i in range(0, len(output)):
            if output[i] > max:
                max = output[i]
                maxIndex = i
        return (max, maxIndex)

    @staticmethod
    def MaxExcluding(idx, output):
        max = output[1] if idx == 0 else output[0]
        maxIndex = 1 if idx == 0 else 0
        for i in range(maxIndex + 1, len(output)):
            if i == idx:
                continue
            if output[i] > max:
                max = output[i]
                maxIndex = i
        return (max, maxIndex)

    @staticmethod
    def Clamp(value, min, max):
        if value < min:
            return min
        elif value > max:
            return max
        else:
            return value

    @staticmethod
    def ClampArray(values, min, max):
        newValues = [None] * len(values)
        for i in range(0, len(values)):
            newValues[i] = UMath.Clamp(values[i], min, max)
        return newValues

    """
    // / < summary >
    // / Calculates
    the
    LInfinity
    distance
    between
    two
    points in Rn
              // / < / summary >
                """

    @staticmethod
    def LInfinityDistance(point1, point2):
        if len(point1) != len(point2):
            raise Exception("Invalid inputs!")
        max = abs(point1[0] - point2[0])
        for i in range(1, len(point1)):
            cur = abs(point1[i] - point2[i])
            if cur > max:
                max = cur
        return max

    @staticmethod
    def L1Distance(point1, point2):
        if len(point1) != len(point2):
            raise Exception("Invalid inputs!")

        curr = abs(point1[0] - point2[0])
        for i in range(1, len(point1)):
            curr += abs(point1[i] - point2[i])
        return curr / float(len(point1))



"""
// / < summary >
// / Various
functions
that
utilize
randomness
// / < / summary >
"""
class URand:
    """
    // / < summary >
    // / Returns
    a
    double
    drawn
    from a Gaussian
    distribution(0, 1)
    // / < / summary >
    """

    @staticmethod
    def NextGaussian1(randoml):
        u1 = randoml.random()
        u2 = randoml.random()
        return math.sqrt(-2.0 * math.log(u1)) * math.sin(2.0 * math.pi * u2)

    @staticmethod
    def NextRandomImage(randoml, size):
        result = [None] * size
        for i in range(size):
            result[i] = math.round(255.0 * randoml.random())
        return result

    """
    // / < summary >
    // / Draw a double from a Gaussian distribution weith a specific mean and deviation
    // / < / summary >
    // / < returns > < / returns >
    """

    @staticmethod
    def NextGaussian(mean, sd, randoml):
        return sd * URand.NextGaussian1(randoml) + mean

    """
    // / < summary >
    // / Standard Fisher - Yates random permutation
    // / < / summary >
    // / < param name = "random" > < / param >
    // / < param name = "length" > < / param >
    // / < returns > < / returns >
    // /
    """

    @staticmethod
    def NextPermutation(randoml, length):
        list = [None] * length
        for i in range(length):
            list[i] = i
        n = length
        for i in range(length - 1, 0, -1):
            """swap randomly with element in (i, length]"""
            k = randoml.randrange(i, length)
            bucket = list[k]
            list[k] = list[i]
            list[i] = bucket
        return list

    @staticmethod
    def GetNoisyPoint(point, addedNoiseSD, randoml):
        newPoint = [None] * len(point)
        addedNoise = URand.NextGaussian(0.0, addedNoiseSD, randoml)
        for j in range(len(point)):
            newPoint[j] = math.min(255.0, math.max(0.0, point[j] + addedNoise))
        return newPoint

"""
class Cmd:
    def RunOptionSet(self, opt, args):
        show_help = False

        var
        p = opt.Add("help", "Show this message and exit", x= > show_help = x != null);

        List < string > extra;

    try
        {
            extra = p.Parse(args);
        }
        catch(OptionException
        e)
        {
            Console.WriteLine(e.Message);
        print "Try `--help' for more information."
        sys.exit()
        }

        if show_help:
            {
            print "Options:"
            p.WriteOptionDescriptions(Console.Out);
            sys.exit()
"""