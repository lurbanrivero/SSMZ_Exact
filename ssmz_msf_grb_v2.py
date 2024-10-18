import os
import networkx as nx
import random as rnd
import sys
import disjoin as dj
import numpy as np
import gurobipy as grb


def create_graph(m,n,c):
	N=m*n
	G=nx.Graph()
	for i in range(0,N):
		if i < N-n:
			if i%n < n-1:
				G.add_edge(i,i+1)
				G.add_edge(i,n+i)
			else:
				G.add_edge(i,n+i)
               # print("i=",i,"v=",n+i)
		else:
			if i%n < n-1:
				G.add_edge(i,i+1)
	for k in range(0,N):
		G.add_edge(k,N)
	for e in G.edges():
		if e[0]!=N and e[1]!=N:
			media=(dj.get_datos(c,e[0],n)+dj.get_datos(c,e[1],n))/2.0
			varianza=(dj.get_datos(c,e[0],n)-media)**2 + (dj.get_datos(c,e[1],n)-media)**2
			G[e[0]][e[1]]['costo']=varianza #abs(dj.get_datos(c,e[0],n)-dj.get_datos(c,e[1],n))
	return G 


def posiciones(G,n):
	pos={}
	for u in G.nodes():
		if u!=K:
			i = int(u / n)
			j = u % n
			pos[u]=np.array([i,j])
		else:
			i=int(u/n) + 2
			j= (u % n) + 2.5
			pos[u]=np.array([i,j])
	return pos

def conv_lista(lista):
   lista_aux=[]
   for k in range(0,len(lista)):
      if len(lista[k])>0:
         lista_aux.append(lista[k])
   return lista_aux
         

def genera_colores(m,n):
	lista=[]
	rnd.seed(45679)
	for i in range(0,m*n):
		r=rnd.random()
		g=rnd.random()
		b=rnd.random()
		lista.append([round(r,2),round(g,2),round(b,2)])
	return lista

def genera_colores2(m,n):
	N=m*n
	colores=[]
	for k in range(0,int(N/2)+1):
		p1 = rnd.randint(0,1)
		if p1==0:
			r=rnd.uniform(0.0,0.3)
			
		else:
			r=rnd.uniform(0.7,1.0)
			
		p2 = rnd.randint(0,1)
		if p2==0:
			g=rnd.uniform(0.0,0.3)
		else:
			g=rnd.uniform(0.7,1.0)
		b=rnd.uniform(0,1.0)
  
		colores.append([r,g,b])
		colores.append([1-r,1-g,1-b])
	return colores

def dibujo(nombre,m,n,c_nodos,seed=456):
	N = m*n
	rnd.seed(seed)
	rgbt = genera_colores2(m,n)  #[(  rnd.gauss(0.5,0.1) ,rnd.uniform(0,1), rnd.gauss(0.5,0.1)  ) for x in range(N)]
	f = open(nombre+".tex",'w')
	f.write("\\documentclass{standalone} \n")
	f.write("\\usepackage[usenames,dvipsnames]{xcolor} \n")
	f.write("\\usepackage{tikz}\n")
	f.write("\\usetikzlibrary{patterns} \n")
	for k in range(0,len(rgbt)):
		f.write("\\definecolor{col"+str(k)+"}{rgb}{"+ str(rgbt[k][0]) +","+ str(rgbt[k][1]) +","+ str(rgbt[k][2]) +"}\n")
	f.write("\\begin{document} \n")
	f.write("\\begin{tikzpicture}[scale=1.5] \n")
	for k in range(0,len(c_nodos)):
		for p in c_nodos[k]:
			if p!=N:
				i=int(p/n)
				j=p % n
				f.write("\\node[text=black, font=\\fontsize{6}{6},opacity=1,text opacity=1,circle,minimum size=0.8cm](v"+ str(p) +") at ("+str(j+0.5)+","+str(m-i-0.5)+"){$"+str(k+1)+"$};\n")
				f.write("\\fill[fill=col"+str(k)+",opacity=0.45]("+str(j)+","+str(m-(i+1))+") rectangle ( " +str(j+1) +","+str(m-i)+");\n")
	f.write("\\end{tikzpicture}\n")
	f.write("\\end{document}\n")
	f.close()
	os.system("pdflatex --interaction=batchmode " + nombre+".tex")	



