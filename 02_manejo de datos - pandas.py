#!/usr/bin/env python
# coding: utf-8

# # Tutorial Manejo de Datos y Pandas
# 
# ## Estructuras de Datos e Índices
# 
# 
# Pandas soporta la lectura de una amplia cantidad de formatos ([más info](http://pandas.pydata.org/pandas-docs/stable/io.html)): 
# 
# - read_csv
# - read_excel
# - read_hdf
# - read_sql
# - read_json
# - read_msgpack (experimental)
# - read_html
# - read_gbq (experimental)
# - read_stata
# - read_sas
# - read_clipboard
# - read_pickle
# 
# Vamos a empezar a probar con una dataset publicado para una competencia de kaggle: [Titanic: Machine Learning from Disaster](https://www.kaggle.com/c/titanic/data).

# In[1]:


import numpy as np
import pandas as pd
import seaborn.apionly as sns
import matplotlib.pyplot as plt


# In[2]:


#setup para el notebook

get_ipython().run_line_magic('matplotlib', 'inline')
pd.options.display.max_rows = 10
pd.options.display.float_format = '{:,.2f}'.format
plt.rcParams['figure.figsize'] = (16, 12)


# In[5]:


data = pd.read_csv("./Bases/titanic.csv", index_col="PassengerId")
data.columns

data
# In[6]:

data.index


# Las estructuras de datos en pandas, por lo general, no son modificadas en vivo con comandos como `set_index`, para hacer eso es necesario cambiar el argumento `inplace` o reasignar la variables

# ## Tipos de Indexado
# 
# Hay varias formas de seleccionar un subconjunto de los datos:
# 
# - Como las listas o arrays, por posición.
# - Como los diccionarios, por llave o etiqueta.
# - Como los arrays, por máscaras de verdadero o falso.
# - Se puede indexar por número, rango o lista (array)
# - Todos estos métodos pueden funcionar subconjunto como en las columnas
# 
# 
# ## Reglas Básicas
# 
# 1. Se usan corchetes (abreviatura para el método `__getitem__`) para seleccionar columnas de un `DataFrame`
# 
#     ```python
#     >>> df[['a', 'b', 'c']]
#     ```
# 
# 2. Se usa `.iloc` para indexar por posición (tanto filas como columnas)
# 
#     ```python
#     >>> df.iloc[[1, 3], [0, 2]]
#     ```
#     
# 3. Se usa `.loc` para indexar por etiquetas (tanto filas como columnas)
# 
#     ```python
#     >>> df.loc[["elemento1", "elemento2", "elemento3"], ["columna1", "columna2"]]
#     ```
# 
# 4. `ix` permite mezclar etiquetas y posiciones (tanto filas como columnas)
# 
#     ```python
#     >>> df.ix[["elemento1", "elemento2", "elemento3"], [0, 2]]
#     ```
#     ```python
#     >>> df.ix[[1, 3], ["columna1", "columna2"]]
#     ```
# 


data.loc[[1, 2, 3], ["Name", "Sex"]]


data.iloc[[1, 2, 3], [2, 3]]


data.ix[[1, 2, 3], ["Name", "Sex"]]


temp = data.copy()
temp.index = ["elemento_" + str(i) for i in temp.index]
temp


temp.loc[["elemento_1", "elemento_2", "elemento_3"], ["Name", "Sex"]]

temp.iloc[[1, 2, 3], [2, 3]]

temp.ix[[1, 2, 3], ["Name", "Sex"]]


del temp

data.loc[:3, :"Sex"]

#indexar por `slices`

data.iloc[:3]

data.iloc[-3:]


data.loc[1:10, ["Name", "Sex", "Ticket"]]


data[["Name", "Ticket"]]


use_cols = ["Name", "Ticket"]
data[use_cols]


data["Name"]


cols =["Name"]
data[cols]


data.Name


temp = data[["Name"]].copy()
temp.OtroNombre = ["OTRO_" + n for n in data.Name]
temp


temp.OtroNombre[:10]


temp["OtroNombre"] = ["OTRO_" + n for n in data.Name]
temp


del temp



data.iloc[1]


data.iloc[[1]]


data.SibSp



data["NumFam"] = data.SibSp + data.Parch
data


# In[31]:


data.SibSp > 0


# In[32]:


#otra forma de filtrar es con mascaras binarias (`boolean`)
data[data.SibSp > 0][["Sex", "Age"]]


# In[27]:


data[["Age", "ex"]]


# In[28]:


data[(data.SibSp > 0) | (data.Age < 18)]


# ### Ejercicio
# 
# ###### seleccionar varones mayores de 65 años que viajan solos

# In[ ]:


# escribir la solucion aqui...


# In[ ]:


# %load soluciones/mayores_solos.py


