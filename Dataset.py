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
from System.IO import *

class Accessor(object):
	def Get(self):
		pass

class MemAccessor(Accessor):
	def __init__(self, data):
		self._data_ = data

	def Get(self):
		return self._data_

class BinDataAccessor(Accessor):
	def __init__(self, fn):
		self._fn_ = fn

	# NB: 1 byte becomes 1 double here! I.e. we were using 0-255 levels.
	def Get(self):
		bytes = File.ReadAllBytes(self._fn_)
		return Utils.UArray.ToDoubleArrayFromDoubleBytes(bytes)

class TxtDataAccessor(Accessor):
	def __init__(self, fn):
		rawstr = File.ReadAllText(fn)
		self._datum = int.Parse(rawstr)

	def Get(self):
		return self._datum

class DSList(object):
	def __init__(self, elems = []):
		self._elems_ = elems

	def Get(self, index):
		return self._elems_[index]

	def GetAccessor(self, index):
		return self._elems_[index]

	def Count(self):
		return self._elems_.Count()

	def Add(self, datum):
		self._elems_.Add(datum)

	def Set(self, index, datum):
		self._elems_[index] = datum

	def CreatePermutation(self, permutation):
		ret = DSList[T]()
		i = 0
		while i < self.Count():
			ret.elems_.Add(self._elems_[permutation[i]])
			i += 1
		return ret

	def CreateSplit(self, counts):
		result = List[DSList]()
		start = 0
		i = 0
		while i < counts.Length:
			data = DSList[T]()
			j = 0
			while j < counts[i]:
				data.Add(self.GetAccessor(start + j))
				j += 1
			result.Add(data)
			start += counts[i]
			i += 1
		if start != self.Count():
			raise Exception("Inconsistent dimensions!")
		return result

	def CreateSplit(self, count):
		counts = Array.CreateInstance(int, 2)
		counts[0] = count
		counts[1] = self.Count() - count
		if counts[1] < 0:
			raise Exception("Cant split past end of dataset!")
		splits = self.CreateSplit(counts)
		return Tuple[DSList, DSList](splits[0], splits[1])

class Dataset(object):
	""" <summary>
	 Image-agnostic representation of a Dataset.
	 Contains the data, their labels and the number of labels.
	 Image-metadata exist in the ImageDataset wrapper.
	 </summary>
	""" # The data collection # The labels collection
	# Invariant: data_.Length == labels_.Length # How many classes of labels exist? (e.g. 10 in CIFAR-10)
	def HasUninitialized(self):
		# exists X in dataset. forall i. X(i) == 0
		i = 0
		while i < self._data_.Count():
			datum = self._data_.Get(i)
			allzero = True
			j = 0
			while j < datum.Length:
				if datum[j] != 0.0:
					allzero = False
					break
				j += 1
			if allzero:
				return True
			i += 1
		return False

	def __init__(self, labelcount):
		self._data_ = DSList[Array[Double]]()
		self._labels_ = DSList[int]()
		self._labelCount_ = labelcount

	def __init__(self, labelcount):
		self._data_ = DSList[Array[Double]]()
		self._labels_ = DSList[int]()
		self._labelCount_ = labelcount

	def __init__(self, labelcount):
		self._data_ = DSList[Array[Double]]()
		self._labels_ = DSList[int]()
		self._labelCount_ = labelcount

	def __init__(self, labelcount):
		self._data_ = DSList[Array[Double]]()
		self._labels_ = DSList[int]()
		self._labelCount_ = labelcount

	def __init__(self, labelcount):
		self._data_ = DSList[Array[Double]]()
		self._labels_ = DSList[int]()
		self._labelCount_ = labelcount

	def LabelCount(self):
		return self._labelCount_

	def Count(self):
		return self._data_.Count()

	def Dimension(self):
		return self._data_.Get(0).Length

	def get_Data(self):
		return self._data_

	Data = property(fget=get_Data)

	def get_Labels(self):
		return self._labels_

	Labels = property(fget=get_Labels)

	def GetDatum(self, i):
		return self._data_.Get(i)

	def GetLabel(self, i):
		return self._labels_.Get(i)

	def MeanDatum(self):
		count = self.Count()
		dim = self.Dimension()
		ret = Array.CreateInstance(Double, dim)
		i = 0
		while i < count:
			j = 0
			while j < dim:
				ret[j] += self._data_.Get(i)[j]
				j += 1
			i += 1
		j = 0
		while j < dim:
			ret[j] /= count
			j += 1
		return ret

	# Random (Fisher-Yates) permutation of a dataset
	def CreateShuffle(self, random):
		permutation = Utils.URand.NextPermutation(random, self.Count())
		d = Dataset(self._data_.CreatePermutation(permutation), self._labels_.CreatePermutation(permutation), self.LabelCount())
		return d

	def Update(self, points):
		enumerator = points.GetEnumerator()
		while enumerator.MoveNext():
			tup = enumerator.Current
			self._data_.Add(MemAccessor[Array[Double]](tup.Item1))
			self._labels_.Add(MemAccessor[int](tup.Item2))

	# Add points with the same label
	def Update(self, points, label):
		enumerator = points.GetEnumerator()
		while enumerator.MoveNext():
			dat = enumerator.Current
			self._data_.Add(MemAccessor[Array[Double]](dat))
			self._labels_.Add(MemAccessor[int](label))

	def CreateSplit(self, counts):
		datasplits = self._data_.CreateSplit(counts)
		labelsplit = self._labels_.CreateSplit(counts)
		d = List[Dataset]()
		i = 0
		while i < datasplits.Count():
			d.Add(Dataset(datasplits[i], labelsplit[i], self._labelCount_))
			i += 1
		return d

	def CreateSplit(self, count):
		if count > self.Count():
			raise Exception("Split point can't be after the dataset!")
		split = self.CreateSplit(Array[int]((count, self.Count() - count)))
		return Tuple[Dataset, Dataset](split[0], split[1])

	def Union(self, datasets):
		self.UnionMany(datasets)

	def UnionMany(self, datasets):
		enumerator = datasets.GetEnumerator()
		while enumerator.MoveNext():
			dataset = enumerator.Current
			i = 0
			while i < dataset.Count():
				self._data_.Add(dataset.data_.GetAccessor(i))
				self._labels_.Add(dataset.labels_.GetAccessor(i))
				i += 1

