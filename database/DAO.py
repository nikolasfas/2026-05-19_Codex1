from database.DB_connect import DBConnect
from model.artist import Artist
from model.genre import Genre


class DAO():
    @staticmethod
    def getAllGenre():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """select *
                    from genre g  
                    order by Name asc"""

        cursor.execute(query)
        res = []
        for row in cursor:
            res.append(Genre(**row))

        cursor.close()
        conn.close()
        return res

    @staticmethod
    def getArtists(genreId):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """select distinct a.ArtistId , a.Name 
                    from artist a , album a2 , track t 
                    where a.ArtistId = a2.ArtistId  
                    and t.AlbumId = a2.AlbumId 
                    and t.GenreId = %s"""

        cursor.execute(query, (genreId,))
        res = []
        for row in cursor:
            res.append(Artist(**row))

        cursor.close()
        conn.close()
        return res

    @staticmethod
    def getConnections(genreId):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """with links as(
                    select i.TrackId , i.Quantity , i2.CustomerId , a.ArtistId 
                    from invoiceline i , invoice i2 , track t , album a
                    where i.InvoiceId = i2.InvoiceId 
                    and i.TrackId = t.TrackId 
                    and t.AlbumId = a.AlbumId 
                    and t.GenreId = %s),
                    popularity as (
                    select a.ArtistId , sum(i.Quantity)as pop
                    from track t , album a , invoiceline i 
                    where t.TrackId = i.TrackId 
                    and a.AlbumId = t.AlbumId 
                    and t.GenreId = %s
                    group by a.ArtistId
                    )
                    select distinct l1.ArtistId as a1, p.pop as pop1, l2.ArtistId as a2, p2.pop as pop2
                    from links l1, links l2, popularity p , popularity p2
                    where l1.CustomerId = l2.CustomerId
                    and l1.ArtistId < l2.ArtistId
                    and l1.ArtistId = p.ArtistId
                    and l2.ArtistId = p2.ArtistId"""

        cursor.execute(query, (genreId, genreId,))
        res = []
        for row in cursor:
            res.append((row["a1"], row["pop1"], row["a2"], row["pop2"]))

        cursor.close()
        conn.close()
        return res
