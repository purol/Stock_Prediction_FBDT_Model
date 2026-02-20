
#include <cstdlib>
#include <iostream>
#include <map>
#include <string>
# include <vector>
#include <fstream>

#include <TMath.h>
#include <TColor.h>
#include <TStyle.h>
#include <TCanvas.h>
#include <TAxis.h>
#include <TFile.h>
#include <TTree.h>
#include <TCut.h>
#include <TString.h>
#include <TLegend.h>
#include <TGraph.h>
#include <TGaxis.h>
#include <TF1.h>
#include <TH1F.h>
#include <TH2F.h>
#include <TH3F.h>
#include <THStack.h>
#include <TPaveText.h>
#include <TKey.h>
#include <TSystemFile.h>
#include <TSystemDirectory.h>
#include <numeric>
#include "Classifier.h"
#include "Variables.h"

int main()
{

    int Nvar = input_variables_names.size();

    // print result of testing sample
    std::fstream in_stream("manager.weightfile", std::ios_base::in);
    FastBDT::Classifier classifier(in_stream);

    std::map<unsigned int, double> rank;
    rank = classifier.GetVariableRanking();
    printf("Variable importance:\n");
    for (auto iter = rank.begin(); iter != rank.end(); iter++)
    {   
        std::cout << "[" << iter->first << ", " << iter->second << "]" << std::endl;
    }
    printf("\n\n");
    printf("Variable importance for plot:\n");
    printf("[");
    for (auto iter = rank.begin(); iter != rank.end(); iter++)
    {   
        int index = std::distance(rank.begin(), iter);
        std::cout << "(\'" << input_variables_names.at(iter->first) << "\'," << iter->second << ")";
        if (index == Nvar - 1) {}
        else {
            std::cout << "," << std::endl;
        }
    }
    printf("]");
    printf("\n\n");

    return 0;
}
