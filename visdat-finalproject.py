#!/usr/bin/env python
# coding: utf-8

# # Final Project

# ### MK Visualisasi Data Semester Ganjil 2021/2022

# #### Instruksi
# Buatlah aplikasi berbasis web yang menampilkan visualisasi interaktif terkait topik tertentu.
# Visualisasi yang ditampilkan harus memiliki sedikitnya 2 fitur interaktif, seperti sidebar,
# dropdown, dll. Visualisasi interaktif dibuat dengan menggunakan module bokeh dan dideploy pada platform Heroku. Pada dasarnya tidak ada batasan terkait topik yang bisa dipilih
# untuk tugas final project ini.

# In[1]:


# Import library
# Data handling
import pandas as pd
import seaborn as sns

# Bokeh libraries
from bokeh.io import curdoc, output_notebook
from bokeh.plotting import figure, show
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.models import CategoricalColorMapper
from bokeh.palettes import Spectral6
from bokeh.layouts import widgetbox, row, gridplot
from bokeh.models import Slider, Select
from bokeh.models.widgets import Tabs, Panel


# In[2]:


# Fetching url
url_1='https://genshin-impact.fandom.com/wiki/Characters/Comparison#Base_Stats'
url_2='https://genshin-impact.fandom.com/wiki/Characters/List#Playable_Characters'


# In[3]:


# Parsing table from url1 & url2 to dataframe
tables_1 = pd.read_html(url_1)
tables_2 = pd.read_html(url_2)
df1 = tables_1[1]
df2 = tables_2[1]


# In[4]:


df1


# In[5]:


df2


# In[6]:


# Removing NaN columns & merge 2 datasets into 1
df1 = df1.drop(['Icon', 'Ascension Stat', 'Ascension Stat Value'], axis = 1)
df2 = df2.drop(['Icon','Rarity'], axis = 1)
df3 = df1.merge(df2)

df3


# In[7]:


df3.info()


# In[8]:


df3.isnull().sum()


# In[9]:


df = df3.dropna()
df.head()


# In[10]:


duplicateRow = df[df.duplicated()]
duplicateRow


# In[11]:


# The figure will be right in my Jupyter Notebook
output_notebook()

# Isolate the data for the gender choice
female = df[df['Sex'] == 'Female']
male = df[df['Sex'] == 'Male']

# Create a ColumnDataSource object for each team
female_cds = ColumnDataSource(female)
male_cds = ColumnDataSource(male)


# In[13]:


# Create and configure the figure
fig_1 = figure(plot_height=400, plot_width=800,
             title='GENSHIN IMPACT',
             x_axis_label='ATK', y_axis_label='DEF')

# Render the race as step lines
fig_1.circle('ATK', 'DEF', 
         color='#CE1141', legend_label='Female', 
         source=female_cds)
fig_1.circle('ATK', 'DEF', 
         color='#006BB6', legend_label='Male', 
         source=male_cds)


# Move the legend to the upper left corner
fig_1.legend.location = 'top_left'

# Format the tooltip
tooltips = [
            ('Nama Karakter','@Name'),('Nation','@Nation'),
            (' Element', '@Element'),
            ( 'Weapon', '@Weapon'),
           ]

# Add the HoverTool to the figure
fig_1.add_tools(HoverTool(tooltips=tooltips))

# Visualize
show(fig_1)


# In[14]:


# Create and configure the figure
fig_2 = figure(plot_height=400, plot_width=800,
             title='GENSHIN IMPACT',
             x_axis_label='HP', y_axis_label='ATK')

# Render the race as step lines
fig_2.circle('HP', 'ATK', 
         color='#CE1141', legend_label='Female', 
         source=female_cds)
fig_2.circle('HP', 'ATK', 
         color='#006BB6', legend_label='Male', 
         source=male_cds)

# Move the legend to the upper left corner
fig_2.legend.location = 'top_left'



# Format the tooltip
tooltips = [
            ('Nama Karakter','@Name'),('Nation','@Nation'),
            (' Element', '@Element'),
            ( 'Weapon', '@Weapon'),
           ]

# Add the HoverTool to the figure
fig_2.add_tools(HoverTool(tooltips=tooltips))

# Visualize
show(fig_2)


# In[15]:


# Create and configure the figure
fig_3 = figure(plot_height=400, plot_width=800,
             title='GENSHIN IMPACT',
             x_axis_label='HP', y_axis_label='DEF')

# Render the race as step lines
fig_3.circle('HP', 'DEF', 
         color='#CE1141', legend_label='Female', 
         source=female_cds)
fig_3.circle('HP', 'DEF', 
         color='#006BB6', legend_label='Male', 
         source=male_cds)

# Move the legend to the upper left corner
fig_3.legend.location = 'top_left'



# Format the tooltip
tooltips = [
            ('Nama Karakter','@Name'),('Nation','@Nation'),
            (' Element', '@Element'),
            ( 'Weapon', '@Weapon'),
           ]

# Add the HoverTool to the figure
fig_3.add_tools(HoverTool(tooltips=tooltips))

# Visualize
show(fig_3)


# In[16]:


# Create two panels, one for each conference
atkdef_panel = Panel(child= fig_1, title='Perbandinga ATK & DEF')
hpatk_panel = Panel(child= fig_2, title='Perbandingan HP & ATK')
hpdef_panel = Panel(child= fig_3, title='Perbandingan HP & DEF')

# Assign the panels to Tabs
tabs = Tabs(tabs=[atkdef_panel, hpatk_panel, hpdef_panel])

# Show the tabbed layout
show(tabs)


# In[58]:


# Define the callback function: update_plot
def update_plot(attr, old, new):
    # set the `gi` name to `slider.value` and `source.data = new_data`
    gi = slider.value
    x = x_select.value
    y = y_select.value
    female = df[df['Sex'] == 'Female']
    male = df[df['Sex'] == 'Male']
    
    # Add title to figure: plot.title.text
    fig_1.title.text = 'Gapminder data for %d' % gi


# In[59]:


# Make a slider object: slider
slider = Slider(start=0, end=1000, step=1, value=0, title='Year')
slider.on_change('value',update_plot)


# In[60]:


# Create layout and add to current document
layout = row(widgetbox(slider), tabs)
curdoc().add_root(layout)


# In[61]:


# Make dropdown menu for x and y axis
# Create a dropdown Select widget for the x data: x_select
x_select = Select(
    options=['ATK', 'HP', 'DF'],
    value='ATK',
    title='x-axis data'
)

# Attach the update_plot callback to the 'value' property of x_select
x_select.on_change('value', update_plot)

# Create a dropdown Select widget for the y data: y_select
y_select = Select(
    options=['ATK', 'HP', 'DF'],
    value='HP',
    title='y-axis data'
)
# Attach the update_plot callback to the 'value' property of y_select
y_select.on_change('value', update_plot)


# In[55]:


# Create layout and add to current document
layout = row(widgetbox(slider, x_select, y_select), fig_1)
show(layout)


# In[ ]:


bokeh serve --show visdat-finalproject.py
bokeh logs --tail --app visdat-finalproject
