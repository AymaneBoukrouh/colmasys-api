from colmasys.models import Model
from sqlalchemy import func, select
import pandas as pd
import plotly
import plotly.express as px
import json

async def number_of_rows(session, model: Model) -> int:
    '''return number of rows of a model'''
    return (await session.execute(select(func.count(model.id)))).scalar_one()

async def get_majors_students_chart(session):
    majors = ['AP', 'GC', 'IIR', 'IFA']
    students = [143, 98, 63, 34]

    df = pd.DataFrame({'major': majors, 'number': students})
    fig = px.pie(df, labels=majors, values='number', hole=.7, color='major')
    fig['layout'].update(showlegend=True, margin=dict(l=0,r=0,b=0,t=0), height=350)

    text = f'Majors<br><b>{len(majors)}</b>'
    fig.update_layout(annotations=[dict(text=text, x=0.5, y=0.5, font_size=30, showarrow=False)])

    majors_students_chart = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return majors_students_chart

async def get_attendance_chart(session):
    import random
    import numpy as np
    import plotly.figure_factory as ff

    x1 = np.random.randn(200)
    x2 = np.random.randn(200)
    x3 = np.random.randn(200)
    x4 = np.random.randn(200)

    hist_data = [x1, x2, x3, x4]

    group_labels = ['IIR', 'AP', 'GC', 'IFA']
    colors = ['#A56CC1', '#A6ACEC', '#63F5EF', '#73F5DF']

    # Create distplot with curve_type set to 'normal'
    fig = ff.create_distplot(hist_data, group_labels, colors=colors,
                            bin_size=.2, show_rug=False)

    fig['layout'].update(
        margin=dict(l=0,r=0,b=0,t=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )

    #fig['layout']['xaxis']['showgrid'] = False
    #fig['layout']['yaxis']['showgrid'] = False

    # Add title
    #fig.update_layout(title_text='Hist and Curve Plot')

    attendance_chart = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return attendance_chart
