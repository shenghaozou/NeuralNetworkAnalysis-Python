import tempfile, os
import numpy as np
import cv2

<<<<<<< HEAD
class UArray(object):
=======
	def ToDoubleArray(point):
		result = Array.CreateInstance(Double, point.Length)
		i = 0
		while i < point.Length:
			result[i] = point[i]
			i += 1
		return result

	ToDoubleArray = staticmethod(ToDoubleArray)

	# NB: Python and our script treat 'float' arrays as C# doubles!
	# Hence 8 byte offets!
	def ToDoubleArray(point):
		result = Array.CreateInstance(Double, point.Length / 8)
		n = 0
		while n < point.Length:
			result[n / 8] = BitConverter.ToDouble(point, n)
			n += 8
		return result

	ToDoubleArrayFromDoubleBytes = staticmethod(ToDoubleArrayFromDoubleBytes)

	def ToDoubleArray(point):
		result = Array.CreateInstance(Double, point.Length)
		i = 0
		while i < point.Length:
			result[i] = point[i]
			i += 1
		return result

	ToDoubleArrayFromInt8Bytes = staticmethod(ToDoubleArrayFromInt8Bytes)

	def ToDoubleArray(point, sourceIndex, length):
		result = [None] * length
		i = 0
		while i < length:
			result[i] = point[sourceIndex + i]
			i += 1
		return result

	ToDoubleArray = staticmethod(ToDoubleArray)

	def ToByteArray(point):
		bytes = Array.CreateInstance(Byte, point.Length)
		i = 0
		while i < point.Length:
			bytes[i] = 255 if point[i] > 255f else (0 if point[i] < 0f else M.Round(point[i]))
			i += 1
		return bytes

	ToByteArray = staticmethod(ToByteArray)

	def ToIntArray(array):
		intArray = Array.CreateInstance(int, array.Length)
		i = 0
		while i < array.Length:
			intArray[i] = array[i]
			i += 1
		return intArray

	ToIntArray = staticmethod(ToIntArray)

	def ToRGBArray(array, scale, offset):
		""" <summary>
		 output[i] = input[i]*scale + offset
		 </summary>
		 <param name="array"></param>
		 <param name="scale"></param>
		 <param name="offset"></param>
		 <returns></returns>
		"""
		result = Array.CreateInstance(int, array.Length)
		i = 0
		while i < array.Length:
			result[i] = UMath.Clamp(array[i] * scale + offset, 0.0, 255.0)
			i += 1
		return result
>>>>>>> ce3bbda448a92936f8dccbf2cd8bde79d66d5fb4

    @staticmethod
    def ToDoubleArray(arr, sourceIndex=0, length=None):
        if length is None:
            length = len(arr)
        return np.array(arr, dtype=np.float64)[sourceIndex:sourceIndex+length]

    @staticmethod
    def ToFloatArray(arr):
        return np.array(arr, dtype=np.float32)

    @staticmethod
    def ToByteArray(arr):
        return np.array(arr, dtype=np.uint8)

    @staticmethod
    def ToIntArray(arr):
        return np.array(arr, dtype=np.uint64)

    @staticmethod
    def ToRGBArray(arr, scale, offset):
        arr = np.array(arr)
        return np.array(scale * arr + offset, dtype=np.uint8)

    @staticmethod
    def InPlaceRoundDoubleArray(arr):
    	return np.around(arr)

    @staticmethod
    def ComputeRoundIdenticals(arr1, arr2):
    	a1 = np.around(arr1)
    	a2 = np.around(arr2)
    	return (a1 == a2).sum()

class UMath(object):

	@staticmethod
	def SoftMax(x):
	    """Compute softmax values for each sets of scores in x."""
    	return np.exp(x) / np.sum(np.exp(x), axis=0)
	
	@staticmethod
	def EnsureInt(value):
		""" <summary>
		 Rounds a double and ensures it was an integer
		 </summary>
		 <param name="value">The double to be converted</param>
		 <returns>The integer represented by the double</returns>
		"""
		intValue = np.around(value)
		if value != intValue:
			raise ValueError("Invalid integer: " + value)
		return intValue

	
	@staticmethod
	def EnsureIntArray(arr):
		""" <summary>
		 Converts an entire array to integers, ensuring their format
		 </summary>        
		"""
		a = np.around(a)
		if np.all(np.array(arr) == a):
			return a

	@staticmethod
	def Max(output):
		i = np.argmax(output)
		return output[i], i
	
	@staticmethod
	def MaxExcluding(idx, output):
		tmp = np.ma.array(output, mask=False)
		tmp.mask[idx] = True
		return UMath.Max(tmp)

	@staticmethod
	def Clamp(value, minimum, maximum):
		return np.clip(value, minimum, maximum)

	@staticmethod
	def ClampArray(values, minimum, maximum):
		return np.clip(values, minimum, maximum)

	@staticmethod
	def LInfinityDistance(point1, point2):
		""" <summary>
		 Calculates the LInfinity distance between two points in Rn
		 </summary>
		"""
		p1 = np.array(point1)
		p2 = np.array(point2)
		if p1.shape != p2.shape:
			raise ValueError("Invalid inputs!")
		return np.max(np.abs(p1 - p2))

	@staticmethod
	def L1Distance(point1, point2):
		p1 = np.array(point1)
		p2 = np.array(point2)
		if p1.shape != p2.shape:
			raise ValueError("Invalid inputs!")
		return np.sum(np.abs(p1 - p2))

