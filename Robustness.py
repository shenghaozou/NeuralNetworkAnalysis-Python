
class RobustnessOptions(object):
	def __init__(self):
		# Filename to register the counterexample and information about it
		self._Registry = "generic-registy"
		# What percentage of the dataset should we iterate over?
		self._DataSetPercentage = 1.0
		# Do the CEGAR loop or not?
		self._CEGAR = True
		# Generate examples with optimization or just by bounding?
		self._DoOptimization = True
		# When bounding for counterexample generation, how far should we look?
		self._Epsilon = 20.0 # 48.0; // 14.69534; // 50.0;
		# Minimum range of each entry?
		self._MinValue = 0.0
		self._MaxValue = 255.0
		# The final label of the image should be not just bigger than others but a lot bigger. Default is 0.0.
		self._LabelConfidenceDiff = 0.0f
		# Objective kind
		self._ObjectiveKind = LPSObjectiveKind.MinLinf
		# Timeout to solver
		self._LPTimeMilliSeconds = 8 * 60 * 1000
		# Parallelism
		self._ParallelOptions = ParallelOptions(MaxDegreeOfParallelism = Environment.ProcessorCount)
		# If confidence of counterexample is low, then just ignore it 
		self._IgnoreLowConfidence = False
		self._LowConfidenceThreshold = 0.55
		# Don't go more than CEGARGiveUpIterations times around CEGAR
		self._CEGARGiveUpIterations = 4
		# Slack (as a percentage of the interecept) for linear constraint
		# strict inequalities. Oh well if the interecept is 0.0 then we will 
		# get 0.0 but it does not matter too much. In general I am not really
		# certain about how important this StrictInequalityLambda is.
		self._StrictInequalityLambda = 0.00001
		# Sample a random percentage of the live constraints, defer the rest
		self._LiveConstraintSamplingRatio = 0.1
		# The formula that we generate may or may not guarantee that
		# * the synthesized image is different than the original by at least the
		# * quantization noise. Setting this flag to true ensures that we round
		# * the image and check that it is indeed a counterexample. For images,
		# * each pixel is a byte representing an integer 0-255 so we just use integer
		# * rounding (by the generated bounding formula we guarantee that it's in [0,255]
		# * ****************************************************************************
		self._QuantizationSafety = True
		# Pause and display synthesized images in the main loop?
		self._DisplaySynthesizedImagesAndPause = False
		# Use rationals (default) or integers for variables in the LP
		self._Integrality = False
		# For pre-processed image data, if we are to dump them in a file we need to scale
		# them appropriately: new = old * scale + offset
		self._ScalePreProcessed = 1.0
		self._OffsetPreProcessed = 0.0
		# save PNG files? (default off) 
		self._SavePNGCounterexamples = False
		self._ReLULogFile = ""

	def Dump():
		print "Robustness options:"
		print "Registry:                    {0:d}".format(self._Registry)
		print "DatasetPercentage:           {0:d}".format(self._DataSetPercentage)
		print "CEGAR:                       {0:d}".format(self._CEGAR)
		print "DoOptimization:              {0:d}".format(self._DoOptimization)
		print "Epsilon (bound):             {0:d}".format(self._Epsilon)
		print "LabelConfidenceDiff:         {0:d}".format(self._LabelConfidenceDiff)
		print "LPTimeMilliSeconds:          {0:d}".format(self._LPTimeMilliSeconds)
		print "IgnoreLowConfidence:         {0:d}".format(self._IgnoreLowConfidence)
		print "LowConfidenceThreshold:      {0:d}".format(self._LowConfidenceThreshold)
		print "CEGARGiveUpIterations:       {0:d}".format(self._CEGARGiveUpIterations)
		print "LiveConstraintSamplingRatio: {0:d}".format(self._LiveConstraintSamplingRatio)
		print "QuantizationSafety:          {0:d}".format(self._QuantizationSafety)
		print "Integrality:                 {0:d}".format(self._Integrality)
		print "MinValue:                    {0:d}".format(self._MinValue)
		print "MaxValue:                    {0:d}".format(self._MaxValue)
		print "ScalePreProcessed:           {0:d}".format(self._ScalePreProcessed)
		print "OffsetPreProcessed:          {0:d}".format(self._OffsetPreProcessed)
		print "SavePNGCounterexamples:      {0:d}".format(self._SavePNGCounterexamples)

	Dump = staticmethod(Dump)

class DiffInfo(object):
	def __init__(self):

