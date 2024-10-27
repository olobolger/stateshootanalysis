import mysql.connector
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from numpy.ma.extras import average

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Bobdole!",
    database="state_shoot_stats"
)
matplotlib.use('TkAgg')
figure = 1;
years = [2024, 2023, 2022, 2021]
friday_singles_events = [(2024, 6), (2023, 5), (2022, 5), (2021, 5)]
friday_handicap_events = [(2024, 7), (2023, 6), (2022, 6), (2021, 6)]
friday_doubles_events = [(2024, 5), (2023, 7), (2022, 7), (2021, 7)]
championship_singles_events = [(2024, 8), (2023, 8), (2022, 8), (2021, 8)]
championship_handicap_events = [(2024, 10), (2023, 10), (2022, 9), (2021, 9)]
championship_doubles_events = [(2024, 9), (2023, 9), (2022, 7), (2021, 7)]

unique_totals = []
unique_residents = []
unique_non_residents = []
non_residents_by_state_labels = []
non_residents_by_state_values = []
youth_event_totals = []
mycursor = mydb.cursor()
resident_color = "lime"
non_resident_color = "red"
total_color = "blue"
best_fit_color = "magenta"

for year in years:
    mycursor.execute("select count(name) as name_count from (select distinct name from entries where year=%s) as names",
                     (year, ))
    unique_totals.append(mycursor.fetchall()[0][0])
    mycursor.execute("select count(name) as name_count from (select distinct name from entries where year=%s and state='ND') as names",
                     (year,))
    unique_residents.append(mycursor.fetchall()[0][0])
    mycursor.execute(
        "select count(name) as name_count from (select distinct name from entries where year=%s and state!='ND') as names",
        (year,))

    unique_non_residents.append(mycursor.fetchall()[0][0])
    mycursor.execute(
        "select distinct state, count(state) from (select distinct name, state from entries where year = %s and state != 'ND') as unique_shooters group by state order by state",
        (year,))
    temp_data = mycursor.fetchall()
    temp_states = []
    temp_counts = []
    for row in temp_data:
        temp_states.append(row[0])
        temp_counts.append(row[1])
    non_residents_by_state_labels.append(temp_states)
    non_residents_by_state_values.append(temp_counts)
mycursor.execute("select distinct year, count(year) from (select name, year from entries where event_number=1) as shooters group by year order by year desc")
youth_event_temp = mycursor.fetchall()



for row in youth_event_temp:
    youth_event_totals.append(row[1])
thursday_singles = []
mycursor.execute("select distinct year, count(year) from (select name, year from entries where event_number=2) as shooters group by year order by year desc")
thursday_singles_temp = mycursor.fetchall()
for row in thursday_singles_temp:
    thursday_singles.append(row[1])

thursday_handicap = []
mycursor.execute("select distinct year, count(year) from (select name, year from entries where event_number=3) as shooters group by year order by year desc")
thursday_handicap_temp = mycursor.fetchall()
for row in thursday_handicap_temp:
    thursday_handicap.append(row[1])

thursday_doubles = []
mycursor.execute("select distinct year, count(year) from (select name, year from entries where event_number=4) as shooters group by year order by year desc")
thursday_doubles_temp = mycursor.fetchall()
for row in thursday_doubles_temp:
    thursday_doubles.append(row[1])

friday_singles = []
first = True
friday_singles_query = ""
for row in friday_singles_events:
    if first:
        first = False
        friday_singles_query = "(select distinct year, event_number, count(year) from (select name, year, event_number from entries where event_number={0} and year={1}) as shooters group by year order by year desc)".format(row[1], row[0])
    else:
        friday_singles_query += "union all (select distinct year, event_number, count(year) from (select name, year, event_number from entries where event_number={0} and year={1}) as shooters group by year order by year desc)".format(row[1], row[0])

mycursor.execute(friday_singles_query)
friday_singles_temp = mycursor.fetchall()
for row in friday_singles_temp:
    friday_singles.append(row[2])
    
friday_handicap = []
first = True
friday_handicap_query = ""
for row in friday_handicap_events:
    if first:
        first = False
        friday_handicap_query = "(select distinct year, event_number, count(year) from (select name, year, event_number from entries where event_number={0} and year={1}) as shooters group by year order by year desc)".format(row[1], row[0])
    else:
        friday_handicap_query += "union all (select distinct year, event_number, count(year) from (select name, year, event_number from entries where event_number={0} and year={1}) as shooters group by year order by year desc)".format(row[1], row[0])

mycursor.execute(friday_handicap_query)
friday_handicap_temp = mycursor.fetchall()
for row in friday_handicap_temp:
    friday_handicap.append(row[2])
    
friday_doubles = []
first = True
friday_doubles_query = ""
for row in friday_doubles_events:
    if first:
        first = False
        friday_doubles_query = "(select distinct year, event_number, count(year) from (select name, year, event_number from entries where event_number={0} and year={1}) as shooters group by year order by year desc)".format(row[1], row[0])
    else:
        friday_doubles_query += "union all (select distinct year, event_number, count(year) from (select name, year, event_number from entries where event_number={0} and year={1}) as shooters group by year order by year desc)".format(row[1], row[0])

