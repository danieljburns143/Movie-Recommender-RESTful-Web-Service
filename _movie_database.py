class _movie_database:
    def __init__(self):
        self.movies = {}
        self.users = {}
        self.ratings = {}
        self.images = {}
        self.moviesVotedOn = {}

    def load_images(self, movie_file):
        self.images.clear()
        myFile = open(movie_file)
        for line in myFile:
            line = line.strip()
            line = line.split('::')
            self.images[int(line[0])] = [line[1], line[2]]
        myFile.close()

    def load_movies(self, movie_file):
        self.movies.clear()
        myFile = open(movie_file)
        for line in myFile:
            line = line.strip()
            line = line.split('::')
            self.movies[int(line[0])] = [line[1], line[2]]
        myFile.close()

    def reset_one_movie(self, movie_file, movie_id):
        myFile = open(movie_file)
        for line in myFile:
            line = line.strip()
            line = line.split('::')
            if line[0] == movie_id:
                self.movies[int(line[0])] = [line[1], line[2]]
        myFile.close()

    def get_movie(self, mid):
        if mid in self.movies:
            return self.movies[mid]
        else:
            return None

    def get_movies(self):
        return [int(x) for x in self.movies]

    def set_movie(self, mid, listParameter):
        self.movies[mid] = listParameter

    def delete_movie(self, mid):
        if mid in self.movies:
            del self.movies[mid]

    def load_users(self, users_file):
        self.users.clear()
        myFile = open(users_file)
        for line in myFile:
            line = line.strip()
            line = line.split('::')
            self.users[int(line[0])] = [line[1], int(line[2]), int(line[3]), line[4]]
        myFile.close()

    def get_user(self, uid):
        if uid in self.users:
            return self.users[uid]
        else:
            return None

    def get_users(self):
        return [int(x) for x in self.users]

    def set_user(self, uid, listParameter):
        self.users[uid] = listParameter

    def delete_user(self, uid):
        if uid in self.users:
            del self.users[uid]

    def load_ratings(self, ratings_file):
        self.ratings.clear()
        self.moviesVotedOn.clear()
        myFile = open(ratings_file)
        for line in myFile:
            line = line.strip()
            line = line.split('::')
            if int(line[1]) not in self.ratings:
                self.ratings[int(line[1])] = {}
            self.ratings[int(line[1])][int(line[0])] = int(line[2])
            if int(line[0]) not in self.moviesVotedOn:
                self.moviesVotedOn[int(line[0])] = set()
            self.moviesVotedOn[int(line[0])].add(int(line[1]))
        myFile.close()

    def get_rating(self, mid):
        if int(mid) not in self.ratings:
            return 0
        else:
            averageRating = float(0)
            for users in self.ratings[int(mid)]:
                averageRating += self.ratings[int(mid)][users]
            averageRating /= len(self.ratings[int(mid)])
            return averageRating

    def get_highest_rated_movie(self):
        highestAverageRatingID = 0
        highestAverageRating = 0
        if len(self.ratings) == 0:
            return None
        for ID in self.ratings:
            if self.get_rating(ID) > highestAverageRating:
                highestAverageRatingID = ID
                highestAverageRating = self.get_rating(ID)
            elif self.get_rating(ID) == highestAverageRating:
                if ID < highestAverageRatingID:
                    highestAverageRatingID = ID
        return highestAverageRatingID

    def set_user_movie_rating(self, uid, mid, rating):
        if uid in self.users and mid in self.movies:
            self.ratings[int(mid)][int(uid)] = int(rating)
            self.moviesVotedOn[int(uid)].add(int(mid))

    def get_user_movie_rating(self, uid, mid):
        if mid in self.ratings and uid in self.ratings[mid]:
            return self.ratings[int(mid)][int(uid)]

    def delete_all_ratings(self):
        self.ratings.clear()
        self.moviesVotedOn.clear()

    def get_highest_rated_unvoted_movie(self, uid):
        uid = int(uid)
        highestAverageRatingID = 0
        highestAverageRating = 0
        if len(self.ratings) == 0:
            return None
        for ID in self.ratings:
            if ID not in self.moviesVotedOn[uid]:
                if self.get_rating(ID) > highestAverageRating:
                    highestAverageRatingID = ID
                    highestAverageRating = self.get_rating(ID)
                elif self.get_rating(ID) == highestAverageRating:
                    if ID < highestAverageRatingID:
                        highestAverageRatingID = ID
        return highestAverageRatingID

if __name__ == "__main__":
       mdb = _movie_database()
       mdb.load_users('ml-1m/users.dat')
