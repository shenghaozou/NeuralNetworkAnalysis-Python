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
from System.Diagnostics import *
from NNAnalysis import *

class RANDTYPE(object):
	def __init__(self):

class IAugmentor(object):
	def Augment(self, datum):
		pass

class AugmentBrightness(IAugmentor):
	def __init__(self, coords, typ, how_many, max_eps):
		self.__typ = typ
		self.__coords = coords
		self.__how_many = how_many
		self.__max_eps = max_eps
		self.__random = Random(System.DateTime.Now.Millisecond)

	def Augment(self, datum):
		newdatums = List[Array[Double]]()
		# How many to generate 
		i = 0
		while i < self.__how_many:
			# Allocate data
			newdatum = Array.CreateInstance(Double, datum.Length)
			# Sample epsilon
			eps = (self.__random.NextDouble() * 2.0 - 1.0) * self.__max_eps if (self.__typ == RANDTYPE.UNIFORM) else Utils.URand.NextGaussian(self.__random) * self.__max_eps
			# Add constant epsilon to all channels.
			c = 0
			while c < self.__coords.ChannelCount:
				x = 0
				while x < self.__coords.RowCount:
					y = 0
					while y < self.__coords.ColumnCount:
						idx = self.__coords.GetIndex(c, x, y)
						newdatum[idx] = Utils.UMath.Clamp(datum[idx] + eps, Utils.RobustnessOptions.MinValue, Utils.RobustnessOptions.MaxValue)
						y += 1
					x += 1
				c += 1
			newdatums.Add(newdatum)
			i += 1
		return newdatums

class AugmentContrast(IAugmentor):
	def __init__(self, coords, how_many, min_contrast_factor, max_contrast_factor):
		self.__coords = coords
		self.__how_many = how_many
		self.__max_contrast_factor = max_contrast_factor
		self.__min_contrast_factor = min_contrast_factor
		self.__random = Random(System.DateTime.Now.Millisecond)

	def ChannelAverages(self, datum):
		rets = Array.CreateInstance(Double, self.__coords.ChannelCount)
		c = 0
		while c < self.__coords.ChannelCount:
			x = 0
			while x < self.__coords.RowCount:
				y = 0
				while y < self.__coords.ColumnCount:
					idx = self.__coords.GetIndex(c, x, y)
					rets[c] += datum[idx]
					y += 1
				x += 1
			c += 1
		return rets

	def Augment(self, datum):
		newdatums = List[Array[Double]]()
		chans = self.ChannelAverages(datum)
		# How many to generate 
		i = 0
		while i < self.__how_many:
			# Allocate data
			newdatum = Array.CreateInstance(Double, datum.Length)
			# Sample epsilon
			eps = self.__random.NextDouble() * (self.__max_contrast_factor - self.__min_contrast_factor) + self.__min_contrast_factor
			# Add constant epsilon to all channels.
			c = 0
			while c < self.__coords.ChannelCount:
				x = 0
				while x < self.__coords.RowCount:
					y = 0
					while y < self.__coords.ColumnCount:
						idx = self.__coords.GetIndex(c, x, y)
						avgc = chans[c] / (self.__coords.ChannelCount * self.__coords.RowCount)
						newdatum[idx] = Utils.UMath.Clamp((datum[idx] - avgc) * eps + avgc, Utils.RobustnessOptions.MinValue, Utils.RobustnessOptions.MaxValue)
						y += 1
					x += 1
				c += 1
			newdatums.Add(newdatum)
			i += 1
		return newdatums

class AugmentRotation(IAugmentor):
	def __init__(self, coords, how_many, degrees):
		self.__coords = coords
		self.__how_many = how_many
		self.__degrees = degrees
		Trace.Assert(degrees >= -180.0 and degrees <= 180.0)
		self.__random = Random(System.DateTime.Now.Millisecond)

	def Augment(self, datum):
		newdatums = List[Array[Double]]()
		# How many to generate 
		i = 0
		while i < self.__how_many:
			# Allocate data
			datum_int = Utils.UArray.ToIntArray(datum)
			Utils.UDraw.DisplayImageAndPause(datum_int, 32, 32, True)
			eps = self.__random.NextDouble()
			real_agle = eps * self.__degrees
			newdatum_int = Utils.UDraw.Rotate(datum_int, self.__coords.RowCount, self.__coords.ColumnCount, (self.__coords.ChannelCount > 1), real_agle)
			Utils.UDraw.DisplayImageAndPause(newdatum_int, 32, 32, True)
			newdatums.Add(Utils.UArray.ToDoubleArray(newdatum_int))
			i += 1
		return newdatums

