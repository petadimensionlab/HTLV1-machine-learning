import math
import time
import numpy as np
import itertools
import shap

from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
from sklearn.svm import SVC
from xgboost import XGBClassifier

from multiprocessing import Pool


def cumpute_shap_value_KernelExplainer(rs_idx, ind_b_ml, X, X_scaled, y, clf_name):

    
    print(f"\nindex : {rs_idx}")
    
    b_ml = ind_b_ml[clf_name]

    print(f"{b_ml['name']}")

    all_params = b_ml["best_param"]
    
    if b_ml['name'] == "RandomForest":
        clf = RandomForestClassifier(**all_params)
    
    elif b_ml['name'] == "XGB":
        clf = XGBClassifier(**all_params)
    
    elif b_ml['name'] == "ExtraTrees":
        clf = ExtraTreesClassifier(**all_params)
    
    elif b_ml['name'] == "SVM":
        clf = SVC(**all_params)

    if b_ml['name'] == "SVM":
        clf.fit(X_scaled, y)
        explainer = shap.KernelExplainer(clf.predict_proba, X_scaled)
        class_4_data_shap_values = explainer(X_scaled)
    
    else:
        clf.fit(X.values, y)
        explainer = shap.KernelExplainer(clf.predict_proba, X)
        class_4_data_shap_values = explainer(X)
    
    class_idx0 = [list(y.index).index(j) for j in list(y[y == 0].index)]
    class_idx1 = [list(y.index).index(j) for j in list(y[y == 1].index)]
    class_idx2 = [list(y.index).index(j) for j in list(y[y == 2].index)]
    class_idx3 = [list(y.index).index(j) for j in list(y[y == 3].index)]
    fi0 = [np.median(abs( class_4_data_shap_values.values[class_idx0, j, 0])) for j in range(5) ]
    fi1 = [np.median(abs( class_4_data_shap_values.values[class_idx1, j, 1])) for j in range(5) ]
    fi2 = [np.median(abs( class_4_data_shap_values.values[class_idx2, j, 2])) for j in range(5) ]
    fi3 = [np.median(abs( class_4_data_shap_values.values[class_idx3, j, 3])) for j in range(5) ]


    return [fi0, fi1, fi2, fi3]

def wrapper_cumpute_shap_value_KernelExplainer(args):
    return cumpute_shap_value_KernelExplainer(*args)

def cumpute_shap_value_all_data_multiprocess(n_processes, rs_best_param_dict, X, X_scaled, y, clf_name):

    start = time.time()

    if clf_name == "XGB":
        print("Since XGBoost is not thread-safe, it oftens face problem of hanging and doing nothing.\nSo in only XGBoost, single process is used here.", flush = True)

        shap_value_all_data = []
        for rs_idx in range(len(rs_best_param_dict)):

            shap_value_all_data.append( cumpute_shap_value_KernelExplainer(rs_idx, rs_best_param_dict[rs_idx], X, X_scaled, y, clf_name) )


        time_consumed = time.time() - start
        print(time_consumed, " sec", flush = True)

        return np.array(shap_value_all_data)

    else:

        args = []
        for rs_idx in range(len(rs_best_param_dict)):

            args.append( [rs_idx, rs_best_param_dict[rs_idx], X, X_scaled, y, clf_name] )

        p = Pool(processes=n_processes)
        shap_value_all_data = p.map(wrapper_cumpute_shap_value_KernelExplainer, args)

        time_consumed = time.time() - start
        print(time_consumed, " sec", flush = True)

        return np.array(shap_value_all_data)

