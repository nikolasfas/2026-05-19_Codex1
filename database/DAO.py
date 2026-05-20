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
    def getAllEdges(genre, idMap):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """with popularity as (
                select a.ArtistId, sum(i2.Quantity) as pop
                from invoice i, invoiceline i2, track t, album a
                where i.InvoiceId = i2.InvoiceId
                and i2.TrackId = t.TrackId
                and t.AlbumId = a.AlbumId
                and t.GenreId = %s
                group by a.ArtistId
                            ),
                sales as (
                                select distinct i.CustomerId, a.ArtistId
                                from invoice i, invoiceline i2, track t, album a
                                where i.InvoiceId = i2.InvoiceId
                                and i2.TrackId = t.TrackId
                                and t.AlbumId = a.AlbumId
                                and t.GenreId = %s
                            )
                select distinct 
                    s.ArtistId as a1,
                    s1.ArtistId as a2,
                    p1.pop as pop1,
                    p2.pop as pop2,
                    p1.pop + p2.pop as peso
                from sales s, sales s1, popularity p1, popularity p2
                where s.CustomerId = s1.CustomerId
                and s.ArtistId < s1.ArtistId
                and s.ArtistId = p1.ArtistId
                and s1.ArtistId = p2.ArtistId
                """

        cursor.execute(query, (genre, genre, ))
        res = []
        for row in cursor:
            a1 = idMap[row["a1"]]
            a2 = idMap[row["a2"]]
            peso = row["peso"]

            if row["pop1"] > row["pop2"]:
                res.append((a1, a2, peso))
            elif row["pop2"] > row["pop1"]:
                res.append((a2, a1, peso))
            else:
                res.append((a1, a2, peso))
                res.append((a2, a1, peso))

        cursor.close()
        conn.close()
        return res

