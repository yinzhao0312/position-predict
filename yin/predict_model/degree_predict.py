# coding = utf-8

from sklearn.ensemble import RandomForestClassifier
# from sklearn.ensemble import GradientBoostingClassifier
import pandas as pd
import numpy as np
import codecs
import os
# from data_deal import common_data_deal as dl
import pickle

path = os.path.dirname(__file__) + '/predictFile/'

outFile1 = codecs.open(path + 'degree_rf.txt', 'w', 'utf-8')
outFile2 = codecs.open(path + 'degree_gbdt.txt', 'w', 'utf-8')
# outPkl1 = file(path+'rfSalaryProb.pkl','w')
# outPkl2 = file(path+'gbdtSalaryProb.pkl','w')
inPklFile = file('feature_pkl.pkl', 'r')
trainFeatureAll, testFeatureAll = pickle.load(inPklFile)
feature_num = [str(i) for i in range(40)]
feature_str = ['age', 'gender', 'comSize1', 'comSize3', 'comSizeN', 'salary1', 'salary3', 'salaryN',
               'time1', 'time2', 'time3', 'time4', 'yearN', 'firstAge', 'posi1List',
               'lengthList', 'lv1', 'lv3', 'aver1', 'aver3', 'year2',
               'industry1Num', 'industry3Num', 'salaryLv1List', 'salaryLv3List',
               'yearSalary1List', 'yearSalary3List', 'majorClass', 'majorNum'] + feature_num


def merge_feature(all_feature):
    train_feature = {}
    test_feature = {}
    for word in all_feature:
        train_feature[word] = trainFeatureAll[word]
        test_feature[word] = testFeatureAll[word]
    train_feature = pd.DataFrame(train_feature)
    test_feature = pd.DataFrame(test_feature)
    train_id_list = trainFeatureAll['id']
    test_id_list = testFeatureAll['id']
    train_tar_list = trainFeatureAll['degree']
    return train_feature, test_feature, train_id_list, test_id_list, train_tar_list


def train():
    degree_result = {}
    train_feature, test_feature, train_id_list, test_id_list, train_tar_list = merge_feature(feature_str)
    # tmp = [t<32 for t in trainTarList]
    # tmp = np.array(tmp)
    # trainFeature = trainFeature[tmp]
    target_list = np.array(train_tar_list)
    # target = target[tmp]
    # train_id_list = np.array(train_id_list)
    # trainIdList = trainIdList[tmp]
    c_feature = train_feature.columns[:]
    clf = RandomForestClassifier(n_estimators=200, min_samples_split=9)
    clf.fit(train_feature[c_feature], target_list)
    preds = clf.predict(test_feature)
    # right = 0
    for j in range(len(preds)):
        degree_result[test_id_list[j]] = preds[j]
    return degree_result


if __name__ == '__main__':
    trainFeature, testFeature, trainIdList, testIdList, trainTarList = merge_feature(feature_str)
    # tmp = [t<32 for t in trainTarList]
    # tmp = np.array(tmp)
    # trainFeature = trainFeature[tmp]
    target = np.array(trainTarList)
    # target = target[tmp]
    trainIdList = np.array(trainIdList)
    # trainIdList = trainIdList[tmp]
    cFeature = trainFeature.columns[:]
    clf1 = RandomForestClassifier(n_estimators=200, min_samples_split=9)
    clf1.fit(trainFeature[cFeature], target)
    preds1 = clf1.predict(testFeature)
    right = 0
    # for i in range(len(preds)):
    #     real = answer[testIdList[i]]['degree']
    #     if preds[i] == real:right+=1.0
    #     outFile1.write(testIdList[i]+'\t'+str(preds[i])+'\t'+str(real)+'\n')
    # print right/20000
    outFile1.write(str(right / 20000))
