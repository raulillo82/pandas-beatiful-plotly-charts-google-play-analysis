import pandas as pd
import plotly.express as px

df_apps = pd.read_csv('apps.csv')

print("""How many rows and columns does apps.csv have? What are the column
names? What does the data look like? Look at a random sample of 5 different
rows with .sample()
      """)
print(df_apps.shape)
print(df_apps.sample(5))

print("""
Remove the columns called Last_Updated and Android_Ver
from the DataFrame. We will not use these columns.
      """)
df_apps.drop(['Last_Updated', 'Android_Ver'],
             axis=1, inplace=True)
print(df_apps.shape)
print(df_apps.sample(5))

print("""
How many rows have a NaN value (not-a-number) in the Rating column?
Create DataFrame called df_apps_clean that does not include these rows.
      """)
nan_rows = df_apps[df_apps.Rating.isna()]
print(nan_rows.shape)
print(nan_rows.head())
df_apps_clean = df_apps.dropna()
print("After processing:")
print(df_apps_clean.shape)

print("""
Are there any duplicates in data? Check for duplicates using the .duplicated() function.
How many entries can you find for the "Instagram" app? Use .drop_duplicates() to remove any duplicates from df_apps_clean.
      """)
duplicated_rows = df_apps_clean[df_apps_clean.duplicated()]
print(duplicated_rows.shape)
print(duplicated_rows.head())
print("")
print(df_apps_clean[df_apps_clean.App == 'Instagram'])
print("")
df_apps_clean = df_apps_clean.drop_duplicates(subset=['App',
                                                      'Type', 'Price'])
print(df_apps_clean[df_apps_clean.App == 'Instagram'])
print("After processing:")
print(df_apps_clean.shape)

print("""
      Identify which apps are the highest rated. What problem might you encounter if you rely exclusively on ratings alone to determine the quality of an app?
      """)
print(df_apps_clean.sort_values('Rating', ascending=False).head())

print("""
      What's the size in megabytes (MB) of the largest Android apps in the Google Play Store. Based on the data, do you think there could be a limit in place or can developers make apps as large as they please?
      """)
print(df_apps_clean.sort_values('Size_MBs', ascending=False).head())

print("""
      Which apps have the highest number of reviews? Are there any paid apps among the top 50?
      """)
df_top_50_reviews = df_apps_clean.sort_values('Reviews', ascending=False).head(50)
print(df_top_50_reviews.head())
print("")
print(not df_top_50_reviews[df_top_50_reviews.Type == 'Paid'].empty)

print("""
      All Android apps have a content rating like “Everyone” or “Teen” or “Mature 17+”. Let’s take a look at the distribution
      """)
ratings = df_apps_clean.Content_Rating.value_counts()
print(ratings)

print("""
      Visualise it with plotly: create a pie chart
      """)

fig = px.pie(labels=ratings.index, values=ratings.values)
fig = px.pie(labels=ratings.index,
             values=ratings.values,
             title="Content Rating",
             names=ratings.index,
             hole=0.6)
fig.update_traces(textposition='outside', textinfo='percent+label')
fig.show()

print("""
      How many apps had over 1 billion (that's right - BILLION) installations? How many apps just had a single install?

    Check the datatype of the Installs column.
    Count the number of apps at each level of installations.
    Convert the number of installations (the Installs column) to a numeric data type. Hint: this is a 2-step process. You'll have to make sure you remove non-numeric characters first.
    """)

print(df_apps_clean.Installs.describe())
print(df_apps_clean[['App', 'Installs']].groupby('Installs').count())

print("""
Remove the ',' character in Installs field
      """)
df_apps_clean.Installs = df_apps_clean.Installs.astype(str).str.replace(',', "")
df_apps_clean.Installs = pd.to_numeric(df_apps_clean.Installs)
print(df_apps_clean[['App', 'Installs']].groupby('Installs').count())

print("""
      Convert the price column to numeric data. Then investigate the top 20 most expensive apps in the dataset.

Remove all apps that cost more than $250 from the df_apps_clean DataFrame.

Add a column called 'Revenue_Estimate' to the DataFrame. This column should hold the price of the app times the number of installs. What are the top 10 highest-grossing paid apps according to this estimate? Out of the top 10, how many are games?
      """)
print(df_apps_clean.Price.describe())
df_apps_clean.Price = df_apps_clean.Price.astype(str).str.replace('$', "")
df_apps_clean.Price = pd.to_numeric(df_apps_clean.Price)
print(df_apps_clean.sort_values('Price', ascending=False).head(20))
print("")
df_apps_clean = df_apps_clean[df_apps_clean['Price'] < 250]
print(df_apps_clean.sort_values('Price', ascending=False).head(5))
df_apps_clean['Revenue_Estimate'] = df_apps_clean.Installs.mul(df_apps_clean.Price)
print("")
print(df_apps_clean.sort_values('Revenue_Estimate', ascending=False)[:10])

print("""
      Find the number of different categories
      """)
print(df_apps_clean.Category.nunique())
print("")
top10_category = df_apps_clean.Category.value_counts()[:10]
print(top10_category)
bar = px.bar(x = top10_category.index, # index = category name
             y = top10_category.values)
bar.show()

