from __future__ import *
import Utils
class SynthEntry(object):
    def __init__(self):
        self.datasetName = None
        self.datasetIndex = None
        self.origPngName = None
        self.origLabel = None
        self.synthPngName = None
        self.synthLabel = None
        self.lInfDist = None
        self.l1Dist = None
        self.confOrig = None
        self.confSynth = None
        self.sndBestDiffOrig = None
        self.sndBestDiffSynth = None


class SynthRegistry(object):
    inMemLock_ = new Object();
    fileLoc_ = new Object();


    def SerializeEntry(self, e):
        lock (fileLoc_)
        {
            registryCsvFileWriter_.WriteLine(
                e.datasetName + "," +
                e.origPngName + "," +
                e.origLabel + "," +
                e.synthPngName + "," +
                e.synthLabel + "," +
                e.lInfDist + "," +
                e.l1Dist + "," +
                e.confOrig + "," +
                e.sndBestDiffOrig + "," +
                e.confSynth + "," +
                e.sndBestDiffSynth)
            registryCsvFileWriter_.Flush()
        }

    def  __init__(self, csvFileName, dataDirectory):
        self.csvFileName_ = csvFileName
        self.registryCsvFileWriter_ = new StreamWriter(csvFileName)
        self.dataDirectory_ = dataDirectory

        exists = System.IO.Directory.Exists(dataDirectory)
        if !exists:
            System.IO.Directory.CreateDirectory(dataDirectory)

        if self.registryCsvFileWriter_ == None:
            raise Exception("Can't open counterexample registry file!")



    def CreatePnG(self, origin, datasetname, datasetIndex, input, scale,  offset, numRows, numCols, isColor, isRowOrder = True):
        path = Path.Combine(dataDirectory_, origin + "-" + datasetname + "-" + datasetIndex + ".png")

        if RobustnessOptions.SavePNGCounterexamples:
            """// Create PnG file for orig"""
            imagePixels = Utils.UArray.ToRGBArray(input, scale, offset)
            Bitmap image = isColor ?
                Utils.UDraw.DrawRGBPixels(imagePixels, numRows, numCols, isRowOrder) :
                Utils.UDraw.DrawGrayscalePixels(imagePixels, numRows, numCols, isRowOrder)
            image.Save(path)
        return path

def RecordAtomically(self, datasetName, datasetIndex, origLab, synthLab, scale, offset, numRows, numCols, isColor, isRowOrder = True):
        e = SynthEntry()
        e.datasetName = datasetName

        e.origPngName = CreatePnG("orig", datasetName, datasetIndex, origLab.datum, scale, offset, numRows, numCols, isColor, isRowOrder)
        e.origLabel = origLab.actualLabel

        e.synthPngName = CreatePnG("snth", datasetName, datasetIndex, synthLab.datum, scale, offset, numRows, numCols, isColor, isRowOrder)
        e.synthLabel = synthLab.actualLabel

        diff = [None] * len(origLab.datum)
        for i in  range(len(origLab.datum)):
            diff[i] = 5 * (origLab.datum[i] - synthLab.datum[i]) + 100

        CreatePnG("diffx5o100", datasetName, datasetIndex,diff,scale,offset,numRows,numCols,isColor,isRowOrder)

        print "Orig path  =" + e.origPngName
        print "Synth path =" + e.synthPngName


        e.lInfDist = Utils.UMath.LInfinityDistance(origLab.datum, synthLab.datum)
        e.l1Dist = Utils.UMath.L1Distance(origLab.datum, synthLab.datum)

        e.confOrig = origLab.softMaxValue
        e.confSynth = synthLab.softMaxValue

        e.sndBestDiffOrig = origLab.diffFromSecondBest
        e.sndBestDiffSynth = synthLab.diffFromSecondBest

        self.SerializeEntry(e)
