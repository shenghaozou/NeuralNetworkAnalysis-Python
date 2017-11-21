import tempfile, os
import numpy as np
import cv2

class UArray(object):

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
		raise ValueError("Invalid integer in array!")


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
