# TODO: what is the role of ALL_IMAGES?
import sys
class MNIST(object):
	def __init__(self):
		self._ALL_IMAGES = -1
		self._InputDimensions = 28 * 28
		self._InputCoordinates = ImageCoordinates(1, 28, 28)

	def GetNN(file):
		return NNetReader.ReadBinNeuralNet(file, self._InputDimensions, self._InputCoordinates)

	GetNN = staticmethod(GetNN)

	def ReadDirectoryData(dir):
		ds = Dataset(dir, 10)
		return ImageDataset(ds, 1, 28, 28, False)

	ReadDirectoryData = staticmethod(ReadDirectoryData)

	def ReadData(labelFile, imageFile, maxImageCount, startImage):
		print "Reading labels from: " + labelFile
		print "Reading images from: " + imageFile

	ReadData = staticmethod(ReadData)

	def ReadData(fsL, fsI, maxImageCount, startImage):
		# Step 0: Read the label file header
		labelHeader = [None] * 8
		fsL.Read(labelHeader, 0, labelHeader.Length)
		if sys.byteorder == "little":
			labelHeader[0 : 0 + 4] = reversed(labelHeader[0 : 0 + 4])
			labelHeader[4 : 4 + 4] = reversed(labelHeader[4 : 4 + 4])
		if BitConverter.ToUInt32(labelHeader, 0) != 2049:
			raise Exception("Invalid label file magic number!")
		labelCount = BitConverter.ToUInt32(labelHeader, 4)
		# Step 1: Read the image file header
		imageHeader = [None] * 16
		fsI.Read(imageHeader, 0, imageHeader.Length)
		raise NotImplementedError("not sure how to deal with this part")
		if sys.byteorder == "little":
			imageHeader[0 : 0 + 4] = reversed(imageHeader[0 : 0 + 4])
			imageHeader[4 : 4 + 4] = reversed(imageHeader[4 : 4 + 4])
			imageHeader[8 : 8 + 4] = reversed(imageHeader[8 : 8 + 4])
			imageHeader[12 : 12 + 4] = reversed(imageHeader[12 : 12 + 4])
		if BitConverter.ToUInt32(imageHeader, 0) != 2051:
			raise Exception("Invalid image file magic number!")
		
		imageCount = BitConverter.ToUInt32(imageHeader, 4)
		rowCount = BitConverter.ToUInt32(imageHeader, 8)
		columnCount = BitConverter.ToUInt32(imageHeader, 12)
		pixelCount = rowCount * columnCount
		# Step 2: Do some validation
		if labelCount != imageCount:
			raise SystemException("Inconsistent number of labels vs images: " + labelCount + " labels vs. " + imageCount + " images")
		readImageCount = imageCount if maxImageCount == self._ALL_IMAGES else min(imageCount, maxImageCount)
		print "Reading " + readImageCount + " images with " + pixelCount + " pixels each"
		# Step 3: Read in the labels
		tempByteLabels = [None] * startImage
		fsL.Read(tempByteLabels, 0, startImage)
		byteLabels = [None] * readImageCount
		fsL.Read(byteLabels, 0, readImageCount)
		labels = Utils.UArray.ToIntArray(byteLabels).ToList()
		# Step 4: Read in the images one by one and write to the memory stream
		images = []
		image = [None] * pixelCount
		i = 0
		while i < startImage:
			fsI.Read(image, 0, image.Length)
			i += 1
		i = 0
		while i < readImageCount:
			# Step 4a: Read the image
			fsI.Read(image, 0, image.Length)
			images.append(Utils.UArray.ToDoubleArray(image))
			i += 1
		# Step 5: Build the data point collection
		print "Done reading images"
		return ImageDataset(Dataset(images, labels, 10), 1, rowCount, columnCount, False)

	ReadData = staticmethod(ReadData)

	def WriteData(labelFile, imageFile, data):
		encoding = UTF8Encoding(True)
		print "Writing labels to: " + labelFile
		print "Writing images to: " + imageFile

	WriteData = staticmethod(WriteData)

	def WriteData(fsL, fsI, data):
		numPixels = data.RowCount * data.ColumnCount
		print "Writing " + data.Dataset.Count() + " images with " + numPixels + " pixels each"
		# Step 0: Write the label file header
		labelHeader = [None] * 8
		Array.Copy(BitConverter.GetBytes(2049), 0, labelHeader, 0, 4)
		Array.Copy(BitConverter.GetBytes(data.Dataset.Count()), 0, labelHeader, 4, 4)
		if sys.byteorder == "little":
			labelHeader[0 : 0 + 4] = reversed(labelHeader[0 : 0 + 4])
			labelHeader[4 : 4 + 4] = reversed(labelHeader[4 : 4 + 4])
		fsL.Write(labelHeader, 0, 8)
		# Step 1: Write the image file header
		imageHeader = [None] * 16
		Array.Copy(BitConverter.GetBytes(2051), 0, imageHeader, 0, 4)
		Array.Copy(BitConverter.GetBytes(data.Dataset.Count()), 0, imageHeader, 4, 4)
		Array.Copy(BitConverter.GetBytes(data.RowCount), 0, imageHeader, 8, 4)
		Array.Copy(BitConverter.GetBytes(data.ColumnCount), 0, imageHeader, 12, 4)
		if sys.byteorder == "little":
			imageHeader[0 : 0 + 4] = reversed(imageHeader[0 : 0 + 4])
			imageHeader[4 : 4 + 4] = reversed(imageHeader[4 : 4 + 4])
			imageHeader[8 : 8 + 4] = reversed(imageHeader[8 : 8 + 4])
			imageHeader[12 : 12 + 4] = reversed(imageHeader[12 : 12 + 4])
		fsI.Write(imageHeader, 0, imageHeader.Length)
		# Step 3: Write the labels
		labels = [None] * data.Dataset.Count()
		i = 0
		while i < data.Dataset.Count():
			labels[i] = Convert.ToByte(data.Dataset.GetLabel(i))
			i += 1
		fsL.Write(labels.ToArray(), 0, labels.Length)
		# Step 4: Write in the images one by one and write to the memory stream
		i = 0
		while i < labels.Length:
			fsI.Write(Utils.UArray.ToByteArray(data.Dataset.GetDatum(i)), 0, data.Dataset.GetDatum(i).Length)
			i += 1
		fsL.Flush()
		fsI.Flush()
		print "Done writing"

	WriteData = staticmethod(WriteData)

class CIFAR(object):
	def __init__(self):
		self._ALL_IMAGES = -1
		self._InputDimensions = 32 * 32 * 3
		self._InputCoordinates = ImageCoordinates(3, 32, 32)

	#  Reading and writing CIFAR networks and data
	def GetNN(file):
		return NNetReader.ReadBinNeuralNet(file, self._InputDimensions, self._InputCoordinates)

	GetNN = staticmethod(GetNN)

	def ReadDirectoryData(dir):
		ds = Dataset(dir, 10)
		return ImageDataset(ds, 3, 32, 32, True)

	ReadDirectoryData = staticmethod(ReadDirectoryData)

	def ReadData(file, maxImageCount, startImage):
		print "Reading data from: " + file

	ReadData = staticmethod(ReadData)

	# Read in the images one by one and write to the memory stream # first byte is label, next 3072 are image
	# Step 4a: Read the label
	# Step 4b: Read the image
	# Step 5: Build the data point collection
	def WriteData(file, images):
		encoding = UTF8Encoding(True)
		print "Writing data to: " + file

	WriteData = staticmethod(WriteData)