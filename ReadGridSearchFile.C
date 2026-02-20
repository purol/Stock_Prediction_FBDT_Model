
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

#include <algorithm>

using std::string;

std::vector<std::string> var_names;

typedef struct data {
    unsigned int nTrees;
    unsigned int depth;
    double shrinkage;
    double subsample;
    unsigned int binning;
    double train_AUC;
    double test_AUC;
} Data;

bool data_sorter(Data const& lhs, Data const& rhs) {
    return lhs.test_AUC > rhs.test_AUC;
}

int ReadGridSearchFile()
{
    const char* fname = "total";
    const int Nlist = 1500;
    std::vector<Data> Datas;

    FILE* fp;
    fp = fopen(fname, "r");

    for (int i = 0; i < Nlist; i++) {
        unsigned int nTrees = 0;
        unsigned int depth = 0;
        double shrinkage = 0;
        double subsample = 0;
        unsigned int binning = 0;
        double train_AUC = 0;
        double test_AUC = 0;

        fscanf(fp,"%u_%u_%lf_%lf_%u %lf %lf\n",&nTrees, &depth, &shrinkage, &subsample, &binning, &train_AUC, &test_AUC);
        Data temp_data = { nTrees, depth, shrinkage, subsample, binning, train_AUC, test_AUC };
        Datas.push_back(temp_data);
    }

    fclose(fp);

    std::sort(Datas.begin(), Datas.end(), &data_sorter);

    double Rank[Nlist];
    for (int i = 0; i < Nlist; i++) Rank[i] = i + 1;
    double train_AUCs[Nlist];
    for (int i = 0; i < Nlist; i++) train_AUCs[i] = Datas.at(i).train_AUC;
    double test_AUCs[Nlist];
    for (int i = 0; i < Nlist; i++) test_AUCs[i] = Datas.at(i).test_AUC;

    for (int i = 0; i < Nlist; i++) printf("%u_%u_%lf_%lf_%u %lf %lf\n", Datas.at(i).nTrees, Datas.at(i).depth, Datas.at(i).shrinkage, Datas.at(i).subsample, Datas.at(i).binning, Datas.at(i).train_AUC, Datas.at(i).test_AUC);

    TGraph* gr_train = new TGraph(Nlist, Rank, train_AUCs);
    TGraph* gr_test = new TGraph(Nlist, Rank, test_AUCs);

    gr_train->SetMarkerStyle(8); gr_train->SetMarkerSize(0.8);
    gr_test->SetMarkerStyle(8); gr_test->SetMarkerSize(0.8);

    gr_train->SetMarkerColor(kRed + 1);
    gr_test->SetMarkerColor(kBlue + 1);

    gr_train->SetTitle(";test AUC rank;AUC");

    TCanvas* c = new TCanvas("c1", "AUC", 200, 10, 600, 600);

    gr_train->Draw("AP");
    gr_test->Draw("P");

    TLegend* legend = new TLegend(0.15, 0.8, 0.35, 0.9); legend->SetFillStyle(0); legend->SetLineWidth(0);
    legend->AddEntry(gr_train,"train","P"); legend->AddEntry(gr_test,"test","P");
    legend->Draw();
    c->SaveAs("AUC.png");

    return 0;
}
