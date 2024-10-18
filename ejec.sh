#!/bin/bash
a=(0.5 0.7 0.9)
for ((i=0; i<=2; i++)); do
    for ((j=1; j<=10; j++)); do
       #"python3" "gloton_v3.2.py"  "Instances-EDA-SSMZ/Class1/Instance-${j}.txt" "${a[i]}" "2"
      "python3" "ssmz_msf_grb.py"  "../Instances-EDA-SSMZ/Class$1/Instance-${j}.txt" "${a[i]}" "../Instances-EDA-SSMZ/incidencias/Inc$1.txt" > "Class$1_Instance-${j}_${a[i]}.txt" &
      wait 
        #"./lector" "20"  "20" < "Instances-EDA-SSMZ/Class5/Instance-${i}.txt" > "Instances-EDA-SSMZ/Class5m/Instance-${i}.txt" & 
    done
done
