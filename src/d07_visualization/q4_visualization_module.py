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

# This color set was created to match the Shift color used by the 
# Fairfax County Fire and Rescue Department
palette_sel_distinct = ['Red','Green','Black']

# To align with the visualizations colors used by the team, I have
# generated this distinct color variable as the default scheme
palette_sel_distinct_2 = 'muted'

# Optional colors 
palette_sel_continuous = 'viridis'
seaborn_theme = 'darkgrid'

# remove the 2 patient outcomes that are null
pat_i.drop(index=pat_i[pat_i['PatientOutcome'].isnull()].index, inplace=True)

# Create dataset with the fields of interest
cols = ['FireStation', 'Shift', 'PatientOutcome',
        'PatientOutcomeCode', 'PatientId', 'DispatchTime']
df_q4 = pat_i[cols].copy(deep=True)

df_q4.drop_duplicates(inplace=True)

df_q4 = df_q4.astype(dtype={
    'Shift': 'str',
    'PatientOutcome': 'str',
    'PatientId': 'str'
})

df_q4['Shift'] = df_q4['Shift'].apply(lambda x: x.strip())
df_q4['PatientOutcome'] = df_q4['PatientOutcome'].apply(lambda x: x.strip())

#############################
### Question 4 DataFrames ###
#############################


def q4_data_frame():
    # Provide an easy method to return the data frame after conditioning.
    # The conditioning performed is tailored to answer focus question 4
    return df_q4


def q4_yearly_subsets():
    # This is a helper function created to help us understand the time
    # ranges associated with the dataset provided by FCFRD.
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
    # This frequency plot function attempts to bin the dataset
    # by frequency range. It provides a useful view to observe
    # EMS call outcomes that are within the 140, 700, 1400, and 
    # 8000 frequency ranges. This approach was not selected for
    # final briefing and/or report.

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

    sns.set_theme(style=seaborn_theme)
    sns.countplot(y=y_sel,
                  data=df,
                  hue=hue_sel,
                  palette=palette_sel_continuous)



