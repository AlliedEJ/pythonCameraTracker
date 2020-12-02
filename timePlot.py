from detectorApp import df
from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool, ColumnDataSource

#date time modification for hover view
df["startString"]=df["Start"].dt.strftime("%Y-%m-%d %H:%M:%S")
df["endString"]=df["End"].dt.strftime("%Y-%m-%d %H:%M:%S")

cds=ColumnDataSource(df)

f1=figure(x_axis_type="datetime", height=300, width=800, title="Motion Graph")

f1.yaxis.minor_tick_line_color=None
f1.yaxis[0].ticker.desired_num_ticks=1

hover=HoverTool(tooltips=[("Start","@startString"),("End","@endString")])
f1.add_tools(hover)

#Passing source cds allows hover to read the Start & End times.
f1.quad(left="Start", right="End", bottom=0, top=1, color="green",source=cds)

output_file("timesVisual.html")

show(f1)