# ### Filtrado de filas y columnas
# 
# Para eliminar lo que no quieren en lugar de seleccionar lo que sì
# 
# ```
# DataFrame.drop(etiquetas, axis=0, ...)
# 
# Parámetros
# ----------
# etiquetas : etiqueta o lista de etiquetas
# axis : entero o nombre de la dimesión
#     - 0 / 'index', para eliminar filas
#     - 1 / 'columns', para elimnar columnas
# ```

# In[38]:


data.shape


# In[39]:


valid_index = np.random.choice(data.index, int(data.index.shape[0] * 0.1), replace=False)
valid_index


# In[40]:


train = data.drop(valid_index)
valid = data.loc.__getitem__(valid_index)
train


# In[41]:


valid


# In[42]:


X_train, y_train = train.drop("Survived", axis=1), train["Survived"]
X_valid, y_valid = valid.drop("Survived", axis=1), valid["Survived"]
X_train


# In[43]:


y_train


# ### Agrupaciones y Tablas de Contingencia
# 
# #### Agrupaciones
# 
# Las agrupaciones sirven para hacer cálculos sobre subconjuntos de los datos, generalmente tienen tres partes:
# 
# 1. Definir los grupos
# 2. Aplicar un cálculo
# 3. Combinar los resultados

# In[44]:


#agrupar
agrupado = data.groupby("Pclass")
agrupado


# In[45]:


#sólo hemos agrupado, no se ha hecho ningún cálculo, para eso hay que aplicar alguna función
agrupado.Survived.mean()


# In[46]:


agrupado.Survived.agg({"media": "mean", "media_2": np.mean, "varianza": "var", "cantidad": "count"})


# In[47]:


data.columns


# In[48]:


data.groupby("Survived")[['Age', 'SibSp', 'Parch', 'NumFam', 'Fare']].mean()


# #### Tablas de Contingencia
# 
# Las tablas de contingencia asemejan las tablas dinámicas de excel, sirven apra ver inteacciones entre variables

# In[49]:


pd.crosstab(data.Pclass, data.Survived)


# In[50]:


pd.crosstab(data.Pclass, data.Survived).apply(lambda x: x/x.sum(), axis=1)


# In[52]:


data.Survived.value_counts()


# In[54]:


get_ipython().run_line_magic('pinfo', 'data.Survived.value_counts')


# In[53]:


data.Survived.value_counts(True).sort_index()


# In[ ]:


pd.crosstab(data.Pclass, pd.cut(data.Age, [i * 10 for i in range(9)]), 
            values=data.Survived, aggfunc=np.mean)


# In[ ]:


pd.crosstab(data.Pclass, pd.cut(data.Age, [i * 10 for i in range(9)]))


# ### Poniendo todo junto en un ejemplo de Data Mining

# In[56]:


#hay variables que no son numericas y que hay que codificar antes que nada
tipos = data.dtypes
tipos.value_counts()


# In[57]:


tipos_objeto = tipos[tipos == "object"]
tipos_objeto


# In[58]:


nulos = data.isnull().sum()
nulos


# In[59]:


nulos[nulos > 0]


# In[60]:


data["Sex"].value_counts()


# In[61]:


data["Sex"] = data.Sex.apply(lambda x: {"male": 0, "female": 1}[x])
data["Sex"].value_counts()


# In[62]:


data["Ticket"].unique().shape


# In[63]:


data["Ticket"].factorize()


# In[64]:


data["Ticket"] = data["Ticket"].factorize()[0]
data["Ticket"].value_counts()


# In[67]:


data.Embarked.fillna(-1).value_counts()


# In[68]:


data[data.Embarked.isnull()]


# In[69]:


data[(data.Fare >= 70) & (data.Fare <= 90)].Embarked.value_counts()


# In[70]:


data.Embarked.fillna("S", inplace=True)
data.Embarked.fillna(-1).value_counts()


# In[71]:


pd.crosstab(data.Embarked, data.Survived)


# In[ ]:


pd.crosstab(data.Embarked, data.Survived).apply(lambda x: x/x.sum(), axis=1)


# In[72]:


pd.get_dummies(data.Embarked)


# In[73]:


data = data.join(pd.get_dummies(data.Embarked)).drop("Embarked", axis=1)


# In[74]:


data


# In[75]:


data.Cabin.fillna(-1).value_counts()


# In[76]:


data["Cabin"] = data.Cabin.fillna(-1).factorize()[0]


# In[77]:


data


# In[78]:


data.Age.fillna(-1).value_counts()


# In[79]:


pd.crosstab(data.Age.isnull(), data.Survived).apply(lambda x: x/x.sum(), axis=1)


# In[80]:


data["Age_nul"] = data.Age.isnull().astype(int)
data


# In[81]:


data.Age.fillna(data.Age.mean(), inplace=True)
data


# In[82]:


data.isnull().sum().sum()


# In[83]:


data.drop("Name", axis=1, inplace=True)
data


# In[84]:


data.dtypes.value_counts()


# In[ ]:


data.info()


# In[ ]:


valid_index