def frequency_plot_station(hue_sel):
    # This frequency plot focus on observing the overall
    # EMS call outcome frequency counts across fire stations
    # segmented on a yearly basis from 2018 to 2021. The 2021
    # year only contains certain calls performed between January
    # and February. This visualization was not selected for 
    # final presention and/or report.
    df = df_q4

    df = df.astype('category')
    df['DispatchTime'] = df['DispatchTime'].astype('datetime64')

    if hue_sel == 'year':
        hue_sel = df['DispatchTime'].dt.year

    sns.set_theme(style=seaborn_theme)
    plt.figure(figsize=(10, 20))
    sns.countplot(y='FireStation',
                  data=df,
                  palette=palette_sel_distinct_2,
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
    # This function method attemps to generate all the violin plots created to
    # analyze the EMS call outcome distribution across fire station and shift.

    # A small amount of data conditioning is included in this function and it
    # is intended to:
    #   * Adjust the order of the EMS call outcome displayed on the y-axis.
    #   * Combine EMS call outcome categories as recommened by FCFRD

    # The method uses the version attribute the data frame for the plot. One
    # data frame (i.e., withTreated) contains all records and the other
    # data frame (i.e., withoutTreated) remove the Treated & Transported
    # EMS call outcome to help us better observe the distributions for the
    # rest of the EMS call outcomes

    # The subset attribute is used to present the violin plot with and
    # without hue. The hue is focused on the Shift variable of the data
    # frame and it is used to observe how the EMS call outcome distribution
    # changes across fire station and shift.

    # The fire station and patient outcome dictionary is created to properly
    # label the ticks for the y ans x axis.
    df = df_q4.copy(deep=True)
    df = df.astype('category')

    cat_order_with_treated = ['Canceled (Prior to Arrival)',
                              'Standby (Operational Support Provided)', 'Standby (No Services Performed)',
                              'Patient Refusal  (AMA)',
                              'No Patient Found', 'No Treatment/Transport Required', 'Canceled (On Scene, No Patient Contact)',
                              'Patient Dead at Scene (EMS CPR Attempted)', 'Patient Dead at Scene (No EMS CPR)',
                              'Treated & Transported',
                              'Treated, Transferred Care', 'EMS Assist (Other Agency)']
    
    cat_order_without_treated = ['Canceled (Prior to Arrival)',
                                 'Standby (Operational Support Provided)', 'Standby (No Services Performed)',
                                 'Patient Refusal  (AMA)',
                                 'No Patient Found', 'No Treatment/Transport Required', 'Canceled (On Scene, No Patient Contact)',
                                 'Patient Dead at Scene (EMS CPR Attempted)', 'Patient Dead at Scene (No EMS CPR)',
                                 'Treated, Transferred Care', 'EMS Assist (Other Agency)']

    new_cats_dict = {'Canceled (Prior to Arrival)': 'Canceled',
                     'Standby (Operational Support Provided)':'Standby',
                     'Standby (No Services Performed)':'Standby',
                     'Patient Refusal  (AMA)': 'Refused',
                     'No Patient Found':'No Patient', 
                     'No Treatment/Transport Required':'No Patient', 
                     'Canceled (On Scene, No Patient Contact)':'No Patient',
                     'Patient Dead at Scene (EMS CPR Attempted)':'Dead',
                     'Patient Dead at Scene (No EMS CPR)':'Dead',
                     'Treated & Transported':'Transport',
                     'Treated, Transferred Care':'Assist', 
                     'EMS Assist (Other Agency)':'Assist'}

    new_cat_order_with_treated = ['Canceled', 'Standby', 'Refused', 
                                  'No Patient', 'Dead', 'Transport', 'Assist']

    new_cat_order_without_treated = ['Canceled', 'Standby', 'Refused', 
                                     'No Patient', 'Dead', 'Assist']                                  


    if subset == 'withoutTreated':
        df = df[df['PatientOutcome'] != 'Treated & Transported'].copy()

        df['FireStation'] = df['FireStation'].cat.remove_unused_categories()
        df['Shift'] = df['Shift'].cat.remove_unused_categories()
        df['PatientOutcome'] = df['PatientOutcome'].cat.remove_unused_categories()

        df['PatientOutcome'] = df['PatientOutcome'].cat.reorder_categories(cat_order_without_treated)

        FireStation_Dict = dict(enumerate(df['FireStation'].cat.categories))
        FireStation_Key_List = list(FireStation_Dict.keys())
        FireStation_Val_List = list(FireStation_Dict.values())

        PatientOutcome_Dict = dict(
            enumerate(df['PatientOutcome'].cat.categories))
        PatientOutcome_Key_List = list(PatientOutcome_Dict.keys())
        PatientOutcome_Val_List = list(PatientOutcome_Dict.values())

    if subset == 'withTreated':
        df = df

        df['FireStation'] = df['FireStation'].cat.remove_unused_categories()
        df['Shift'] = df['Shift'].cat.remove_unused_categories()
        df['PatientOutcome'] = df['PatientOutcome'].cat.remove_unused_categories()

        df['PatientOutcome'] = df['PatientOutcome'].cat.reorder_categories(cat_order_with_treated)

        FireStation_Dict = dict(enumerate(df['FireStation'].cat.categories))
        FireStation_Key_List = list(FireStation_Dict.keys())
        FireStation_Val_List = list(FireStation_Dict.values())

        PatientOutcome_Dict = dict(
            enumerate(df['PatientOutcome'].cat.categories))
        PatientOutcome_Key_List = list(PatientOutcome_Dict.keys())
        PatientOutcome_Val_List = list(PatientOutcome_Dict.values())

    if subset == 'new_cat_withoutTreated':
        
        df = df
        df['PatientOutcome'] = df['PatientOutcome'].replace(new_cats_dict)
        df = df.astype('category')
        df = df[df['PatientOutcome'] != 'Transport'].copy()


        df['FireStation'] = df['FireStation'].cat.remove_unused_categories()
        df['Shift'] = df['Shift'].cat.remove_unused_categories()
        df['PatientOutcome'] = df['PatientOutcome'].cat.remove_unused_categories()

        df['PatientOutcome'] = df['PatientOutcome'].cat.reorder_categories(new_cat_order_without_treated)

        FireStation_Dict = dict(enumerate(df['FireStation'].cat.categories))
        FireStation_Key_List = list(FireStation_Dict.keys())
        FireStation_Val_List = list(FireStation_Dict.values())

        PatientOutcome_Dict = dict(
                    enumerate(df['PatientOutcome'].cat.categories))
        PatientOutcome_Key_List = list(PatientOutcome_Dict.keys())
        PatientOutcome_Val_List = list(PatientOutcome_Dict.values())
    
    if subset == 'new_cat_withTreated':
        df = df
        df['PatientOutcome'] = df['PatientOutcome'].replace(new_cats_dict)
        df = df.astype('category')

        df['FireStation'] = df['FireStation'].cat.remove_unused_categories()
        df['Shift'] = df['Shift'].cat.remove_unused_categories()
        df['PatientOutcome'] = df['PatientOutcome'].cat.remove_unused_categories()

        df['PatientOutcome'] = df['PatientOutcome'].cat.reorder_categories(new_cat_order_with_treated)

        FireStation_Dict = dict(enumerate(df['FireStation'].cat.categories))
        FireStation_Key_List = list(FireStation_Dict.keys())
        FireStation_Val_List = list(FireStation_Dict.values())

        PatientOutcome_Dict = dict(
                    enumerate(df['PatientOutcome'].cat.categories))
        PatientOutcome_Key_List = list(PatientOutcome_Dict.keys())
        PatientOutcome_Val_List = list(PatientOutcome_Dict.values())

    if version == 0:
        fig, ax1 = plt.subplots(figsize=(100, 30))
        sns.violinplot(ax=ax1,
                       data=df,
                       x=df['FireStation'].cat.codes,
                       y=df['PatientOutcome'].cat.codes,
                       scale='count',
                       inner='box',
                       vw=.9,
                       cut=0,
                       palette=palette_sel_distinct_2)
        ax1.set_yticks(PatientOutcome_Key_List)
        ax1.set_yticklabels(PatientOutcome_Val_List)
        ax1.set_xticks(FireStation_Key_List)
        ax1.set_xticklabels(FireStation_Val_List, visible=True)
        ax1.tick_params(labelsize=75)
        fig.tight_layout()

    if version == 1:
        fig, ax1 = plt.subplots(figsize=(160, 40))
        sns.violinplot(ax=ax1,
                       data=df,
                       x=df['FireStation'].cat.codes,
                       y=df['PatientOutcome'].cat.codes,
                       scale='count',
                       inner='box',
                       vw=.9,
                       cut=0,
                       palette=palette_sel_distinct,
                       hue='Shift',
                       hue_order=['A - Shift', 'B - Shift', 'C - Shift'])
        ax1.set_yticks(PatientOutcome_Key_List)
        ax1.set_yticklabels(PatientOutcome_Val_List)
        ax1.set_xticks(FireStation_Key_List)
        ax1.set_xticklabels(FireStation_Val_List, visible=True)
        ax1.tick_params(labelsize=95)
        ax1.legend(fontsize=95, loc='lower right')
        fig.tight_layout()


def presentation_frequency_plot_figures(outcome):
    # This function method attemps to generate all the frequency plots created to
    # analyze each EMS call outcome distribution across fire station and shift.

    # This function used the outcome variable to define which distribution we
    # would like to visualize:
    #  * The Overall value is used to plot the distribution for all the
    #    EMS call outcomes across fire station and shift (this plot was
    #    not used on the presentation or report).
    #
    #  * The Outcome value is used to plot the EMS call outcome frequency
    #    count across shift.
    #  
    #  * The Top 4 Outcomes value is used to plot the top 4 EMS call outcome
    #    frequency count across shift (This plot was created for the presentation 
    #    with the intent of optimizing space usage for the briefing)
    #
    #  * The remaining plots can be generated by entering the EMS call outcome
    #    of interest. If the EMS call outcome is properly entered as value the
    #    data frame is reduced to show only the records associated for the
    #    individual EMS call outcome across fire station and shift.
    df = df_q4.copy(deep=True)

    # Axis Labels
    x_label = 'Counts'
    y_label = 'Fire Station'

    # Y Selection
    y_sel = 'FireStation'

    # General figure and font size
    gen_fig_size = (20,20)
    gen_font_size = 24

    if outcome == 'Overall':
        title = outcome + ' Fire Station Outcomes Across Shift'
    elif outcome == 'Outcome':
        title = 'Patient Outcome Frequency'
        y_label = 'Patient Outcome'
        y_sel = 'PatientOutcome'
        sns.set_theme(style=seaborn_theme)
    elif outcome == 'Top 4 Outcomes':
        title = 'Patient Outcome Frequency'
        y_label = 'Patient Outcome'
        y_sel = 'PatientOutcome'
        out_list = ['Treated & Transported', 
                    'Patient Refusal  (AMA)', 
                    'No Treatment/Transport Required', 
                    'Canceled (Prior to Arrival)']
        df = df_q4[df_q4['PatientOutcome'].isin(out_list)].copy(deep=True)
        gen_fig_size = (10,5)
        gen_font_size = 18
    else:
        title = outcome + ' Outcome Across Fire Station and Shift'
        df = df_q4[df_q4['PatientOutcome'] == outcome].copy(deep=True)

    #Plot
    plt.subplots(figsize=gen_fig_size)
    sns.set_theme(style=seaborn_theme)
    ax = sns.countplot(data=df,
                       y=y_sel,
                       hue='Shift',
                       palette=palette_sel_distinct,
                       order=df[y_sel].value_counts().index,
                       hue_order=['A - Shift', 'B - Shift', 'C - Shift'])
    ax.set_title(title, fontsize=gen_font_size)
    ax.set_xlabel(x_label, fontsize=gen_font_size)
    ax.set_ylabel(y_label, fontsize=gen_font_size)
    ax.tick_params(labelsize=gen_font_size)
    ax.legend(fontsize=gen_font_size, loc='lower right')