mycursor.execute(friday_doubles_query)
friday_doubles_temp = mycursor.fetchall()
for row in friday_doubles_temp:
    friday_doubles.append(row[2])
    
championship_singles = []
first = True
championship_singles_query = ""
for row in championship_singles_events:
    if first:
        first = False
        championship_singles_query = "(select distinct year, event_number, count(year) from (select name, year, event_number from entries where event_number={0} and year={1}) as shooters group by year order by year desc)".format(row[1], row[0])
    else:
        championship_singles_query += "union all (select distinct year, event_number, count(year) from (select name, year, event_number from entries where event_number={0} and year={1}) as shooters group by year order by year desc)".format(row[1], row[0])

mycursor.execute(championship_singles_query)
championship_singles_temp = mycursor.fetchall()
for row in championship_singles_temp:
    championship_singles.append(row[2])

championship_handicap = []
first = True
championship_handicap_query = ""
for row in championship_handicap_events:
    if first:
        first = False
        championship_handicap_query = "(select distinct year, event_number, count(year) from (select name, year, event_number from entries where event_number={0} and year={1}) as shooters group by year order by year desc)".format(row[1], row[0])
    else:
        championship_handicap_query += "union all (select distinct year, event_number, count(year) from (select name, year, event_number from entries where event_number={0} and year={1}) as shooters group by year order by year desc)".format(row[1], row[0])

mycursor.execute(championship_handicap_query)
championship_handicap_temp = mycursor.fetchall()
for row in championship_handicap_temp:
    championship_handicap.append(row[2])

championship_doubles = []
first = True
championship_doubles_query = ""
for row in championship_doubles_events:
    if first:
        first = False
        championship_doubles_query = "(select distinct year, event_number, count(year) from (select name, year, event_number from entries where event_number={0} and year={1}) as shooters group by year order by year desc)".format(row[1], row[0])
    else:
        championship_doubles_query += "union all (select distinct year, event_number, count(year) from (select name, year, event_number from entries where event_number={0} and year={1}) as shooters group by year order by year desc)".format(row[1], row[0])

mycursor.execute(championship_doubles_query)
championship_doubles_temp = mycursor.fetchall()
for row in championship_doubles_temp:
    championship_doubles.append(row[2])

total_entries = []
mycursor.execute("select year, count(year) from entries group by year order by year desc")
total_entries_temp = mycursor.fetchall()
for row in total_entries_temp:
    total_entries.append(row[1])

total_unique_categories_years = []
total_unique_categories_labels = []
total_unique_categories_data =[]
mycursor.execute("select year, category, count(category) from (select distinct distinct name, year, category from entries order by name) as unique_shooters group by category, year order by year desc, category")
total_unique_temp = mycursor.fetchall()
for row in total_unique_temp:
    total_unique_categories_years.append(row[0])
    total_unique_categories_labels.append(row[1])
    total_unique_categories_data.append(row[2])
df_categories = pd.DataFrame({"Year": total_unique_categories_years, "Category": total_unique_categories_labels, "Counts": total_unique_categories_data})
df_categories_pivot= df_categories.pivot(index="Year", columns="Category", values="Counts")

total_unique_aggregate_categories_years = []
total_unique_aggregate_categories_labels = []
total_unique_aggregate_categories_data =[]
mycursor.execute("select year, aggregate_category, count(aggregate_category) from (select distinct distinct name, year, case when category = \"SJ\" or category=\"JR\" or category=\"JRG\" then \"Youth Category\" when category = \"LD1\" or category=\"LD1\" then \"Lady Category\" when category = \"SBVT\" or category=\"VT\" or category=\"SRVT\" then \"Veteran Category\"  else \"Open\" end as aggregate_category from entries order by name) as unique_shooters group by aggregate_category, year order by year desc, aggregate_category")
total_unique_aggregate_temp = mycursor.fetchall()
for row in total_unique_aggregate_temp:
    total_unique_aggregate_categories_years.append(row[0])
    total_unique_aggregate_categories_labels.append(row[1])
    total_unique_aggregate_categories_data.append(row[2])
df_categories_aggregate = pd.DataFrame({"Year": total_unique_aggregate_categories_years, "Category": total_unique_aggregate_categories_labels, "Counts": total_unique_aggregate_categories_data})
df_categories_aggregate_pivot= df_categories_aggregate.pivot(index="Year", columns="Category", values="Counts")



