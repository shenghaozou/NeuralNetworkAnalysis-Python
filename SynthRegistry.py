

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
		print "Orig path  =" + e.origPngName
		print "Synth path =" + e.synthPngName
		e.lInfDist = Utils.UMath.LInfinityDistance(origLab.datum, synthLab.datum)
		e.l1Dist = Utils.UMath.L1Distance(origLab.datum, synthLab.datum)
		e.confOrig = origLab.softMaxValue
		e.confSynth = synthLab.softMaxValue
		e.sndBestDiffOrig = origLab.diffFromSecondBest
		e.sndBestDiffSynth = synthLab.diffFromSecondBest
		self.SerializeEntry(e)