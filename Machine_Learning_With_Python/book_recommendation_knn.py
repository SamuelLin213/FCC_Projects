# -*- coding: utf-8 -*-
"""Copy of fcc_book_recommendation_knn.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1RMrKDvgmFb8ATNlnMWZc9QCSV_qyjoDZ
"""

# import libraries (you may add additional imports but you may not have to)
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
import matplotlib.pyplot as plt

# get data files
!wget https://cdn.freecodecamp.org/project-data/books/book-crossings.zip

!unzip book-crossings.zip

books_filename = 'BX-Books.csv'
ratings_filename = 'BX-Book-Ratings.csv'

# import csv data into dataframes
df_books = pd.read_csv(
    books_filename,
    encoding = "ISO-8859-1",
    sep=";",
    header=0,
    names=['isbn', 'title', 'author'],
    usecols=['isbn', 'title', 'author'],
    dtype={'isbn': 'str', 'title': 'str', 'author': 'str'})

print("df_books: ")
print(df_books)

df_ratings = pd.read_csv(
    ratings_filename,
    encoding = "ISO-8859-1",
    sep=";",
    header=0,
    names=['user', 'isbn', 'rating'],
    usecols=['user', 'isbn', 'rating'],
    dtype={'user': 'int32', 'isbn': 'str', 'rating': 'float32'})

print("df_ratings")
print(df_ratings)

# drop users with less than 200 ratings and books with less than 100 ratings
countUser = df_ratings['user'].value_counts()
countRating = df_ratings['isbn'].value_counts()

ratings = df_ratings[(df_ratings['user'].isin(countUser[countUser >= 200].index)) & (df_ratings['isbn'].isin(countRating[countRating >= 100].index)) ]

# Combine book rating with user rating
merged = pd.merge(df_books, ratings, on='isbn')

cols = ['author']

# contains: isbn, title, user, rating
merged = merged.drop(cols, axis=1)

print(merged.head())

merged = merged.dropna(axis = 0, subset = ['title']) # remove title column

merged = merged.drop_duplicates(['user', 'title'], keep='first') # drop duplicates in df, by user and title
merged_pivot = merged.pivot(
    index='isbn',
    columns='user',
    values='rating'
).fillna(0)
merged_matrix = csr_matrix(merged_pivot.values) # convert df into matrix

model_knn = NearestNeighbors(metric='cosine') 
model_knn.fit(merged_matrix) # fit the matrix onto knn

# function to return recommended books - this will be tested
def get_recommends(book = ""):
  # check if inputted book exists
  if ~((merged['title'] == book).any()):
    return
  
  result = merged.loc[merged["title"] == book] # rows w/ matching title
  query_index = merged_pivot.loc[merged_pivot.index.isin(result["isbn"])] # get index of matching title
  distances, indices = model_knn.kneighbors([x for x in query_index.values], n_neighbors=6)

  distances =  distances[0][1:]
  indices = indices[0][1:]

  # creates list of recommendations, for each index
  titles = [
      df_books.loc[df_books['isbn'] == merged_pivot.iloc[i].name]["title"].values[0]\
      for i in indices
  ]

  # reverse array
  recommended = [list(z) for z in zip(titles, distances)][::-1]
  return [book, recommended]

books = get_recommends("Where the Heart Is (Oprah's Book Club (Paperback))")
print(books)

def test_book_recommendation():
  test_pass = True
  recommends = get_recommends("Where the Heart Is (Oprah's Book Club (Paperback))")
  if recommends[0] != "Where the Heart Is (Oprah's Book Club (Paperback))":
    test_pass = False
  recommended_books = ["I'll Be Seeing You", 'The Weight of Water', 'The Surgeon', 'I Know This Much Is True']
  recommended_books_dist = [0.8, 0.77, 0.77, 0.77]
  for i in range(2): 
    if recommends[1][i][0] not in recommended_books:
      test_pass = False
    if abs(recommends[1][i][1] - recommended_books_dist[i]) >= 0.05:
      test_pass = False
  if test_pass:
    print("You passed the challenge! 🎉🎉🎉🎉🎉")
  else:
    print("You haven't passed yet. Keep trying!")

test_book_recommendation()