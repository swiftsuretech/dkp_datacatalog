with open("./queries.txt", 'w+') as queries:

    for year in range(2017, 2023):
        for month in range(1, 13):
            month = str(month)
            if len(month) == 1:
                month = "0"+month
                for day in range(1, 32):
                    day = str(day)
                    if len(day) == 1:
                        day = "0"+day
                    for hour in range(1, 24):
                        hour = str(hour)
                        if len(hour) == 1:
                            hour = "0"+hour
                        queries.write(f"https://api.gdeltproject.org/api/v2/doc/doc?query=technology%20soureceLang:eng&mode=ArtList&maxrecords=250&sort=DateAsc&format=json&STARTDATETIME={year}{month}{day}{hour}0000&ENDDATETIME={year}{month}{day}{hour}5959\n")

