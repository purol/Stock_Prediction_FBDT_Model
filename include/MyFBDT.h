#ifndef MYFBDT_H
#define MYFBDT_H

#include <vector>
#include "Classifier.h"

bool IsItSignal(float pricechange) {
    if (pricechange > 1.3) return true;
    else return false;
    return false;
}

double PrintAUC(const FastBDT::Classifier& classifier, std::vector<std::vector<float>> InputVariables, std::vector<bool> IsSignal, std::vector<float> weight) {
    const int step = 100;
    double AUC = 0;
    double NBKG_total = 0;
    double NSIG_total = 0;
    std::vector<double> TPRs;
    std::vector<double> FPRs;

    for (unsigned int i = 0; i < IsSignal.size(); ++i) {
        if (IsSignal[i]) NSIG_total = NSIG_total + weight[i];
        else NBKG_total = NBKG_total + weight[i];
    }

    for (int i = 0; i < step; i++) {
        float value = ((float)i) / ((float)step);
        double NBKG = 0;
        double NSIG = 0;

        for (unsigned int i = 0; i < IsSignal.size(); ++i) {
            std::vector<float> temp;
            for (int j = 0; j < InputVariables.size(); j++) temp.push_back(InputVariables.at(j).at(i));
            float p = classifier.predict(temp);
            if (p >= value) {
                if (IsSignal[i]) NSIG = NSIG + weight[i];
                else NBKG = NBKG + weight[i];
            }
        }

        double TPR = NSIG / NSIG_total;
        double FPR = NBKG / NBKG_total;

        TPRs.push_back(TPR);
        FPRs.push_back(FPR);
    }

    for (unsigned int i = 0; i < TPRs.size(); ++i) {
        if (i != TPRs.size() - 1) {
            double del_FPR = FPRs.at(i) - FPRs.at(i + 1);
            double avg_TPR = (TPRs.at(i) + TPRs.at(i + 1)) / 2.0;
            AUC = AUC + del_FPR * avg_TPR;
        }
        else {
            double del_FPR = FPRs.at(i) - 0.0;
            double avg_TPR = (TPRs.at(i) + 0.0) / 2.0;
            AUC = AUC + del_FPR * avg_TPR;
        }
    }

    return AUC;
}

#endif 