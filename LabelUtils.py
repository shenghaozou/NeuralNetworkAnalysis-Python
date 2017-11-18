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
from MathNet.Numerics.LinearAlgebra import *
from MathNet.Numerics.LinearAlgebra.Double import *
from MathNet.Numerics import *
# The crop parameter indicates whether we are giving the network a cropped image or not
# Essentially we need to use NNet.CropMaybe() if the image is not cropped already.
class LabelWithConfidence(object):
	def __init__(self, dat, lab, seclab, val, diff):
		self._datum = dat
		self._actualLabel = lab
		self._secBestLabel = seclab
		self._softMaxValue = val
		self._diffFromSecondBest = diff

class ULabel(object):
	def RunWithSoftmax(model, datum, crop):
		datum_v = DenseVector.OfArray(datum)
		if crop:
			datum_v = model.CropMaybe(datum_v)
		outs = model.EvaluateNNConcretePostCrop(datum_v, None)
		UMath.SoftMax(outs)
		return outs

	RunWithSoftmax = staticmethod(RunWithSoftmax)

	def LabelWithConfidence(model, instr, datum, crop):
		datum_v = DenseVector.OfArray(datum)
		if crop:
			datum_v = model.CropMaybe(datum_v)
		outs = model.EvaluateNNConcretePostCrop(datum_v, instr)
		#                Console.WriteLine("Outs = {0}", DenseVector.OfArray(outs));
		max = UMath.Max(outs)
		secmax = UMath.MaxExcluding(max.Item2, outs)
		UMath.SoftMax(outs)
		result = LabelWithConfidence(datum = datum, actualLabel = max.Item2, secBestLabel = secmax.Item2, softMaxValue = outs[max.Item2], diffFromSecondBest = Math.Abs(outs[max.Item2] - outs[secmax.Item2]))
		return result

	LabelWithConfidence = staticmethod(LabelWithConfidence)

	def LabelWithConfidence(model, datum, crop):
		return ULabel.LabelWithConfidence(model, None, datum, crop)

	LabelWithConfidence = staticmethod(LabelWithConfidence)

	def Label(model, datum, crop):
		return ULabel.LabelWithConfidence(model, datum, crop).actualLabel

	Label = staticmethod(Label)

	def LabelWithConfidence(model, input):
		result = Array.CreateInstance(LabelWithConfidence, input.Count())
		i = 0
		while i < input.Count():
			result[i] = ULabel.LabelWithConfidence(model, input.GetDatum(i), True)
			i += 1
		return result

	LabelWithConfidence = staticmethod(LabelWithConfidence)

	def Label(model, input):
		result = Array.CreateInstance(int, input.Count())
		i = 0
		while i < input.Count():
			result[i] = ULabel.Label(model, input.GetDatum(i), True)
			i += 1
		return result

	Label = staticmethod(Label)