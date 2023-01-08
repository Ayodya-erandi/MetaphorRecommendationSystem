import requests, os, time, csv
from bs4 import BeautifulSoup
import mtranslate
from googletrans import Translator
import json,re
import pandas as pd


def translate_to_sinhala(value):
	translator = Translator()
	#sinhala_val = mtranslate.translate(value, 'si', 'en')
	sinhala_val = translator.translate(value, dest='si')
	return sinhala_val.text

def parse_lyrics(lyrics):
	space_set = set([' '])
	processed = ''
	regex = r"([A-z])+|[0-9]|\||-|∆|([.!?\\\/\(\)\+#&])+"
	lyric_lines = lyrics.split('\n')
	for line in lyric_lines:
		new = re.sub(regex, '', line)
		chars = set(new)
		if not ((chars == space_set) or (len(chars) is 0)):
			processed += new + '\n'
	return processed


def key_val_split(key_val):
	key_val_list = key_val.split(":")
	if len(key_val_list) >= 2 :
		key = key_val_list[0]
		vals = key_val_list[1]
		if vals[0] == " ":
			vals = vals[1:]
		if "," in vals :
			vals = vals.split(",")
		return key, vals

def get_song_info(song_page,song_id):
	soup = BeautifulSoup(song_page, 'html.parser')

	song = soup.find('h1', {'class': 'entry-title'})
	singer = soup.find('span', {'class': 'entry-categories'})
	genre = soup.find('span', {'class': 'entry-tags'})
	lyricist = soup.find('span', {'class': 'lyrics'})
	metaphors = getMetaphors(song_id)
	composer = soup.find('span', {'class': 'music'})
	movie = soup.find('span', {'class': 'movies'})
	lyrics = parse_lyrics(soup.find_all('pre')[0].get_text())
	song_meta_data = {}
	song_meta_data['Song_id'] = song_id
	if song : 
		song_meta_data['title'] = song.get_text()

	song_list = [singer, genre, lyricist, composer, movie]
	key_mappings = {"Artist": "Singer", "Genre": "Genre", "Lyrics":"Lyricist", "Music": "Composer", "Movie":"Movie"}
	for key_val in song_list:
		if key_val :
			if isinstance(key_val, str):
				key_vals = key_val_split(key_val)
			else :
				key_vals = key_val_split(key_val.get_text())
			if key_vals :
				key = key_mappings[key_vals[0]]
				vals = key_vals[1]
				song_meta_data[key] = vals
	
	if lyrics :
		song_meta_data['song_lyrics'] = lyrics

	song_meta_data['Metaphors'] = metaphors

	return song_meta_data


def translate_values(dict_meta_data):
	sinhala_meta_data = {}
	for key in dict_meta_data:
		if isinstance(dict_meta_data[key], int) or key == "song_lyrics" or key == "title" or key=="Song_id" or key=="Metaphors":
			sinhala_meta_data[key] = dict_meta_data[key]
		elif type(dict_meta_data[key]) == list :
			value_list = []
			for i in dict_meta_data[key]:
				value_list.append(translate_to_sinhala(i))
			sinhala_meta_data['{}_en'.format(key)] = dict_meta_data[key]
			sinhala_meta_data['{}_si'.format(key)] = value_list
		else :
			sinhala_meta_data['{}_en'.format(key)] = dict_meta_data[key]
			sinhala_meta_data['{}_si'.format(key)] = translate_to_sinhala(dict_meta_data[key])
	return sinhala_meta_data

def parse_html(html_pg):
	links = []
	soup = BeautifulSoup(html_pg, 'html.parser')
	song_links = soup.find_all("a", {"class": "_blank"})
	for tag in song_links:
		link = tag.get('href')
		links.append(link)
	return links                            


def get_songs_list():
	with open('song-corpus/song_links.csv', 'r') as f:
		lines = f.readlines()
	count = len(lines)
	list_songs = []
	for i in range(count):
		s_id = i+1
		headers = requests.utils.default_headers()
		res = requests.get(lines[i], headers)
		print('Scraping songs', i)
		song = get_song_info(res.text,s_id)
		song_sinhala = translate_values(song)
		list_songs.append(song_sinhala)
	return list_songs


def get_songs_data():
	list_songs = get_songs_list()
	with open ('song-corpus/songs.json','w+') as f:
		f.write(json.dumps(list_songs))
	return list_songs


def create_meta_all():
	dict_all_meta = {}
	list_keys = ['Singer_en', 'Singer_si', 'Genre_en', 'Genre_si', 'Composer_en', 'Composer_si', 'Lyricist_en', 'Lyricist_si']
	for i in list_keys :
		dict_all_meta[i] = []

	with open('song-corpus/songs.json') as f:
		data = json.loads(f.read())

	for items in data:
		for key in items:
			if key in list_keys:
				if type(items[key]) == list:
					for val in items[key]:
						if val not in dict_all_meta[key]:
							dict_all_meta[key].append(val)
				else :
					if items[key] not in dict_all_meta[key]:
						dict_all_meta[key].append(items[key])
	
	with open ('song-corpus/songs_meta_all.json','w+') as f:
		f.write(json.dumps(dict_all_meta))

def get_metaphor_data():
        metaphor_df = pd.read_csv('song-corpus/Metaphors.csv')
        metaphor_df.rename(columns=metaphor_df.iloc[0]).drop(metaphor_df.index[0])
        return metaphor_df


def getMetaphors(song_id):
        song_metaphors = metaphor_df[metaphor_df.Song_id == song_id]
        song_metaphors = song_metaphors.drop("Song_id", axis=1)
        metaphor_metadata = json.loads(song_metaphors.to_json(orient='records'))
        return metaphor_metadata

def initiate_song_df(metaphor_df):
  song_df = metaphor_df.copy()
  i=1
  for heading in heading_list:
    song_df.insert(i, heading, "")
    i+=1
  return song_df

def add_values_to_song_df():
  for song in song_list:
    songId = song["Song_id"]
    for heading in heading_list:
      item = song[heading]
      if (type(item) is list):
        item = item[0]
      song_df.loc[song_df.Song_id == songId, heading] = item

if __name__ == "__main__":
		heading_list = ["title","Singer_en","Singer_si","Genre_en","Genre_si","Lyricist_en","Lyricist_si","Composer_en","Composer_si","song_lyrics"]
		metaphor_df = get_metaphor_data()
		song_df = initiate_song_df(metaphor_df)
		song_list = get_songs_data()
		add_values_to_song_df()
		song_df.to_csv("song_list.csv", index = False)
		create_meta_all()

    