championship_singles_unique_category = []
championship_singles_unique_categories_years = []
championship_singles_unique_categories_labels = []
championship_singles_unique_categories_data =[]
first = True
championship_singles_unique_category_query = ""
for row in championship_singles_events:
    if first:
        first = False
        #(select year, category, count(category) from (select year, category from entries where year={1} and event_number={0}) as unique_shooters group by category order by category)
        championship_singles_unique_category_query = "(select year, category, count(category) from (select year, category from entries where year={1} and event_number={0}) as unique_shooters group by category order by category)".format(row[1], row[0])
    else:
        championship_singles_unique_category_query += " union all (select year, category, count(category) from (select year, category from entries where year={1} and event_number={0}) as unique_shooters group by category order by category)".format(row[1], row[0])
mycursor.execute(championship_singles_unique_category_query)
championship_singles_unique_category_temp = mycursor.fetchall()
for row in championship_singles_unique_category_temp:
    championship_singles_unique_categories_years.append(row[0])
    championship_singles_unique_categories_labels.append(row[1])
    championship_singles_unique_categories_data.append(row[2])
df_championship_singles_categories = pd.DataFrame({"Year": championship_singles_unique_categories_years, "Category": championship_singles_unique_categories_labels, "Counts": championship_singles_unique_categories_data})
df_championship_singles_categories_pivot= df_championship_singles_categories.pivot(index="Year", columns="Category", values="Counts")

championship_singles_aggregate_category = []
championship_singles_aggregate_categories_years = []
championship_singles_aggregate_categories_labels = []
championship_singles_aggregate_categories_data =[]
first = True
championship_singles_aggregate_category_query = ""
for row in championship_singles_events:
    if first:
        first = False
        championship_singles_aggregate_category_query = "(select year, aggregate_category, count(aggregate_category) from (select year, case when category = \"SJ\" or category=\"JR\" or category=\"JRG\" then \"Youth Category\" when category = \"LD1\" or category=\"LD1\" then \"Lady Category\" when category = \"SBVT\" or category=\"VT\" or category=\"SRVT\" then \"Veteran Category\"  else \"Open\" end as aggregate_category from entries where year={1} and event_number={0}) as unique_shooters group by aggregate_category order by aggregate_category)".format(row[1], row[0])
    else:
        championship_singles_aggregate_category_query += " union all (select year, aggregate_category, count(aggregate_category) from (select year, case when category = \"SJ\" or category=\"JR\" or category=\"JRG\" then \"Youth Category\" when category = \"LD1\" or category=\"LD1\" then \"Lady Category\" when category = \"SBVT\" or category=\"VT\" or category=\"SRVT\" then \"Veteran Category\"  else \"Open\" end as aggregate_category from entries where year={1} and event_number={0}) as unique_shooters group by aggregate_category order by aggregate_category)".format(row[1], row[0])
mycursor.execute(championship_singles_aggregate_category_query)
championship_singles_aggregate_category_temp = mycursor.fetchall()
for row in championship_singles_aggregate_category_temp:
    championship_singles_aggregate_categories_years.append(row[0])
    championship_singles_aggregate_categories_labels.append(row[1])
    championship_singles_aggregate_categories_data.append(row[2])
df_championship_singles_aggregate_categories = pd.DataFrame({"Year": championship_singles_aggregate_categories_years, "Category": championship_singles_aggregate_categories_labels, "Counts": championship_singles_aggregate_categories_data})
df_championship_singles_aggregate_categories_pivot= df_championship_singles_aggregate_categories.pivot(index="Year", columns="Category", values="Counts")

championship_handicap_unique_category = []
championship_handicap_unique_categories_years = []
championship_handicap_unique_categories_labels = []
championship_handicap_unique_categories_data =[]
first = True
aggregated_championship_handicap_unique_category_query = ""
for row in championship_handicap_events:
    if first:
        first = False
        aggregated_championship_handicap_unique_category_query = "(select year, category, count(category) from (select year, category from entries where year={1} and event_number={0}) as unique_shooters group by category order by category)".format(row[1], row[0])
    else:
        aggregated_championship_handicap_unique_category_query += " union all (select year, category, count(category) from (select year, category from entries where year={1} and event_number={0}) as unique_shooters group by category order by category)".format(row[1], row[0])
mycursor.execute(aggregated_championship_handicap_unique_category_query)
aggregated_championship_handicap_unique_category_temp = mycursor.fetchall()
for row in aggregated_championship_handicap_unique_category_temp:
    championship_handicap_unique_categories_years.append(row[0])
    championship_handicap_unique_categories_labels.append(row[1])
    championship_handicap_unique_categories_data.append(row[2])
df_championship_handicap_categories = pd.DataFrame({"Year": championship_handicap_unique_categories_years, "Category": championship_handicap_unique_categories_labels, "Counts": championship_handicap_unique_categories_data})
df_championship_handicap_categories_pivot= df_championship_handicap_categories.pivot(index="Year", columns="Category", values="Counts")

