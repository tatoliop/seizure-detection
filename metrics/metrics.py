import numpy as np
from sklearn import metrics

from utils.constants import EVAL_COEFF_DEFAULT, EVAL_ALPHA_DEFAULT
from utils.enums import Metrics_enum


class Metrics:
    __point_auc_roc = 'Point_AUC_ROC'
    __point_auc_pr = 'Point_AUC_PR'
    __point_precision = 'Point_Precision'
    __point_recall = 'Point_Recall'
    __point_f = 'Point_F'
    __range_precision = 'Range_Precision'
    __range_recall = 'Range_Recall'
    __range_existence = 'Existence_reward'
    __range_overlap = 'Overlap_reward'
    __range_f = 'Range_F'
    __range_auc_roc = 'Range_AUC_ROC'
    __range_auc_pr = 'Range_AUC_PR'
    __vus_roc = 'VUS_ROC'
    __vus_pr = 'VUS_PR'
    __bias = 'flat'  # TODO the diffs in values from TSB

    def metrics(self, type: Metrics_enum, score: np.array, label: np.array, coeff: float = EVAL_COEFF_DEFAULT,
                alpha: float = EVAL_ALPHA_DEFAULT, subsequence_size: int = 1):
        if type == Metrics_enum.POINT:
            return self.__point_metrics(score, label, coeff)
        else:
            point_metrics = self.__point_metrics(score, label, coeff)
            range_metrics = self.__range_metrics(score, label, coeff, alpha, subsequence_size)
            vus_metrics = self.__vus_metrics(score, label, subsequence_size)
            return point_metrics | range_metrics | vus_metrics

    def __point_metrics(self, score: np.array, label: np.array, coeff: float) -> dict:
        # Get binary
        binary = self.__transform_binary(score, coeff)
        # Get metrics
        auc = metrics.roc_auc_score(label, score)
        auc_pr = metrics.average_precision_score(label, score)
        Precision, Recall, F, Support = metrics.precision_recall_fscore_support(label, binary, zero_division=0)
        precision = Precision[1]
        recall = Recall[1]
        f = F[1]
        return {
            self.__point_auc_roc: auc,
            self.__point_auc_pr: auc_pr,
            self.__point_precision: precision,
            self.__point_recall: recall,
            self.__point_f: f
        }

    def __range_metrics(self, score, label, coeff, alpha, subsequence_size):
        # Get binary
        binary = self.__transform_binary(score, coeff)
        # range anomaly
        Rrecall, ExistenceReward, OverlapReward = self.__range_recall_new(label, binary, alpha)
        Rprecision = self.__range_recall_new(binary, label, 0)[0]
        if Rprecision + Rrecall == 0:
            Rf = 0
        else:
            Rf = 2 * Rrecall * Rprecision / (Rprecision + Rrecall)
        R_AUC_ROC, R_AUC_PR = self.__RangeAUC(labels=label, score=score, window=subsequence_size)
        return {
            self.__range_recall: Rrecall,
            self.__range_existence: ExistenceReward,
            self.__range_overlap: OverlapReward,
            self.__range_precision: Rprecision,
            self.__range_f: Rf,
            self.__range_auc_roc: R_AUC_ROC,
            self.__range_auc_pr: R_AUC_PR,
        }

    def __vus_metrics(self, score, label, subsequence_size):
        VUS_ROC, VUS_PR = self.__generate_curve(label, score, subsequence_size)
        return {
            self.__vus_roc: VUS_ROC,
            self.__vus_pr: VUS_PR
        }

    def __transform_binary(self, score, coeff):
        # precision, recall, F
        preds = score > (np.mean(score) + coeff * np.std(score))
        return preds

    def __range_recall_new(self, labels, preds, alpha):

        p = np.where(preds == 1)[0]  # positions of predicted label==1
        range_pred = self.__range_convers_new(preds)
        range_label = self.__range_convers_new(labels)

        Nr = len(range_label)  # total # of real anomaly segments

        ExistenceReward = self.__existence_reward(range_label, p)

        OverlapReward = 0
        for i in range_label:
            OverlapReward += self.__w(i, p) * self.__Cardinality_factor(i, range_pred)

        score = alpha * ExistenceReward + (1 - alpha) * OverlapReward
        if Nr != 0:
            return score / Nr, ExistenceReward / Nr, OverlapReward / Nr
        else:
            return 0, 0, 0

    @staticmethod
    def __range_convers_new(label):
        '''
        input: arrays of binary values
        output: list of ordered pair [[a0,b0], [a1,b1]... ] of the inputs
        '''
        L = []
        i = 0
        j = 0
        while j < len(label):
            while label[i] == 0:
                i += 1
                if i >= len(label):
                    break
            j = i + 1
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

    @staticmethod
    def __existence_reward(labels, preds):
        '''
        labels: list of ordered pair
        preds predicted data
        '''

        score = 0
        for i in labels:
            if np.sum(np.multiply(preds <= i[1], preds >= i[0])) > 0:
                score += 1
        return score

    def __w(self, AnomalyRange, p):
        MyValue = 0
        MaxValue = 0
        start = AnomalyRange[0]
        AnomalyLength = AnomalyRange[1] - AnomalyRange[0] + 1
        for i in range(start, start + AnomalyLength):
            bi = self.__b(i, AnomalyLength)
            MaxValue += bi
            if i in p:
                MyValue += bi
        return MyValue / MaxValue

    def __b(self, i, length):
        bias = self.__bias
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

    @staticmethod
    def __Cardinality_factor(Anomolyrange, Prange):
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

    def __RangeAUC(self, labels, score, window=0, percentage=0, AUC_type='window'):
        # AUC_type='window'/'percentage'
        score_sorted = -np.sort([-x for x in score])

        P = np.sum(labels)
        if AUC_type == 'window':
            labels = self.__extend_postive_range(labels, window=window)
        else:
            labels = self.__extend_postive_range_individual(labels, percentage=percentage)

        L = self.__range_convers_new(labels)
        TF_list = np.zeros((252, 2))
        Precision_list = np.ones(251)
        j = 0
        for i in np.linspace(0, len(score) - 1, 250).astype(int):
            threshold = score_sorted[i]
            pred = score >= threshold
            TPR, FPR, Precision = self.__TPR_FPR_RangeAUC(labels, pred, P, L)
            j += 1
            TF_list[j] = [TPR, FPR]
            Precision_list[j] = (Precision)

        TF_list[j + 1] = [1, 1]

        width = TF_list[1:, 1] - TF_list[:-1, 1]
        height = (TF_list[1:, 0] + TF_list[:-1, 0]) / 2
        AUC_range = np.dot(width, height)

        width_PR = TF_list[1:-1, 0] - TF_list[:-2, 0]
        height_PR = (Precision_list[1:] + Precision_list[:-1]) / 2
        AP_range = np.dot(width_PR, height_PR)

        return AUC_range, AP_range

    def __extend_postive_range(self, x, window=5):
        label = x.copy().astype(float)
        L = self.__range_convers_new(label)  # index of non-zero segments
        length = len(label)
        for k in range(len(L)):
            s = L[k][0]
            e = L[k][1]

            x1 = np.arange(e + 1, min(e + window // 2 + 1, length))
            label[x1] += np.sqrt(1 - (x1 - e) / (window))

            x2 = np.arange(max(s - window // 2, 0), s)
            label[x2] += np.sqrt(1 - (s - x2) / (window))

        label = np.minimum(np.ones(length), label)
        return label

    def __extend_postive_range_individual(self, x, percentage=0.2):
        label = x.copy().astype(float)
        L = self.__range_convers_new(label)  # index of non-zero segments
        length = len(label)
        for k in range(len(L)):
            s = L[k][0]
            e = L[k][1]

            l0 = int((e - s + 1) * percentage)

            x1 = np.arange(e, min(e + l0, length))
            label[x1] += np.sqrt(1 - (x1 - e) / (2 * l0))

            x2 = np.arange(max(s - l0, 0), s)
            label[x2] += np.sqrt(1 - (s - x2) / (2 * l0))

        label = np.minimum(np.ones(length), label)
        return label

    def __TPR_FPR_RangeAUC(self, labels, pred, P, L):
        product = labels * pred

        TP = np.sum(product)

        # recall = min(TP/P,1)
        P_new = (P + np.sum(labels)) / 2  # so TPR is neither large nor small
        # P_new = np.sum(labels)
        recall = min(TP / P_new, 1)
        # recall = TP/np.sum(labels)

        existence = 0
        for seg in L:
            if np.sum(product[seg[0]:(seg[1] + 1)]) > 0:
                existence += 1

        existence_ratio = existence / len(L)

        # TPR_RangeAUC = np.sqrt(recall*existence_ratio)
        TPR_RangeAUC = recall * existence_ratio

        FP = np.sum(pred) - TP
        # TN = np.sum((1-pred) * (1-labels))

        # FPR_RangeAUC = FP/(FP+TN)
        N_new = len(labels) - P_new
        FPR_RangeAUC = FP / N_new

        Precision_RangeAUC = TP / np.sum(pred)

        return TPR_RangeAUC, FPR_RangeAUC, Precision_RangeAUC

    def __generate_curve(self, label, score, slidingWindow, version='opt', thre=250):
        if version == 'opt_mem':
            tpr_3d, fpr_3d, prec_3d, window_3d, avg_auc_3d, avg_ap_3d = self.RangeAUC_volume_opt_mem(
                labels_original=label, score=score, windowSize=slidingWindow, thre=thre)
        else:
            tpr_3d, fpr_3d, prec_3d, window_3d, avg_auc_3d, avg_ap_3d = self.RangeAUC_volume_opt(
                labels_original=label, score=score, windowSize=slidingWindow, thre=thre)

        # X = np.array(tpr_3d).reshape(1, -1).ravel()
        # X_ap = np.array(tpr_3d)[:, :-1].reshape(1, -1).ravel()
        # Y = np.array(fpr_3d).reshape(1, -1).ravel()
        # W = np.array(prec_3d).reshape(1, -1).ravel()
        # Z = np.repeat(window_3d, len(tpr_3d[0]))
        # Z_ap = np.repeat(window_3d, len(tpr_3d[0]) - 1)
        # return Y, Z, X, X_ap, W, Z_ap, avg_auc_3d, avg_ap_3d
        return avg_auc_3d, avg_ap_3d

    def RangeAUC_volume_opt_mem(self, labels_original, score, windowSize, thre=250):
        window_3d = np.arange(0, windowSize + 1, 1)
        P = np.sum(labels_original)
        seq = self.__range_convers_new(labels_original)
        l = self.__new_sequence(labels_original, seq, windowSize)

        score_sorted = -np.sort(-score)

        tpr_3d = np.zeros((windowSize + 1, thre + 2))
        fpr_3d = np.zeros((windowSize + 1, thre + 2))
        prec_3d = np.zeros((windowSize + 1, thre + 1))

        auc_3d = np.zeros(windowSize + 1)
        ap_3d = np.zeros(windowSize + 1)

        tp = np.zeros(thre)
        N_pred = np.zeros(thre)
        p = np.zeros((thre, len(score)))

        for k, i in enumerate(np.linspace(0, len(score) - 1, thre).astype(int)):
            threshold = score_sorted[i]
            pred = score >= threshold
            p[k] = pred
            N_pred[k] = np.sum(pred)

        for window in window_3d:

            labels = self.__sequencing(labels_original, seq, window)
            L = self.__new_sequence(labels, seq, window)

            TF_list = np.zeros((thre + 2, 2))
            Precision_list = np.ones(thre + 1)
            j = 0
            N_labels = 0

            for seg in l:
                N_labels += np.sum(labels[seg[0]:seg[1] + 1])

            for i in np.linspace(0, len(score) - 1, thre).astype(int):

                TP = 0
                for seg in l:
                    TP += np.dot(labels[seg[0]:seg[1] + 1], p[j][seg[0]:seg[1] + 1])

                TP += tp[j]
                FP = N_pred[j] - TP

                existence = 0
                for seg in L:
                    if np.dot(labels[seg[0]:(seg[1] + 1)], p[j][seg[0]:(seg[1] + 1)]) > 0:
                        existence += 1

                existence_ratio = existence / len(L)

                P_new = (P + N_labels) / 2
                recall = min(TP / P_new, 1)

                TPR = recall * existence_ratio
                N_new = len(labels) - P_new
                FPR = FP / N_new

                Precision = TP / N_pred[j]
                j += 1

                TF_list[j] = [TPR, FPR]
                Precision_list[j] = Precision

            TF_list[j + 1] = [1, 1]

            tpr_3d[window] = TF_list[:, 0]
            fpr_3d[window] = TF_list[:, 1]
            prec_3d[window] = Precision_list

            width = TF_list[1:, 1] - TF_list[:-1, 1]
            height = (TF_list[1:, 0] + TF_list[:-1, 0]) / 2
            AUC_range = np.dot(width, height)
            auc_3d[window] = (AUC_range)

            width_PR = TF_list[1:-1, 0] - TF_list[:-2, 0]
            height_PR = (Precision_list[1:] + Precision_list[:-1]) / 2
            AP_range = np.dot(width_PR, height_PR)
            ap_3d[window] = (AP_range)

        return tpr_3d, fpr_3d, prec_3d, window_3d, sum(auc_3d) / len(window_3d), sum(ap_3d) / len(window_3d)

    def RangeAUC_volume_opt(self, labels_original, score, windowSize, thre=250):
        window_3d = np.arange(0, windowSize + 1, 1)
        P = np.sum(labels_original)
        seq = self.__range_convers_new(labels_original)
        l = self.__new_sequence(labels_original, seq, windowSize)

        score_sorted = -np.sort([-x for x in score])

        tpr_3d = np.zeros((windowSize + 1, thre + 2))
        fpr_3d = np.zeros((windowSize + 1, thre + 2))
        prec_3d = np.zeros((windowSize + 1, thre + 1))

        auc_3d = np.zeros(windowSize + 1)
        ap_3d = np.zeros(windowSize + 1)

        tp = np.zeros(thre)
        N_pred = np.zeros(thre)

        for k, i in enumerate(np.linspace(0, len(score) - 1, thre).astype(int)):
            threshold = score_sorted[i]
            pred = score >= threshold
            N_pred[k] = np.sum(pred)

        for window in window_3d:

            labels = self.__sequencing(labels_original, seq, window)
            L = self.__new_sequence(labels, seq, window)

            TF_list = np.zeros((thre + 2, 2))
            Precision_list = np.ones(thre + 1)
            j = 0
            N_labels = 0

            for seg in l:
                N_labels += np.sum(labels[seg[0]:seg[1] + 1])

            for i in np.linspace(0, len(score) - 1, thre).astype(int):
                threshold = score_sorted[i]
                pred = score >= threshold

                TP = 0
                for seg in l:
                    TP += np.dot(labels[seg[0]:seg[1] + 1], pred[seg[0]:seg[1] + 1])

                TP += tp[j]
                FP = N_pred[j] - TP

                existence = 0
                for seg in L:
                    if np.dot(labels[seg[0]:(seg[1] + 1)], pred[seg[0]:(seg[1] + 1)]) > 0:
                        existence += 1

                existence_ratio = existence / len(L)

                P_new = (P + N_labels) / 2
                recall = min(TP / P_new, 1)

                TPR = recall * existence_ratio
                N_new = len(labels) - P_new
                FPR = FP / N_new

                Precision = TP / N_pred[j]

                j += 1
                TF_list[j] = [TPR, FPR]
                Precision_list[j] = Precision

            TF_list[j + 1] = [1, 1]  # otherwise, range-AUC will stop earlier than (1,1)

            tpr_3d[window] = TF_list[:, 0]
            fpr_3d[window] = TF_list[:, 1]
            prec_3d[window] = Precision_list

            width = TF_list[1:, 1] - TF_list[:-1, 1]
            height = (TF_list[1:, 0] + TF_list[:-1, 0]) / 2
            AUC_range = np.dot(width, height)
            auc_3d[window] = (AUC_range)

            width_PR = TF_list[1:-1, 0] - TF_list[:-2, 0]
            height_PR = (Precision_list[1:] + Precision_list[:-1]) / 2

            AP_range = np.dot(width_PR, height_PR)
            ap_3d[window] = AP_range

        return tpr_3d, fpr_3d, prec_3d, window_3d, sum(auc_3d) / len(window_3d), sum(ap_3d) / len(window_3d)

    @staticmethod
    def __new_sequence(label, sequence_original, window):
        a = max(sequence_original[0][0] - window // 2, 0)
        sequence_new = []
        for i in range(len(sequence_original) - 1):
            if sequence_original[i][1] + window // 2 < sequence_original[i + 1][0] - window // 2:
                sequence_new.append((a, sequence_original[i][1] + window // 2))
                a = sequence_original[i + 1][0] - window // 2
        sequence_new.append((a, min(sequence_original[len(sequence_original) - 1][1] + window // 2, len(label) - 1)))
        return sequence_new

    @staticmethod
    def __sequencing(x, L, window=5):
        label = x.copy().astype(float)
        length = len(label)

        for k in range(len(L)):
            s = L[k][0]
            e = L[k][1]

            x1 = np.arange(e + 1, min(e + window // 2 + 1, length))
            label[x1] += np.sqrt(1 - (x1 - e) / (window))

            x2 = np.arange(max(s - window // 2, 0), s)
            label[x2] += np.sqrt(1 - (s - x2) / (window))

        label = np.minimum(np.ones(length), label)
        return label
