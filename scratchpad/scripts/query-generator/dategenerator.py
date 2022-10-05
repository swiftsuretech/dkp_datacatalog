with open("./queries.txt", 'w+') as queries:
    for year in range(2023, 2016, -1):
        for month in range(12, 0, -1):
            month = str(month)
            if len(month) == 1:
                month = "0"+month
            for day in range(31, 0, -1):
                day = str(day)
                if len(day) == 1:
                    day = "0"+day
                query = f"https://api.gdeltproject.org/api/v2/doc/doc?query=kubernetes%20sourceLang:eng&mode=ArtList&maxrecords=250&sort=DateAsc&format=json&STARTDATETIME={year}{month}{day}000000&ENDDATETIME={year}{month}{day}235959\n"
                queries.write(query)