def dibujo2(nombre,G,m,n,c_nodos,c_arcos,seed=456):
	N = m*n
	rnd.seed(seed)
	v_list=conv_lista(c_nodos)
	e_list=conv_lista(c_arcos)
	rgbt = genera_colores2(m,n)  #[(  rnd.gauss(0.5,0.1) ,rnd.uniform(0,1), rnd.gauss(0.5,0.1)  ) for x in range(N)]
	f = open(nombre+".tex",'w')
	f.write("\\documentclass{standalone} \n")
	f.write("\\usepackage[usenames,dvipsnames]{xcolor} \n")
	f.write("\\usepackage{tikz}\n")
	f.write("\\usetikzlibrary{patterns} \n")
	for k in range(0,len(rgbt)):
		f.write("\\definecolor{col"+str(k)+"}{rgb}{"+ str(rgbt[k][0]) +","+ str(rgbt[k][1]) +","+ str(rgbt[k][2]) +"}\n")
	f.write("\\begin{document} \n")
	f.write("\\begin{tikzpicture}[scale=1.5] \n")
	for k in range(0,len(v_list)):
		for q in v_list[k]:
			if q!=N:
				i=int(q/n)
				j=q % n
				f.write("\\node[fill=col"+str(k)+",text=black, font=\\fontsize{6}{6},opacity=0.45,text opacity=1,circle,minimum size=0.8cm](v"+ str(q) +") at ("+str(j+0.5)+","+str(m-i-0.5)+"){$"+str(k+1)+"$};\n")

	#i=int(N/n)
	#j=N % n
	#f.write("\\node[fill=col"+str(N-1)+",font=\\fontsize{8}{8},opacity=0.5,circle,minimum size=0.4cm](v"+ str(N) +") at ("+str(j+0.5)+","+str(m-i-0.5)+"){$"+str(N)+"$};\n")
	for k in range(0,len(e_list)):
		for q in e_list[k]:
			if q[0]!=N and q[1]!=N:
				f.write("\\draw[bend left=0,color=col"+str(k)+",thick,opacity=1.0](v"+str(q[0])+") edge (v"+str(q[1])+");\n")
	f.write("\\end{tikzpicture}\n")
	f.write("\\end{document}\n")
	f.close()
	os.system("pdflatex --interaction=batchmode " + nombre+".tex")	


def buscar_color(sol,elem):
	for k in range(0,len(sol)):
		for q in sol[k]:
			if q==elem:
				return k
				break
	return -1


fh = open(sys.argv[1], "r")
alpha = float(sys.argv[2])

l = 0
c = {}
for linea in fh:
    l_list = linea.split(" ")
    if l == 0:
        m = int(l_list[0])
        n = int(l_list[1])
        # print(m,n)
    else:
        for j in range(0, n):
           # print((l_list[j]))
            c[l - 1, j] = float(l_list[j])
    if l == m:
        break
    l = l + 1


fh.close

[A, L, S] = dj.leerInc(sys.argv[3])
incident=dj.get_samples(A)
VT=dj.calcVT(c,m,n)



#m=10
#n=10
G1=create_graph(m,n,c)
K=m*n

G=G1.to_directed()


x={} #x[u,k]=1 si el vertice u tiene el color k, 0 otro caso.
y={} #y[u,v,k]=1 Si el arco (u,v) tiene con color k se usa en el arbol k. 0 En otro caso 
z={} # Número de vertices con el color k
V={} # V[u,k] Variable auxiliar para el vertice u para cada color k
r={} # r[k]=1 Si se usa el color k, En otro caso 
prod={}
media={}
p={}
d={}
dif_abs={}


mod=grb.Model("msf_ssmz")
#z[k]*y[e[0],e[1],k] 

 

for u in G.nodes():
	for k in range(0,K):
		x[u,k]=mod.addVar(vtype=grb.GRB.BINARY,name="x_"+str(u)+"_"+str(k))     
		V[u,k]=mod.addVar(vtype=grb.GRB.CONTINUOUS,name="V_"+str(u)+"_"+str(k))
		p[u,k]=mod.addVar(vtype=grb.GRB.CONTINUOUS,lb=0,ub=grb.GRB.INFINITY,name="p_"+str(u)+"_"+str(k))
		#d[u,k]=mod.addVar(vtype=grb.GRB.BINARY,name="d_"+str(u)+"_"+str(k))
		dif_abs[u,k]=mod.addVar(vtype=grb.GRB.CONTINUOUS,lb=0,ub=grb.GRB.INFINITY,name="dabs_"+str(u)+"_"+str(k))


			
		
  
for e in G.edges():
   for k in range(0,K):
      y[e[0],e[1],k]=mod.addVar(vtype=grb.GRB.BINARY,name="y_"+str(e[0])+"_"+str(e[1])+"_"+str(k))
     # prod[e[0],e[1],k]=mod.addVar(vtype=grb.GRB.BINARY,name="prod_"+str(e[0])+"_"+str(e[1])+"_"+str(k))
      