championship_handicap_aggregate_category = []
championship_handicap_aggregate_categories_years = []
championship_handicap_aggregate_categories_labels = []
championship_handicap_aggregate_categories_data =[]
first = True
championship_handicap_aggregate_category_query = ""
for row in championship_handicap_events:
    if first:
        first = False
        championship_handicap_aggregate_category_query = "(select year, aggregate_category, count(aggregate_category) from (select year, case when category = \"SJ\" or category=\"JR\" or category=\"JRG\" then \"Youth Category\" when category = \"LD1\" or category=\"LD1\" then \"Lady Category\" when category = \"SBVT\" or category=\"VT\" or category=\"SRVT\" then \"Veteran Category\"  else \"Open\" end as aggregate_category from entries where year={1} and event_number={0}) as unique_shooters group by aggregate_category order by aggregate_category)".format(row[1], row[0])
    else:
        championship_handicap_aggregate_category_query += " union all (select year, aggregate_category, count(aggregate_category) from (select year, case when category = \"SJ\" or category=\"JR\" or category=\"JRG\" then \"Youth Category\" when category = \"LD1\" or category=\"LD1\" then \"Lady Category\" when category = \"SBVT\" or category=\"VT\" or category=\"SRVT\" then \"Veteran Category\"  else \"Open\" end as aggregate_category from entries where year={1} and event_number={0}) as unique_shooters group by aggregate_category order by aggregate_category)".format(row[1], row[0])
mycursor.execute(championship_handicap_aggregate_category_query)
championship_handicap_aggregate_category_temp = mycursor.fetchall()
for row in championship_handicap_aggregate_category_temp:
    championship_handicap_aggregate_categories_years.append(row[0])
    championship_handicap_aggregate_categories_labels.append(row[1])
    championship_handicap_aggregate_categories_data.append(row[2])
df_championship_handicap_aggregate_categories = pd.DataFrame({"Year": championship_handicap_aggregate_categories_years, "Category": championship_handicap_aggregate_categories_labels, "Counts": championship_handicap_aggregate_categories_data})
df_championship_handicap_aggregate_categories_pivot= df_championship_handicap_aggregate_categories.pivot(index="Year", columns="Category", values="Counts")



championship_doubles_unique_category = []
championship_doubles_unique_categories_years = []
championship_doubles_unique_categories_labels = []
championship_doubles_unique_categories_data =[]
first = True
aggregated_championship_doubles_unique_category_query = ""
for row in championship_doubles_events:
    if first:
        first = False
        aggregated_championship_doubles_unique_category_query = "(select year, category, count(category) from (select year, category from entries where year={1} and event_number={0}) as unique_shooters group by category order by category)".format(row[1], row[0])
    else:
        aggregated_championship_doubles_unique_category_query += " union all (select year, category, count(category) from (select year, category from entries where year={1} and event_number={0}) as unique_shooters group by category order by category)".format(row[1], row[0])
mycursor.execute(aggregated_championship_doubles_unique_category_query)
aggregated_championship_doubles_unique_category_temp = mycursor.fetchall()
for row in aggregated_championship_doubles_unique_category_temp:
    championship_doubles_unique_categories_years.append(row[0])
    championship_doubles_unique_categories_labels.append(row[1])
    championship_doubles_unique_categories_data.append(row[2])
df_championship_doubles_categories = pd.DataFrame({"Year": championship_doubles_unique_categories_years, "Category": championship_doubles_unique_categories_labels, "Counts": championship_doubles_unique_categories_data})
df_championship_doubles_categories_pivot= df_championship_doubles_categories.pivot(index="Year", columns="Category", values="Counts")

championship_doubles_aggregate_category = []
championship_doubles_aggregate_categories_years = []
championship_doubles_aggregate_categories_labels = []
championship_doubles_aggregate_categories_data =[]
first = True
championship_doubles_aggregate_category_query = ""
for row in championship_doubles_events:
    if first:
        first = False
        championship_doubles_aggregate_category_query = "(select year, aggregate_category, count(aggregate_category) from (select year, case when category = \"SJ\" or category=\"JR\" or category=\"JRG\" then \"Youth Category\" when category = \"LD1\" or category=\"LD1\" then \"Lady Category\" when category = \"SBVT\" or category=\"VT\" or category=\"SRVT\" then \"Veteran Category\"  else \"Open\" end as aggregate_category from entries where year={1} and event_number={0}) as unique_shooters group by aggregate_category order by aggregate_category)".format(row[1], row[0])
    else:
        championship_doubles_aggregate_category_query += " union all (select year, aggregate_category, count(aggregate_category) from (select year, case when category = \"SJ\" or category=\"JR\" or category=\"JRG\" then \"Youth Category\" when category = \"LD1\" or category=\"LD1\" then \"Lady Category\" when category = \"SBVT\" or category=\"VT\" or category=\"SRVT\" then \"Veteran Category\"  else \"Open\" end as aggregate_category from entries where year={1} and event_number={0}) as unique_shooters group by aggregate_category order by aggregate_category)".format(row[1], row[0])
mycursor.execute(championship_doubles_aggregate_category_query)
championship_doubles_aggregate_category_temp = mycursor.fetchall()
for row in championship_doubles_aggregate_category_temp:
    championship_doubles_aggregate_categories_years.append(row[0])
    championship_doubles_aggregate_categories_labels.append(row[1])
    championship_doubles_aggregate_categories_data.append(row[2])
