
# coding: utf-8

# ## Import packages

# In[1]:


import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()


# ## Import raw data

# In[2]:


col=['col1','col2','col3','col4','col5','col6','col7','col8','col9','col10','NAN']

## function import data
def import_data(name,Col):
    filename=pd.read_csv(name,names=Col,header=None)
    filename = filename.drop('NAN',axis=1)
    filename = filename.drop('col2',axis=1)
    return filename

## impoprt Data
dataF1 = import_data("path/to/file",col)
dataF2 = import_data("path/to/file",col)
dataF3 = import_data("path/to/file",col)
dataF4 = import_data("path/to/file",col)
dataF5 = import_data("path/to/file",col)
dataF6 = import_data("path/to/file",col)
dataF7 = import_data("path/to/file",col)
dataF8 = import_data("path/to/file",col)


# ## New col1 list

# In[3]:


col1=list(dataF1['col1'].str.split(' '))
col1_list={}
for i in range (0,24):
    col1_list[col1[i][4]]= '{num:02d}'.format(num=i)
col1_new=col1_list.values()


# In[4]:


date=dataF1['col1'][1][1:12]


# ## analysis

# In[5]:


## counting
def counting(name1):
    total1 = name1['col3'].sum()
    total2 = name1['col4'].sum()
    total3 = name1['col5'].sum()
    total4 = total1+total2+total3
    total=[total1,total2,total3,total4]
    return total

sbTotal = counting(dataF2)
smTotal = counting(dataF8)
stTotal = counting(dataF4)
ssTotal = counting(dataF6)

col2_one = int(sbTotal[0]+smTotal[0]+stTotal[0]+ssTotal[0])
col2_two = int(sbTotal[1]+smTotal[1]+stTotal[1]+ssTotal[1])
col2_three = int(sbTotal[2]+smTotal[2]+stTotal[2]+ssTotal[2])
col2_four = int(sbTotal[3]+smTotal[3]+stTotal[3]+ssTotal[3])


# In[6]:


## summary Table
def stat(name2):
    stat_list=[]
    for i in range(2,10):
        stat_list.append(round(name2[col[i]].mean(),2))
    
    return stat_list

sb_mean= stat(dataF2)
sm_mean= stat(dataF8)
st_mean= stat(dataF4)
ss_mean= stat(dataF6)
summ_table = pd.DataFrame()
summ_table['Title']= col[2:10]
summ_table['sb']=sb_mean
summ_table['sm']=sm_mean
summ_table['st']=st_mean
summ_table['ss']=ss_mean


# In[7]:


## Check Status
list_thrs = ['col6','col7','col9','col10']
col6_thrs = 95
ms_thrs = 99
mo_thrs = 95
mt_thrs = 96

ms_min = mo_min = mt_min = col6_min = 80

def create_minlist(name3):
    min_list=[]
    for kpi in list_thrs:
        col1 , percent =(name3[['col1',kpi]][name3[kpi] ==name3[85:][kpi].min()]).iloc[0,:]
        min_list.append((col1[12:] , percent))
    return min_list


sb_min=create_minlist(dataF2)
sm_min=create_minlist(dataF8)
st_min=create_minlist(dataF4)
ss_min=create_minlist(dataF6)

Min_table = pd.DataFrame()
Min_table['Title']= list_thrs
Min_table['sb']=sb_min
Min_table['sm']=sm_min
Min_table['st']=st_min
Min_table['ss']=ss_min

def find_cntmin(name4):
    cnt_list=[]
    cnt_list.append(len(name4[85:]['col1'][name4[85:].col6 < col6_thrs]))
    cnt_list.append(len(name4[85:]['col1'][name4[85:].col7 < ms_thrs]))
    cnt_list.append(len(name4[85:]['col1'][name4[85:].col9 < mo_thrs]))
    cnt_list.append(len(name4[85:]['col1'][name4[85:].col10 < mt_thrs]))
    return cnt_list

sb_cnt = find_cntmin(dataF2)
sm_cnt = find_cntmin(dataF8)
st_cnt = find_cntmin(dataF4)
ss_cnt = find_cntmin(dataF6)

Cnt_table = pd.DataFrame()
Cnt_table['Title']= list_thrs
Cnt_table['sb']=sb_cnt
Cnt_table['sm']=sm_cnt
Cnt_table['st']=st_cnt
Cnt_table['ss']=ss_cnt


# In[8]:


Cnt_table


# In[9]:


Min_table


# ##  Charts

# In[10]:


get_ipython().run_line_magic('matplotlib', 'qt')
fig , ax = plt.subplots(2,3)
fig.suptitle(date, fontsize=16)


def plot_sc(n,m,name,title,total):
    ax[n,m].set_title(title )
    ax[n,m].set_xlabel('col1(h)')
    ax[n,m].set_ylabel('TotalCount: %i' % total[3] )

    width = 0.4
    p1 = ax[n,m].bar(col1_new,name['col3'],width,color='orange')
    p2 = ax[n,m].bar(col1_new,name['col4'],width, bottom=name['col3'],color='cyan')
    p3 = ax[n,m].bar(col1_new,name['col5'], width , bottom=name['col3']+name['col4'],color='r')
    ax[n,m].legend(['CPtoMS','col4','MStoCP'],loc=2)
    #plt.rcParams["figure.figsize"]=(20,20)
    ax2 = ax[n,m].twinx()
    ax2.set_ylabel('Percentage')
    c1 = ax2.plot(col1_new,name['col6'],color='b')
    c2 = ax2.plot(col1_new,name['col7'],color='r')
    c3 = ax2.plot(col1_new,name['col9'],color='g')
    c4 = ax2.plot(col1_new,name['col10'],color='olive')
    ax2.legend(['col6','%col4','%col3','%col5'],loc=1)
#    fig.tight_layout()
    return ax[n,m]


plot_sc(0,0,dataF1,'F1',sbTotal)
plot_sc(0,2,dataF7,'F7',smTotal)
plot_sc(1,0,dataF3,'F3',stTotal)
plot_sc(1,2,dataF5,'F5',ssTotal)


## pie chart

labels = 'col5','col4','col3'
size=[col2_one,col2_two,col2_three]
colors =['gold','lightcoral','lightskyblue']
explode = (0.1 , 0.1 , 0.1)
ax[0,1].pie(size,explode = explode,labels=labels,colors=colors,autopct='%1.1f%%',shadow=True,startangle=140)
ax[0,1].set_title('Total = %i' % col2_four) 

ax[1,1].axis('off')
ax[1,1].axis('tight')
table =ax[1,1].table(cellText=summ_table.values, colLabels=summ_table.columns, loc='center')
table.auto_set_font_size(False)
table.set_fontsize(14)

plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=.3)

