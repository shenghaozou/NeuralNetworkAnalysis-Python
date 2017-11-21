import Dataset
import Utils
import math
class NNAccuracy(object):
    lockObject = None

    @staticmethod
    def Filter(nn, ds, predicate):
        ret = Dataset(ds.LabelCount())

        for i in range(ds.Count()):
            datum = ds.GetDatum(i)
            ground_label = ds.GetLabel(i)

            if predicate(nn,datum,ground_label):
                ret.Data.Add(Dataset.MemAccessor(datum))
                ret.Labels.Add(Dataset.MemAccessor(ground_label))

        return ret

    @staticmethod
    def KeepAboveConfidenceThreshold(net, ds, conf):
        return Filter(net,ds, (nn, datum, ground_label) =>
            LabelWithConfidence lab = Utils.ULabel.LabelWithConfidence(nn, datum, true)
            return (lab.softMaxValue >= conf)

    @staticmethod
    def KeepMisclass(net, ds):
        return Filter(net, ds, (nn, datum, ground_label) =>
        {
            LabelWithConfidence lab = Utils.ULabel.LabelWithConfidence(nn, datum, true);
            return (lab.actualLabel != ground_label);

    @staticmethod
    def GetAccuracy(nn, ds):
        cnt = 0
        prg = 0

        for i in range(ds.Count()):
            datum = ds.GetDatum(i)
            ground_label = ds.GetLabel(i)


            labconf = Utils.ULabel.LabelWithConfidence(nn,ds.GetDatum(i),True)
            label = labconf.actualLabel

            lock (lockObject)
                prg+=1

            if label == ground_label:
                lock (lockObject)
                    cnt+=1

            lock (lockObject)
            {
                print "{0:f}, Accuracy:{1:f}".format( float(prg) * 100.0 / ds.Count(), float(cnt) * 100.0 / prg)
            }


        print "\nCorrectly classified = " + `cnt`
        print "Total images         = " + `ds.Count()`

        acc = float(cnt) / ds.Count()
        print "\nAccuracy: "+ `acc`
        print "ReLU Collisions = " + Instrumentation.Collisions
        return acc


    @staticmethod
    def GetLoss(nn, ds):
        loss = 0.0
        prg = 0
        Parallel.For(0, ds.Count(), RobustnessOptions.ParallelOptions, i =>
            softmax = Utils.ULabel.RunWithSoftmax(nn, ds.GetDatum(i), True)
            lock (lockObject)
                prg+=1
                lab = ds.GetLabel(i)


                if softmax[lab] == 0.0:
                    softmax[lab] += 1e-10

                loss += math.log(softmax[lab])
                print "{0:0.000}%".format( float(prg * 100.0 / ds.Count()))


        print "\nTotal loss: " + `loss`


        return loss