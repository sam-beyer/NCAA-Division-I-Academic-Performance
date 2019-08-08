# Sam Beyer
# Dr. Stonedahl
# Individual Visualization Project
# April 29th, 2019


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

main_df = pd.read_csv("database.csv")

# Cleaning the dataframe up. Getting rid of all the unneccessary columns
del main_df["SCHOOL_ID"]
del main_df["SCHOOL_TYPE"]
del main_df["SPORT_CODE"]

# Specifically looking at NCAA Divison 1 Schools (not sufficient evidence of 
# other schools)
main_df = main_df[main_df.NCAA_DIVISION != 2]
main_df = main_df[main_df.NCAA_DIVISION != 3]

# For any value that the data set did not have, the data uses the value "-99".
# I instead converted all the "-99" values to NaN to make them easier to work
# with.
df_with_na = main_df.replace(-99, np.nan)

# Drop all values with no information. This goes for any row. "clean_df"
# will be used when looking at data set as a whole
clean_df = df_with_na.dropna()

# Grouping the conferences by the average 2014 eligibility of all the sports in
# each conference.
conference_eligibility_2014 = df_with_na.groupby('NCAA_CONFERENCE').mean()['2014_ELIGIBILITY']

by_conf = df_with_na.groupby('NCAA_CONFERENCE').mean()

by_sport = df_with_na.groupby('SPORT_NAME').mean()

by_school = df_with_na.groupby('SCHOOL_NAME').mean()

by_gender = by_sport.reset_index(level=0)

# Graph 1
# Looking at the difference between the year 2004 and 2014 of top 10 and bottom
# 10 APR schools. Size of the dot shows eligibility.
top_10_APR_by_school = by_school.sort_values(by = 'FOURYEAR_SCORE', ascending=False)[:10]
top_10_APR_by_school = top_10_APR_by_school.reset_index(level=0)


bottom_10_APR = by_school.sort_values(by = 'FOURYEAR_SCORE')[:10]
bottom_10_APR = bottom_10_APR.reset_index(level=0)

top_bottom_10 = pd.concat([top_10_APR_by_school, bottom_10_APR])

top_bottom_10['APR Rank'] = top_bottom_10['FOURYEAR_SCORE'] > 960

top_bottom_10 = top_bottom_10.replace(False, "Bottom 10 Institution")
top_bottom_10 = top_bottom_10.replace(True, "Top 10 Institution")
# Make the graph labels clear
top_bottom_10 = top_bottom_10.rename(index=str, columns={"2014_SCORE": "2014 APR Score",
                                                   "2004_SCORE": "2004 APR Score",
                                                   "FOURYEAR_ELIGIBILITY":
                                                       "4 Year Eligibility Percentage"})

sns.set()
sns.relplot(x="2004 APR Score", y="2014 APR Score", hue="APR Rank", size=
            "4 Year Eligibility Percentage",
            data=top_bottom_10)
plt.ylim(900, None)
plt.xlim(900, None)

plt.title("Progression of APR Scores\n in NCAA Division 1 Athletics")    
plt.savefig("Graph_1.png")
  
# Graph number 2
# Looking at the progession of the top 10 APR schools from 2004 to 2016 versus
# the progression of the bottom 10 APR schools from 2004 to 2016.
new_data = top_10_APR_by_school[['SCHOOL_NAME',
        '2014_SCORE', 
        '2013_SCORE', 
        '2012_SCORE', 
        '2011_SCORE', 
       '2010_SCORE', 
        '2009_SCORE', 
       '2008_SCORE', 
        '2007_SCORE', 
        '2006_SCORE', 
       '2005_SCORE',
       '2004_SCORE', ]]

new_top10 = pd.melt(new_data, id_vars=["SCHOOL_NAME"], 
                  var_name="Year", value_name="APR Score")

new_top10['Year'] = new_top10['Year'].apply(lambda yr: int(yr.replace('_SCORE','')))



new_bottom10 = bottom_10_APR[['SCHOOL_NAME',
        '2014_SCORE', 
        '2013_SCORE', 
        '2012_SCORE', 
        '2011_SCORE', 
       '2010_SCORE', 
        '2009_SCORE', 
       '2008_SCORE', 
        '2007_SCORE', 
        '2006_SCORE', 
       '2005_SCORE',
       '2004_SCORE']]

