# --------------------------------------------------------------------------------------------------
# Neural Network Analysis Framework
#
# Copyright(c) Microsoft Corporation
# All rights reserved.
#
# MIT License
#  
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
#  associated documentation files (the "Software"), to deal in the Software without restriction,
#  including without limitation the rights to use, copy, modify, merge, publish, distribute,
#  sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#  
#  The above copyright notice and this permission notice shall be included in all copies or
#  substantial portions of the Software.
#  
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
#  NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
#  NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# --------------------------------------------------------------------------------------------------

from System.Collections.Generic import *
from System.Linq import *
from System.Text import *
from System.Threading.Tasks import *

# TODO: what is the role of ALL_IMAGES?
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
		Console.WriteLine("Reading labels from: " + labelFile)
		Console.WriteLine("Reading images from: " + imageFile)

	ReadData = staticmethod(ReadData)

	def ReadData(fsL, fsI, maxImageCount, startImage):
		# Step 0: Read the label file header
		labelHeader = Array.CreateInstance(Byte, 8)
		fsL.Read(labelHeader, 0, labelHeader.Length)
		if BitConverter.IsLittleEndian:
			Array.Reverse(labelHeader, 0, 4)
			Array.Reverse(labelHeader, 4, 4)
		if BitConverter.ToUInt32(labelHeader, 0) != 2049:
			raise Exception("Invalid label file magic number!")
		labelCount = BitConverter.ToUInt32(labelHeader, 4)
		# Step 1: Read the image file header
		imageHeader = Array.CreateInstance(Byte, 16)
		fsI.Read(imageHeader, 0, imageHeader.Length)
		if BitConverter.IsLittleEndian:
			Array.Reverse(imageHeader, 0, 4)
			Array.Reverse(imageHeader, 4, 4)
			Array.Reverse(imageHeader, 8, 4)
			Array.Reverse(imageHeader, 12, 4)
		if BitConverter.ToUInt32(imageHeader, 0) != 2051:
			raise Exception("Invalid image file magic number!")
		imageCount = BitConverter.ToUInt32(imageHeader, 4)
		rowCount = BitConverter.ToUInt32(imageHeader, 8)
		columnCount = BitConverter.ToUInt32(imageHeader, 12)
		pixelCount = rowCount * columnCount
		# Step 2: Do some validation
		if labelCount != imageCount:
			raise SystemException("Inconsistent number of labels vs images: " + labelCount + " labels vs. " + imageCount + " images")
		readImageCount = imageCount if maxImageCount == self._ALL_IMAGES else Math.Min(imageCount, maxImageCount)
		Console.WriteLine("Reading " + readImageCount + " images with " + pixelCount + " pixels each")
		# Step 3: Read in the labels
		tempByteLabels = Array.CreateInstance(Byte, startImage)
		fsL.Read(tempByteLabels, 0, startImage)
		byteLabels = Array.CreateInstance(Byte, readImageCount)
		fsL.Read(byteLabels, 0, readImageCount)
		labels = Utils.UArray.ToIntArray(byteLabels).ToList()
		# Step 4: Read in the images one by one and write to the memory stream
		images = List[Array[Double]]()
		image = Array.CreateInstance(Byte, pixelCount)
		i = 0
		while i < startImage:
			fsI.Read(image, 0, image.Length)
			i += 1
		i = 0
		while i < readImageCount:
			# Step 4a: Read the image
			fsI.Read(image, 0, image.Length)
			images.Add(Utils.UArray.ToDoubleArrayFromInt8Bytes(image))
			i += 1
		# Step 5: Build the data point collection
		Console.WriteLine("Done reading images")
		return ImageDataset(Dataset(images, labels, 10), 1, rowCount, columnCount, False)

	ReadData = staticmethod(ReadData)

	def WriteData(labelFile, imageFile, data):
		encoding = UTF8Encoding(True)
		Console.WriteLine("Writing labels to: " + labelFile)
		Console.WriteLine("Writing images to: " + imageFile)

	WriteData = staticmethod(WriteData)

	def WriteData(fsL, fsI, data):
		numPixels = data.RowCount * data.ColumnCount
		Console.WriteLine("Writing " + data.Dataset.Count() + " images with " + numPixels + " pixels each")
		# Step 0: Write the label file header
		labelHeader = Array.CreateInstance(Byte, 8)
		Array.Copy(BitConverter.GetBytes(2049), 0, labelHeader, 0, 4)
		Array.Copy(BitConverter.GetBytes(data.Dataset.Count()), 0, labelHeader, 4, 4)
		if BitConverter.IsLittleEndian:
			Array.Reverse(labelHeader, 0, 4)
			Array.Reverse(labelHeader, 4, 4)
		fsL.Write(labelHeader, 0, 8)
		# Step 1: Write the image file header
		imageHeader = Array.CreateInstance(Byte, 16)
		Array.Copy(BitConverter.GetBytes(2051), 0, imageHeader, 0, 4)
		Array.Copy(BitConverter.GetBytes(data.Dataset.Count()), 0, imageHeader, 4, 4)
		Array.Copy(BitConverter.GetBytes(data.RowCount), 0, imageHeader, 8, 4)
		Array.Copy(BitConverter.GetBytes(data.ColumnCount), 0, imageHeader, 12, 4)
		if BitConverter.IsLittleEndian:
			Array.Reverse(imageHeader, 0, 4)
			Array.Reverse(imageHeader, 4, 4)
			Array.Reverse(imageHeader, 8, 4)
			Array.Reverse(imageHeader, 12, 4)
		fsI.Write(imageHeader, 0, imageHeader.Length)
		# Step 3: Write the labels
		labels = Array.CreateInstance(Byte, data.Dataset.Count())
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
		Console.WriteLine("Done writing")

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
		Console.WriteLine("Reading data from: " + file)

	ReadData = staticmethod(ReadData)

	# Read in the images one by one and write to the memory stream # first byte is label, next 3072 are image
	# Step 4a: Read the label
	# Step 4b: Read the image
	# Step 5: Build the data point collection
	def WriteData(file, images):
		encoding = UTF8Encoding(True)
		Console.WriteLine("Writing data to: " + file)

	WriteData = staticmethod(WriteData)