df_championship_doubles_aggregate_categories = pd.DataFrame({"Year": championship_doubles_aggregate_categories_years, "Category": championship_doubles_aggregate_categories_labels, "Counts": championship_doubles_aggregate_categories_data})
df_championship_doubles_aggregate_categories_pivot= df_championship_doubles_aggregate_categories.pivot(index="Year", columns="Category", values="Counts")


plt.figure()
#Figure 1: plot without best fit lines
plt.plot(years, unique_totals, label="Total Shooters", marker='o', color=total_color)
plt.plot(years, unique_residents, label="Residents", marker='o', color=resident_color)
plt.plot(years, unique_non_residents, label="Non-Residents", marker='o', color=non_resident_color)
plt.xlabel("Year")
plt.ylabel("# Shooters")
plt.xticks(years)
plt.title("Figure {}: Total Unique Shooters by Residency".format(figure))
plt.legend()
plt.savefig("figure{}.png".format(figure))
figure +=1 
plt.close()

#figure 2: best fit lines added to Figure 1.
plt.figure()
plt.plot(years, unique_totals, label="Total Shooters", marker='o', color=total_color)
m_t, b_t = np.polyfit(years, unique_totals, 1)
x = np.array(years)
y_t = m_t * x + b_t
plt.plot(x, y_t, color=best_fit_color)
plt.text(average(years), min(unique_totals)-10, "y = {0:,.{2}f}x + {1:,.{2}f}".format(m_t,b_t, 1))
plt.plot(years, unique_residents, label="Residents", marker='o', color=resident_color)
m_r, b_r = np.polyfit(years, unique_residents, 1)
y_r = m_r * x + b_r
plt.plot(x, y_r, color=best_fit_color)
plt.text(average(years), min(unique_residents)-10, "y = {0:,.{2}f}x + {1:,.{2}f}".format(m_r,b_r, 1))
plt.plot(years, unique_non_residents, label="Non-Residents", marker='o', color=non_resident_color)
m_n, b_n = np.polyfit(years, unique_non_residents, 1)
y_n = m_n * x + b_n
plt.plot(x, y_n, color=best_fit_color)
plt.text(average(years), min(unique_non_residents)-10, "y = {0:,.{2}f}x + {1:,.{2}f}".format(m_n,b_n, 1))
plt.xlabel("Year")
plt.ylabel("# Shooters")
plt.xticks(years)
plt.title("Figure {}: Total Unique Shooters by Residency With Best Fit Lines".format(figure))
plt.legend()
plt.savefig("figure{}.png".format(figure))
figure +=1 
plt.close()

#Figure 3: pie charts with residents vs. non-residents
for i in range(0, len(years)):
    plt.figure()
    labels = ["Residents", "Non-Residents"]
    colors = [resident_color, non_resident_color]
    data = [unique_residents[i], unique_non_residents[i]]
    plt.pie(data, labels=labels, colors=colors, autopct="%1.1f%%")
    plt.title("Figure {}: {} Unique Attendance by Residency".format(figure, years[i]))
    plt.savefig("figure{}.png".format(figure))
    figure +=1 
plt.close()

#Figure 4: pie charts with non-residents by State
for i in range(0, len(years)):
    plt.figure()
    plt.pie(np.array(non_residents_by_state_values[i]), labels=np.array(non_residents_by_state_labels[i]), autopct="%1.1f%%")
    plt.title("Figure {}: {} Unique Non-Resident Attendance by State".format(figure, years[i]))
    plt.savefig("figure{}.png".format(figure))
    figure +=1 
plt.close()

#Figure 5: Youth Event plot without best fit lines
plt.figure()
plt.plot(years, youth_event_totals, label="Total Shooters", marker='o', color=total_color)
plt.xlabel("Year")
plt.ylabel("# Shooters")
plt.xticks(years)
plt.title("Figure {}: Total Youth Event Shooters".format(figure))
plt.legend()
plt.savefig("figure{}.png".format(figure))
figure +=1 
plt.close()

#Figure 6: Youth Event plot with best fit lines
plt.figure()
plt.plot(years, youth_event_totals, label="Total Shooters", marker='o', color=total_color)
m_youth, b_youth = np.polyfit(years, youth_event_totals, 1)
y_youth = m_youth * x + b_youth
plt.plot(x, y_youth, color=best_fit_color)
plt.text(average(years), min(youth_event_totals), "y = {0:,.{2}f}x + {1:,.{2}f}".format(m_youth,b_youth, 1))
plt.xlabel("Year")
plt.ylabel("# Shooters")
plt.xticks(years)
plt.title("Figure {}: Total Youth Event Shooters With Best Fit Line".format(figure))
plt.legend()
plt.savefig("figure{}.png".format(figure))
figure +=1 
plt.close()

