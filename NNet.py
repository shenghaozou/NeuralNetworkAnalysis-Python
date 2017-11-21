from abc import ABC, abstractmethod
from __future__ import *
from enum import Enum

class LayerType(Enum):
    RECTIFIED_LINEAR = 1
    INNER_PRODUCT = 2
    LOSS = 3
    CONVOLUTION_LAYER = 4
    POOLING_LAYER = 5
    VIRTUAL_LAYER = 6
    DATA_LAYER = 7


"""
/// <summary>
///  A layer of the neural network and the operations it supports
/// <summary>
"""


class Layer(ABC):
    def InitLayer(self, index, layerType, inputDimension, outputDimension, inputCoordinates, outputCoordinates):
        self.index_ = index
        self.layerType_ = layerType
        self.inputDimension_ = inputDimension
        self.outputDimension_ = outputDimension
        self.inputCoordinates_ = inputCoordinates
        self.outputCoordinates_ = outputCoordinates

    @abstractmethod
    def EvaluateSymbolic(self, state, input):
        pass

    @abstractmethod
    def EvaluateConcrete(self, input):
        pass

    @abstractmethod
    def Instrument(self, instrumentation, input, output):
        pass

    @abstractmethod
    def IsAffine(self):
        pass

    """
    // / < summary >
    // / A neural network: just a collection of layers
    // / < / summary > \
    """
class NeuralNet:
    """
    // We elevate cropping to a first-class citizen of a neural network
    // to expose it to the symbolic evaluator. If cropT == null, then no
    // cropping happens.
    """
    def __init__(self):
        self.cropT = None
        self.layers_ = []

    def AddCropTransform(self, crop):
        self.cropT = crop
    def AddLayer(self, layer):
        self.layers_.append(layer)

    def LayerCount(self):
        return len(self.layers_)

    def InputDimensionPostCrop(self):
        return self.layers_[0].InputDimension

    def InputDimensionPreCrop(self):
        if self.cropT != None:
            return self.cropT.OriginalDimension()
        else:
            return self.layers_[0].InputDimension

    def CropMaybe(self, image):
        if self.cropT != None:
            return self.cropT.Transform(image)
        else:
            return image

    def UnCropMaybe(self, orig, image):
        if self.cropT != None:
            return self.cropT.UnTransform(orig, image)
        else:
            return image

    def LayerTypes(self):
        layerTypes = []
        for i in range(self.LayerCount()):
            layerTypes.append(self.layers_[i].LayerType)
        return layerTypes

    def EvaluateNNConcretePostCrop(self, input, instr = None):
        return EvaluateNNConcretePostCrop(DenseVector.OfArray(input), instr)

    def EvaluateNNConcretePostCrop(self, input, instr):
        v = input
        for i in range(self.LayerCount()):
            curr = self.layers_[i]
            w = curr.EvaluateConcrete(v)
            if instr != None:
                curr.Instrument(instr, v, w)
                v = w
        return v

    def EvaluateNNSymbolicPostCrop(self, state, input):
        v = input
        for i in range(self.LayerCount()):
            curr = self.layers_[i]
            stopwatch = Stopwatch()
            stopwatch.Start()
            w = curr.EvaluateSymbolic(state, v)
            stopwatch.Stop()
            v = w
            print "Symbolic interpreter: layer index:" + `curr.Index` + ", elapsed milliseconds = " + `stopwatch.ElapsedMilliseconds`
        return v


     def CoalesceToVirtual(self):
        newLayers = []
        currAffList = []
        for i in range(self.LayerCount()):
            curr = self.layers_[i]
            if curr.IsAffine():
                currAffList.append(curr)
                continue
            """
            // Current layer is not affine
            // If we have anything in the affine list, we should coalesce and insert before current.
            """
            if len(currAffList) > 0:
                virt = VirtualLayer(currAffList)
                currAffList.Clear()
                newLayers.append(virt)
            newLayers.append(curr)

        if len(currAffList) > 0:
            virt = VirtualLayer(currAffList)
            currAffList.Clear()
            newLayers.append(virt)
        newLayers.append(curr)
