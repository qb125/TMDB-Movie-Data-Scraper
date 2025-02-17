# TMDB-Movie-Data-Scraper
Movie Data Scraper for TMDB


# 🎬 TMDB Movie Data Scraper  
## 📊 Overview  
This Python script extracts **movie production data** from the **TMDB API**, allowing users to filter movies based on:
- 🎭 **Genre**
- 📅 **Release Year & Month**
- 🌍 **Production Country**
- 🎟️ **Theatrical vs Non-Theatrical Releases**
- ⭐ **IMDb Ratings**  

The filtered data is then **saved as a CSV file** for further analysis, making it perfect for data visualization projects in **Tableau or Excel**.

---

## 🚀 Features  
✅ **API-Based Data Extraction:** Fetches real-time movie data from TMDB.  
✅ **Dynamic Filtering:** Users can specify genre, country, date range, and more.  
✅ **Automated CSV Export:** Generates a unique filename with filter details.  
✅ **User-Friendly UI:** Uses **Tkinter** for simple user input prompts.  
✅ **Optimized for Data Analysis:** Output can be used in **Tableau, Excel, or Pandas**.

---

## 🛠️ Installation & Setup  
###

1️⃣ Clone this repository:  
git clone https://github.com/qb125/TMDB-Movie-Data-Scraper.git



2️⃣ Install dependencies:
Ensure you have Python 3.x installed, then install required libraries:
pip install requests pandas python-dotenv tk


3️⃣ Set up your API key:
Get a free API key from TMDB: https://www.themoviedb.org/settings/api
Create a .env file in the project directory.
Add the following line to .env:
TMDB_API_KEY=your_api_key_here


//////


🎬 How to Use
Run the script using:
python main.py

When the script runs, a simple UI will prompt you to enter: ✔ Genre (or type "all" for all genres)
✔ Start Year & Month
✔ End Year & Month
✔ Production Countries (comma-separated, e.g., "US, Canada")
✔ Theatrical vs. Non-Theatrical Release
✔ Minimum & Maximum IMDb Rating

📁 Output:
A .csv file will be generated in the same folder with a unique filename:
filtered_movie_data_Genre_YYYY-MM_YYYY-MM_Countries_Min-MaxRating.csv


📊 Sample Output (CSV Structure)
Title	Release Year	Release Month	Genre	IMDb Rating	Production Country	Release Type
Movie A	2024	01	Action	7.5	United States	Theatrical
Movie B	2024	05	Comedy	6.8	Canada	Non-Theatrical


🔍 Key Insights (from Analysis)
This script was used to analyze 2024 US & Canada movie production trends. Some key findings from the dataset include:

📅 Peak movie releases occur in May, July, and December.
🎭 Most produced genres: Documentary, Drama, Comedy, Horror.
🌍 Most common co-production country: United Kingdom 🇬🇧.
⭐ Highest-rated genre: Music (8.042 IMDb avg.).
🔍 Lowest-rated genre: TV Movies (6.011 IMDb avg.).
📊 Full Analysis & Dashboard:
https://public.tableau.com/app/profile/bradley.sutherland/viz/MovieReleaseTrendAnalysis/MovieIndustryDataAnalysis2024?publish=yes

⚠️ Limitations & Challenges
🚧 API Restriction: TMDB limits to 500 pages max, meaning very large datasets cannot be extracted in full.
💰 No Revenue Data: TMDB API does not provide box office revenue figures.
🌍 Co-Production Countries: Some movies have multiple production locations, which required data cleaning.

🎯 Next Steps & Future Improvements
🔹 Automate Tableau dashboard creation from the extracted data.
🔹 Use IMDb API (paid) or Kaggle datasets for revenue-based insights.
🔹 Expand to analyze global movie production trends (beyond US & Canada).

📜 License
This project is open-source under the MIT License. Feel free to fork, modify, and improve!

📞 Contact & Portfolio
🔗 Portfolio & Full Write-Up: https://linktr.ee/bradleyksutherland
💼 LinkedIn: https://www.linkedin.com/in/bradley-sutherland-7a6999269/
📧 Email: sutherland.bradley13@gmail.com
