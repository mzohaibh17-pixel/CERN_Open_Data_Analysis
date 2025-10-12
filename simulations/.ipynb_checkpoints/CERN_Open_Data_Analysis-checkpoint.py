#!/usr/bin/env python
# coding: utf-8

# In[5]:


import numpy as np
import matplotlib.pyplot as plt
import uproot
import mplhep as hep
from scipy.optimize import curve_fit
import json
from pathlib import Path
import os
hep.style.use('CMS')

# Base Directory Creation

try:
    base_dir = Path().resolve().parent
except NameError:
    base_dir = Path(__file__).parent.parent.resolve()

# Subfolders and Gaussian Function for fitting

data_dir = base_dir / 'data'
plots_dir = base_dir / 'plots'
csv_dir = base_dir / 'csvs'
json_dir = base_dir / 'jsons'
simulations_dir = base_dir / 'simulations'
for d in [data_dir, plots_dir, csv_dir, json_dir, simulations_dir]:
    os.makedirs(d, exist_ok = True)
    print(f'Directory created:\n {d}')
print('')
def gaussian(x, a, mean, sigma):
    return a * np.exp(-(x-mean) ** 2/(2*sigma**2))

# Loop over ROOT files

for file_name in os.listdir(data_dir):
    if not file_name.endswith('.root'):
        continue
    file_path = os.path.join(data_dir, file_name)
    print(f'The file {file_name} is being processed.')

    try:

        # Extract histogram from ROOT file and Fit Gaussian

        file = uproot.open(file_path)
        hist = file['demo/massZto2muon']
        counts, edges = hist.to_numpy()
        bin_centers = (edges[:-1] + edges[1:]) / 2
        print(f'The histogram is loaded successfully from file {file_name}, bins = {len(bin_centers)}')
        popt, _ = curve_fit(gaussian, bin_centers, counts, p0 = [max(counts), 91, 2])
        a, mean, sigma = popt
        print(f'Fit Successful: Mean = {mean:.3f}, Sigma = {sigma:.3f}, Amplitude = {a:.3f}')

        # Plot histogram and Fit

        plt.figure(figsize = (8, 6))
        plt.bar(bin_centers, counts, width = (edges[1] - edges[0]), label = f'{file_name} Histogram')
        plt.plot(bin_centers, gaussian(bin_centers, *popt), "r--", label = f"Gaussian Fit: Mean = {mean:.3f} GeV, Sigma = {sigma:.3f}")
        plt.xlabel('Invariant Mass (GeV)', fontsize = 10, loc = 'center')
        plt.ylabel('Events', fontsize = 10, loc = 'center')
        plt.title(f"Z -> mu+ mu- Invariant Mass Spectrum ({file_name})", fontsize=12, loc='center')
        plt.tick_params(axis = 'both', which = 'major', labelsize = 8)
        hep.cms.text('', loc = 0, fontsize = 10)
        plt.legend(fontsize = 8, loc='upper left')
        plt.grid(alpha = 0.3)
        plt.tight_layout(pad = 0.2)

        # Save Outputs

        plot_file = plots_dir / f"{file_name.replace('.root','')}_massZto2muon.png"
        plt.savefig(plot_file, dpi=300)
        plt.close()
        csv_file = csv_dir / f"{file_name.replace('.root','')}_massZto2muon.csv"
        np.savetxt(csv_file, np.column_stack([bin_centers, counts]), delimiter=",", header="Mass(GeV),Counts", comments='')
        json_file = json_dir / f"{file_name.replace('.root','')}_massZto2muon.json"
        with open(json_file, "w") as f:
            json.dump({"a": a, "mean": mean, "sigma": sigma}, f, indent=4) 
        print(f'[SAVED] Plot Graph: {plot_file}')
        print(f'[SAVED] CSV Histogram: {csv_file}')
        print(f'[SAVED] JSON Fit: {json_file}\n')

    except Exception as e:
        print(f'[ERROR] File {file_name} could not be processed. : {e}')


# In[ ]:





# In[ ]:




