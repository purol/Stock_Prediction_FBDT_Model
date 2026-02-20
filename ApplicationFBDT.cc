#include <algorithm>
#include <cstdlib>
#include <map>
#include <string>
#include <iostream>
#include <filesystem>
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
#include "MyFBDT.h"
#include "base.h"

typedef struct data {
    std::string ticker;
    std::string date;
    float FBDToutput;
    float pricechange;
} Data;

bool data_sorter(Data const& lhs, Data const& rhs) {
    return lhs.FBDToutput > rhs.FBDToutput;
}

void DrawApplicationHistogram(const FastBDT::Classifier& classifier, std::vector<std::vector<float>> InputVariables_application, std::vector<bool> IsSignal_application, std::vector<float> weight_application, std::string filename) {

    TH1D* signal_application_hist = new TH1D(("signal_application_" + filename).c_str(), ("signal_application_" + filename).c_str(), 50, 0.0, 1.0);
    TH1D* background_application_hist = new TH1D(("background_application_" + filename).c_str(), ("background_application_" + filename).c_str(), 50, 0.0, 1.0);

    for (unsigned int i = 0; i < IsSignal_application.size(); ++i) {
        std::vector<float> temp;
        for (int j = 0; j < InputVariables_application.size(); j++) temp.push_back(InputVariables_application.at(j).at(i));
        float p = classifier.predict(temp);
        if (IsSignal_application.at(i) == true) signal_application_hist->Fill(p, weight_application.at(i));
        else background_application_hist->Fill(p, weight_application.at(i));
    }

    TCanvas* c_temp = new TCanvas("c", "", 800, 800); c_temp->cd();

    double factor = 1.0;

    // normalization
    signal_application_hist->Scale(factor / signal_application_hist->Integral(), "width");
    background_application_hist->Scale(factor / background_application_hist->Integral(), "width");

    // set color (BKG: kRed, SIGNAL: kBlue)
    signal_application_hist->SetFillStyle(3004);
    signal_application_hist->SetLineColor(kBlue);
    signal_application_hist->SetFillColor(kBlue);

    background_application_hist->SetFillStyle(3005);
    background_application_hist->SetLineColor(kRed);
    background_application_hist->SetFillColor(kRed);

    gStyle->SetOptStat(0);

    background_application_hist->Draw("Hist"); signal_application_hist->Draw("Hist SAME");
    TLegend* legend = gPad->BuildLegend(0.9, 0.9, 0.6, 0.6); legend->SetFillStyle(0); legend->SetLineWidth(0);
    c_temp->SaveAs(("result_application_" + filename + ".png").c_str());

    delete signal_application_hist;
    delete background_application_hist;

    delete c_temp;

}

void PrintApplicationResult(const FastBDT::Classifier& classifier, std::vector<std::string> ticker, std::vector<std::string> date, std::vector<float> pricechange, std::vector<std::vector<float>> input_vars, std::string filename) {

    std::vector<Data> Datas;

    for (unsigned int i = 0; i < ticker.size(); ++i) {
        std::vector<float> temp;
        for (int j = 0; j < input_vars.size(); j++) temp.push_back(input_vars.at(j).at(i));
        float p = classifier.predict(temp);

        Data temp_data = { ticker.at(i), date.at(i), p, pricechange.at(i) };
        Datas.push_back(temp_data);
    }

    std::sort(Datas.begin(), Datas.end(), &data_sorter);

    FILE* fp = fopen(("Application_output_" + filename + ".log").c_str(), "w");
    for (int i = 0; i < Datas.size(); i++) fprintf(fp, "%s %s %f %f\n", Datas.at(i).ticker.c_str(), Datas.at(i).date.c_str(), Datas.at(i).FBDToutput, Datas.at(i).pricechange);
    fclose(fp);

}

int main(int argc, char* argv[])
{
    std::fstream in_stream("manager.weightfile", std::ios_base::in);
    FastBDT::Classifier classifier(in_stream);

    /*============================== 2022 Application ==============================*/

    // define input of the classifier
    std::vector<std::string> variable_names_application;
    std::vector<std::vector<float>> variables_application;
    std::vector<std::vector<float>> input_variables_application;
    std::vector<bool> IsSignal_application;
    std::vector<float> weight_application;
    std::vector<std::string> symbols_application;
    std::vector<std::string> dates_application;
    std::vector<float> pricechanges_application;

    // load application CSV
    std::string filename = "application_2021.csv";
    LoadCSV("./application", filename, &variable_names_application, &variables_application, &IsSignal_application, &weight_application, &symbols_application, &dates_application, &pricechanges_application);

    // select input variables
    get_input_variables(&variable_names_application, &variables_application, &input_variables_names, &input_variables_application);

    // get AUC
    double AUC_application = PrintAUC(classifier, input_variables_application, IsSignal_application, weight_application);

    PrintApplicationResult(classifier, symbols_application, dates_application, pricechanges_application, input_variables_application, filename);

    DrawApplicationHistogram(classifier, input_variables_application, IsSignal_application, weight_application, filename);

    return 0;
}