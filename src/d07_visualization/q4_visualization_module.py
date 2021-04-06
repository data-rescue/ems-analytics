import numpy as np

import pandas as pd
from pandas import Series, DataFrame

import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import matplotlib

# Load the patient dataset, this file needs to exist for this
# module to function properly. If you don't have this file
# run the patients intermediate dataset notebook before running
# this module.
pat_i = pd.read_csv('../data/02_intermediate/dfPatients_dedup.csv')

# Visualization Color Configuration
# Change this parameter witha valid matplotlib parameter to
# update appropriate graphs color.
palette_sel_distinct = 'Dark2'
palette_sel_continuous = 'viridis'

# remove the 2 patient outcomes that are null
pat_i.drop(index=pat_i[pat_i['PatientOutcome'].isnull()].index, inplace=True)

# Create dataset with the fields of interest
cols = ['FireStation', 'Shift', 'PatientOutcome',
        'PatientOutcomeCode', 'PatientId', 'DispatchTime']
df_q4 = pat_i[cols].copy(deep=True)

df_q4.drop_duplicates(inplace=True)

df_q4 = df_q4.astype(dtype={
    #'FireStation': 'string',
    'Shift': 'string',
    'PatientOutcome': 'string',
    'PatientId': 'string'
})

df_q4['Shift'] = df_q4['Shift'].apply(lambda x: x.strip())
df_q4['PatientOutcome'] = df_q4['PatientOutcome'].apply(lambda x: x.strip())

#############################
### Question 4 DataFrames ###
#############################


def q4_data_frame():
    return df_q4


def q4_yearly_subsets():
    df = df_q4

    df = df.astype('category')
    df['DispatchTime'] = df['DispatchTime'].astype('datetime64')

    df18 = df[df['DispatchTime'].dt.year == 2018].copy()
    df19 = df[df['DispatchTime'].dt.year == 2019].copy()
    df20 = df[df['DispatchTime'].dt.year == 2020].copy()
    df21 = df[df['DispatchTime'].dt.year == 2021].copy()

    df_out = DataFrame({
        'Year': ['2018', '2019', '2020', '2021'],
        'Record Count': [
            '{:,}'.format(df18.shape[0]),
            '{:,}'.format(df19.shape[0]),
            '{:,}'.format(df20.shape[0]),
            '{:,}'.format(df21.shape[0])
        ],
        'Start Date-Time': [
            df18['DispatchTime'].min(),
            df19['DispatchTime'].min(),
            df20['DispatchTime'].min(),
            df21['DispatchTime'].min()
        ],
        'End Date-Time': [
            df18['DispatchTime'].max(),
            df19['DispatchTime'].max(),
            df20['DispatchTime'].max(),
            df21['DispatchTime'].max()
        ]
    })
    df_out = df_out.set_index('Year')
    return df_out


#########################
### EXPLORATORY PLOTS ###
#########################
def frequency_plot_station_outcome(subset, sel):
    if sel == 'station':
        y_sel = 'PatientOutcome'
        hue_sel = 'FireStation'

    if sel == 'outcome':
        y_sel = 'FireStation'
        hue_sel = 'PatientOutcome'

    if subset == 140:
        cat_list = ['Patient Dead at Scene (No EMS CPR)',
                    'Standby (Operational Support Provided)',
                    'Treated, Transferred Care',
                    'Patient Dead at Scene (EMS CPR Attempted)']
        df = df_q4[df_q4['PatientOutcome'].isin(cat_list)]
        plt.figure(figsize=(20, 25))

    if subset == 700:
        cat_list = ['Canceled (On Scene, No Patient Contact)',
                    'No Patient Found',
                    'Standby (No Services Performed)',
                    'EMS Assist (Other Agency)']
        df = df_q4[df_q4['PatientOutcome'].isin(cat_list)]
        plt.figure(figsize=(20, 25))

    if subset == 1400:
        cat_list = ['Patient Refusal  (AMA)',
                    'No Treatment/Transport Required',
                    'Canceled (Prior to Arrival)']
        df = df_q4[df_q4['PatientOutcome'].isin(cat_list)]
        plt.figure(figsize=(20, 25))

    if subset == 8000:
        cat_list = ['Treated & Transported']
        df = df_q4[df_q4['PatientOutcome'].isin(cat_list)]
        plt.figure(figsize=(20, 10))

    fig = sns.countplot(y=y_sel,
                        data=df,
                        hue=hue_sel,
                        palette=palette_sel_continuous)

    return fig


def frequency_plot_station(hue_sel):
    df = df_q4

    df = df.astype('category')
    df['DispatchTime'] = df['DispatchTime'].astype('datetime64')

    if hue_sel == 'year':
        hue_sel = df['DispatchTime'].dt.year

    sns.set_theme(style='darkgrid')
    plt.figure(figsize=(10, 20))
    sns.countplot(y='FireStation',
                  data=df,
                  palette=palette_sel_distinct,
                  hue=hue_sel)


