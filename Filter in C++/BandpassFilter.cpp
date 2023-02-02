#include <iostream>
#include <fstream>
#include <vector>
#include <cmath>
#include <algorithm>

using namespace std;

const int N = 1024;
double f1 = 0.5 / 72, f2 = 7 / 72;
vector<double> b, a, x, y, time, ppg_signal;

void ButterworthFilter(vector<double> &b, vector<double> &a, vector<double> &x, vector<double> &y)
{
    int n = x.size();
    y.resize(n);
    vector<double> tmp(n);
    for (int i = 0; i < n; i++)
    {
        tmp[i] = 0;
        for (int j = 0; j < b.size(); j++)
        {
            if (i - j >= 0)
                tmp[i] += b[j] * x[i - j];
        }
        for (int j = 1; j < a.size(); j++)
        {
            if (i - j >= 0)
                tmp[i] -= a[j] * y[i - j];
        }
        y[i] = tmp[i] / a[0];
    }
}

int main()
{
    ifstream input_file("sampleoutput.txt");
    if (!input_file.is_open())
    {
        cout << "File not found" << endl;
        return -1;
    }
    double t, v;
    while (input_file >> t >> v)
    {
        time.push_back(t);
        ppg_signal.push_back(1 / v);
    }
    input_file.close();

    int n = ppg_signal.size();
    x.resize(n);
    for (int i = 500; i < n; i++)
        x[i - 500] = ppg_signal[i];

    // Replace the call to butter with your custom implementation, or include the library that defines it.
    // butter(2, Wn, "bandpass", "sos", b, a);

    // Apply filter
    ButterworthFilter(b, a, x, y);

    // Save filtered signal to file
    ofstream output_file("filtered_signal.txt");
    for (int i = 0; i < y.size(); i++)
    {
        output_file << time[i + 500] << " " << y[i] << endl;
    }
    output_file.close();

    return 0;
}