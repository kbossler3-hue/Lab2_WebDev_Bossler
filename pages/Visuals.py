# This creates the page for displaying data visualizations.

import streamlit as st
import json
import os
import matplotlib.pyplot as plt
import pandas as pd
import statistics

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Visuals",
    page_icon="📈",
)

# PAGE TITLE
st.title("Data Visualizations 📈")


# PART 1: GRAPHS FROM data.json
# --- YOUR CODE GOES HERE ---
path = os.path.join(os.path.dirname(__file__), "..", "data.json")
D = json.load(open(path))
chart_title = D["chart_title"]
per_game_data = D["data_points"]
num_games = len(per_game_data)

wins = 0
losses = 0
ties = 0
for i in range(len(per_game_data)):
    game = per_game_data[i]
    broncos_points = game["Points Scored"]
    opponent_points = game["Points Allowed"]
    if (broncos_points > opponent_points):
        wins += 1
    elif (broncos_points < opponent_points):
        losses += 1    
    else: 
        ties += 1
     
        

# Matplotlib Pie Chart
fig, ax = plt.subplots()
ax.pie([wins, losses], labels = ["Wins", "Losses"])
ax.set_title("2025 Wins vs Losses")
st.pyplot(fig)


if "slide_num" not in st.session_state:
    st.session_state.slide_num = 0     

left, right = st.columns(2)

previous_clicked = left.button("Previous")
next_clicked = right.button("Next")

if previous_clicked:
    if st.session_state.slide_num > 0:
        st.session_state.slide_num = (st.session_state.slide_num - 1)
if next_clicked:
    if st.session_state.slide_num < num_games - 1:
        st.session_state.slide_num = (st.session_state.slide_num + 1)
        
# print(st.session_state.slide_num)

game = per_game_data[st.session_state.slide_num]

data = {"Team" : ["Broncos", game["Opponent"]], "Points": [game["Points Scored"], game["Points Allowed"]]}

st.subheader("Head to Head Scores by week")
st.subheader("Week " + str(game["Game"]) + ": " + game["Opponent"])
st.bar_chart(data, x = "Team", y = "Points")

#extra credit
points_so_far = []
for i in range(st.session_state.slide_num + 1):
    points_so_far.append(per_game_data[i]["Points Scored"])

pts_mean = round(sum(points_so_far) / len(points_so_far), 2)
pts_median = statistics.median(points_so_far)

if "old_pts_mean" not in st.session_state:
    st.session_state.old_pts_mean = pts_mean
    st.session_state.old_pts_median = pts_median

col1, col2 = st.columns(2)
col1.metric("Mean Points (Season So Far)", pts_mean, round(pts_mean - st.session_state.old_pts_mean, 2))
col2.metric("Median Points (Season So Far)", pts_median, pts_median - st.session_state.old_pts_median)

st.session_state.old_pts_mean = pts_mean
st.session_state.old_pts_median = pts_median   

# PART 2: GRAPHS FROM data.csv
st.header("Fan Survey Results")

csv_path = os.path.join(os.path.dirname(__file__), "..", "data.csv")
survey = pd.read_csv(csv_path)

if len(survey) == 0:
    st.write("No survey responses yet!")
else:
    #static chart
    st.subheader("Favorite Games")
    game_counts = {}
    for i in range(len(survey)):
        opponent = survey["Category"][i]
        if opponent in game_counts:
            game_counts[opponent] += 1
        else:
            game_counts[opponent] = 1    
            
    data = {"Opponent": list(game_counts.keys()), "Votes": list(game_counts.values())}  
    st.bar_chart(data, x = "Opponent", y = "Votes")
    
        # Dynamic chart: favorite games among fans who rated the season at or above the slider
    st.subheader("Favorite Games by Season Rating")
    st.write("Each fan rated the 2025 season from 1-10.")

    if "min_rating" not in st.session_state:
        st.session_state.min_rating = 1

    st.session_state.min_rating = st.slider("Minimum season rating:", 1, 10, st.session_state.min_rating)

    filtered_counts = {}
    num_fans = 0
    filtered_ratings= []
    for i in range(len(survey)):
        opponent = survey["Category"][i]
        rating = survey["Value"][i]
        if rating >= st.session_state.min_rating:
            num_fans += 1
            filtered_ratings.append(rating)
            if opponent in filtered_counts:
                filtered_counts[opponent] += 1
            else:
                filtered_counts[opponent] = 1

    if len(filtered_counts) == 0:
        st.write("No fans rated the season that high yet!")
    else:
        st.write("Showing " + str(num_fans) + " of " + str(len(survey)) + " fans.")

        fig2, ax2 = plt.subplots()
        ax2.pie(list(filtered_counts.values()))
        ax2.legend(list(filtered_counts.keys()), title = "Opponent", loc = "center left", bbox_to_anchor = (1, 0.5))
        ax2.set_title("Favorite Games of Fans Who Rated the Season " + str(st.session_state.min_rating) + "/10 or Higher")
        st.pyplot(fig2) 
        #extra credit
        mean_rating = round(sum(filtered_ratings) /len(filtered_ratings), 2)
        median_rating = statistics.median(filtered_ratings)
        if "old_mean" not in st.session_state:
            st.session_state.old_mean = mean_rating
            st.session_state.old_median = median_rating
        mean_change = round(mean_rating - st.session_state.old_mean, 2)
        median_change = median_rating - st.session_state.old_median
        col1, col2 = st.columns(2)
        col1.metric("Mean Rating", mean_rating, mean_change)
        col2.metric("Median Rating", median_rating, median_change)
        st.session_state.old_mean = mean_rating
        st.session_state.old_median = median_rating                              
            