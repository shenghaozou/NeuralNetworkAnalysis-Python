
class UArray(object):
	def ToDoubleArray(point):
		result = Array.CreateInstance(Double, point.Length)
		i = 0
		while i < point.Length:
			result[i] = point[i]
			i += 1
		return result

	ToDoubleArray = staticmethod(ToDoubleArray)

	def ToFloatArray(point):
		result = Array.CreateInstance(Single, point.Length)
		i = 0
		while i < point.Length:
			result[i] = point[i]
			i += 1
		return result

	ToFloatArray = staticmethod(ToFloatArray)

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
	def ToDoubleArrayFromDoubleBytes(point):
		result = Array.CreateInstance(Double, point.Length / 8)
		n = 0
		while n < point.Length:
			result[n / 8] = BitConverter.ToDouble(point, n)
			n += 8
		return result

	ToDoubleArrayFromDoubleBytes = staticmethod(ToDoubleArrayFromDoubleBytes)

	def ToDoubleArrayFromInt8Bytes(point):
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

	ToRGBArray = staticmethod(ToRGBArray)

	def ToIntArray(array):
		intArray = Array.CreateInstance(int, array.Length)
		i = 0
		while i < array.Length:
			intArray[i] = array[i]
			i += 1
		return intArray

	ToIntArray = staticmethod(ToIntArray)

	def InPlaceRoundDoubleArray(array):
		i = 0
		while i < array.Length:
			array[i] = Math.Round(array[i])
			i += 1

	InPlaceRoundDoubleArray = staticmethod(InPlaceRoundDoubleArray)

	def ComputeRoundIdenticals(oldarr, newarr):
		samcount = 0
		i = 0
		while i < oldarr.Length:
			if Math.Round(oldarr[i]) == Math.Round(newarr[i]):
				samcount += 1
			i += 1
		return samcount

	ComputeRoundIdenticals = staticmethod(ComputeRoundIdenticals)

class UMath(object):
	def SoftMax(input):
		""" <summary>
		 In-place soft max
		 </summary>
		 <param name="input"></param>
		"""
		max = input[0]
		min = input[0]
		i = 0
		while i < input.Length:
			if input[i] > max:
				max = input[i]
			i += 1
		k = max - 4
		i = 0
		while i < input.Length:
			input[i] = M.Exp(input[i] - k)
			i += 1
		sum = 0
		i = 0
		while i < input.Length:
			sum += input[i]
			i += 1
		i = 0
		while i < input.Length:
			input[i] /= sum
			i += 1

	SoftMax = staticmethod(SoftMax)

	def EnsureInt(value):
		""" <summary>
		 Rounds a double and ensures it was an integer
		 </summary>
		 <param name="value">The double to be converted</param>
		 <returns>The integer represented by the double</returns>
		"""
		intValue = M.Round(value)
		if value != intValue:
			raise SystemException("Invalid integer: " + value)
		return intValue

	EnsureInt = staticmethod(EnsureInt)

	def EnsureIntArray(array):
		""" <summary>
		 Converts an entire array to integers, ensuring their format
		 </summary>        
		"""
		integerArray = Array.CreateInstance(int, array.Length)
		i = 0
		while i < array.Length:
			integerArray[i] = UMath.EnsureInt(array[i])
			i += 1
		return integerArray

	EnsureIntArray = staticmethod(EnsureIntArray)

	def Max(output):
		max = output[0]
		maxIndex = 0
		i = 1
		while i < output.Length:
			if output[i] > max:
				max = output[i]
				maxIndex = i
			i += 1
		return Tuple[int, int](max, maxIndex)

	Max = staticmethod(Max)

	def Max(output):
		max = output[0]
		maxIndex = 0
		i = 1
		while i < output.Length:
			if output[i] > max:
				max = output[i]
				maxIndex = i
			i += 1
		return Tuple[Single, int](max, maxIndex)

	Max = staticmethod(Max)

	def Max(output):
		max = output[0]
		maxIndex = 0
		i = 1
		while i < output.Length:
			if output[i] > max:
				max = output[i]
				maxIndex = i
			i += 1
		return Tuple[Double, int](max, maxIndex)

	Max = staticmethod(Max)

	def MaxExcluding(idx, output):
		max = output[1] if (idx == 0) else output[0]
		maxIndex = 1 if (idx == 0) else 0
		i = (maxIndex + 1)
		while i < output.Length:
			if i == idx:
				continue # excluded index
			if output[i] > max:
				max = output[i]
				maxIndex = i
			i += 1
		return Tuple[Double, int](max, maxIndex)

	MaxExcluding = staticmethod(MaxExcluding)

	def Clamp(value, min, max):
		return min if (value < min) else (max if (value > max) else value)

	Clamp = staticmethod(Clamp)

	def Clamp(value, min, max):
		return min if (value < min) else (max if (value > max) else value)

	Clamp = staticmethod(Clamp)

	def ClampArray(values, min, max):
		newValues = Array.CreateInstance(Double, values.Length)
		i = 0
		while i < values.Length:
			newValues[i] = UMath.Clamp(values[i], min, max)
			i += 1
		return newValues

	ClampArray = staticmethod(ClampArray)

	def ClampArray(values, min, max):
		newValues = Array.CreateInstance(int, values.Length)
		i = 0
		while i < values.Length:
			newValues[i] = UMath.Clamp(values[i], min, max)
			i += 1
		return newValues

	ClampArray = staticmethod(ClampArray)

	def LInfinityDistance(point1, point2):
		""" <summary>
		 Calculates the LInfinity distance between two points in Rn
		 </summary>
		"""
		if point1.Length != point2.Length:
			raise SystemException("Invalid inputs!")
		max = M.Abs(point1[0] - point2[0])
		i = 1
		while i < point1.Length:
			cur = M.Abs(point1[i] - point2[i])
			if cur > max:
				max = cur
			i += 1
		return max

	LInfinityDistance = staticmethod(LInfinityDistance)

	def L1Distance(point1, point2):
		if point1.Length != point2.Length:
			raise SystemException("Invalid inputs!")
		curr = M.Abs(point1[0] - point2[0])
		i = 1
		while i < point1.Length:
			curr += M.Abs(point1[i] - point2[i])
			i += 1
		return (curr / point1.Length)

	L1Distance = staticmethod(L1Distance)

