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

from System.Drawing import *
from NNAnalysis.Utils import *

class SynthEntry(object):
	def __init__(self):
 # Data set name # Position in the dataset
class SynthRegistry(object):
	def SerializeEntry(self, e):

	def __init__(self, csvFileName, dataDirectory):
		self._inMemLock_ = Object()
		self._fileLoc_ = Object()
		self._csvFileName_ = csvFileName
		self._registryCsvFileWriter_ = StreamWriter(csvFileName)
		self._dataDirectory_ = dataDirectory
		exists = System.IO.Directory.Exists(dataDirectory)
		if not exists:
			System.IO.Directory.CreateDirectory(dataDirectory)
		if self._registryCsvFileWriter_ == None:
			raise Exception("Can't open counterexample registry file!")

	def CreatePnG(self, origin, datasetname, datasetIndex, input, scale, offset, numRows, numCols, isColor, isRowOrder):
		path = Path.Combine(self._dataDirectory_, origin + "-" + datasetname + "-" + datasetIndex + ".png")
		if RobustnessOptions.SavePNGCounterexamples:
			# Create PnG file for orig
			imagePixels = Utils.UArray.ToRGBArray(input, scale, offset)
			image = Utils.UDraw.DrawRGBPixels(imagePixels, numRows, numCols, isRowOrder) if isColor else Utils.UDraw.DrawGrayscalePixels(imagePixels, numRows, numCols, isRowOrder)
			image.Save(path)
		return path

	def RecordAtomically(self, datasetName, datasetIndex, origLab, synthLab, scale, offset, numRows, numCols, isColor, isRowOrder):
		e = SynthEntry()
		e.datasetName = datasetName
		e.origPngName = self.CreatePnG("orig", datasetName, datasetIndex, origLab.datum, scale, offset, numRows, numCols, isColor, isRowOrder)
		e.origLabel = origLab.actualLabel
		e.synthPngName = self.CreatePnG("snth", datasetName, datasetIndex, synthLab.datum, scale, offset, numRows, numCols, isColor, isRowOrder)
		e.synthLabel = synthLab.actualLabel
		diff = Array.CreateInstance(Double, origLab.datum.Length)
		i = 0
		while i < origLab.datum.Length:
			diff[i] = 5 * (origLab.datum[i] - synthLab.datum[i]) + 100
			i += 1 # -20 ... 20 -> -100 .. 100 -> 0 .. 200
		self.CreatePnG("diffx5o100", datasetName, datasetIndex, diff, scale, offset, numRows, numCols, isColor, isRowOrder)
		Console.WriteLine("Orig path  =" + e.origPngName)
		Console.WriteLine("Synth path =" + e.synthPngName)
		e.lInfDist = Utils.UMath.LInfinityDistance(origLab.datum, synthLab.datum)
		e.l1Dist = Utils.UMath.L1Distance(origLab.datum, synthLab.datum)
		e.confOrig = origLab.softMaxValue
		e.confSynth = synthLab.softMaxValue
		e.sndBestDiffOrig = origLab.diffFromSecondBest
		e.sndBestDiffSynth = synthLab.diffFromSecondBest
		self.SerializeEntry(e)