import grblogtools as glt
import plotly.graph_objects as go
import pandas as pd
import time


nlogs=11
results = glt.parse('*.log')
timelines=results.progress("nodelog")
print(timelines)
runs={}
for i in range(1,nlogs):
    runs[i]=timelines[timelines["LogFilePath"]=="Class1_Instance-"+str(i)+"_0.5.log"]

#run1=timelines[(timelines["LogFilePath"]=="Class1_Instance-1_0.5.log")]
#df=pd.DataFrame({"Time 1":run1["Time"], "Obj 1":run1["Incumbent"],"Time 2":run2["Time"], "Obj 2":run2["Incumbent"] })
#print(df)
#df.to_csv("salida.csv",index=True)
#glt.plot(nl[nl["LogNumber"] == "0"], title="912-Cuts0-Heuristics0.1", type="line", y="Gap", color="Seed", log_x=True)
#print(run1)
#plt.scatter(x=run1["Time"],y=run1["Incumbent"])
fig1 = go.Figure()
fig2 = go.Figure()
for i in range(1,nlogs):
    fig1.add_trace(go.Scatter(x=runs[i]["Time"], y=runs[i]["Incumbent"], name="Instance-"+str(i)))
    fig2.add_trace(go.Scatter(x=runs[i]["Time"], y=runs[i]["Gap"], name="Instance-"+str(i)))
#fig.add_trace(go.Scatter(x=run2["Time"], y=run2["Incumbent"], name="Instance-2"))

fig1.update_xaxes(title_text="Runtime (s)")
fig2.update_xaxes(title_text="Runtime (s)")
fig1.update_yaxes(title_text="Objective function value")
fig2.update_yaxes(title_text="GAP")
fig1.update_layout(title_font_family="Times New Roman",title='$\\text{Class 1 Instances with } \\alpha=0.7$', title_x=0.5,paper_bgcolor='rgb(255,255,255)', plot_bgcolor='rgb(245,245,245)',legend=dict(bgcolor='rgb(255,255,255)',bordercolor="Black",borderwidth=2))
fig2.update_layout(title_font_family="Times New Roman",title='$\\text{Class 1 Instances with } \\alpha=0.7$', title_x=0.5,paper_bgcolor='rgb(255,255,255)', plot_bgcolor='rgb(245,245,245)',legend=dict(bgcolor='rgb(255,255,255)',bordercolor="Black",borderwidth=2))

fig1.write_image("fig1.pdf")
time.sleep(2)
fig1.write_image("fig1.pdf")

fig2.write_image("fig2.pdf")
time.sleep(2)
fig2.write_image("fig2.pdf")
#fig.show()
