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
                        queries.write(f"https://api.gdeltproject.org/api/v2/doc/doc?query=(devops OR gitops OR kubernetes OR containerization OR \"cloud native\" OR \"machine learning\")&mode=ArtList&maxrecords=250&sort=DateAsc&format=json&STARTDATETIME={year}{month}{day}000000&ENDDATETIME={year}{month}{day}235959\n")