print("""
      What matters is not just the total number of apps in the category but how often apps are downloaded in that category.
      This will give us an idea of how popular a category is:
      """)
category_installs = df_apps_clean.groupby('Category').agg({'Installs': pd.Series.sum})
h_bar = px.bar(x = category_installs.Installs,
               y = category_installs.index,
               orientation='h',
               title='Category Popularity')
h_bar.update_layout(xaxis_title='Number of Downloads', yaxis_title='Category')
h_bar.show()

print("""
      Let’s use plotly to create a scatter plot.
      Create a DataFrame that has the number of apps in one column and the number of installs in another.
      Then use the plotly express examples from the documentation alongside the
      .scatter() API reference to create scatter plot that looks like the chart
      above.
      Hint: Use the size, hover_name and color parameters in .scatter().
      To scale the y-axis, call .update_layout() and specify that the y-axis should be on a log-scale like so: yaxis=dict(type='log')
      """)
cat_number = df_apps_clean.groupby('Category').agg({'App': pd.Series.count})
cat_merged_df = pd.merge(cat_number, category_installs, on='Category', how="inner")
print(f'The dimensions of the DataFrame are: {cat_merged_df.shape}')
cat_merged_df.sort_values('Installs', ascending=False)
scatter = px.scatter(cat_merged_df, # data
                     x='App', # column name
                     y='Installs',
                     title='Category Concentration',
                     size='App',
                     hover_name=cat_merged_df.index,
                     color='Installs')

scatter.update_layout(xaxis_title="Number of Apps (Lower=More Concentrated)",
                      yaxis_title="Installs",
                      yaxis=dict(type='log'))
scatter.show()

print("""
      How many different types of genres are there?
      Can an app belong to more than one genre?
      Check what happens when you use .value_counts() on a column with nested values?
      See if you can work around this problem by using the .split() function and the DataFrame's .stack() method.
      """)
print(len(df_apps_clean.Genres.unique()))
print(df_apps_clean.Genres.value_counts().sort_values()[:5])
# Split the strings on the semi-colon and then .stack them.
stack = df_apps_clean.Genres.str.split(';', expand=True).stack()
print(f'We now have a single column with shape: {stack.shape}')
num_genres = stack.value_counts()
print(f'Number of genres: {len(num_genres)}')

print("""
      Create a chart with the Series containing the genre data
      """)
bar = px.bar(x = num_genres.index[:15], # index = category name
             y = num_genres.values[:15], # count
             title='Top Genres',
             hover_name=num_genres.index[:15],
             color=num_genres.values[:15],
             color_continuous_scale='Agsunset')

bar.update_layout(xaxis_title='Genre',
yaxis_title='Number of Apps',
coloraxis_showscale=False)
bar.show()

print("""
      Let’s see what the split is between free and paid apps.
      """)
print(df_apps_clean.Type.value_counts())
df_free_vs_paid = df_apps_clean.groupby(["Category", "Type"], as_index=False).agg({'App': pd.Series.count})
print(df_free_vs_paid.head())
print("""
      Use the plotly express bar chart examples and the .bar() API reference to create a bar chart:
      You'll want to use the df_free_vs_paid DataFrame that you created above that has the total number of free and paid apps per category.
      See if you can figure out how to get the look above by changing the categoryorder to 'total descending' as outlined in the documentation here.
      """)
g_bar = px.bar(df_free_vs_paid,
               x='Category',
               y='App',
               title='Free vs Paid Apps by Category',
               color='Type',
               barmode='group')
g_bar.update_layout(xaxis_title='Category',
                    yaxis_title='Number of Apps',
                    xaxis={'categoryorder':'total descending'},
                    yaxis=dict(type='log'))
g_bar.show()

print("""
      Create a box plot that shows the number of Installs for free versus paid apps.
      How does the median number of installations compare? Is the difference large or small?
      Use the Box Plots Guide and the .box API reference to create the chart above.
      """)
box = px.box(df_apps_clean,
             y='Installs',
             x='Type',
             color='Type',
             notched=True,
             points='all',
             title='How Many Downloads are Paid Apps Giving Up?')

box.update_layout(yaxis=dict(type='log'))
box.show()

print("""
      Generate a chart with more data:
      """)
df_paid_apps = df_apps_clean[df_apps_clean['Type'] == 'Paid']

box = px.box(df_paid_apps,
             x='Category',
             y='Revenue_Estimate',
             title='How Much Can Paid Apps Earn?')

box.update_layout(xaxis_title='Category',
                  yaxis_title='Paid App Ballpark Revenue',
                  xaxis={'categoryorder':'min ascending'},
                  yaxis=dict(type='log'))


box.show()

print("""
      What is the median price for a paid app?
      Then compare pricing by category by creating another box plot.
      But this time examine the prices (instead of the revenue estimates) of the paid apps.
      I recommend using {categoryorder':'max descending'} to sort the categories.
      """)
box = px.box(df_paid_apps,
             x='Category',
             y="Price",
             title='Price per Category')

box.update_layout(xaxis_title='Category',
                  yaxis_title='Paid App Price',
                  xaxis={'categoryorder':'max descending'},
                  yaxis=dict(type='log'))
box.show()
