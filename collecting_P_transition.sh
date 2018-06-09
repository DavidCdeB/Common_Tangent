#!/bin/bash

ScriptDir=`pwd`

rm -Rf All_P_H_real_intersection_at_Ts
mkdir All_P_H_real_intersection_at_Ts


FOLDERS="
10.00K
30.10K
50.20K
70.30K
90.40K
110.51K
130.61K
150.71K
170.81K
190.91K
211.01K
231.11K
251.21K
271.31K
291.41K
311.52K
331.62K
351.72K
371.82K
391.92K
412.02K
432.12K
452.22K
472.32K
492.42K
512.53K
532.63K
552.73K
572.83K
592.93K
"
#613.03K
#633.13K
#653.23K
#673.33K
#693.43K
#713.54K
#733.64K
#753.74K
#773.84K
#793.94K
#814.04K
#834.14K
#854.24K
#874.34K
#894.44K
#914.55K
#934.65K
#954.75K
#974.85K
#994.95K
#1015.05K
#1035.15K
#1055.25K
#1075.35K
#1095.45K
#1115.56K
#1135.66K
#1155.76K
#1175.86K
#1195.96K
#1216.06K
#1236.16K
#1256.26K
#1276.36K
#1296.46K
#1316.57K
#1336.67K
#1356.77K
#1376.87K
#1396.97K
#1417.07K
#1437.17K
#1457.27K
#1477.37K
#1497.47K
#1517.58K
#1537.68K
#1557.78K
#1577.88K
#1597.98K
#1618.08K
#1638.18K
#1658.28K
#1678.38K
#1698.48K
#1718.59K
#1738.69K
#1758.79K
#1778.89K
#1798.99K
#1819.09K
#1839.19K
#1859.29K
#1879.39K
#1899.49K
#1919.60K
#1939.70K
#1959.80K
#1979.90K
#2000.00K
#"

for i in ${FOLDERS}; do

cp ./G_PT/${i}/P_H_slope_common_tangent_T_* $ScriptDir/All_P_H_real_intersection_at_Ts

done 

cd $ScriptDir

########### Analytical cat-ing:
cd $ScriptDir/All_P_H_real_intersection_at_Ts
cat P_H_slope_common_tangent_T_* > All_TEMPERATS_P_H_slope_common_tangent.dat

#cat $ScriptDir/EL_level/P_H_slope_common_tangent_T_*  >> All_TEMPERATS_P_H_slope_common_tangent.dat
cat $ScriptDir/EL_plus_E0_level/P_H_slope_common_tangent_T_* >>  All_TEMPERATS_P_H_slope_common_tangent.dat
grep -v "Temperature" All_TEMPERATS_P_H_slope_common_tangent.dat > templat && mv templat  All_TEMPERATS_P_H_slope_common_tangent.dat
 
sort -k1 -n All_TEMPERATS_P_H_slope_common_tangent.dat > templat2 && mv templat2 All_TEMPERATS_P_H_slope_common_tangent.dat

(echo "# Temperature of Intersection(K)        Pressure of Intersection (GPa)" && cat All_TEMPERATS_P_H_slope_common_tangent.dat) > templat3 && mv templat3  All_TEMPERATS_P_H_slope_common_tangent.dat


cd $ScriptDir

python Phase_Boundary.py
bash make_pdflatex.sh


