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
		outputCount = (Math.Ceiling(outputCountFloat) if padEnding else Math.Floor(outputCountFloat))
		# Remove last kernel application if it starts in the padding
		return outputCount + (-1 if ((outputCount - 1) * stride >= imageDimension + padding) else 0)

	ComputeOutputCounts = staticmethod(ComputeOutputCounts)