class URand(object):
	""" <summary>
	 Various functions that utilize randomness
	 </summary>
	"""
	def NextGaussian(random):
		""" <summary>
		 Returns a double drawn from a Gaussian distribution(0,1)
		 </summary>
		"""
		u1 = random.NextDouble()
		u2 = random.NextDouble()
		return M.Sqrt(-2.0 * M.Log(u1)) * M.Sin(2.0 * M.PI * u2)

	NextGaussian = staticmethod(NextGaussian)

	def NextRandomImage(random, size):
		result = [None] * size
		i = 0
		while i < size:
			result[i] = M.Round(255.0 * random.NextDouble())
			i += 1
		return result

	NextRandomImage = staticmethod(NextRandomImage)

	def NextGaussian(mean, sd, random):
		""" <summary>
		  Draws a double from a Gaussian distribution weith a specific mean and deviation
		 </summary>
		 <returns></returns>
		"""
		return sd * URand.NextGaussian(random) + mean

	NextGaussian = staticmethod(NextGaussian)

	def NextPermutation(random, length):
		""" <summary>
		 Standard Fisher-Yates random permutation
		 </summary>
		 <param name="random"></param>
		 <param name="length"></param>
		 <returns></returns>
		 
		"""
		list = [None] * length
		i = 0
		while i < length:
			list[i] = i
			i += 1
		n = length
		i = length - 1
		while i > 0:
			# swap randomly with element in (i, length]
			k = random.Next(i, length)
			bucket = list[k]
			list[k] = list[i]
			list[i] = bucket
			i -= 1
		return list

	NextPermutation = staticmethod(NextPermutation)

	def GetNoisyPoint(point, addedNoiseSD, random):
		newPoint = Array.CreateInstance(Double, point.Length)
		addedNoise = Utils.URand.NextGaussian(0.0, addedNoiseSD, random)
		j = 0
		while j < point.Length:
			newPoint[j] = M.Min(255.0, M.Max(0.0, point[j] + addedNoise))
			j += 1
		return newPoint

	GetNoisyPoint = staticmethod(GetNoisyPoint)

