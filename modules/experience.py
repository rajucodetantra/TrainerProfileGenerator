from datetime import datetime


class Experience:


    def calculate(self, joining_date):

        if not joining_date:
            return "Not Available"


        try:

            if isinstance(joining_date, datetime):

                doj = joining_date

            else:

                doj = datetime.strptime(
                    str(joining_date),
                    "%d-%m-%Y"
                )


            today = datetime.today()


            years = today.year - doj.year

            months = today.month - doj.month

            days = today.day - doj.day


            if days < 0:

                months -= 1
                days += 30


            if months < 0:

                years -= 1
                months += 12


            return (
                f"{years} Years "
                f"{months} Months "
                f"{days} Days"
            )


        except:

            return "Not Available"