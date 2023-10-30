import sqlite3

class StephenKingAdaptationsDatabase:
    def __init__(self, database_file):
        self.conn = sqlite3.connect(database_file)
        self.create_table()

    def create_table(self):
        self.conn.execute('''CREATE TABLE IF NOT EXISTS stephen_king_adaptations_table
                             (movieID INT PRIMARY KEY NOT NULL,
                             movieName TEXT NOT NULL,
                             movieYear INT NOT NULL,
                             imdbRating REAL NOT NULL);''')

    def insert_movie(self, movieID, movieName, movieYear, imdbRating):
        self.conn.execute("INSERT INTO stephen_king_adaptations_table (movieID, movieName, movieYear, imdbRating) VALUES (?,?,?,?)",
                          (movieID, movieName, movieYear, imdbRating))
        self.conn.commit()

    def search_movie_by_name(self, movie_name):
        cursor = self.conn.execute("SELECT * FROM stephen_king_adaptations_table WHERE movieName=?", (movie_name,))
        return cursor.fetchone()

    def search_movie_by_year(self, year):
        cursor = self.conn.execute("SELECT * FROM stephen_king_adaptations_table WHERE movieYear=?", (year,))
        return cursor.fetchall()

    def search_movie_by_rating(self, rating):
        cursor = self.conn.execute("SELECT * FROM stephen_king_adaptations_table WHERE imdbRating>=?", (rating,))
        return cursor.fetchall()

    def close(self):
        self.conn.close()

def read_movie_list(file_path):
    with open(file_path, 'r') as file:
        movie_list = file.readlines()
        movie_list = [movie.strip() for movie in movie_list]
    return movie_list

def main():
    database = StephenKingAdaptationsDatabase('stephen_king_adaptations.db')
    movie_list = read_movie_list('D:\Download\Github仓库\Python-examples\Exercise\exercise 2\stephen_king_adaptations.txt')

    for i, movie in enumerate(movie_list):
        movie_details = movie.split(',')
        database.insert_movie(i+1, movie_details[1], int(movie_details[2]), float(movie_details[3]))

    while True:
        print("\nPlease select an option:")
        print("1. Search for a movie by name")
        print("2. Search for a movie by year")
        print("3. Search for a movie by rating")
        print("4. Quit\n")
        option = input()

        if option == '1':
            movie_name = input("\nPlease enter the name of the movie: ")
            movie_details = database.search_movie_by_name(movie_name)
            if movie_details:
                print("Movie ID:", movie_details[0])
                print("Movie Name:", movie_details[1])
                print("Movie Year:", movie_details[2])
                print("IMDB Rating:", movie_details[3])
                print("\n")
            else:
                print("No such movie exists in our database.\n")

        elif option == '2':
            year = input("\nPlease enter the year: ")
            movies = database.search_movie_by_year(year)
            if movies:
                for movie in movies:
                    print("Movie ID:", movie[0])
                    print("Movie Name:", movie[1])
                    print("Movie Year:", movie[2])
                    print("IMDB Rating:", movie[3])
                    print("\n")
            else:
                print("No movies were found.\n")

        elif option == '3':
            rating = input("\nPlease enter the rating: ")
            movies = database.search_movie_by_rating(rating)
            if movies:
                for movie in movies:
                    print("Movie ID:", movie[0])
                    print("Movie Name:", movie[1])
                    print("Movie Year:", movie[2])
                    print("IMDB Rating:", movie[3])
                    print("\n")
            else:
                print("There is no movie with the same rating or higher.\n")

        elif option == '4':
            break

        print("Do you want to query other information? (Yes or No)")
        option1 = input()

        if option1 == 'No':
            break

    database.close()

if __name__ == "__main__":
    main()
