# Plot Allocation by Strata

## Description of Scripts

### setup_env.sh 
Sets up the environment for the scripts to run. Run this first

### config.yml 
Configuration file for the scripts. Edit this file to change the default values.
- currently assumes that the user will be calling this sripts from within the "src/" directory.
$$~$$
### "gen_spreedsheet.py" 
The script reads pixel data from a raster file to get standard deviation.
A shapefile is used to define the strata. Many stratum can be defined or repeated. 
Area is automatically calculated for each stratum based on the shapefile.
An Excel workbook will be created allowing the user to enter and adjust data.
- noteably, the total number of plot is entered on the first page.
- on the second page, the auto generated values can be edited.
Additional strata can be added.
- if the user wants to specify the number of plots in a stratum, then use the hard set column. Otherwise, leave it 0.
this hard set numbers will contribute to the total number of plots but can not exceed the total number of plots.
- The user can also deweight a stratum by entering a number between 0 and 1 in the deweight column.
This will reduce the number of plots in the stratum and reallocate them to the other calculated strata.
The use case for this is to deenphasize a stratum that is not of interest and focus resources on the strata of interest.
$$~$$

### "calc_sampling_intensity.py" 
takes the data entered by the user on the spreedsheet and calculates the optimal 
number of plots based on the standard deviation and the area while taking into account the number of plots that have been
hard set and any deweighting of strata. The results are added to the spreedsheet on the third page. 
if the values need to be recalculated delete the third page in excel, save, exit excel and rerun the script.

## Usege
```bash
./setup_env.sh

nvim config.yml # edit the config file

python3 gen_spreadsheet.py #edit the spreadsheet
python3 calc_sampling_intensity.py #results will be added to page 3 of the spreadsheet
```


## Neyman Optimal Allocation
$$
n_{h} = \left[ \frac{N_{h} S_{h}}{\displaystyle\sum_{h+1}^{L} N_{h} s_{h}} \right]
$$
- $n_{h}$: This is the number of sample plots you should measure in stratum h (a specific forest type or area). The formula is calculating how many plots to measure in each stratum to get the most accurate estimate of the total.
    
- $N_{h}$: This is the total area of stratum h (e.g., the total area of a specific forest type or region).
    
- $S_{h}$: This is the standard deviation of the variable of interest (e.g., tree volume, biomass, number of trees) in stratum h. This would be based on your a priori knowledge or previous measurements.
    
- $\displaystyle\sum_{h+1}^{L} N_{h} s_{h}$: This is a summation from h+1 to L (the total number of strata) of the product of the area and the standard deviation of each stratum. It's essentially a weighted sum of the variability in each stratum, where the weights are the areas of the strata.
    

The fraction $N_{h} S_{h}$ divided by the summation represents the proportion of the total variability that is present in stratum h based on its area and variability. This is then used to determine the optimal number of sample plots for that stratum.

By using this formula, you are distributing your sampling effort in a way that gives more plots to strata with greater area and/or greater variability, which can improve the accuracy and precision of your overall estimates.
