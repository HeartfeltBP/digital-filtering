#include <iostream>
#include <vector>
#include <fstream>
#include <cmath>

int main()
{
    // Read data from "sampleoutput.xlsx" into the vector T
    std::vector<std::pair<double, double>> T;
    std::ifstream file("sampleoutput.xlsx");
    double t, x;
    while (file >> t >> x)
    {
        T.push_back({t, x});
    }
    file.close();

    int N = T.size();
    std::vector<double> x_vec, x2_vec;
    for (const auto &[t, x] : T)
    {
        x_vec.push_back(1.0 / x);
        x2_vec.push_back(x);
    }

    int count = 0;
    int maxiter = 3;
    std::vector<std::vector<double>> I;
    while (true)
    {
        count++;
        if (count > maxiter)
        {
            break;
        }

        std::vector<double> s = x_vec;
        double sig = 3;
        while (sig > 0.009)
        {
            std::vector<double> d;
            for (int i = 0; i < N - 1; i++)
            {
                d.push_back(s[i + 1] - s[i]);
            }
            std::vector<int> mm;
            for (int i = 0; i < N - 2; i++)
            {
                if (d[i] == 0)
                {
                    mm.push_back(i);
                }
                else if ((d[i] > 0) != (d[i + 1] > 0))
                {
                    mm.push_back(i + 1);
                }
            }
            if (mm.size() < 2)
            {
                break;
            }

            std::vector<int> ma, mi;
            if (mm[0] > mm[1])
            {
                for (int i = 0; i < mm.size(); i += 2)
                {
                    ma.push_back(mm[i]);
                }
                for (int i = 1; i < mm.size(); i += 2)
                {
                    mi.push_back(mm[i]);
                }
            }
            else
            {
                for (int i = 1; i < mm.size(); i += 2)
                {
                    ma.push_back(mm[i]);
                }
                for (int i = 0; i < mm.size(); i += 2)
                {
                    mi.push_back(mm[i]);
                }
            }
            ma.insert(ma.begin(), 1);
            ma.push_back(N);
            mi.insert(mi.begin(), 1);
            mi.push_back(N);

            std::vector<double> maev, miev;
            for (int i = 1; i <= N; i++)
            {
                double t = i;
                maev.push_back(0.0);
                miev.push_back(0.0);
                for (int j = 1; j < ma.size(); j++)
                {
                    int m = ma[j];
                    int l = mi[j - 1];
                    double c = (x2_vec[m - 1] - x2_vec[l - 1]) / (x_vec[m - 1] - x_vec[l - 1]);
                    double k = x2_vec[m - 1] - c * x_vec[m - 1];
                    maev[i - 1] = maev[i - 1] + c / (m - l) * (t - l) * (t - m);
                    miev[i - 1] = miev[i - 1] + k / (m - l) * (t - l) * (t - m);
                }
            }
            std::vector<double> y_vec;
            for (int i = 0; i < N; i++)
            {
                y_vec.push_back(x2_vec[i] - miev[i] - maev[i] * x_vec[i]);
            }

            std::vector<double> c;
            for (int i = 0; i < N - 1; i++)
            {
                c.push_back(y_vec[i + 1] - y_vec[i]);
            }

            std::vector<double> v;
            for (int i = 0; i < N - 1; i++)
            {
                v.push_back(c[i] / (x_vec[i + 1] - x_vec[i]));
            }

            double sig1 = 0;
            for (int i = 0; i < N - 1; i++)
            {
                sig1 = sig1 + (v[i] - s[i]) * (v[i] - s[i]);
            }
            sig1 = sqrt(sig1 / (N - 1));
            s = v;
            sig = sig1;
        }
        I.push_back(s);
    }
    std::cout << "Iterations: " << I.size() << std::endl;
    return 0;
}