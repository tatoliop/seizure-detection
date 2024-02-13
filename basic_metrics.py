from sklearn import metrics
import numpy as np


class basic_metricor:
    def __init__(self, alpha=0.2, metric_outlierness=3, bias='flat' ):
        self.alpha = alpha
        self.metric_outlierness = metric_outlierness
        self.bias = bias

    def w(self, AnomalyRange, p):
        MyValue = 0
        MaxValue = 0
        start = AnomalyRange[0]
        AnomalyLength = AnomalyRange[1] - AnomalyRange[0] + 1
        for i in range(start, start + AnomalyLength):
            bi = self.b(i, AnomalyLength)
            MaxValue += bi
            if i in p:
                MyValue += bi
        return MyValue / MaxValue

    def Cardinality_factor(self, Anomolyrange, Prange):
        score = 0
        start = Anomolyrange[0]
        end = Anomolyrange[1]
        for i in Prange:
            if i[0] >= start and i[0] <= end:
                score += 1
            elif start >= i[0] and start <= i[1]:
                score += 1
            elif end >= i[0] and end <= i[1]:
                score += 1
            elif start >= i[0] and end <= i[1]:
                score += 1
        if score == 0:
            return 0
        else:
            return 1 / score

    def b(self, i, length):
        bias = self.bias
        if bias == 'flat':
            return 1
        elif bias == 'front-end bias':
            return length - i + 1
        elif bias == 'back-end bias':
            return i
        else:
            if i <= length / 2:
                return i
            else:
                return length - i + 1

    def metric_new(self, label, score):
        '''input:
               Real labels and anomaly score in prediction

           output:
               AUC,
               Precision,
               Recall,
               F-score,
               Range-precision,
               Range-recall,
               Range-Fscore,
               Precison@k,

            k is chosen to be # of outliers in real labels
        '''
        if np.sum(label) == 0:
            print('All labels are 0. Label must have groud truth value for calculating AUC score.')
            return None

        if np.isnan(score).any() or score is None:
            print('Score must not be none.')
            return None

        # area under curve
        auc = metrics.roc_auc_score(label, score)

        # precision, recall, F
        preds = score > (np.mean(score) + self.metric_outlierness * np.std(score))
        Precision, Recall, F, Support = metrics.precision_recall_fscore_support(label, preds, zero_division=0)
        precision = Precision[1]
        recall = Recall[1]
        f = F[1]

        # range anomaly
        Rrecall, ExistenceReward, OverlapReward = self.range_recall_new(label, preds, self.alpha)
        Rprecision = self.range_recall_new(preds, label, 0)[0]

        if Rprecision + Rrecall == 0:
            Rf = 0
        else:
            Rf = 2 * Rrecall * Rprecision / (Rprecision + Rrecall)

        # top-k
        k = int(np.sum(label))
        threshold = np.percentile(score, 100 * (1 - k / len(label)))

        # precision_at_k = metrics.top_k_accuracy_score(label, score, k)
        p_at_k = np.where(preds > threshold)[0]
        TP_at_k = sum(label[p_at_k])
        precision_at_k = TP_at_k / k

        L = [auc, precision, recall, f, Rrecall, ExistenceReward, OverlapReward, Rprecision, Rf, precision_at_k]
        return L


    def range_recall_new(self, labels, preds, alpha):

        p = np.where(preds == 1)[0]  # positions of predicted label==1
        range_pred = self.range_convers_new(preds)
        range_label = self.range_convers_new(labels)

        Nr = len(range_label)  # total # of real anomaly segments

        ExistenceReward = self.existence_reward(range_label, p)

        OverlapReward = 0
        for i in range_label:
            OverlapReward += self.w(i, p) * self.Cardinality_factor(i, range_pred)

        score = alpha * ExistenceReward + (1 - alpha) * OverlapReward
        if Nr != 0:
            return score / Nr, ExistenceReward / Nr, OverlapReward / Nr
        else:
            return 0, 0, 0

    def range_convers_new(self, label):
        '''
        input: arrays of binary values
        output: list of ordered pair [[a0,b0], [a1,b1]... ] of the inputs
        '''
        L = []
        i = 0
        j = 0
        while j < len(label):
            # print(i)
            while label[i] == 0:
                i += 1
                if i >= len(label):
                    break
            j = i + 1
            # print('j'+str(j))
            if j >= len(label):
                if j == len(label):
                    L.append((i, j - 1))

                break
            while label[j] != 0:
                j += 1
                if j >= len(label):
                    L.append((i, j - 1))
                    break
            if j >= len(label):
                break
            L.append((i, j - 1))
            i = j
        return L

    def existence_reward(self, labels, preds):
        '''
        labels: list of ordered pair
        preds predicted data
        '''

        score = 0
        for i in labels:
            if np.sum(np.multiply(preds <= i[1], preds >= i[0])) > 0:
                score += 1
        return score

