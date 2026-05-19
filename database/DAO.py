from database.DB_connect import DBConnect
from model.artist import Artist
from model.genre import Genre


class DAO():
    @staticmethod
    def getAllGenre():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """select *
                    from genre g  """

        cursor.execute(query)
        res = []
        for row in cursor:
            res.append(Genre(**row))

        cursor.close()
        conn.close()
        return res

    @staticmethod
    def getArtistByGenre(genre):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """select distinct a2.ArtistId , a2.Name  
                    from track t, album a, artist a2 
                    where t.AlbumId = a.AlbumId and a.ArtistId = a2.ArtistId
                    and t.GenreId = %s"""

        cursor.execute(query, (genre, ))
        res = []
        for row in cursor:
            res.append(Artist(**row))

        cursor.close()
        conn.close()
        return res

    @staticmethod
    def getAllEdges(genre):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """select distinct t.ArtistId as a1, t2.ArtistId as a2
                    from (select i.CustomerId, t.Name ,  a.ArtistId 
                    from invoice i, invoiceline i2, track t, album a, artist a2  
                    where i.InvoiceId = i2.InvoiceId 
                    and i2.TrackId = t.TrackId 
                    and t.AlbumId = a.AlbumId 
                    and a.ArtistId = a2.ArtistId 
                    and t.GenreId = %s)t, 
                    (select i.CustomerId, t.Name ,  a.ArtistId 
                    from invoice i, invoiceline i2, track t, album a, artist a2  
                    where i.InvoiceId = i2.InvoiceId 
                    and i2.TrackId = t.TrackId 
                    and t.AlbumId = a.AlbumId 
                    and a.ArtistId = a2.ArtistId 
                    and t.GenreId = %s) t2
                    where t.CustomerId = t2.CustomerId
                    and t.ArtistID > t2.ArtistID"""

        cursor.execute(query, (genre, genre,))
        res = []
        for row in cursor:
            res.append((row["a1"], row["a2"]))

        cursor.close()
        conn.close()
        return res

