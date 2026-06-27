from database.DB_connect import DBConnect
from model.customer import Customer


class DAO():
    @staticmethod
    def getAllCountries():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """select distinct Country 
                    from customer c 
                    order by Country asc """

        cursor.execute(query)
        res = []
        for row in cursor:
            res.append(row["Country"])

        cursor.close()
        conn.close()
        return res

    @staticmethod
    def getAllCustomers(country, S):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """select c.CustomerId , c.FirstName , c.LastName , c.Phone , c.Email
                    from customer c , invoice i , invoiceline i2 , track t 
                    where c.CustomerId = i.CustomerId 
                    and i.InvoiceId = i2.InvoiceId 
                    and i2.TrackId = t.TrackId 
                    and c.Country =  %s
                    group by c.CustomerId 
                    having count(distinct t.GenreId) >= %s
                    """

        cursor.execute(query, (country, S,))
        res = []
        for row in cursor:
            res.append(Customer(**row))

        cursor.close()
        conn.close()
        return res

    @staticmethod
    def getAllStats(country, customerTracks, customerGenres):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """select distinct c.CustomerId , a.ArtistId , t.GenreId 
                    from customer c , invoice i , invoiceline i2 , track t , album a 
                    where c.CustomerId = i.CustomerId 
                    and i.InvoiceId = i2.InvoiceId 
                    and i2.TrackId = t.TrackId 
                    and t.AlbumId = a.AlbumId 
                    and c.Country =  %s"""

        cursor.execute(query, (country,))

        for row in cursor:
            customerId = row["CustomerId"]
            artistId = row["ArtistId"]
            genreId = row["GenreId"]

            if customerId in customerTracks:
                customerTracks[customerId].append(artistId)
            else:
                customerTracks[customerId] = [artistId]
            if customerId in customerGenres:
                customerGenres[customerId].append(genreId)
            else:
                customerGenres[customerId] = [genreId]


        cursor.close()
        conn.close()
        return customerTracks, customerGenres

