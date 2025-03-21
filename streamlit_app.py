import streamlit as st
from google.cloud import firestore

db = firestore.Client.from_service_account_json("firestore-key.json")

# Streamlit widgets to let a user create a new post
title = st.text_input("Post title")
url = st.text_input("Post url")
description=st.text_input("Post the description")
submit = st.button("Submit new post")


# Once the user has submitted, upload it to the database
if title and url and description and submit:
	doc_ref = db.collection("posts").document(title)
	doc_ref.set({
		"title": title,
		"url": url,
		"description":description
	})


# And then render each post, using some light Markdown
posts_ref = db.collection("posts")
for doc in posts_ref.stream():
	post = doc.to_dict()
	title = post["title"]
	url = post["url"]
	description=post["description"]

	st.subheader(f"Post: {title}")
	st.write(f":link: [{url}]({url})")
	st.write(f"Description: {description}")