class ImageDataset(object):
	""" <summary>
	  Wrapper around a Dataset. Contains image encoding information
	 </summary>
	"""
	def __init__(self, dataset, metadata):

	def __init__(self, dataset, metadata):

	def __init__(self, dataset, metadata):

	def get_Dataset(self):
		return self._dataset_

	def set_Dataset(self, value):
		self._dataset_ = value

	Dataset = property(fget=get_Dataset, fset=set_Dataset)

	def get_ChannelCount(self):
		return self._channelCount_

	ChannelCount = property(fget=get_ChannelCount)

	def get_RowCount(self):
		return self._rowCount_

	RowCount = property(fget=get_RowCount)

	def get_ColumnCount(self):
		return self._columnCount_

	ColumnCount = property(fget=get_ColumnCount)

	def get_IsColor(self):
		return self._isColor_

	IsColor = property(fget=get_IsColor)

	def get_Metadata(self):
		return Tuple[int, int, int, Boolean](self._channelCount_, self._rowCount_, self._columnCount_, self._isColor_)

	Metadata = property(fget=get_Metadata)

	def Split(self, count):
		split = self.Dataset.CreateSplit(count)
		id1 = ImageDataset(split.Item1, self.Metadata)
		id2 = ImageDataset(split.Item2, self.Metadata)
		return Tuple[ImageDataset, ImageDataset](id1, id2)

	def ShuffleSplitMany(self, counts):
		buckets = Math.Ceiling(self.Dataset.Count() / counts)
		clist = Array.CreateInstance(int, buckets)
		i = 0
		while i < buckets:
			clist[i] = Math.Min(counts, self.Dataset.Count() - i * counts)
			i += 1
		splits = self.Dataset.CreateShuffle(Random()).CreateSplit(clist)
		ret = List[ImageDataset](splits.Count())
		i = 0
		while i < splits.Count():
			ret.Add(ImageDataset(splits[i], self.Metadata))
			i += 1
		return ret

	def Update(self, newImages):
		self.Dataset.Update(newImages)

	def Update(self, newImages, newLabel):
		self.Dataset.Update(newImages, newLabel)

class Data(object):
	def __init__(self):
		self._NO_LABEL = -1
		self._ANY_LABEL = -2

	def LabelMatch(label1, label2):
		return label1 == self._ANY_LABEL or label2 == self._ANY_LABEL or label1 == label2

	LabelMatch = staticmethod(LabelMatch)

	def CalculateDistances(dataset):
		avgdata = Array.CreateInstance(Double, dataset.LabelCount(), dataset.LabelCount())
		countdata = Array.CreateInstance(int, dataset.LabelCount(), dataset.LabelCount())
		data = List[Tuple]()
		i = 0
		while i < dataset.Count():
			data.Add(Tuple[Array[Double], int](dataset.GetDatum(i), dataset.GetLabel(i)))
			i += 1
		query = data.GroupBy()
		enumerator = query.GetEnumerator()
		while enumerator.MoveNext():
			grp1 = enumerator.Current
			enumerator = query.GetEnumerator()
			while enumerator.MoveNext():
				grp2 = enumerator.Current
				if grp1 == grp2:
					continue
				enumerator = grp1.GetEnumerator()
				while enumerator.MoveNext():
					x1 = enumerator.Current
					enumerator = grp2.GetEnumerator()
					while enumerator.MoveNext():
						x2 = enumerator.Current
						dist = UMath.L1Distance(x1.Item1, x2.Item1)
						avgdata[x1.Item2][x2.Item2] += dist
						countdata[x1.Item2][x2.Item2] += 1
		i = 0
		while i < dataset.LabelCount():
			j = 0
			while j < dataset.LabelCount():
				if i == j:
					continue
				avgdata[i][j] = avgdata[i][j] / countdata[i][j]
				j += 1
			i += 1
		Console.WriteLine("Distance statistics:")
		i = 0
		while i < dataset.LabelCount():
			j = 0
			while j < dataset.LabelCount():
				if i == j:
					continue
				Console.WriteLine("Average distance, classes {0}-{1} = {2}", i, j, avgdata[i][j])
				j += 1
			i += 1

	CalculateDistances = staticmethod(CalculateDistances)

	def UnionMany(imagesets):
		metadata = imagesets[0].Metadata
		dlist = Array.CreateInstance(Dataset, imagesets.Count())
		i = 0
		while i < imagesets.Count():
			dlist[i] = imagesets[i].Dataset
			i += 1
		dataset = Dataset(DSList[Array[Double]](), DSList[int](), imagesets[0].Dataset.LabelCount())
		dataset.UnionMany(dlist)
		return ImageDataset(dataset, metadata)

	UnionMany = staticmethod(UnionMany)