#Figure 7: Thursday Singles plot without best fit lines
plt.figure()
plt.plot(years, thursday_singles, label="Total Shooters", marker='o', color=total_color)
plt.xlabel("Year")
plt.ylabel("# Shooters")
plt.xticks(years)
plt.title("Figure {}: Total Thursday Singles Shooters".format(figure))
plt.legend()
plt.savefig("figure{}.png".format(figure))
figure +=1 
plt.close()

#Figure 8: Thursday Singles plot with best fit lines
plt.figure()
plt.plot(years, thursday_singles, label="Total Shooters", marker='o', color=total_color)
m_ts, b_ts = np.polyfit(years, thursday_singles, 1)
y_ts = m_ts * x + b_ts
plt.plot(x, y_ts, color=best_fit_color)
plt.text(average(years), min(thursday_singles), "y = {0:,.{2}f}x + {1:,.{2}f}".format(m_ts,b_ts, 1))
plt.xlabel("Year")
plt.ylabel("# Shooters")
plt.xticks(years)
plt.title("Figure {}: Total Thursday Singles Shooters With Best Fit Line".format(figure))
plt.legend()
plt.savefig("figure{}.png".format(figure))
figure +=1 
plt.close()

#Figure 9: Thursday Handicap plot without best fit lines
plt.figure()
plt.plot(years, thursday_handicap, label="Total Shooters", marker='o', color=total_color)
plt.xlabel("Year")
plt.ylabel("# Shooters")
plt.xticks(years)
plt.title("Figure {}: Total Thursday Handicap Shooters".format(figure))
plt.legend()
plt.savefig("figure{}.png".format(figure))
figure +=1 
plt.close()

#Figure 10: Thursday handicap plot with best fit lines
plt.figure()
plt.plot(years, thursday_handicap, label="Total Shooters", marker='o', color=total_color)
m_th, b_th = np.polyfit(years, thursday_handicap, 1)
y_th = m_th * x + b_th
plt.plot(x, y_th, color=best_fit_color)
plt.text(average(years), min(thursday_handicap), "y = {0:,.{2}f}x + {1:,.{2}f}".format(m_th,b_th, 1))
plt.xlabel("Year")
plt.ylabel("# Shooters")
plt.xticks(years)
plt.title("Figure {}: Total Thursday Handicap Shooters With Best Fit Line".format(figure))
plt.legend()
plt.savefig("figure{}.png".format(figure))
figure +=1 
plt.close()

#Figure 11: Thursday Doubles plot without best fit lines
plt.figure()
plt.plot(years, thursday_doubles, label="Total Shooters", marker='o', color=total_color)
plt.xlabel("Year")
plt.ylabel("# Shooters")
plt.xticks(years)
plt.title("Figure {}: Total Thursday Doubles Shooters".format(figure))
plt.legend()
plt.savefig("figure{}.png".format(figure))
figure +=1 
plt.close()

#Figure 12: Thursday doubles plot with best fit lines
plt.figure()
plt.plot(years, thursday_doubles, label="Total Shooters", marker='o', color=total_color)
m_th, b_th = np.polyfit(years, thursday_doubles, 1)
y_th = m_th * x + b_th
plt.plot(x, y_th, color=best_fit_color)
plt.text(average(years), min(thursday_doubles), "y = {0:,.{2}f}x + {1:,.{2}f}".format(m_th,b_th, 1))
plt.xlabel("Year")
plt.ylabel("# Shooters")
plt.xticks(years)
plt.title("Figure {}: Total Thursday Doubles Shooters With Best Fit Line".format(figure))
plt.legend()
plt.savefig("figure{}.png".format(figure))
figure +=1 
plt.close()

#Figure 13: Friday Singles plot without best fit lines
plt.figure()
plt.plot(years, friday_singles, label="Total Shooters", marker='o', color=total_color)
plt.xlabel("Year")
plt.ylabel("# Shooters")
plt.xticks(years)
plt.title("Figure {}: Total Friday Singles Shooters".format(figure))
plt.legend()
plt.savefig("figure{}.png".format(figure))
figure +=1 
plt.close()

#Figure 14: Friday singles plot with best fit lines
plt.figure()
plt.plot(years, friday_singles, label="Total Shooters", marker='o', color=total_color)
m, b = np.polyfit(years, friday_singles, 1)
y = m * x + b
plt.plot(x, y, color=best_fit_color)
plt.text(average(years), min(friday_singles), "y = {0:,.{2}f}x + {1:,.{2}f}".format(m,b, 1))
plt.xlabel("Year")
plt.ylabel("# Shooters")
plt.xticks(years)
plt.title("Figure {}: Total Friday Singles Shooters With Best Fit Line".format(figure))
plt.legend()
plt.savefig("figure{}.png".format(figure))
figure +=1 
plt.close()

