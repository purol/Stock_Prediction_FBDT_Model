#include <algorithm>
#include <cstdlib>
#include <map>
#include <string>
#include <iostream>
#include <filesystem>
#include <vector>
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
#include "MyFBDT.h"
#include "base.h"

void DrawHistogram(const FastBDT::Classifier& classifier, std::vector<std::vector<float>> InputVariables_train, std::vector<bool> IsSignal_train, std::vector<float> weight_train, std::vector<std::vector<float>> InputVariables_test, std::vector<bool> IsSignal_test, std::vector<float> weight_test, std::string plot_name) {

    TH1D* signal_train_hist = new TH1D("signal_train", "signal_train", 50, 0.0, 1.0);
    TH1D* background_train_hist = new TH1D("background_train", "background_train", 50, 0.0, 1.0);
    TH1D* signal_test_hist = new TH1D("signal_test", "signal_test", 50, 0.0, 1.0);
    TH1D* background_test_hist = new TH1D("background_test", "background_test", 50, 0.0, 1.0);

    for (unsigned int i = 0; i < IsSignal_train.size(); ++i) {
        std::vector<float> temp;
        for (int j = 0; j < InputVariables_train.size(); j++) temp.push_back(InputVariables_train.at(j).at(i));
        float p = classifier.predict(temp);
        if (IsSignal_train.at(i) == true) signal_train_hist->Fill(p, weight_train.at(i));
        else background_train_hist->Fill(p, weight_train.at(i));
    }

    for (unsigned int i = 0; i < IsSignal_test.size(); ++i) {
        std::vector<float> temp;
        for (int j = 0; j < InputVariables_test.size(); j++) temp.push_back(InputVariables_test.at(j).at(i));
        float p = classifier.predict(temp);
        if (IsSignal_test.at(i) == true) signal_test_hist->Fill(p, weight_test.at(i));
        else background_test_hist->Fill(p, weight_test.at(i));
    }

    TCanvas* c_temp = new TCanvas("c", "", 800, 800); c_temp->cd();

    double factor = 1.0;

    // normalization
    signal_test_hist->Scale(factor / signal_test_hist->Integral(), "width");
    background_test_hist->Scale(factor / background_test_hist->Integral(), "width");
    signal_train_hist->Scale(factor / signal_train_hist->Integral(), "width");
    background_train_hist->Scale(factor / background_train_hist->Integral(), "width");

    // set color (BKG: kRed, SIGNAL: kBlue)
    // solid line: test, histogram: traing
    signal_test_hist->SetMarkerStyle(kFullCircle);
    signal_test_hist->SetLineColor(kBlue);
    signal_test_hist->SetMarkerColor(kBlue);
    signal_test_hist->SetLineWidth(1);

    background_test_hist->SetMarkerStyle(kFullCircle);
    background_test_hist->SetLineColor(kRed);
    background_test_hist->SetMarkerColor(kRed);
    background_test_hist->SetLineWidth(1);

    signal_train_hist->SetFillStyle(3004);
    signal_train_hist->SetLineColor(kBlue);
    signal_train_hist->SetFillColor(kBlue);

    background_train_hist->SetFillStyle(3005);
    background_train_hist->SetLineColor(kRed);
    background_train_hist->SetFillColor(kRed);

    gStyle->SetOptStat(0);

    background_train_hist->Draw("Hist"); signal_train_hist->Draw("HistSAME");
    background_test_hist->Draw("AP SAME"); signal_test_hist->Draw("AP SAME");
    TLegend* legend = gPad->BuildLegend(0.9, 0.9, 0.6, 0.6); legend->SetFillStyle(0); legend->SetLineWidth(0);
    c_temp->SaveAs(plot_name.c_str());

    delete signal_train_hist;
    delete background_train_hist;
    delete signal_test_hist;
    delete background_test_hist;

    delete c_temp;

}

