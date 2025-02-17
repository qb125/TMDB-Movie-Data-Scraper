import requests
import pandas as pd
import time
import os
from dotenv import load_dotenv
import tkinter as tk
from tkinter import simpledialog
from datetime import datetime

# Load environment variables
load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"

# Mapping of country codes to full names
COUNTRY_MAP = {
    "us": "United States of America",
    "canada": "Canada",
    "uk": "United Kingdom",
    "france": "France",
    "germany": "Germany",
    "india": "India",
    "china": "China",
    "japan": "Japan",
    "australia": "Australia",
    "mexico": "Mexico",
    "brazil": "Brazil",
}


# Function to fetch JSON data from TMDB API
def fetch_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    print(f"⚠️ Error fetching data: {response.status_code} - {response.text}")
    return None


# Function to get genre ID from genre name
def get_genre_id(genre_name):
    url = f"{BASE_URL}/genre/movie/list?api_key={API_KEY}"
    data = fetch_data(url)
    if not data:
        return None
    for genre in data.get("genres", []):
        if genre["name"].lower() == genre_name.lower():
            return genre["id"]
    return None


# Function to fetch genre names for a movie
def get_movie_genres(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}?api_key={API_KEY}"
    data = fetch_data(url)
    return ", ".join([genre["name"] for genre in data.get("genres", [])]) if data else "Unknown"


# Function to fetch production countries for a movie
def get_movie_production_countries(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}?api_key={API_KEY}"
    data = fetch_data(url)
    return [country["name"] for country in data.get("production_countries", [])] if data else []


# Function to fetch movies based on filters
def get_movies_by_filter(genre, start_year, start_month, end_year, end_month, min_gross, max_gross, countries,
                         release_type):
    movie_list, seen_movies = [], set()
    page, genre_id = 1, get_genre_id(genre) if genre.lower() != "all" else None
    normalized_countries = [COUNTRY_MAP.get(country.lower(), country.title()) for country in countries]
    start_date, end_date = f"{start_year}-{str(start_month).zfill(2)}-01", f"{end_year}-{str(end_month).zfill(2)}-31"
    release_type_filter = "&with_release_type=3|2" if release_type == "theatrical" else "&with_release_type=1|4|5|6" if release_type == "non-theatrical" else ""

    while True:
        url = (f"{BASE_URL}/discover/movie?api_key={API_KEY}&sort_by=revenue.desc"
               f"&primary_release_date.gte={start_date}&primary_release_date.lte={end_date}{release_type_filter}"
               f"&page={page}")
        if genre_id:
            url += f"&with_genres={genre_id}"

        print(f"Fetching Page {page} for Movies in {', '.join(normalized_countries)} Released as {release_type}... ")
        data = fetch_data(url)
        if not data or "results" not in data:
            break

        for movie in data["results"]:
            title, release_date = movie.get("title", ""), movie.get("release_date", "")
            release_year, release_month = map(int, (release_date[:4], release_date[5:7])) if release_date else (0, 0)

            if not (start_year <= release_year <= end_year and start_month <= release_month <= end_month):
                continue

            movie_id = movie.get("id")
            if not movie_id:
                continue

            country_list = get_movie_production_countries(movie_id)
            print(f"🔍 {title} ({release_year}-{release_month}) - Production Countries: {country_list}")

            if any(country.lower() in [c.lower() for c in country_list] for country in normalized_countries) and (
            title, release_year) not in seen_movies:
                revenue = movie.get("revenue", 0)
                if (min_gross == "all" or revenue >= min_gross) and (max_gross == "all" or revenue <= max_gross):
                    movie_data = {
                        "Title": title, "Release Year": release_year, "Release Month": release_month,
                        "Revenue (USD)": revenue, "Genres": get_movie_genres(movie_id),
                        "IMDb Rating": movie.get("vote_average"), "Overview": movie.get("overview"),
                        "Production Countries": ", ".join(country_list), "Release Type": release_type
                    }
                    movie_list.append(movie_data)
                    seen_movies.add((title, release_year))
            else:
                print(f"❌ Skipping {title} - Not produced in selected countries or duplicate")

        print(f"Page {page} processed. Total unique movies collected: {len(movie_list)}")
        if page >= data.get("total_pages", 1):
            break
        page += 1
        time.sleep(1)
    return movie_list


# Function to generate a unique filename
def generate_filename(genre, start_year, start_month, end_year, end_month, countries, min_gross, max_gross):
    date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    countries_str = "_".join(countries)
    return f"filtered_movie_data_{genre}_{start_year}-{start_month}_{end_year}-{end_month}_{countries_str}_{min_gross}-{max_gross}_{date_str}.csv"


# Function to save movies to CSV
def save_to_csv(movies, filename):
    df = pd.DataFrame(movies)
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")


# Simple UI to get user input
root = tk.Tk()
root.withdraw()

genre = simpledialog.askstring("Input", "Enter genre (or type 'all' for all genres):")
start_year = simpledialog.askinteger("Input", "Enter start year:")
start_month = simpledialog.askinteger("Input", "Enter start month (1-12):")
end_year = simpledialog.askinteger("Input", "Enter end year:")
end_month = simpledialog.askinteger("Input", "Enter end month (1-12):")
country_input = simpledialog.askstring("Input", "Enter countries (comma-separated, e.g., US, Canada, India):")
release_type = simpledialog.askstring("Input", "Choose release type: theatrical, non-theatrical, both:")
min_gross = simpledialog.askinteger("Input", "Enter minimum box office revenue (or type 0 for no filter):")
max_gross = simpledialog.askinteger("Input", "Enter maximum box office revenue (or type 0 for no filter):")

countries = [country.strip().title() for country in country_input.split(",")]
movies_data = get_movies_by_filter(genre, start_year, start_month, end_year, end_month, min_gross, max_gross, countries,
                                   release_type)
filename = generate_filename(genre, start_year, start_month, end_year, end_month, countries, min_gross, max_gross)
save_to_csv(movies_data, filename)
