## Run notebook first to generate pickle files. ##

import tkinter as tk
import tkinter.ttk
from tkinter import *
import tkinter.messagebox

##### load files #####
import pickle
with open('Pickle/genres.pkl', 'rb') as file:
    genres = pickle.load(file)
    
with open('Pickle/genres_based_movies.pkl', 'rb') as file:
    genres_based = pickle.load(file)
    
with open('Pickle/similarity.pkl', 'rb') as file:
    similarity = pickle.load(file)

with open('Pickle/filtered_movies_title.pkl', 'rb') as file:
    temp = pickle.load(file)

import pandas as pd
filtered_movies_content = pd.DataFrame()
filtered_movies_content['title'] = temp    


#### Utility functions for Recommendation System ####

def genreBasedRecommendation(genre):
    if genre not in genres:
        return None
    else:
        return genres_based[genre]['title']


import difflib
'''
    input should only be title of a movie
    will output top n similar movies
'''
def contentBasedRecommendation(movie, n=10):
    res=""
    try:
        index = filtered_movies_content[filtered_movies_content['title'] == movie].index[0]
    except:
        res += "No exact match.. Chech these results: \n"
        closest_match = difflib.get_close_matches(movie, filtered_movies_content['title'], n=1, cutoff=0.5)
#         print("close ", closest_match)
        if not closest_match:
            return "No such movie."
        
        index = filtered_movies_content[filtered_movies_content['title'] == closest_match[0]].index[0]
    
    distances = sorted(list(enumerate(similarity[index])),reverse=True,key = lambda x: x[1])
    
    for i in distances[0:n]:
        res+=filtered_movies_content.iloc[i[0]].title
        res+="\n"
    return res

# contentBasedRecommendation is like recommending similar movies based on given content (title here).
# It's not search. So, it's expected that the user will provide a correct matching title.
# However, we have a fuzzy lexicographic search.
# TODO: Implement a SEARCH ENGINE in titles based on movie query.


##############################################################################################################

### GUI : Tkinter ###

# create root window
root = Tk()
# root window title and dimension4
root.title("Movie Mate")
# Set geometry (widthxheight)
root.geometry("1250x580")


def selected(event):
    string = clicked.get()
    label2.config(text=genreBasedRecommendation(string))

# Dropdown menu options
options = [
    'Action',
    'Adventure',
    'Animation',
    'Comedy',
    'Crime',
    'Documentary',
    'Drama',
    'Family',
    'Fantasy',
    'History',
    'Horror',
    'Music',
    'Mystery',
    'Romance',
    'Science Fiction',
    'TV Movie',
    'Thriller',
    'War',
    'Western'
]


# adding a label to the root window
l1 = Label(
    root, text="MOVIE RECOMMENDER SYSTEM", fg="blue")
l1.grid(row=0, column=17,columnspan=5)
#l1.config(font=('verdana'))
l2 = Label(root, text="Select genre of the movie you want to watch : ",fg="blue")
l2.grid(row=1, column=0, sticky=W, pady=2)


# datatype of menu text
clicked = StringVar()
# # initial menu text
clicked.set("Select Genre")

# # Create Dropdown menu
drop = OptionMenu(root, clicked, *options,command=selected)
drop.grid(row=3, column=0, sticky=W)

# # Initialize a Label to display the User Input
# label2 = Label(root, text="", font=("Courier 22 bold"))
# label2.grid(row=6, column=1)


def display_text():
    global entry
    string = entry.get()
    label2.config(text=contentBasedRecommendation(string))
    
# Initialize a Label to display the User Input
label2 = Label(root, text="", font=("Courier 22 bold"))
label2.grid(row=8, column=17)

# Create an Entry widget to accept User Input
entry = Entry(root, width=40)
entry.focus_set()
entry.grid(row=4, column=17)

# Create a Button to validate Entry Widget
btn = Button(root, text="Search", width=20,
             command=display_text).grid(row=5, column=17,columnspan=5)


root.mainloop()

# TODO: Better UI and display of results.