class UDraw(object):
	""" <summary>
	 Displaying images
	 </summary>
	"""
	def DrawGrayscalePixels(pixels, numRows, numCols, isRowOrder):
		image = Bitmap(numRows, numCols)
		i = 0
		while i < numRows:
			j = 0
			while j < numCols:
				greyScale = pixels[numRows * j + i] if isRowOrder else pixels[numCols * i + j]
				c = Color.FromArgb(255, greyScale, greyScale, greyScale)
				image.SetPixel(i, j, c)
				j += 1
			i += 1
		return image

	DrawGrayscalePixels = staticmethod(DrawGrayscalePixels)

	def DrawRGBPixels(pixels, numRows, numCols, isRowOrder):
		image = Bitmap(numRows, numCols)
		colorOffset = numRows * numCols
		i = 0
		while i < numRows:
			j = 0
			while j < numCols:
				pixelOffset = numRows * j + i if isRowOrder else numCols * i + j
				c = Color.FromArgb(255, pixels[pixelOffset], pixels[pixelOffset + colorOffset], pixels[pixelOffset + 2 * colorOffset])
				image.SetPixel(i, j, c)
				j += 1
			i += 1
		return image

	DrawRGBPixels = staticmethod(DrawRGBPixels)

	def DisplayImageAndPause(imagePixels, numRows, numCols, isColor, isRowOrder):
		image = UDraw.DrawRGBPixels(imagePixels, numRows, numCols, isRowOrder) if isColor else UDraw.DrawGrayscalePixels(imagePixels, numRows, numCols, isRowOrder)
		temporaryPath = Path.Combine(System.IO.Path.GetTempPath(), "visualization.png")
		image.Save(temporaryPath)
		Thread.Sleep(800)
		System.Diagnostics.Process.Start(temporaryPath)
		print "Hit enter to continue..."
		Console.ReadLine()

	DisplayImageAndPause = staticmethod(DisplayImageAndPause)

	def Rotate(imagePixels, numRows, numCols, isColor, degrees, isRowOrder):
		image_0 = UDraw.DrawRGBPixels(imagePixels, numRows, numCols, isRowOrder) if isColor else UDraw.DrawGrayscalePixels(imagePixels, numRows, numCols, isRowOrder)
		g_0 = Graphics.FromImage(image_0)
		g_0.RotateTransform(degrees)
		g_0.DrawImage(image_0, Point(0, 0))
		image = UDraw.DrawRGBPixels(imagePixels, numRows, numCols, isRowOrder) if isColor else UDraw.DrawGrayscalePixels(imagePixels, numRows, numCols, isRowOrder)
		g = Graphics.FromImage(image)
		curr = image
		i = 0
		while i < degrees:
			g.RotateTransform(i)
			g.DrawImage(curr, Point(0, 0))
			ms = MemoryStream()
			curr.Save(ms, ImageFormat.Png)
			curr = Bitmap(ms)
			g = Graphics.FromImage(curr)
			i += 2
		g.DrawImage(image_0, Point(0, 0))
		#MemoryStream ms = new MemoryStream();
		#image.Save(ms, ImageFormat.Png);
		#Bitmap rotated = new Bitmap(ms); 
		return UDraw.FromBitmap(curr, numRows, numCols, isColor, isRowOrder)

	Rotate = staticmethod(Rotate)

	def FromBitmap(m, numRows, numCols, isColor, isRowOrder):
		newImagePixels = Array.CreateInstance(int, numRows * numCols * (3 if isColor else 1))
		x = 0
		while x < numRows:
			y = 0
			while y < numCols:
				pixel = m.GetPixel(y, x)
				if isColor:
					newImagePixels[0 * numRows * numCols + x * numCols + y] = pixel.R
					newImagePixels[1 * numRows * numCols + x * numCols + y] = pixel.G
					newImagePixels[2 * numRows * numCols + x * numCols + y] = pixel.B
				else:
					newImagePixels[x * numCols + y] = (pixel.R + pixel.G + pixel.B) / 3
				y += 1
			x += 1
		return newImagePixels

	FromBitmap = staticmethod(FromBitmap)

	# NB: photoquality 0 - 50 
	def LossyJPGAndBack(imagePixels, numRows, numCols, isColor, photoquality, isRowOrder):
		image = UDraw.DrawRGBPixels(imagePixels, numRows, numCols, isRowOrder) if isColor else UDraw.DrawGrayscalePixels(imagePixels, numRows, numCols, isRowOrder)
		encoders = ImageCodecInfo.GetImageEncoders()
		jpgEncoder = None
		i = 0
		while i < encoders.Length:
			if encoders[i].FormatID == ImageFormat.Jpeg.Guid:
				jpgEncoder = encoders[i]
				break
			i += 1
		Trace.Assert(jpgEncoder != None)
		myEncoder = System.Drawing.Imaging.Encoder.Quality
		myEncoderParameters = EncoderParameters(1)
		myEncoderParameter = EncoderParameter(myEncoder, photoquality)
		myEncoderParameters.Param[0] = myEncoderParameter
		mstream = MemoryStream()
		image.Save(mstream, jpgEncoder, myEncoderParameters)
		reload_image = System.Drawing.Image.FromStream(mstream)
		m = Bitmap(reload_image)
		newImagePixels = UDraw.FromBitmap(m, numRows, numCols, isColor, isRowOrder)
		#for (int x = 0; x < numRows; x++)
		#{
		#    for (int y = 0; y < numCols; y++)
		#    {
		#        Color pixel = m.GetPixel(y,x);
		#        if (isColor)
		#        {
		#            newImagePixels[0* numRows * numCols + x * numCols + y] = pixel.R;
		#            newImagePixels[1* numRows * numCols + x * numCols + y] = pixel.G;
		#            newImagePixels[2* numRows * numCols + x * numCols + y] = pixel.B;
		#        }
		#        else
		#        {
		#            newImagePixels[x * numCols + y] = pixel.R + pixel.G + pixel.B;
		#        }
		#    }
		#}
		# Utils.UDraw.DisplayImageAndPause(newImagePixels, numRows, numCols, isColor);
		# print "Linf distance = {0}", Utils.UMath.LInfinityDistance(UArray.ToDoubleArray(newImagePixels), UArray.ToDoubleArray(imagePixels));
		return newImagePixels

	LossyJPGAndBack = staticmethod(LossyJPGAndBack)

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