def sunburst(path_in, col_in, subset):
    if subset == 140:
        cat_list = ['Patient Dead at Scene (No EMS CPR)',
                    'Standby (Operational Support Provided)',
                    'Treated, Transferred Care',
                    'Patient Dead at Scene (EMS CPR Attempted)']
        df = df_q4[df_q4['PatientOutcome'].isin(cat_list)]

    if subset == 700:
        cat_list = ['Canceled (On Scene, No Patient Contact)',
                    'No Patient Found',
                    'Standby (No Services Performed)',
                    'EMS Assist (Other Agency)']
        df = df_q4[df_q4['PatientOutcome'].isin(cat_list)]

    if subset == 1400:
        cat_list = ['Patient Refusal  (AMA)',
                    'No Treatment/Transport Required',
                    'Canceled (Prior to Arrival)']
        df = df_q4[df_q4['PatientOutcome'].isin(cat_list)]

    if subset == 8000:
        cat_list = ['Treated & Transported']
        df = df_q4[df_q4['PatientOutcome'].isin(cat_list)]

    if subset == 0:
        df = df_q4

    fig = px.sunburst(
        data_frame=df,
        path=path_in,
        color=col_in,
        color_discrete_sequence=px.colors.qualitative.Pastel,
        width=1500,
        height=1400,
        branchvalues="total",
        hover_name="PatientOutcome",
        hover_data={'PatientOutcome': False}
    )
    fig.update_traces(textinfo='label+percent entry')
    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))

    return fig.show()

#####################
### PROJECT PLOTS ###
#####################
# From this point forward you will have the graphics that will be used
# for the project. The graphics created before were exploratory options.


def violinplot(version, subset):
    df = df_q4.copy(deep=True)
    df = df.astype('category')

    if subset == 'withoutTreated':
        df = df[df['PatientOutcome'] != 'Treated & Transported'].copy()

        df['FireStation'] = df['FireStation'].cat.remove_unused_categories()
        df['Shift'] = df['Shift'].cat.remove_unused_categories()
        df['PatientOutcome'] = df['PatientOutcome'].cat.remove_unused_categories()

        FireStation_Dict = dict(enumerate(df['FireStation'].cat.categories))
        FireStation_Key_List = list(FireStation_Dict.keys())
        FireStation_Val_List = list(FireStation_Dict.values())

        PatientOutcome_Dict = dict(
            enumerate(df['PatientOutcome'].cat.categories))
        PatientOutcome_Key_List = list(PatientOutcome_Dict.keys())
        PatientOutcome_Val_List = list(PatientOutcome_Dict.values())

    if subset == 'withTreated':
        df = df
        FireStation_Dict = dict(enumerate(df['FireStation'].cat.categories))
        FireStation_Key_List = list(FireStation_Dict.keys())
        FireStation_Val_List = list(FireStation_Dict.values())

        PatientOutcome_Dict = dict(
            enumerate(df['PatientOutcome'].cat.categories))
        PatientOutcome_Key_List = list(PatientOutcome_Dict.keys())
        PatientOutcome_Val_List = list(PatientOutcome_Dict.values())

    if version == 0:
        fig, ax1 = plt.subplots(figsize=(160, 60))
        sns.violinplot(ax=ax1,
                       data=df,
                       x=df['FireStation'].cat.codes,
                       y=df['PatientOutcome'].cat.codes,
                       hue='Shift',
                       scale='count',
                       inner='box',
                       vw=.9,
                       cut=0,
                       palette=palette_sel_distinct)
        ax1.set_yticks(PatientOutcome_Key_List)
        ax1.set_yticklabels(PatientOutcome_Val_List, visible=True)
        ax1.set_xticks(FireStation_Key_List)
        ax1.set_xticklabels(FireStation_Val_List, visible=True)
        ax1.tick_params(labelsize=65)
        ax1.legend(fontsize=65)
        fig.tight_layout()

    if version == 1:
        fig = sns.violinplot(y=df['PatientOutcomeCode'],
                             x='FireStation',
                             data=df,
                             scale='count',
                             vw=.9,
                             cut=0)


def presentation_frequency_plot_figures(outcome):
    df = df_q4.copy(deep=True)

    # Axis Labels
    x_label = 'Counts'
    y_label = 'Fire Station'

    # Y Selection
    y_sel = 'FireStation'

    if outcome == 'Overall':
        title = outcome + ' Fire Station Outcomes Across Shift'
    elif outcome == 'Outcome':
        title = 'Patient Outcome Frequency'
        y_label = 'Patient Outcome'
        y_sel = 'PatientOutcome'
    else:
        title = outcome + ' Outcome Across Fire Station and Shift'
        df = df_q4[df_q4['PatientOutcome'] == outcome].copy(deep=True)

    #Plot
    plt.subplots(figsize=(20, 20))
    ax = sns.countplot(data=df,
                       y=y_sel,
                       hue='Shift',
                       palette=palette_sel_distinct,
                       order=df[y_sel].value_counts().index,
                       hue_order=['A - Shift', 'B - Shift', 'C - Shift'])
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