class AugmentLossyJpeg(IAugmentor): # 0L - 100L 
	def __init__(self, coords, how_many, loss):
		self.__coords = coords
		self.__how_many = how_many
		self.__loss = loss
		Trace.Assert(loss >= 0 and loss <= 100)
		self.__random = Random(System.DateTime.Now.Millisecond)

	def Augment(self, datum):
		newdatums = List[Array[Double]]()
		# How many to generate 
		i = 0
		while i < self.__how_many:
			# Allocate data
			datum_int = Utils.UArray.ToIntArray(datum)
			photoquality = self.__random.Next(self.__loss, 101)
			newdatum_int = Utils.UDraw.LossyJPGAndBack(datum_int, self.__coords.RowCount, self.__coords.ColumnCount, (self.__coords.ChannelCount > 1), photoquality)
			newdatums.Add(Utils.UArray.ToDoubleArray(newdatum_int))
			i += 1
		return newdatums

class AugmentRandom(IAugmentor):
	def __init__(self, coords, typ, how_many, eps):
		self.__typ = typ
		self.__coords = coords
		self.__how_many = how_many
		self.__max_eps = eps
		self.__random = Random(System.DateTime.Now.Millisecond)

	def Augment(self, datum):
		newdatums = List[Array[Double]]()
		# How many to generate 
		i = 0
		while i < self.__how_many:
			# Allocate data
			newdatum = Array.CreateInstance(Double, datum.Length)
			# Add constant epsilon to all channels.
			c = 0
			while c < self.__coords.ChannelCount:
				x = 0
				while x < self.__coords.RowCount:
					y = 0
					while y < self.__coords.ColumnCount:
						# Sample epsilon
						eps = (self.__random.NextDouble() * 2.0 - 1.0) * self.__max_eps if (self.__typ == RANDTYPE.UNIFORM) else Utils.URand.NextGaussian(self.__random) * self.__max_eps
						idx = self.__coords.GetIndex(c, x, y)
						newdatum[idx] = Utils.UMath.Clamp(datum[idx] + eps, Utils.RobustnessOptions.MinValue, Utils.RobustnessOptions.MaxValue)
						y += 1
					x += 1
				c += 1
			newdatums.Add(newdatum)
			i += 1
		return newdatums

class AugmentGeometric(IAugmentor):
	def __init__(self, coords, typ, how_many, xoffest, yoffset):
		self.__typ = typ
		self.__coords = coords
		self.__how_many = how_many
		self.__xoffset = xoffest
		self.__yoffset = yoffset
		self.__random = Random(System.DateTime.Now.Millisecond)

	def Augment(self, datum):
		newdatums = List[Array[Double]]()
		i = 0
		while i < self.__how_many:
			newdatum = Array.CreateInstance(Double, datum.Length)
			# Sample epsilon
			eps = (self.__random.NextDouble() * 2.0 - 1.0) if (self.__typ == RANDTYPE.UNIFORM) else Utils.URand.NextGaussian(self.__random)
			c = 0
			while c < self.__coords.ChannelCount:
				x = 0
				while x < self.__coords.RowCount:
					y = 0
					while y < self.__coords.ColumnCount:
						xnew = (x + eps * self.__xoffset)
						ynew = (y + eps * self.__yoffset)
						if xnew < 0 or xnew >= self.__coords.RowCount:
							xnew = x
						if ynew < 0 or ynew >= self.__coords.ColumnCount:
							ynew = y
						idx = self.__coords.GetIndex(c, x, y)
						newidx = self.__coords.GetIndex(c, xnew, ynew)
						newdatum[newidx] = datum[idx]
						y += 1
					x += 1
				c += 1
			# Utils.UDraw.DisplayImageAndPause(Utils.UArray.ToRGBArray(datum, 1.0, 0.0), 32, 32, true);
			# Utils.UDraw.DisplayImageAndPause(Utils.UArray.ToRGBArray(newdatum, 1.0, 0.0), 32, 32, true);
			newdatums.Add(newdatum)
			i += 1
		return newdatums