import math
class ImageCoordinates(object):
	""" <summary>
	 Class used to convert between an index in a 1D array to the channel/row/column of the image the array represents
	 
	 And the math:
	 (x, y, z) -> a = (x * Ny * Nz + y * Nz + z)
	 x = a % (Nx * Ny * Nz) / (Ny * Nz) = a / (Ny * Nz)
	 y = a % (Ny * Nz) / Nz
	 z = a % (Nz) / 1 = a % Nz
	 </summary>
	""" # e.g. The input ImageCoordinates for MNIST (grayscale) = 1, CIFAR (RGB) = 3
	def __init__(self, channelCount, rowCount, columnCount):
		self._channelCount_ = channelCount
		self._rowCount_ = rowCount
		self._columnCount_ = columnCount

	def GetImageChannel(self, index):
		return index / (self._rowCount_ * self._columnCount_)

	def GetImageRow(self, index):
		return (index % (self._rowCount_ * self._columnCount_)) / self._columnCount_

	def GetImageColumn(self, index):
		return index % self._columnCount_

	def GetIndex(self, channel, row, column):
		return self._rowCount_ * self._columnCount_ * channel + self._columnCount_ * row + column

	def get_ChannelCount(self):
		return self._channelCount_

	ChannelCount = property(fget=get_ChannelCount)

	def get_RowCount(self):
		return self._rowCount_

	RowCount = property(fget=get_RowCount)

	def get_ColumnCount(self):
		return self._columnCount_

	ColumnCount = property(fget=get_ColumnCount)

class UImageCoordinate(object):
	# TODO: Cross-check logic
	def ComputeOutputCounts(kernelDimension, imageDimension, stride, padding, padEnding):
		outputCountFloat = ((imageDimension + 2 * padding - kernelDimension)) / stride + 1
		outputCount = (math.ceil(outputCountFloat) if padEnding else math.floor(outputCountFloat))
		# Remove last kernel application if it starts in the padding
		return outputCount + (-1 if ((outputCount - 1) * stride >= imageDimension + padding) else 0)

	ComputeOutputCounts = staticmethod(ComputeOutputCounts)