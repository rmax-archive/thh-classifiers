# -*- coding: utf-8 -*-
from sklearn.metrics import accuracy_score


def mc_accuracy_score(y_true, y_pred, level=1, normalize=True, sample_weight=None):
    y_truel = y_true.apply(lambda l: l[level])
    y_predl = y_pred.apply(lambda l: l[level])
    return accuracy_score(y_truel, y_predl, normalize, sample_weight)