class URand(object):
	""" <summary>
	 Various functions that utilize randomness
	 </summary>
	"""
	@staticmethod
	def NextGaussian(rand): 
		""" <summary>
		 Returns a double drawn from a Gaussian distribution(0,1)
		 </summary>
		"""
		assert isinstance(rand, random.Random), "Wrong Type!"
		return rand.gauss(0, 1)
		
	@staticmethod
	def NextRandomImage(rand, size):
		assert isinstance(rand, random.Random), "Wrong Type!"
		arr = [rand.randint(0, 255) for i in range]
		return np.array(arr, dtype=np.uint8)

	@staticmethod
	def NextGaussian(mean, sd, rand):
		""" <summary>
		  Draws a double from a Gaussian distribution weith a specific mean and deviation
		 </summary>
		 <returns></returns>
		"""
		return sd * URand.NextGaussian(rand) + mean

	@staticmethod
	def NextPermutation(random, length):
		""" <summary>
		 Standard Fisher-Yates random permutation
		 </summary>
		 <param name="random"></param>
		 <param name="length"></param>
		 <returns></returns>
		 
		"""
		lst = [None] * length
		i = 0
		while i < length:
			lst[i] = i
			i += 1
		n = length
		i = length - 1
		while i > 0:
			# swap randomly with element in (i, length]
			k = rand.randint(i + 1, length)
			bucket = lst[k]
			lst[k] = lst[i]
			lst[i] = bucket
			i -= 1
		return lst

	@staticmethod
	def GetNoisyPoint(point, addedNoiseSD, rand):
		addedNoise = URand.NextGaussian(0.0, addedNoiseSD, rand)
		pt = np.array(point)
		return np.clip(pt + addedNoise, 0.0, 255.0)
		
class UDraw(object):
	""" <summary>
	 Displaying images
	 </summary>
	"""

	#########TODO: CHECK!###########
	@staticmethod
	def DrawGrayscalePixels(pixels, numRows, numCols, isRowOrder):
		image = np.array(pixels, dtype=np.uint8)
		order = 'C' if isRowOrder else 'F'
		image = np.reshape(image, (numRows, numRows), order=order)
		return image

	#########TODO: CHECK!##########
	@staticmethod
	def DrawRGBPixels(pixels, numRows, numCols):
		image = np.array(pixels, dtype=np.uint8)
		order = 'C' if isRowOrder else 'F'
		image = np.reshape(image, (3, numRows, numRows), order=order)
		return image

	@staticmethod
	def DisplayImageAndPause(imagePixels, numRows, numCols, isColor, isRowOrder):
		image = UDraw.DrawRGBPixels(imagePixels, numRows, numCols, isRowOrder) if isColor 
				else UDraw.DrawGrayscalePixels(imagePixels, numRows, numCols, isRowOrder)
		cv2.imshow("Image Visualization", image)
		cv2.waitKey(0)
		cv2.destroyAllWindows()

	@staticmethod
	def Rotate(imagePixels, numRows, numCols, isColor, degrees, isRowOrder):
		image_0 = UDraw.DrawRGBPixels(imagePixels, numRows, numCols, isRowOrder) if isColor
				  else UDraw.DrawGrayscalePixels(imagePixels, numRows, numCols, isRowOrder)
		curr = imutils.rotate_bound(image_0, degrees)
		return UDraw.FromBitmap(curr, numRows, numCols, isColor, isRowOrder)
	
	@staticmethod
	def FromBitmap(m, numRows, numCols, isColor, isRowOrder):
		return m.reshape(m.size)

	@staticmethod
	def LossyJPGAndBack(imagePixels, numRows, numCols, isColor, photoquality, isRowOrder):
		image = UDraw.DrawRGBPixels(imagePixels, numRows, numCols, isRowOrder) if isColor 
				else UDraw.DrawGrayscalePixels(imagePixels, numRows, numCols, isRowOrder)		

		assert 0 <= photoquality <= 50, "0 <= photoquality <= 50; provided: %d"%photoquality
		tmpDir = tempfile.mkdtemp()
		tmpImage = os.path.append(tmpDir, 'tmp.jpg')
		cv2.imwrite( , image,  [int(cv2.IMWRITE_JPEG_QUALITY), photoquality])
		newImage = cv2.imread(tmpImage)
		newImagePixels = UDraw.FromBitmap(newImage, *newImage.shape, isColor, isRowOrder)
		return newImagePixels

class Cmd(object):
	def RunOptionSet(opt, args):
		show_help = False
		p = opt.append("help", "Show this message and exit", )
		try:
			extra = p.Parse(args)
		except OptionException, e:
			print e.Message
			print "Try `--help' for more information."
			Environment.Exit(0)
		finally:
		if show_help:
			print "Options:"
			p.WriteOptionDescriptions(Console.Out)
			Environment.Exit(0)

	RunOptionSet = staticmethod(RunOptionSet)