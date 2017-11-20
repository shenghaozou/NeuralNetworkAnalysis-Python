

class Options(object):
	def InitializeNNAnalysis():
		Control.UseNativeMKL()
		relulog = Utils.RobustnessOptions.ReLULogFile
		if relulog != "":
			Instrumentation.InitReLULogging()

	InitializeNNAnalysis = staticmethod(InitializeNNAnalysis)