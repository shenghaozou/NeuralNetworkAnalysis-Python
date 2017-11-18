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

class NNAccuracy(object):
	def __init__(self):
		self._lockObject = Object()

	def Filter(nn, ds, predicate):
		ret = Dataset(ds.LabelCount())
		i = 0
		while i < ds.Count():
			datum = ds.GetDatum(i)
			ground_label = ds.GetLabel(i)
			if NNAccuracy.predicate(nn, datum, ground_label):
				ret.Data.Add(MemAccessor[Array[Double]](datum))
				ret.Labels.Add(MemAccessor[int](ground_label))
			i += 1
		return ret

	Filter = staticmethod(Filter)

	def KeepAboveConfidenceThreshold(net, ds, conf):
		return NNAccuracy.Filter(net, ds, )

	KeepAboveConfidenceThreshold = staticmethod(KeepAboveConfidenceThreshold)

	def KeepMisclass(net, ds):
		return NNAccuracy.Filter(net, ds, )

	KeepMisclass = staticmethod(KeepMisclass)

	def GetAccuracy(nn, ds):
		cnt = 0
		prg = 0
		# Parallel.For(0, ds.Count(), RobustnessOptions.ParallelOptions, i =>
		i = 0
		while i < ds.Count():
			#if (i < 10000) { continue;  }
			datum = ds.GetDatum(i)
			ground_label = ds.GetLabel(i)
			labconf = Utils.ULabel.LabelWithConfidence(nn, ds.GetDatum(i), True)
			label = labconf.actualLabel
			# int label = Utils.ULabel.Label(nn, ds.GetDatum(i), true);
			# Console.WriteLine("Confidence = {0}", labconf.softMaxValue);
			if label == ground_label:
			else:
			# Console.WriteLine("Missclassifciation: " + label + " vs " + testImages.Dataset.GetLabel(i));
			i += 1
		# Utils.UDraw.DisplayImageAndPause(Utils.UArray.ToRGBArray(datum, 1.0, 0.0), 32, 32, true);
		Console.WriteLine("\nCorrectly classified = {0}", cnt)
		Console.WriteLine("Total images         = {0}", ds.Count())
		acc = cnt / ds.Count()
		Console.Write("\nAccuracy: ")
		Console.WriteLine(acc)
		Console.WriteLine("ReLU Collisions = {0}", Instrumentation.Collisions)
		return acc

	GetAccuracy = staticmethod(GetAccuracy)

	def GetLoss(nn, ds):
		loss = 0.0
		prg = 0
		Parallel.For(0, ds.Count(), RobustnessOptions.ParallelOptions, )
		#                for (int i =0; i < ds.Count(); i++)
		# safety for infinity ... 
		Console.Write("\nTotal loss: ")
		Console.WriteLine(loss)
		return loss

	GetLoss = staticmethod(GetLoss)