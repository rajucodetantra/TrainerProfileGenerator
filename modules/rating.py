class Rating:

    def get_rating(self, rating):

        try:
            rating = int(float(rating))
        except:
            rating = 5

        if rating < 1:
            rating = 1

        if rating > 5:
            rating = 5

        return "★" * rating + "☆" * (5 - rating)