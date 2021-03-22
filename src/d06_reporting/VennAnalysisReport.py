import numpy as np

import pandas as pd
from pandas import Series, DataFrame

from matplotlib_venn import venn3_unweighted
from matplotlib import pyplot as plt


def venn_analysis_table(key_id,
                        col_from_patients, 
                        col_from_procedures, 
                        col_from_medications,
                        out_flag=True):
    """
    The utility function venn_analysis_table was created to obtain a better understanding
    of the missing records that we have encountered with the data set provided. For instance,
    the raw data provided patient and provider IDs in the Medications and Procedures datasets
    that does not exist in the patients table.
    
    Cautions: you need to understand that the context is associated to the analysis we
    are creating for the Fairfax County Fire and Rescue Department.
    
    Properties:
    -----------
        key_id : string (mandatory)
            The string will help document the ID/Column we used to perform this particular
            analysis. (i.e., PatientId, 
                             FRDResponelID (a.k.a., ProviderId), 
                             Composite Index (Concatenation of PatientId with FRDPersonnelID))
                             
        col_from_patients: Pandas Series (mandatory)
            The Series object needs to cointain a single feature. It should either be the
            PatientId, FRDPersonelID, or a concatenate version of these two columns.
            
            Caution: In order to maintain the proper context for this analysis this pandas
                     series or data frame should come from the *Patients* dataset. Otherwise
                     the Observations made may not make sense with the results obtained
        
        col_from_procedures: Pandas Series (mandatory)
            The Series object needs to cointain a single feature. It should either be the
            PatientId, FRDPersonelID, or a concatenate version of these two columns.
            
            Caution: In order to maintain the proper context for this analysis this pandas
                     series or data frame should come from the *Procedures* dataset. Otherwise
                     the Observations made may not make sense with the results obtained
        
        col_from_medications: Pandas Series (mandatory)
            The Series object needs to cointain a single feature. It should either be the
            PatientId, FRDPersonelID, or a concatenate version of these two columns.
            
            Caution: In order to maintain the proper context for this analysis this pandas
                     series or data frame should come from the *Medications* dataset. Otherwise
                     the Observations made may not make sense with the results obtained
        
        out_flag: Boolean (Mandatory)
            The boolean will be used to determine which one of the 2 data frames to return,
            either the observations from the venn analysis or a DataFrame with all the key
            IDs not found on the Patients Table.
            
            Defaults to True
            
            True = Observations DataFrame
            False = IDs missing from Patients Table
    
    Return
    ------
        A pandas DataFrame that will show the results of the Venn Analysis performed.
        
        Caution: Attributes provided in the wrong order will cause the observations to 
        loose the context for which they were made.
    """
    ### Import Libraries ###
    import numpy as np

    import pandas as pd
    from pandas import Series, DataFrame
    
    ### Assert Input ###
    exp_out = "<class 'pandas.core.series.Series'>"
    s1_in = str(type(col_from_patients))
    s2_in = str(type(col_from_procedures))
    s3_in = str(type(col_from_medications))
    
    assert (s1_in == exp_out and s2_in == exp_out and s3_in == exp_out), '''One 
        of the column inputs provided is not a Series, please read the function 
        information available at /src/d06_reporting folder'''
        
    assert (str(type(key_id)) == "<class 'str'>"),'''The key_id provided is not
        a string, please read the function information available at 
        /src/d06_reporting folder'''
        
    assert (str(type(out_flag)) == "<class 'bool'>"), '''The out_flag provided is not a 
        boolean, please read the function information available at 
        /src/d06_reporting folder'''
            
    a = set(col_from_patients)
    b = set(col_from_procedures)
    c = set(col_from_medications)
            
    """
        REMINDER! set operators for Python are:
            | for union
            & for intersection
            - for difference
            ^ for symmetric difference
    """
    if key_id == 'PatientId':
        key_id = 'Patients'
    
    if key_id == 'FRDPersonnelID':
        key_id = 'Providers'
    
    if key_id == 'comp_idx':
        key_id = 'Compound IDs: Patient & Provider'
        
    observations_df = DataFrame({
        'Observations':[
            '{} that only exist in Patients'.format(key_id),
            '{} that only exist in the Procedures but not in Patients (?)'.format(key_id),
            '{} that exist in Patients and Procedures'.format(key_id),
            '{} that only exists in the Medications but not in Patients (?)'.format(key_id),
            '{} that exists in Patients and Medications'.format(key_id),
            '{} that exists in Procedures and Medications only but not in Patients (?)'.format(key_id),
            '{} that exists in all datasets'.format(key_id)
        ],
        'Count':[
            len(a-(b|c)),
            len(b-(a|c)),
            len((a&b)-c),
            len(c-(a|b)),
            len((a&c)-b),
            len((b&c)-a),
            len(a&b&c)
        ]
    }).set_index('Observations')
    
    key_id_in_pro_not_pat = b-(a|c)
    key_id_in_med_not_pat = c-(a|b)
    key_id_in_pro_med_not_pat = (b&c)-a
    
    all_miss_id_from_pat = (key_id_in_pro_not_pat | 
                            key_id_in_med_not_pat |
                            key_id_in_pro_med_not_pat)
    missing_df = DataFrame({
        'Missing IDs': list(all_miss_id_from_pat)
    })
    
    if out_flag == False:
        return missing_df
    return observations_df