#Figure 15: Friday handicap plot without best fit lines
plt.figure()
plt.plot(years, friday_handicap, label="Total Shooters", marker='o', color=total_color)
plt.xlabel("Year")
plt.ylabel("# Shooters")
plt.xticks(years)
plt.title("Figure {}: Total Friday Handicap Shooters".format(figure))
plt.legend()
plt.savefig("figure{}.png".format(figure))
figure +=1 
plt.close()

#Figure 16: Friday handicap plot with best fit lines
plt.figure()
plt.plot(years, friday_handicap, label="Total Shooters", marker='o', color=total_color)
m, b = np.polyfit(years, friday_handicap, 1)
y = m * x + b
plt.plot(x, y, color=best_fit_color)
plt.text(average(years), min(friday_handicap), "y = {0:,.{2}f}x + {1:,.{2}f}".format(m,b, 1))
plt.xlabel("Year")
plt.ylabel("# Shooters")
plt.xticks(years)
plt.title("Figure {}: Total Friday Handicap Shooters With Best Fit Line".format(figure))
plt.legend()
plt.savefig("figure{}.png".format(figure))
figure +=1 
plt.close()

#Figure 17: Friday doubles plot without best fit lines
plt.figure()
plt.plot(years, friday_doubles, label="Total Shooters", marker='o', color=total_color)
plt.xlabel("Year")
plt.ylabel("# Shooters")
plt.xticks(years)
plt.title("Figure {}: Total Friday Doubles Shooters".format(figure))
plt.legend()
plt.savefig("figure{}.png".format(figure))
figure +=1 
plt.close()

#Figure 18: Friday doubles plot with best fit lines
plt.figure()
plt.plot(years, friday_doubles, label="Total Shooters", marker='o', color=total_color)
m, b = np.polyfit(years, friday_doubles, 1)
y = m * x + b
plt.plot(x, y, color=best_fit_color)
plt.text(average(years), min(friday_doubles), "y = {0:,.{2}f}x + {1:,.{2}f}".format(m,b, 1))
plt.xlabel("Year")
plt.ylabel("# Shooters")
plt.xticks(years)
plt.title("Figure {}: Total Friday Doubles Shooters With Best Fit Line".format(figure))
plt.legend()
plt.savefig("figure{}.png".format(figure))
figure +=1 
plt.close()

#Figure 19: Championship singles plot without best fit lines
plt.figure()
plt.plot(years, championship_singles, label="Total Shooters", marker='o', color=total_color)
plt.xlabel("Year")
plt.ylabel("# Shooters")
plt.xticks(years)
plt.title("Figure {}: Total Championship Singles Shooters".format(figure))
plt.legend()
plt.savefig("figure{}.png".format(figure))
figure +=1 
plt.close()

#Figure 20: Championship singles plot with best fit lines
plt.figure()
plt.plot(years, championship_singles, label="Total Shooters", marker='o', color=total_color)
m, b = np.polyfit(years, championship_singles, 1)
y = m * x + b
plt.plot(x, y, color=best_fit_color)
plt.text(average(years), min(championship_singles), "y = {0:,.{2}f}x + {1:,.{2}f}".format(m,b, 1))
plt.xlabel("Year")
plt.ylabel("# Shooters")
plt.xticks(years)
plt.title("Figure {}: Total category_championship Singles Shooters With Best Fit Line".format(figure))
plt.legend()
plt.savefig("figure{}.png".format(figure))
figure +=1 
plt.close()

#Figure 21: category_championship handicap plot without best fit lines
plt.figure()
plt.plot(years, championship_handicap, label="Total Shooters", marker='o', color=total_color)
plt.xlabel("Year")
plt.ylabel("# Shooters")
plt.xticks(years)
plt.title("Figure {}: Total category_championship Handicap Shooters".format(figure))
plt.legend()
plt.savefig("figure{}.png".format(figure))
figure +=1 
plt.close()

#Figure 22: Championship handicap plot with best fit lines
plt.figure()
plt.plot(years, championship_handicap, label="Total Shooters", marker='o', color=total_color)
m, b = np.polyfit(years, championship_handicap, 1)
y = m * x + b
plt.plot(x, y, color=best_fit_color)
plt.text(average(years), min(championship_handicap), "y = {0:,.{2}f}x + {1:,.{2}f}".format(m,b, 1))
plt.xlabel("Year")
plt.ylabel("# Shooters")
plt.xticks(years)
plt.title("Figure {}: Total Championship Handicap Shooters With Best Fit Line".format(figure))
plt.legend()
plt.savefig("figure{}.png".format(figure))
figure +=1 
plt.close()

#Figure 23: Championship doubles plot without best fit lines
plt.figure()
plt.plot(years, championship_doubles, label="Total Shooters", marker='o', color=total_color)
plt.xlabel("Year")
plt.ylabel("# Shooters")
plt.xticks(years)
plt.title("Figure {}: Total Championship Doubles Shooters".format(figure))
plt.legend()
plt.savefig("figure{}.png".format(figure))
figure +=1 
plt.close()