for k in range(0,K):
   r[k]=mod.addVar(vtype=grb.GRB.BINARY,name="r_"+str(k))
   z[k]=mod.addVar(vtype=grb.GRB.INTEGER,name="z_"+str(k))
   media[k]=mod.addVar(vtype=grb.GRB.CONTINUOUS,name="media_"+str(k))
   
theta=mod.addVar(vtype=grb.GRB.INTEGER,name="theta")
H_num=mod.addVar(vtype=grb.GRB.CONTINUOUS,lb=0,ub=grb.GRB.INFINITY,name="Hnum")
H_den=mod.addVar(vtype=grb.GRB.CONTINUOUS,lb=0,ub=grb.GRB.INFINITY,name="Hden")
obj2=grb.quicksum( [ G[e[0]][e[1]]['costo'] * y[e[0],e[1],k] for e in G.edges() if e[0]!=K and e[1]!=K for k in range(0,K) ])

mod.setObjective(theta ,grb.GRB.MINIMIZE)  

for k in range(0,K):
	mod.addConstr( grb.quicksum([x[u,k] for u in G.nodes() if u!=K ]) == z[k], "No_de_vertices_del_color_"+str(k))
	if k>0:
		mod.addConstr( r[k]<=r[k-1])
	else:
		mod.addConstr( r[k]<=1)

		
for u in G.nodes():
	if u!=K:
		mod.addConstr( grb.quicksum( [x[u,k] for k in range(0,K) ]  ) == 1 ,"El_vertice_"+str(u)+"debe_tener_color" )
	else:
		mod.addConstr( grb.quicksum([x[u,k] for k in range(0,K)]) == theta ,"El_vertice_"+str(u)+"debe_tener_theta_colores" )
   
for u in G.nodes():
	for k in range(0,K):
		mod.addConstr(x[u,k] <= r[k],"Uso_del_color_"+str(k)+"en_el_vertice_"+str(u))
  
for e in G.edges():
	for k in range(0,K):
		mod.addConstr(y[e[0],e[1],k] <= r[k],"Uso_del_color_"+str(k)+"en_la_arista_"+str(e[0])+"_"+str(e[1]))  

# El nodo final debe recibir una flecha del color k 
for k in range(0,K):
	mod.addConstr(grb.quicksum( [y[u,K,k]  for u in G.nodes() if u != K]) == r[k],"Nodo_sumidero_"+str(k))
	mod.addConstr(grb.quicksum( [y[K,u,k]  for u in G.nodes() if u != K]) == 0 ,"Nodo_sumidero2_"+str(k))


mod.addConstr( grb.quicksum( [r[k] for k in range(0,K)] ) == theta,"colores_usados")
#mod.addConstraint( lpSum(y[u,K,k] for u in G.nodes() if u!=K for k in range(0,K) ) == theta )
for k in range(0,K):
	mod.addConstr(r[k] <= grb.quicksum( [x[u,k] for u in G.nodes() if u!=K]) ,"El_color_"+str(k)+"_debe_tener_elementos") #lpSum(y[e[0],e[1],k] for e in G.edges()
	for u in G.nodes():
		if u!=K:
			r[k]>=x[u,k]


# x[e[0],k] * x[e[1],k]
for e in G.edges():
	for k in range(0,K):
		mod.addConstr( y[e[0],e[1],k] + y[e[1],e[0],k] <=x[e[0],k]*x[e[1],k] )





for e in G.edges():
	mod.addConstr( grb.quicksum( [y[e[0],e[1],k] for k in range(0,K)] )  <= 1 ,"La_arista_"+str(e[0])+"_"+str(e[1])+"_puede_tener_a_lo_mas_un_color")

for u in G.nodes():
	if u!=K:
		for k in range(0,K):
			mod.addConstr( grb.quicksum([y[u,q,k] for q in G.neighbors(u) if q<=K]) == x[u,k] , "El_vertice_"+str(u)+"_tiene_flujo_si_esta_con_color_"+str(k))
			#mod.addConstr( dif_abs[u,k] - (dj.get_datos(c,u,n) - media[k]) >=0 )
			#mod.addConstr( dif_abs[u,k] - (dj.get_datos(c,u,n) - media[k]) <= 10000*d[u,k] )
			#mod.addConstr( dif_abs[u,k] - (-dj.get_datos(c,u,n) + media[k]) >=0 )
			#mod.addConstr( dif_abs[u,k] - (-dj.get_datos(c,u,n) + media[k]) <= 10000*(1-d[u,k]) )
			mod.addConstr( dif_abs[u,k] >= dj.get_datos(c,u,n) - media[k] )
			mod.addConstr( dif_abs[u,k] >= -(dj.get_datos(c,u,n) - media[k] ))
			mod.addConstr(  p[u,k] <= 10000 * x[u,k] )
			mod.addConstr(  p[u,k] >= dif_abs[u,k]  - 10000 * (1-x[u,k])  )
			mod.addConstr(  p[u,k] <= dif_abs[u,k] )