def venn_analysis_diagram(key_id,
                          col_from_patients, 
                          col_from_procedures, 
                          col_from_medications):
    """
    The utility function venn_analysis_diagram was created to obtain a better understanding
    of the missing records that we have encountered with the data set provided. For instance,
    the raw data provided patient and provider IDs in the Medications and Procedures datasets
    that does not exist in the patients table.
    
    Cautions: you need to understand that the context is associated to the analysis we
    are creating for the Fairfax County Fire and Rescue Department.
    
    Properties:
    -----------
        key_id : string (mandatory)
            The string will help document the ID/Column we used to perform this particular
            analysis. (i.e., PatientId, 
                             FRDResponelID (a.k.a., ProviderId), 
                             Composite Index (Concatenation of PatientId with FRDPersonnelID))
                             
        col_from_patients: Pandas Series (mandatory)
            The Series object needs to cointain a single feature. It should either be the
            PatientId, FRDPersonelID, or a concatenate version of these two columns.
            
            Caution: In order to maintain the proper context for this analysis this pandas
                     series or data frame should come from the *Patients* dataset. Otherwise
                     the Observations made may not make sense with the results obtained
        
        col_from_procedures: Pandas Series (mandatory)
            The Series object needs to cointain a single feature. It should either be the
            PatientId, FRDPersonelID, or a concatenate version of these two columns.
            
            Caution: In order to maintain the proper context for this analysis this pandas
                     series or data frame should come from the *Procedures* dataset. Otherwise
                     the Observations made may not make sense with the results obtained
        
        col_from_medications: Pandas Series (mandatory)
            The Series object needs to cointain a single feature. It should either be the
            PatientId, FRDPersonelID, or a concatenate version of these two columns.
            
            Caution: In order to maintain the proper context for this analysis this pandas
                     series or data frame should come from the *Medications* dataset. Otherwise
                     the Observations made may not make sense with the results obtained
        
    Return
    ------
        A Venn Diagram plot.
        
        Caution: Attributes provided in the wrong order will cause the observations to 
        loose the context for which they were made.
    """
    
    ### Assert Input ###
    exp_out = "<class 'pandas.core.series.Series'>"
    s1_in = str(type(col_from_patients))
    s2_in = str(type(col_from_procedures))
    s3_in = str(type(col_from_medications))
    
    assert (s1_in == exp_out and s2_in == exp_out and s3_in == exp_out), '''One 
        of the column inputs provided is not a Series, please read the function 
        information available at /src/d06_reporting folder'''
        
    assert (str(type(key_id)) == "<class 'str'>"),'''The key_id provided is not
        a string, please read the function information available at 
        /src/d06_reporting folder'''
    
    
    
    vd3 = venn3_unweighted([set(col_from_patients),
                            set(col_from_procedures),
                            set(col_from_medications)],
                            set_labels=('Patients','Procedures', 'Medications'),
                            set_colors=('#d7191c','#abdda4', '#2b83ba'),
                            alpha = 0.8)

    for text in vd3.set_labels: # Change Label Size
        text.set_fontsize(16)
    for text in vd3.subset_labels: # Change number size
        text.set_fontsize(12)
        
    if key_id == 'PatientId':
        key_id = 'Patients'
    
    if key_id == 'FRDPersonnelID':
        key_id = 'Providers'
    
    if key_id == 'comp_idx':
        key_id = 'Compound IDs: Patient & Provider'

    plt.title('Venn Diagram for {} Across All Datasets'.format(key_id),
              fontname = 'Times New Roman',
              fontsize = 20,
              pad = 30,
              backgroundcolor = '#f1a340',
              color = 'black')

    return plt.show()

def venn_analysis_short_test(key_id, pat_df_raw, miss_id_df):
                          
    """
    The utility function venn_analysis_short_test was created to provide a visual
    validation of the Venn analysis results.
          
    Properties:
    -----------
                             
        key_id : string (mandatory)
            The string will help document the ID/Column we used to perform this particular
            analysis. (i.e., PatientId, 
                             FRDResponelID (a.k.a., ProviderId), 
                             comp_idx (Concatenation of PatientId with FRDPersonnelID))
                             
        pat_df_raw: DataFrame (mandatory)
            The DataFrame object needs to be the raw patients data frame.
            
            Caution: In order to maintain the proper context for this analysis this pandas
                     DataFrame should come from the *Patients* dataset. Otherwise
                     the test report may show failed status.
        
        miss_id_df: DataFrame (mandatory)
            The DataFrame object needs to be the the missing_df DataFrame provided by
            the venn_analysis_table method.
        
    Return
    ------
        A pandas DataFrame that will show the short test performed.
    """
    
    ### Assert Input ###
    exp_out = "<class 'pandas.core.frame.DataFrame'>"
    s1_in = str(type(pat_df_raw))
    s2_in = str(type(miss_id_df))
    
    assert (s1_in == exp_out and s2_in == exp_out), '''One of the column inputs 
        provided is not a Series, please read the function information available
        at /src/d06_reporting folder'''
    
    assert (str(type(key_id)) == "<class 'str'>"),'''The key_id provided is not
        a string, please read the function information available at 
        /src/d06_reporting folder'''
    
    ### Start Test Script ### 
    test_dict = {"PatientId": [],
                 "Raw Shape": [],
                 "Logical Index Shape": [],
                 "Pass/Fail": []}

    for missId in np.nditer(miss_id_df.values.astype('str')):

        idx = pat_df_raw[key_id] == missId

        if pat_df_raw[idx].shape == (0,12):
            tst_cri = 'PASS'
        else:
            tst_cri = 'FAIL'

        # Update Dictionary
        test_dict["PatientId"].append(missId)
        test_dict["Raw Shape"].append(pat_df_raw.shape)
        test_dict["Logical Index Shape"].append(pat_df_raw[idx].shape)
        test_dict["Pass/Fail"].append(tst_cri)

    test_df=DataFrame(test_dict)

    print('The total number patient IDs with failed status is {}'\
          .format(test_df[test_df['Pass/Fail']=='FAIL'].shape[0]))
    
    return test_df