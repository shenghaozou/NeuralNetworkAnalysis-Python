from enum import Enum
import abc
import random
import Utils
from datetime import datetime

class RANDTYPE(Enum):
	GAUSSIAN = 1
	UNIFORM = 2

class IAugmentor(object):
	def __init__(self):
		__metaclass__ = abc.ABCMeta
	@abc.abstractmethod
	def Augment(self, datum):
		raise NotImplementedError("Please use a concrete IAugmentor object")

class AugmentBrightness(IAugmentor):
	def __init__(self, coords, typ, how_many, max_eps):
		self.__typ = typ
		self.__coords = coords
		self.__how_many = how_many
		self.__max_eps = max_eps
		self.__random = random.Random()
		self.__random.seed(datetime.now())
		
	def Augment(self, datum):
		newdatums = []
		# How many to generate 
		i = 0
		while i < self.__how_many:
			# Allocate data
			newdatum = [None] * len(datum)
			# Sample epsilon
			eps = (self.__random.random() * 2.0 - 1.0) * self.__max_eps if (self.__typ == RANDTYPE.UNIFORM) else random.gauss(mu = self.__random, sigma = 1) * self.__max_eps
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
			newdatums.append(newdatum)
			i += 1
		return newdatums

class AugmentContrast(IAugmentor):
	def __init__(self, coords, how_many, min_contrast_factor, max_contrast_factor):
		self.__coords = coords
		self.__how_many = how_many
		self.__max_contrast_factor = max_contrast_factor
		self.__min_contrast_factor = min_contrast_factor
		self.__random = random.Random()
		self.__random.seed(datetime.now())

	def ChannelAverages(self, datum):
		rets = [None] * self.__coords.ChannelCount
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
		newdatums = []
		chans = self.ChannelAverages(datum)
		# How many to generate 
		i = 0
		while i < self.__how_many:
			# Allocate data
			newdatum = [None] * len(datum)
			# Sample epsilon
			eps = self.__random.random() * (self.__max_contrast_factor - self.__min_contrast_factor) + self.__min_contrast_factor
			# Add constant epsilon to all channels.
			c = 0
			while c < self.__coords.ChannelCount:
				x = 0
				while x < self.__coords.RowCount:
					y = 0
					while y < self.__coords.ColumnCount:
						idx = self.__coords.GetIndex(c, x, y)
						avgc = chans[c] / (self.__coords.ChannelCount * self.__coords.RowCount)
						#__ newdatum[idx] = Utils.UMath.Clamp((datum[idx] - avgc) * eps + avgc, Utils.RobustnessOptions.MinValue, Utils.RobustnessOptions.MaxValue)
						y += 1
					x += 1
				c += 1
			newdatums.append(newdatum)
			i += 1
		return newdatums

class AugmentRotation(IAugmentor):
	def __init__(self, coords, how_many, degrees):
		self.__coords = coords
		self.__how_many = how_many
		self.__degrees = degrees
		assert degrees >= -180.0 and degrees <= 180.0
		self.__random = random.Random()
		self.__random.seed(datetime.now())

	def Augment(self, datum):
		newdatums = []
		# How many to generate 
		i = 0
		while i < self.__how_many:
			# Allocate data
			#__ datum_int = Utils.UArray.ToIntArray(datum)
			# FIX ME
			#__ Utils.UDraw.DisplayImageAndPause(datum_int, 32, 32, True)
			eps = self.__random.random()
			real_agle = eps * self.__degrees
			#__ newdatum_int = Utils.UDraw.Rotate(datum_int, self.__coords.RowCount, self.__coords.ColumnCount, (self.__coords.ChannelCount > 1), real_agle)
			#__ Utils.UDraw.DisplayImageAndPause(newdatum_int, 32, 32, True)
			#__ newdatums.append(Utils.UArray.ToDoubleArray(newdatum_int))
			i += 1
		return newdatums

class AugmentLossyJpeg(IAugmentor): # 0L - 100L 
	def __init__(self, coords, how_many, loss):
		self.__coords = coords
		self.__how_many = how_many
		self.__loss = loss
		Trace.Assert(loss >= 0 and loss <= 100)
		self.__random = random.Random()
		self.__random.seed(datetime.now())

	def Augment(self, datum):
		newdatums = []
		# How many to generate 
		i = 0
		while i < self.__how_many:
			# Allocate data
			datum_int = Utils.UArray.ToIntArray(datum)
			photoquality = self.__random.Next(self.__loss, 101)
			#__ newdatum_int = Utils.UDraw.LossyJPGAndBack(datum_int, self.__coords.RowCount, self.__coords.ColumnCount, (self.__coords.ChannelCount > 1), photoquality)
			#__ newdatums.append(Utils.UArray.ToDoubleArray(newdatum_int))
			i += 1
		return newdatums

class AugmentRandom(IAugmentor):
	def __init__(self, coords, typ, how_many, eps):
		self.__typ = typ
		self.__coords = coords
		self.__how_many = how_many
		self.__max_eps = eps
		self.__random = random.Random()
		self.__random.seed(datetime.now())

	def Augment(self, datum):
		newdatums = []
		# How many to generate 
		i = 0
		while i < self.__how_many:
			# Allocate data
			newdatum = [None] * len(datum)
			# Add constant epsilon to all channels.
			c = 0
			while c < self.__coords.ChannelCount:
				x = 0
				while x < self.__coords.RowCount:
					y = 0
					while y < self.__coords.ColumnCount:
						# Sample epsilon
						#__ eps = (self.__random.random() * 2.0 - 1.0) * self.__max_eps if (self.__typ == RANDTYPE.UNIFORM) else Utils.URand.NextGaussian(self.__random) * self.__max_eps
						eps = (self.__random.random() * 2.0 - 1.0) * self.__max_eps if (self.__typ == RANDTYPE.UNIFORM) else random.gauss(mu = self.__random, sigma = 1) * self.__max_eps
						idx = self.__coords.GetIndex(c, x, y)[]
						#__ newdatum[idx] = Utils.UMath.Clamp(datum[idx] + eps, Utils.RobustnessOptions.MinValue, Utils.RobustnessOptions.MaxValue)
						y += 1
					x += 1
				c += 1
			newdatums.append(newdatum)
			i += 1
		return newdatums

class AugmentGeometric(IAugmentor):
	def __init__(self, coords, typ, how_many, xoffest, yoffset):
		self.__typ = typ
		self.__coords = coords
		self.__how_many = how_many
		self.__xoffset = xoffest
		self.__yoffset = yoffset
		self.__random = random.Random()
		self.__random.seed(datetime.now())

	def Augment(self, datum):
		newdatums = [[]] # FIX ME
		i = 0
		while i < self.__how_many:
			newdatum = [None] * len(datum)
			# Sample epsilon
			eps = (self.__random.random() * 2.0 - 1.0) if (self.__typ == RANDTYPE.UNIFORM) else random.gauss(mu = self.__random, sigma = 1)
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
			newdatums.append(newdatum)
			i += 1
		return newdatums