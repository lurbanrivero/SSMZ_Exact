#!/bin/bash
a=(0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0)
for ((i=0; i<=1; i++)); do
       #"python3" "gloton_v3.2.py"  "Instances-EDA-SSMZ/Class1/Instance-${j}.txt" "${a[i]}" "2"
	 "python3" "ssmz_msf_grb_v2.py"  "../Instances-EDA-SSMZ/Reales/$1.txt" "${a[i]}" "../Instances-EDA-SSMZ/incidencias/Inc1.txt" #> "Reales_$1_${a[i]}.txt" &
   wait 
        #"./lector" "20"  "20" < "Instances-EDA-SSMZ/Class5/Instance-${i}.txt" > "Instances-EDA-SSMZ/Class5m/Instance-${i}.txt" & 
done
