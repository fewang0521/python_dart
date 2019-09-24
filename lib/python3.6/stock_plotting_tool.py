#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# -*- coding: utf-8 -*-

## import necessary module
import pandas as pd
import numpy as np
import subprocess as sp

#class start
class stock_plotting_tool:
    def __init__(self, directory, plot_keyword):
        self.str_dir=directory
        self.target_search_keyword=plot_keyword
        ##due to null character, excludes the last character
        self.current_directory=sp.check_output('pwd').decode('utf-8')[:-1]
        self.target_file=self.current_directory+self.str_dir
    
    def load_table(self,category):
        #read html file and conver to dataframe
        html=pd.read_html(self.target_file, '총매출액')
        org_dataframe=html[0]
        
        #pick '순매출액' from the table
        table_get=(org_dataframe['구 분']==category)
        org_dataframe=org_dataframe[table_get['구 분']]
        return org_dataframe
    
    def load_table_html(self,html_org,category):
        #read html file and conver to dataframe
        html=pd.read_html(html_org, category)
        org_dataframe=html[0]
        
        #pick '순매출액' from the table
        table_get=(org_dataframe['구 분']==category)
        org_dataframe=org_dataframe[table_get['구 분']]
        return org_dataframe
    
    def refine_loaded_table(self, dataframe):
        #category column extract
        target_name_column_join='부문'
        target_name_first_column=dataframe[target_name_column_join].columns[0]
        target_name_second_column=dataframe[target_name_column_join].columns[1]
        result_name_column_join= target_name_first_column+' - '+ target_name_second_column
        list_category=[]
        dataframe_for_target_column=pd.DataFrame()
        size_indice=dataframe.index.size
        
        for index in range(size_indice):
            string=dataframe[target_name_column_join][target_name_first_column].iloc[index]+' - ' +dataframe[target_name_column_join][target_name_second_column].iloc[index]
            list_category.append(string)
        dataframe_for_target_column[result_name_column_join]=list_category
        #############
        
        ## period column start index get
        index_column=0
        for i in dataframe.columns:
            #print(i)
            if i[0] == '구 분':
                refer_column=index_column
                start_column = refer_column + 1
                break
            index_column=index_column +1
        ##################
        
        ## set creation for storing target periods
        set_periods=set()
        for top_column_cate in dataframe.iloc[:,start_column:]:
            set_periods.add(top_column_cate[0])
        set_periods_sorted=sorted(set_periods, reverse=True)
        ###################
        
        ######## dataframe for info in periods' table
        temp_df=pd.DataFrame()
        for period in set_periods_sorted:
            temp_df[period]=dataframe.iloc[:,start_column:-1][period][self.target_search_keyword]
            #print(temp_df[period])
            temp_df[period]=temp_df[period].replace('-','0')
            temp_df[period]=pd.to_numeric(temp_df[period])
        
        ######################
        
        ## check temp df created
        temp_df.reset_index(inplace=True)
        temp_df=temp_df.drop(columns=['index'])
        #########
        
        ###dataframe merge
        new_df=pd.merge(dataframe_for_target_column,temp_df,how='outer', left_index=True, right_index= True)
        #############
        return new_df
    
    def portion_get(self, dataframe):
        total=dataframe.iloc[:,1:].sum(axis=0)
        new_df=pd.DataFrame()
        firstcolumn=dataframe.columns[0]
        new_df[firstcolumn]=dataframe[firstcolumn]
        for i in dataframe.iloc[:,1:].columns:
            new_df[i]=dataframe[i]/total[i]
        return new_df