int main(int argc, char* argv[])
{
    // grid search
    // unsigned int nTrees[5] = { 100, 500, 1000, 1500, 2000 };  default is 100
    // unsigned int depth[3] = { 2, 3, 4 };  default is 3 
    // double shrinkage[4] = { 0.05, 0.1, 0.15, 0.2 };  default is 0.1
    // double subsample[5] = { 0.3, 0.4, 0.5, 0.6, 0.7 };  default is 0.5
    // unsigned int binning[4] = { 6, 7, 8, 9 };  default is 2^8 bins per feature

    /*
    * argv[1]: nTrees
    * argv[2]: depth
    * argv[3]: shrinkage path
    * argv[4]: subsample type
    * argv[5]: binning
    */

    int Nvar = input_variables_names.size();

    unsigned int nTrees = (unsigned int)atoi(argv[1]);
    unsigned int depth = (unsigned int)atoi(argv[2]);
    double shrinkage = atof(argv[3]);
    double subsample = atof(argv[4]);
    unsigned int binning_num = (unsigned int)atoi(argv[5]);

    // set classifier option
    FastBDT::Classifier classifier;
    classifier.SetNTrees(nTrees);
    classifier.SetDepth(depth);
    classifier.SetShrinkage(shrinkage);
    classifier.SetSubsample(subsample);
    std::vector<unsigned int> binning(Nvar, binning_num); classifier.SetBinning(binning);

    /*============================== train ==============================*/

    // define input variables
    std::vector<std::string> variable_names_train;
    std::vector<std::vector<float>> variables_train;
    std::vector<std::vector<float>> input_variables_train;
    std::vector<bool> IsSignal_train;
    std::vector<float> weight_train;
    std::vector<std::string> symbols_train;
    std::vector<std::string> dates_train;
    std::vector<float> pricechanges_train;

    // load train CSV
    LoadCSV("./train", "train.csv", & variable_names_train, &variables_train, &IsSignal_train, &weight_train, &symbols_train, &dates_train, &pricechanges_train);

    // select input variables
    get_input_variables(&variable_names_train, &variables_train, &input_variables_names, &input_variables_train);

    // fit
    classifier.fit(input_variables_train, IsSignal_train, weight_train);

    // get AUC
    double AUC_train = PrintAUC(classifier, input_variables_train, IsSignal_train, weight_train);

    /*============================== test ==============================*/

    // define input variables
    std::vector<std::string> variable_names_test;
    std::vector<std::vector<float>> variables_test;
    std::vector<std::vector<float>> input_variables_test;
    std::vector<bool> IsSignal_test;
    std::vector<float> weight_test;
    std::vector<std::string> symbols_test;
    std::vector<std::string> dates_test;
    std::vector<float> pricechanges_test;

    // load test CSV
    LoadCSV("./test", "test.csv", &variable_names_test, &variables_test, &IsSignal_test, &weight_test, &symbols_test, &dates_test, &pricechanges_test);

    // select input variables
    get_input_variables(&variable_names_test, &variables_test, &input_variables_names, &input_variables_test);

    // get AUC
    double AUC_test = PrintAUC(classifier, input_variables_test, IsSignal_test, weight_test);

    /*============================== print result ==============================*/

    std::string plot_name = "./out/plot_" + std::string(argv[1]) + "_" + std::string(argv[2]) + "_" + std::string(argv[3]) + "_" + std::string(argv[4]) + "_" + std::string(argv[5]) + ".png";
    DrawHistogram(classifier, input_variables_train, IsSignal_train, weight_train, input_variables_test, IsSignal_test, weight_test, plot_name);

    printf("%u_%u_%lf_%lf_%u %lf %lf\n", nTrees, depth, shrinkage, subsample, binning_num, AUC_train, AUC_test);

    FILE* fp;
    fp = fopen(("./out/Result_" + std::string(argv[1]) + "_" + std::string(argv[2]) + "_" + std::string(argv[3]) + "_" + std::string(argv[4]) + "_" + std::string(argv[5])).c_str(), "w");
    fprintf(fp, "%u_%u_%lf_%lf_%u %lf %lf\n", nTrees, depth, shrinkage, subsample, binning_num, AUC_train, AUC_test);
    fclose(fp);

    // save model
    std::fstream out_stream(("./out/classifier_" + std::string(argv[1]) + "_" + std::string(argv[2]) + "_" + std::string(argv[3]) + "_" + std::string(argv[4]) + "_" + std::string(argv[5]) + ".weightfile").c_str(), std::ios_base::out | std::ios_base::trunc);
    out_stream << classifier << std::endl;
    out_stream.close();

    return 0;
}
