from Utils import UMath, ULabel
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
		#                print "Outs = {0}", DenseVector.OfArray(outs);
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
		result = [None] * input.Count()
		i = 0
		while i < input.Count():
			result[i] = ULabel.LabelWithConfidence(model, input.GetDatum(i), True)
			i += 1
		return result

	LabelWithConfidence = staticmethod(LabelWithConfidence)

	def Label(model, input):
		result = [None] * input.Count()
		i = 0
		while i < input.Count():
			result[i] = ULabel.Label(model, input.GetDatum(i), True)
			i += 1
		return result

	Label = staticmethod(Label)