class Robustness(object):
	def __init__(self):
		self._lockObj = Object()
		# A dictionary such that for each class we have a difference compared to
		# a class that we have found a counterexample to! 
		self._diffDict = Dictionary[Tuple, DiffInfo]()

	def Satisfiable(ct, image_plus_eps):
		# Native inner product more efficient
		lhs = image_plus_eps * ct.Term.GetCoefficients() # ct.Term.GetCoefficients().SubVector(0, image.Count);
		rhs = 0.0
		sat = False
		rhs = -ct.Term.Intercept
		if ct.Inequality == InequalityType.EQ:
			sat = (lhs == rhs)
		elif ct.Inequality == InequalityType.GE:
			sat = (lhs >= rhs)
		elif ct.Inequality == InequalityType.GT:
			sat = (lhs > rhs)
		elif ct.Inequality == InequalityType.LE:
			sat = (lhs <= rhs)
		elif ct.Inequality == InequalityType.LT:
			sat = (lhs < rhs)
		return sat

	Satisfiable = staticmethod(Satisfiable)

	def GenSymbolicInputs(inputDimension):
		""" <summary>
		 Generate symbolic inputs and (potentially) a term for the epsilon of the objective.
		 </summary>
		"""
		inputs = None
		epsilon = None
		LPSTerm.ResetVariableFactory(inputDimension + 1)
		all = LPSTerm.FreshVariables(inputDimension + 1)
		epsilon = all[inputDimension]
		inputs = [None] * inputDimension
		Array.Copy(all, inputs, inputDimension)
		return Tuple[Array[LPSTerm], LPSTerm](inputs, epsilon)

	GenSymbolicInputs = staticmethod(GenSymbolicInputs)

	def SynthesizeCounterexamplesAndStore(nn, ds, snapshot):
		data = []
		labs = [None] * 
		results = Robustness.SynthesizeCounterexamples(nn, ds, snapshot)
		i = 0
		while i < results.Count():
			data.append(results[i].datum)
			labs.append(results[i].actualLabel)
			i += 1
		newdata = Dataset(data, labs, ds.Dataset.LabelCount())
		return ImageDataset(newdata, ds.ChannelCount, ds.RowCount, ds.ColumnCount, ds.IsColor)

	SynthesizeCounterexamplesAndStore = staticmethod(SynthesizeCounterexamplesAndStore)

	def SynthesizeCounterexamples(nn, ds, snapshot):
		""" <summary>
		 Generate and return a list of counterexamples by iterating over the training set
		 </summary>
		 <param name="datasetname"></param>
		 <param name="options"></param>
		 <param name="nn"></param>
		 <param name="ds"></param>
		 <returns></returns>
		"""
		# Initialization stuff
		counterexamples = [None] * 
		reg = SynthRegistry(RobustnessOptions.Registry + ".csv", RobustnessOptions.Registry)
		# How many training points to do
		trainingPointsToDo = Math.Round(ds.Dataset.Count() * RobustnessOptions.DataSetPercentage)
		completed = 0
		# The symbolic variables: NB we use the dimension PostCrop to avoid generating lots of useless variables
		inputs = Robustness.GenSymbolicInputs(nn.InputDimensionPostCrop)
		# Alternatively (the code is thread-safe already):
		# Parallel.For(0, ds.Dataset.Count(), RobustnessOptions.ParallelOptions, i =>
		i = 0
		while i < ds.Dataset.Count():
			if completed < trainingPointsToDo:
				print "Image count = {0}", i
				instr = NNInstrumentation()
				imageLab = ULabel.LabelWithConfidence(nn, instr, ds.Dataset.GetDatum(i), True)
				synthLab = None
				try:
					stopwatch = Stopwatch()
					stopwatch.Start()
					synthLab = Robustness.SynthesizeCounterexample(nn, inputs.Item1, inputs.Item2, imageLab, instr, ds.Dataset.GetLabel(i), ds.RowCount, ds.ColumnCount, ds.IsColor)
					stopwatch.Stop()
					print "Processed image in {0} milliseconds", stopwatch.ElapsedMilliseconds
					GC.Collect()
				except , :
					continue
				finally:
			i += 1
		# VERY IMPORTANTLY: Change the label of the counterexample
		# to be the label of the original point! This was a horrible bug.
		return counterexamples

	SynthesizeCounterexamples = staticmethod(SynthesizeCounterexamples)

	def SynthesizeCounterexample(nn, inputs, epsilon, imageLab, instr, realLabel, rowSize, colSize, isColor):
		""" <summary>
		 Synthesize a counterexample from an existing labelled image.
		 </summary>
		 <param name="options"></param>
		 <param name="nn">The model.</param>
		 <param name="imageLab">The image and labeling information from the network.</param>
		 <param name="instr"></param>
		 <param name="realLabel">The label of the image from the training set.</param>
		 <param name="rowSize"></param>
		 <param name="colSize"></param>
		 <param name="isColor"></param>
		 <returns>NULL if we were not able to synthesize a counterexample, otherwise some information about it.</returns>
		""" # Symbolic inputs (cropped) # Epsilon variable # Original image classification info (uncropped) # Ground truth for this image (from training set) # Original (uncropped) row size # Original (uncropped) col size
		origLabel = imageLab.actualLabel
		targetLabel = imageLab.secBestLabel
		input_dimension_pre_crop = nn.InputDimensionPreCrop
		input_dimension_post_crop = nn.InputDimensionPostCrop
		orig_image = imageLab.datum
		orig_image_crop = nn.CropMaybe(DenseVector.OfArray(orig_image)).ToArray()
		if realLabel != origLabel:
			print "This image is misclassifed already! Skipping."
			return None
		if RobustnessOptions.IgnoreLowConfidence and imageLab.softMaxValue < RobustnessOptions.LowConfidenceThreshold:
			print "This image is misclassifed with low confidence! Skipping."
			return None
		# Fast path:
		# DiffInfo diff_info;
		# *********************
		# * DV: Commenting out the fast path for now (but we are still keeping the Dictionary, for debugging)
		# * *********************
		# if (diffDict.TryGetValue(new Tuple<int,int>(origLabel,targetLabel),out diff_info))
		# {
		# print "Got a hit in the difference cache!";
		# Vector<double> diff_counterexample = diff_info.diff;
		# 
		# Vector<double> cand = DenseVector.OfArray(orig_image) + diff_counterexample;
		# 
		# 
		# print "oooooooooooooooo Checking with the fast path!";
		# 
		# double[] cand_arr_crop = nn.CropMaybe(cand).ToArray();
		# 
		# if (RobustnessOptions.QuantizationSafety)
		# {
		# Utils.UArray.InPlaceRoundDoubleArray(cand_arr_crop);
		# }
		# 
		# LabelWithConfidence candLab = Utils.ULabel.LabelWithConfidence(nn, cand_arr_crop,false); // Already  cropped, don't crop!
		# 
		# if (candLab.actualLabel != origLabel)
		# {
		# 
		# print "=> Real counterexample (from fast path)!";
		# diff_info.number++;
		# return candLab;
		# }
		# 
		# print "xxxx Fast path failed, continuing with symbolic interpreter ...";
		# // otherwise continue with the slow path ...
		# }
		# **********************
		state = LPSState(instr, orig_image_crop)
		nomodelcount = 0
		if nomodelcount += 1 > 0:
			return None
		state.ClearConstraints()
		output = nn.EvaluateNNSymbolicPostCrop(state, inputs)
		# Just some tracing ...
		# ReportSparsity(output);
		currentCts = state.CurrentCts
		deferredCts = state.DeferredCts
		# Conjoin the label formula
		currentCts.And(NNetFormulas.LabelFormula(output, targetLabel, RobustnessOptions.LabelConfidenceDiff))
		# If we are just looking for bounds, then the variables themselves will contain "origin" bounds
		if RobustnessOptions.DoOptimization:
			NNETObjectives.AddEpsilonBounds(currentCts, inputs, epsilon, orig_image_crop)
		# Ensure that at least *one* entry is different by at least 1.0
		if RobustnessOptions.QuantizationSafety:
			NNETObjectives.AddQuantizationSafety(currentCts, inputs, orig_image_crop)
		# Create objective
		objective = None
		if RobustnessOptions.DoOptimization:
			if RobustnessOptions.ObjectiveKind == LPSObjectiveKind.MinLinf:
				objective = NNETObjectives.MinLInf(currentCts, inputs, epsilon, orig_image_crop)
			elif RobustnessOptions.ObjectiveKind == LPSObjectiveKind.MaxConf:
				objective = NNETObjectives.MaxConf(output, origLabel, targetLabel)
			else:
				pass
		if not RobustnessOptions.CEGAR:
			currentCts.And(deferredCts)
			deferredCts = LPSConstraints()
		# CEGAR loop header
		print "Current constraints: {0}, deferred: {1}", currentCts.Count, deferredCts.Count
		lps = LPSolver(input_dimension_post_crop, currentCts.Count + deferredCts.Count, orig_image_crop, RobustnessOptions.Epsilon)
		lps.AddConstraints(currentCts, objective)
		cegar_iterations = 0
		while True:
			if cegar_iterations += 1 > RobustnessOptions.CEGARGiveUpIterations:
				print "xxxxxxxxxxxxxxxx Giving up CEGAR, could not find model!"
			newImage = lps.SolveLowLevelLP()
			currentCts = LPSConstraints()
			if newImage == None:
				print "xxxxxxxxxxxxxxxx No model!"
			print "oooooooooooooooo Found model!"
			newImageUnrounded = Array.CreateInstance(Double, newImage.Length)
			Array.Copy(newImage, newImageUnrounded, newImage.Length)
			if RobustnessOptions.QuantizationSafety:
				Utils.UArray.InPlaceRoundDoubleArray(newImage)
			samcount = Utils.UArray.ComputeRoundIdenticals(orig_image_crop, newImage)
			print "Synthesized image has {0} identical inputs (after rounding) to original (cropped)", samcount
			# Now, try to label the new example
			newLab = Utils.ULabel.LabelWithConfidence(nn, newImage, False) # Already  cropped, don't crop!
			if newLab.actualLabel != targetLabel:
				if newLab.actualLabel == realLabel:
					# Here the synthesized image is not really a counterexample. 
					# This could be due to either (a) quantization errors or (b) CEGAR 
					# underapproximation. But the only thing we can try and do here is
					# add mor constraints and try to resolve. 
					if RobustnessOptions.CEGAR:
						print "Not really a counterexample, going round CEGAR loop."
					added = 0
					# new_image_plus_eps = newImage : 0.0 
					# so that the length matches the coefficients of each constraint ... 
					newimage_plus_eps = Array.CreateInstance(Double, newImage.Length + 1)
					Array.Copy(newImageUnrounded, newimage_plus_eps, newImage.Length)
					newimage_plus_eps[newImage.Length] = 0.0
					newImageVec_eps = DenseVector.OfArray(newimage_plus_eps)
					dfor e in deferredCts:
					Parallel.For(0, deferredCts.Count, )
					# currentCts.And(curr_deferred.Term, curr_deferred.Inequality);
					print 
					print "Added {0} constraints for CEGAR", added
					if added == 0:
						print "=> CEGAR cannot improve things."
					# return null;
					# lps.AddConstraints(currentCts, null);
					continue
				else:
					print "=> Real counterexample! (Although with different label than expected)"
					break
			else:
				print "=> Real counterexample! (New image has second-best label"
				break
		if RobustnessOptions.DisplaySynthesizedImagesAndPause:
			Utils.UDraw.DisplayImageAndPause(Utils.UArray.ToIntArray(imageLab.datum), rowSize, colSize, isColor)
			Utils.UDraw.DisplayImageAndPause(Utils.UArray.ToIntArray(newLab.datum), rowSize, colSize, isColor)
		# NB: Uncrop the image in newLab
		newLab.datum = nn.UnCropMaybe(DenseVector.OfArray(orig_image), DenseVector.OfArray(newLab.datum)).ToArray()
		tmp = nn.UnCropMaybe(DenseVector.OfArray(orig_image), DenseVector.OfArray(newImageUnrounded)).ToArray()
		diff_val = DenseVector.OfArray(tmp) - DenseVector.OfArray(orig_image)
		key = Tuple[int, int](origLabel, newLab.actualLabel)
		if self._diffDict.TryGetValue(key, ):
			dinfo.number += 1
		else:
			dinfo = DiffInfo()
			dinfo.diff = diff_val
			dinfo.number = 1
			self._diffDict.append(Tuple[int, int](origLabel, newLab.actualLabel), dinfo)
		return newLab

	SynthesizeCounterexample = staticmethod(SynthesizeCounterexample)

	def ReportSparsity(output):
		""" <summary>
		 Given the symbolic output we check which columns are completely zero,
		 which effectively implies that the corresponding variables do not participate
		 in the Jacobian.
		 </summary>
		 <param name="output"></param>
		"""
		matrix = LPSTerm.UnderlyingMatrix(output)
		zeros = DenseVector.Create(output.Length, 0.0)
		# int sparse_count = 0;
		stats = [None] * 
		i = 0
		while i < matrix.ColumnCount:
			col = matrix.Column(i)
			stats.append(Tuple[int, Double](i, col.Maximum()))
			i += 1
		stats.Sort()
		for e in stats:
		while enumerator.MoveNext():
			s = enumerator.Current
			print s.Item2

	ReportSparsity = staticmethod(ReportSparsity)
