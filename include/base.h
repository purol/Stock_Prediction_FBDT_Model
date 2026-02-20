#ifndef BASE_H
#define BASE_H

#include <vector>
#include <string>

void LoadCSV(std::string path, std::string filename, std::vector<std::string>* variable_names_, std::vector<std::vector<float>>* variables_, std::vector<bool>* IsSignal_, std::vector<float>* weight_, std::vector<std::string>* symbols_, std::vector<std::string>* dates_, std::vector<float>* pricechanges_) {
    std::vector<std::string> sample_dirs;
    for (const auto& entry : std::filesystem::directory_iterator(path)) sample_dirs.push_back(entry.path().string());
    std::sort(sample_dirs.begin(), sample_dirs.end());

    std::string lastest_dir = sample_dirs.at(sample_dirs.size() - 1);

    std::ifstream file;
    file.open((lastest_dir + "/" + filename).c_str());

    if (!file.is_open()) {
        throw std::runtime_error("Could not open the file.");
    }

    std::vector<std::string> variable_names;
    std::vector<std::string> symbols;
    std::vector<std::string> dates;
    std::vector<float> pricechanges;
    std::vector<std::vector<float>> variables;

    // Read the header row
    std::string line;
    std::getline(file, line);
    std::istringstream header_stream(line);
    std::string column;
    std::unordered_map<std::string, int> column_indices;

    int column_index = 0;
    while (std::getline(header_stream, column, ',')) {
        if ((column != "symbol") && (column != "date") && (column != "pricechange/year")) variable_names.push_back(column);
        column_indices[column] = column_index++;
    }

    // Find indices for symbol, date, and pricechange/year
    int symbol_idx = column_indices["symbol"];
    int date_idx = column_indices["date"];
    int pricechange_idx = column_indices["pricechange/year"];

    // Prepare space for variables
    int Nvar = variable_names.size(); // Exclude `symbol`, `date`, and `pricechange/year`
    variables.resize(Nvar);

    // Read the data rows
    while (std::getline(file, line)) {
        std::istringstream row_stream(line);
        std::string value;
        std::vector<std::string> row;

        // Split the line into columns
        while (std::getline(row_stream, value, ',')) {
            row.push_back(value);
        }

        // Extract symbol, date, and pricechange/year
        symbols.push_back(row[symbol_idx]);
        dates.push_back(row[date_idx]);
        pricechanges.push_back(std::stof(row[pricechange_idx]));

        // Extract variable data
        int var_index = 0;
        for (int i = 0; i < row.size(); ++i) {
            if (i == symbol_idx || i == date_idx || i == pricechange_idx) {
                continue;
            }
            variables[var_index++].push_back(std::stof(row[i]));
        }
    }

    file.close();

    // copy variable names
    (*variable_names_) = variable_names;

    // copy input variables
    (*variables_) = variables;

    // set signal/background
    double N_signal = 0.0;
    double N_background = 0.0;
    for (int i = 0; i < pricechanges.size(); i++) {
        if (IsItSignal(pricechanges.at(i))) {
            IsSignal_->push_back(true);
            N_signal = N_signal + 1.0;
        }
        else {
            IsSignal_->push_back(false);
            N_background = N_background + 1.0;
        }
    }

    // set weight, scale signal to background
    for (int i = 0; i < pricechanges.size(); i++) {
        if (IsItSignal(pricechanges.at(i))) weight_->push_back(N_background / N_signal);
        else weight_->push_back(1.0);
    }

    (*symbols_) = symbols;
    (*dates_) = dates;
    (*pricechanges_) = pricechanges;

}

void get_input_variables(
    std::vector<std::string>* variable_names_, std::vector<std::vector<float>>* variables_,
    std::vector<std::string>* input_variables_names_, std::vector<std::vector<float>>* selected_variables_) {

    for (int i = 0; i < input_variables_names_->size(); i++) {
        std::string temp_ = input_variables_names_->at(i);
        if (std::find(variable_names_->begin(), variable_names_->end(), temp_) == variable_names_->end()) {
            printf("unknown input variable name: %s\n", temp_.c_str());
        }
        else {
            int index = std::find(variable_names_->begin(), variable_names_->end(), temp_) - variable_names_->begin();
            selected_variables_->push_back(variables_->at(index));
        }
    }

}

#endif 