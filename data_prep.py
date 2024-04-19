from tkinter import N
import numpy as np
import sys
import shutil
import pandas as pd
import time
import re
import pickle

dataset = sys.argv[1]

# thresholds = {"spambase": -0.8}
# tot_points = {"spambase": 3681}

def split_dataset(X_train, y_train):
    N = X_train.shape[0]
    # ind = np.random.choice(range(N), size=round(N), replace=False)
    ind = np.random.permutation(N)
    ind1 = ind[:round(N/3)]
    ind2 = ind[round(N/3):round(2*N/3)]
    ind3 = ind[round(2*N/3):]

    Xs1 = X_train[ind1,:]
    Xs2 = X_train[ind2,:]
    Xs3 = X_train[ind3,:]
    ys1 = y_train[ind1]
    ys2 = y_train[ind2]
    ys3 = y_train[ind3]

    return [Xs1, Xs2, Xs3], [ys1, ys2, ys3]

def local_entropy(xin, yin, bins):
    N = xin.shape[0]
    H, xe, ye = np.histogram2d(xin, yin.reshape(yin.shape[0]), bins=bins, range=[[0,1],[0,1]])
    H = H/N
    Exy = np.array([-x*np.log2(x) for x in H.flatten() if x > 0]).sum()
    return Exy

def local_entropies(X, y, bins):
    out = []
    F, T = split_dataset(X, y)
    for Xs,ys in zip(F,T):
        row = [local_entropy(xs,ys,bins) for xs in Xs.transpose()]
        out.append(row)
    return out

def get_entropy(H):
    return np.array([-x*np.log2(x) for x in H.flatten() if x > 0]).sum()

def get_logs(H, cutoff=1e-4):
    Htmp = np.array([max(h,cutoff) for h in H])
    return np.array([np.log2(x) for x in Htmp])


if dataset == "spo2":
    binsx = 20
    binsy = 2

    rangex = [0,300]
    rangey = [0,1]
    
    dfX = pd.read_csv('./Player-Data/Xdata_hist.txt', sep=' ', header=None)
    dfy = pd.read_csv('./Player-Data/ydata_hist.txt', sep=' ', header=None)

if dataset == "synth_big":
    binsx = 35
    binsy = 35

    rangex = [-1,1]
    rangey = [-1,1]
    
    dfX = pd.read_csv('./Player-Data/X_synth_big.txt', sep=' ', header=None)
    dfy = pd.read_csv('./Player-Data/y_synth_big.txt', sep=' ', header=None)

if dataset == "spambase":
    binsx = 10
    binsy = 2

    rangex = [-1,1]
    rangey = [0,1]

    dfX = pd.read_csv('./Player-Data/X_spambase.txt', sep=' ', header=None)
    dfy = pd.read_csv('./Player-Data/y_spambase.txt', sep=' ', header=None)

if dataset == "gisette":
    binsx = 30
    binsy = 2

    rangex = [0,1000]
    rangey = [-1,1]

    dfX = pd.read_csv('./Player-Data/X_gisette.txt', sep=' ', header=None)
    dfy = pd.read_csv('./Player-Data/y_gisette.txt', sep=' ', header=None)

if dataset == "SD_without":
    binsx = 30
    binsy = 2

    # fix this
    # rangex = [-1,1]
    # not using speed data
    rangex = [-1,258]
    rangey = [0,1]

    dfX = pd.read_csv('./Player-Data/X_SD_without_120_121.txt', sep=' ', header=None)
    dfy = pd.read_csv('./Player-Data/y_SD_without_120_121.txt', sep=' ', header=None)

Xt = dfX.values.transpose()
y = dfy.values

if dataset == "spambase":
    # Xt = np.array([(cc-cc.min())/(cc.max()-cc.min()) for cc in Xt])
    Xt = np.array([(cc-cc.mean())/(4*cc.std()) for cc in Xt])

N = Xt.shape[1]
Xs, ys = split_dataset(Xt.transpose(), y)

weights = [Xs[ii].shape[0]/N for ii in [0,1,2]]
cutoff = 1e-4

tic = time.time()
for party in [0,1,2]:
    coll = []
    coll2 = []
    coll2c = []
    coll3 = []

    # for MI
    coll4 = []

    Hy, tmp_ = np.histogram(ys[party], bins=binsy, range=rangey)
    Hy = Hy/ys[party].shape[0]
    coll5 = [list(Hy.flatten()*weights[party])]

    for rr in Xs[party].transpose():

        Nloc = Xs[party].shape[0]

        Hjoint, tmp1, tmp2 = np.histogram2d(rr, ys[party].reshape(ys[party].shape[0]), bins=[binsx, binsy], range=[rangex, rangey])
        H, tmp3 = np.histogram(rr, bins=binsx, range=rangex)

        Hjoint = Hjoint/Nloc
        H = H/Nloc
        Hc = np.array([max(h,cutoff) for h in H])

        Hxy = get_entropy(Hjoint)
        xlogs = get_logs(H, cutoff=cutoff)

        coll.append(xlogs*weights[party])
        coll2.append(H*weights[party])
        coll2c.append(Hc*weights[party])
        coll3.append([Hxy*weights[party]])

        # for MI
        hjoint = Hjoint.flatten()
        coll4.append(hjoint*weights[party])

    
    coll = np.array(coll).transpose()
    coll2 = np.array(coll2).transpose()
    coll2c = np.array(coll2c).transpose()
    coll4 = np.array(coll4).transpose()
    coll5 = np.array(coll5).transpose()

    coll_prep = [list(c) for c in coll]
    pickle.dump(coll_prep, open("./Player-Data/L%s.p" % party, 'wb'))

    coll_prep2 = [list(c) for c in coll2]
    pickle.dump(coll_prep2, open("./Player-Data/P%s.p" % party, 'wb'))

    coll_prep2c = [list(c) for c in coll2c]
    pickle.dump(coll_prep2c, open("./Player-Data/P%sc.p" % party, 'wb'))

    coll_prep3 = [list(c) for c in coll3]
    pickle.dump(coll_prep3, open("./Player-Data/Hxy%s.p" % party, 'wb'))

    # for MI
    coll_prep4 = [list(c) for c in coll4]
    pickle.dump(coll_prep4, open("./Player-Data/hjoint%s.p" % party, 'wb'))

    pickle.dump(coll5, open("./Player-Data/hy%s.p" % party, 'wb'))