#Figure 24: category_championship doubles plot with best fit lines
plt.figure()
plt.plot(years, championship_doubles, label="Total Shooters", marker='o', color=total_color)
m, b = np.polyfit(years, championship_doubles, 1)
y = m * x + b
plt.plot(x, y, color=best_fit_color)
plt.text(average(years), min(championship_doubles), "y = {0:,.{2}f}x + {1:,.{2}f}".format(m,b, 1))
plt.xlabel("Year")
plt.ylabel("# Shooters")
plt.xticks(years)
plt.title("Figure {}: Total Championship Doubles Shooters With Best Fit Line".format(figure))
plt.legend()
plt.savefig("figure{}.png".format(figure))
figure +=1 
plt.close()

#Figure 25: Total Entries plot without best fit lines
plt.figure()
plt.plot(years, total_entries, label="Total Shooters", marker='o', color=total_color)
plt.xlabel("Year")
plt.ylabel("# Shooters")
plt.xticks(years)
plt.title("Figure {}: Total Event Entries".format(figure))
plt.legend()
plt.savefig("figure{}.png".format(figure))
figure +=1
plt.close()

#Figure 26: Total Entries plot with best fit lines
plt.figure()
plt.plot(years, total_entries, label="Total Shooters", marker='o', color=total_color)
m, b = np.polyfit(years, total_entries, 1)
y = m * x + b
plt.plot(x, y, color=best_fit_color)
plt.text(average(years), min(total_entries), "y = {0:,.{2}f}x + {1:,.{2}f}".format(m,b, 1))
plt.xlabel("Year")
plt.ylabel("# Shooters")
plt.xticks(years)
plt.title("Figure {}: Total Entries With Best Fit Line".format(figure))
plt.legend()
plt.savefig("figure{}.png".format(figure))
figure +=1
plt.close()

#Figure 27: Total Categories plot with best fit lines
plt.figure()
df_categories_pivot.plot()
plt.xlabel("Year")
plt.ylabel("# Shooters")
plt.xticks(years)
plt.title("Figure {}: Total Unique Category Shooters By Year".format(figure))
plt.legend()
plt.savefig("figure{}.png".format(figure))
figure +=1
plt.close()

#Figure 28: Aggregated Categories plot with best fit lines
plt.figure()
df_categories_aggregate_pivot.plot()
plt.xlabel("Year")
plt.ylabel("# Shooters")
plt.xticks(years)
plt.title("Figure {}: Total Unique Aggregated Category Shooters By Year".format(figure))
plt.legend()
plt.savefig("figure{}.png".format(figure))
figure +=1
plt.close()

#Figure 29: Championship Singles Categories plot
plt.figure()
df_championship_singles_categories_pivot.plot()
plt.xlabel("Year")
plt.ylabel("# Shooters")
plt.xticks(years)
plt.title("Figure {}: Championship Singles Category Shooters By Year".format(figure))
plt.legend()
plt.savefig("figure{}.png".format(figure))
figure +=1
plt.close()

#Figure 29.1: Championship Singles Aggregated Categories plot
plt.figure()
df_championship_singles_aggregate_categories_pivot.plot()
plt.xlabel("Year")
plt.ylabel("# Shooters")
plt.xticks(years)
plt.title("Figure {}: Championship Singles Aggregated Category Shooters By Year".format(figure))
plt.legend()
plt.savefig("figure{}.png".format(figure))
figure +=1
plt.close()

#Figure 30: Championship Handicap Categories plot
plt.figure()
df_championship_handicap_categories_pivot.plot()
plt.xlabel("Year")
plt.ylabel("# Shooters")
plt.xticks(years)
plt.title("Figure {}: Championship Handicap Category Shooters By Year".format(figure))
plt.legend()
plt.savefig("figure{}.png".format(figure))
figure +=1
plt.close()

#Figure 30.1: Championship handicap Aggregated Categories plot
plt.figure()
df_championship_handicap_aggregate_categories_pivot.plot()
plt.xlabel("Year")
plt.ylabel("# Shooters")
plt.xticks(years)
plt.title("Figure {}: Championship Handicap Aggregated Category Shooters By Year".format(figure))
plt.legend()
plt.savefig("figure{}.png".format(figure))
figure +=1
plt.close()

#Figure 31: Championship Doubles Categories plot
plt.figure()
df_championship_doubles_categories_pivot.plot()
plt.xlabel("Year")
plt.ylabel("# Shooters")
plt.xticks(years)
plt.title("Figure {}: Championship Doubles Category Shooters By Year".format(figure))
plt.legend()
plt.savefig("figure{}.png".format(figure))
figure +=1
plt.close()

#Figure 31.1: Championship doubles Aggregated Categories plot
plt.figure()
df_championship_doubles_aggregate_categories_pivot.plot()
plt.xlabel("Year")
plt.ylabel("# Shooters")
plt.xticks(years)
plt.title("Figure {}: Championship Doubles Aggregated Category Shooters By Year".format(figure))
plt.legend()
plt.savefig("figure{}.png".format(figure))
figure +=1
plt.close()