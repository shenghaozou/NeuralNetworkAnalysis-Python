import Utils
class Options (object):
    @staticmethod
    def InitializeNNAnalysis():
            Control.UseNativeMKL()
            relulog = Utils.RobustnessOptions.ReLULogFile

            if relulog != "" :
                Instrumentation.InitReLULogging()