for u in G.nodes():
	if u!=K:
		for e in G.edges():
			if u==e[0]:
				for k in range(0,K):
					mod.addConstr( V[e[0],k] >= V[e[1],k] + y[e[0],e[1],k] - (K+1)*(1-y[e[0],e[1],k]) )
	else:
		for k in range(0,K):
			mod.addConstr(V[u,k]==0)

#warm_start(x,sys.argv[4])
for k in range(0,m*n):
   mod.addConstr(media[k]*z[k] == grb.quicksum( [ dj.get_datos(c,u,n) * x[u,k] for u in G.nodes() if u!=K] ), "Media_de_la_region_"+str(k) )
   mod.addConstr(media[k] <= 10000 * r[k])
    
#mod.addConstr( (VT*m*n - VT*theta)*(1-alpha) >= grb.quicksum( [ (dj.get_datos(c,u,n)*x[u,k] - media[k]) * (dj.get_datos(c,u,n)*x[u,k] - media[k] ) for u in G.nodes() if u!=K for k in range(0,m*n) ] )   ,"Homogeneidad" )
mod.addConstr( H_num == grb.quicksum( [ p[u,k]*p[u,k] for u in G.nodes() if u!=K for k in range(0,m*n) ] )   ,"Homogeneidad" )
mod.addConstr( H_den == (VT*m*n - VT*theta)*(1-alpha) )
mod.addConstr( H_den >= H_num )
#mod.addConstr(theta <= 6)

mod.write('ssmz_grb.lp')
mod.params.NonConvex = 2
#mod.setParam("TuneTimeLimit",3600)
mod.params.Heuristics=0.001
mod.params.Cuts=1
mod.params.PreQLinearize=0
mod.params.PrePasses=1
mod.params.ScaleFlag=2

basename=sys.argv[1].split("/")
ins_name=basename[3].split(".")
logfile=basename[2]+"_"+ins_name[0]+"_"+str(alpha)+".log"
dibname=basename[2]+"_"+ins_name[0]+"_"+str(alpha)+"_dib"
mod.setParam('TimeLimit', 16*1800)
#mod.setParam("Heuristics",0.1)
#mod.setParam("MIPFocus",1)
mod.setParam('OutputFlag', 1)
mod.setParam("LogFile",logfile)
mod.optimize()

lista_arcos={}
for k in range(0,K):
	lista_arcos[k]=[]
	for e in G.edges():
		if abs(y[e[0],e[1],k].x) >=0.001:
			lista_arcos[k].append(e)
lista_nodos={}
for k in range(0,K):
	lista_nodos[k]=[]
	for u in sorted(G.nodes()):
		if abs(x[u,k].x)>=0.001:
			lista_nodos[k].append(u)
		

#for u in sorted(G.nodes()):
#	if u!=K:
#		for k in range(0,K):
#			if abs(x[u,k].x)>=0.001:
#				if u % n == n-1 :
#					print(k)
#				else:
#					print(k, end=" ")
   
#print("Medias:")
#for k in range(0,K):
#	print(media[k].x,end=": ")

#print()
#print("P:")
#for u in sorted(G.nodes()):
#	if u!=K:
#		for k in range(0,K):
#			if abs(x[u,k].x)>=0.0001:
#				if u % n == n-1 :
#					print(p[u,k].x)
#				else:
#					print(p[u,k].x,end=" ")

#print("R")       
#for k in range(0,K):
#   if abs(r[k].x)>=0.0001:
#      print(k)
   

#print()
#print("Hnum",H_num.x)
#print("Hden",H_den.x)
#	for u in sorted(G.nodes()) :
#		print("u[",u,"]=",V[u,k].varValue,end=" ")
#	print()

st=dj.sol_no_lineas(lista_nodos,m,n)
#print(lista_nodos)
#print(st.z)
st.up_vars(c)
minimo=st.fobj(VT,alpha)
valorH=st.calcH(VT)
print(minimo,valorH,VT)




dibujo2(dibname+"_graph",G,m,n,lista_nodos,lista_arcos,789123)
dibujo(dibname+"_rec",m,n,lista_nodos,789123)





