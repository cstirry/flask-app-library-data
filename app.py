#from __future__ import print_function
from flask import Flask, render_template, request, redirect

import flask

import pandas as pd
import numpy as np

from bokeh.models import NumeralTickFormatter
from bokeh.models import CustomJS, ColumnDataSource, Select
from bokeh.layouts import column

from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8

app = flask.Flask(__name__)



@app.route("/")
def main():

    df = pd.read_csv('static/data.csv')
    df = df.set_index('YEAR')

    col = list(df.columns.values)
    y = df['RURAL']
    x = df[col].index

    source = ColumnDataSource(data=df)

    p = figure(title="Median Number of Annual Computer Uses by Library Vistors", x_axis_label="year", y_axis_label="annual count of unique uses of library computers")
    p.line(x=x, y=y,source=source)
    p.circle(x=x, y=y,source=source)

    p.xaxis.minor_tick_line_color = None
    p.yaxis[0].formatter = NumeralTickFormatter(format="0.")

    callback = CustomJS(args=dict(source=source), code="""
        var data = source.get('data');
        var f = cb_obj.get('value')
        data['y'] = data[f]
        source.trigger('change');
        """)

    col_select = Select(title="Option:", value=col[0], options=col)
    col_select.js_on_change('value', callback)

    layout = column(col_select,p)

    script, div = components( layout )
    return render_template('chart.html',
    js_resources = INLINE.render_js(),
    css_resources=INLINE.render_css(),
    script = script,
    div = div)

    return encode_utf8(html)

if __name__ == '__main__':
  app.run(port=33507)