new_bottom10 = pd.melt(new_bottom10, id_vars=["SCHOOL_NAME"], 
                  var_name="Year", value_name="APR Score")

new_bottom10['Year'] = new_bottom10['Year'].apply(lambda yr: int(yr.replace('_SCORE','')))

new_top_bottom = pd.concat([new_bottom10, new_top10])

new_top_bottom['Bottom or Top'] = new_top_bottom['APR Score']

new_top_bottom['Bottom or Top'].values[new_top_bottom['Bottom or Top'] < 981] = 0

new_top_bottom['Bottom or Top'].values[new_top_bottom['Bottom or Top'] > 981] = 1

new_top_bottom = new_top_bottom.replace(0, "Bottom 10 Institution")
new_top_bottom = new_top_bottom.replace(1, "Top 10 Institution")


sns.relplot(x="Year", y="APR Score",
            hue="SCHOOL_NAME", col="Bottom or Top",
            facet_kws=dict(sharex=False),
            kind="line", legend="full", data=new_top_bottom);

plt.savefig("Graph_2.png")

# Graph number 3

# Looking at progession of APR scores for conferecnes as a whole from 2004 to
# 2014. Compares the power 5 conferences with the Ivy League.
power_5 = {"Big Ten Conference", "Atlantic Coast Conference", "Pac-12 Conference", 
           "Big 12 Conference", "Southeastern Conference", "The Ivy League"}

p5_academics = by_conf[by_conf.index.isin(power_5)]

p5_academics = p5_academics.reset_index(level=0)

new_p5 = p5_academics[['NCAA_CONFERENCE',
        '2014_SCORE', 
        '2013_SCORE', 
        '2012_SCORE', 
        '2011_SCORE', 
       '2010_SCORE', 
        '2009_SCORE', 
       '2008_SCORE', 
        '2007_SCORE', 
        '2006_SCORE', 
       '2005_SCORE',
       '2004_SCORE', ]]

new_p5 = pd.melt(new_p5, id_vars=["NCAA_CONFERENCE"], 
                  var_name="Year", value_name="APR Score")

new_p5['Year'] = new_p5['Year'].apply(lambda yr: int(yr.replace('_SCORE','')))

new_p5 = new_p5.rename(index=str, columns={'NCAA_CONFERENCE':'NCAA Conference'})

sns.relplot(x="Year", y="APR Score",
            hue="NCAA Conference",
            facet_kws=dict(sharex=False),
            kind="line", legend="full", data=new_p5);

plt.title("Power 5 Conferences and The Ivy League \n APR Score Progression\n")
plt.savefig("Graph_3.png")
# Graph number 4

# Looking at all the power 5 conferences spread of all sports 4 year APR
# score compared to the Ivy League's schools/sports 4 year APR scores.

exdf = clean_df[clean_df['NCAA_CONFERENCE'].str.match('Southeastern')]

exdf1 = clean_df[clean_df['NCAA_CONFERENCE'].str.match('Big Ten')]

exdf2 = clean_df[clean_df['NCAA_CONFERENCE'].str.match('Big 12')]

exdf3 = clean_df[clean_df['NCAA_CONFERENCE'].str.match('Pac-12')]

exdf4 = clean_df[clean_df['NCAA_CONFERENCE'].str.match('Atlantic Coast')]

exdf5 = clean_df[clean_df['NCAA_CONFERENCE'].str.match('The Ivy League')]

power_5_conferences = pd.concat([exdf, exdf1, exdf2, exdf3, exdf4, exdf5])

power_5_conferences = power_5_conferences.rename(index=str, columns={"FOURYEAR_SCORE": "4 Year APR Score",
                                                   "NCAA_CONFERENCE": "NCAA Conference"})
  
sns.catplot(x="4 Year APR Score", y="NCAA Conference",height=3.5, 
            aspect=1.5, kind="box", legend=False, data=power_5_conferences)
plt.title("Power 5 Conferences and The Ivy League \n Four Year APR Scores\n")
plt.savefig("Graph_4.png")
