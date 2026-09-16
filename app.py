
from flask import Flask, render_template, request, jsonify
import mysql.connector

app = Flask(__name__)


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_db_connection():

    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Sagar@48",
        database="ott_platform"
    )


# =========================================================
# HOME PAGE
# =========================================================

@app.route("/")
def home():

    return render_template("index.html")


# =========================================================
# GET PLATFORMS
# =========================================================

@app.route("/api/platforms", methods=["GET"])
def get_platforms():

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            platform_id,
            platform_name
        FROM platforms
        ORDER BY platform_id
    """)

    data = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(data)


# =========================================================
# GET GENRES
# =========================================================

@app.route("/api/genres", methods=["GET"])
def get_genres():

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            genre_id,
            genre_name
        FROM genres
        ORDER BY genre_id
    """)

    data = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(data)


# =========================================================
# GET DASHBOARD COUNTS
# =========================================================

@app.route("/api/dashboard", methods=["GET"])
def dashboard():

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) AS count FROM platforms")
    platforms = cursor.fetchone()["count"]

    cursor.execute("SELECT COUNT(*) AS count FROM movies")
    movies = cursor.fetchone()["count"]

    cursor.execute("SELECT COUNT(*) AS count FROM series")
    series = cursor.fetchone()["count"]

    cursor.execute("SELECT COUNT(*) AS count FROM documentaries")
    documentaries = cursor.fetchone()["count"]

    cursor.close()
    connection.close()

    return jsonify({
        "platforms": platforms,
        "movies": movies,
        "series": series,
        "documentaries": documentaries
    })


# =========================================================
# GET MOVIES
# =========================================================

@app.route("/api/movies", methods=["GET"])
def get_movies():

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            m.movie_id,
            m.platform_id,
            m.genre_id,
            m.title,
            m.description,
            m.release_year,
            m.duration_minutes,
            m.language,
            m.rating,
            m.content_url,
            p.platform_name,
            g.genre_name
        FROM movies m

        JOIN platforms p
        ON m.platform_id = p.platform_id

        LEFT JOIN genres g
        ON m.genre_id = g.genre_id

        ORDER BY m.movie_id
    """)

    data = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(data)


# =========================================================
# GET SERIES
# =========================================================

@app.route("/api/series", methods=["GET"])
def get_series():

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            s.series_id,
            s.platform_id,
            s.genre_id,
            s.title,
            s.description,
            s.release_year,
            s.seasons,
            s.language,
            s.rating,
            s.content_url,
            p.platform_name,
            g.genre_name
        FROM series s

        JOIN platforms p
        ON s.platform_id = p.platform_id

        LEFT JOIN genres g
        ON s.genre_id = g.genre_id

        ORDER BY s.series_id
    """)

    data = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(data)


# =========================================================
# GET DOCUMENTARIES
# =========================================================

@app.route("/api/documentaries", methods=["GET"])
def get_documentaries():

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            d.documentary_id,
            d.platform_id,
            d.genre_id,
            d.title,
            d.description,
            d.release_year,
            d.duration_minutes,
            d.language,
            d.rating,
            d.content_url,
            p.platform_name,
            g.genre_name
        FROM documentaries d

        JOIN platforms p
        ON d.platform_id = p.platform_id

        LEFT JOIN genres g
        ON d.genre_id = g.genre_id

        ORDER BY d.documentary_id
    """)

    data = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(data)


# =========================================================
# ADD MOVIE
# =========================================================

@app.route("/api/movies", methods=["POST"])
def add_movie():

    data = request.json

    connection = get_db_connection()
    cursor = connection.cursor()

    try:

        # Get genre name
        cursor.execute("""
            SELECT genre_name
            FROM genres
            WHERE genre_id = %s
        """, (data["genre_id"],))

        genre = cursor.fetchone()

        if genre is None:

            return jsonify({
                "error": "Invalid genre"
            }), 400

        genre_name = genre[0]


        # Insert movie
        cursor.execute("""
            INSERT INTO movies
            (
                platform_id,
                genre_id,
                genre_name,
                title,
                description,
                release_year,
                duration_minutes,
                language,
                rating,
                content_url
            )

            VALUES
            (
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s,%s
            )
        """, (
            data["platform_id"],
            data["genre_id"],
            genre_name,
            data["title"],
            data["description"],
            data["release_year"],
            data["duration_minutes"],
            data["language"],
            data["rating"],
            data["content_url"]
        ))

        movie_id = cursor.lastrowid


        # Insert many-to-many relationship
        cursor.execute("""
            INSERT INTO movie_genres
            (
                movie_id,
                genre_id
            )

            VALUES
            (%s, %s)
        """, (
            movie_id,
            data["genre_id"]
        ))


        connection.commit()

        return jsonify({
            "message": "Movie added successfully",
            "id": movie_id
        })


    except Exception as e:

        connection.rollback()

        return jsonify({
            "error": str(e)
        }), 500


    finally:

        cursor.close()
        connection.close()


# =========================================================
# ADD SERIES
# =========================================================

@app.route("/api/series", methods=["POST"])
def add_series():

    data = request.json

    connection = get_db_connection()
    cursor = connection.cursor()

    try:

        cursor.execute("""
            SELECT genre_name
            FROM genres
            WHERE genre_id = %s
        """, (data["genre_id"],))

        genre = cursor.fetchone()

        if genre is None:

            return jsonify({
                "error": "Invalid genre"
            }), 400

        genre_name = genre[0]


        cursor.execute("""
            INSERT INTO series
            (
                platform_id,
                genre_id,
                genre_name,
                title,
                description,
                release_year,
                seasons,
                language,
                rating,
                content_url
            )

            VALUES
            (
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s
            )
        """, (
            data["platform_id"],
            data["genre_id"],
            genre_name,
            data["title"],
            data["description"],
            data["release_year"],
            data["seasons"],
            data["language"],
            data["rating"],
            data["content_url"]
        ))

        series_id = cursor.lastrowid


        cursor.execute("""
            INSERT INTO series_genres
            (
                series_id,
                genre_id
            )

            VALUES
            (%s, %s)
        """, (
            series_id,
            data["genre_id"]
        ))


        connection.commit()

        return jsonify({
            "message": "Series added successfully",
            "id": series_id
        })


    except Exception as e:

        connection.rollback()

        return jsonify({
            "error": str(e)
        }), 500


    finally:

        cursor.close()
        connection.close()


# =========================================================
# ADD DOCUMENTARY
# =========================================================

@app.route("/api/documentaries", methods=["POST"])
def add_documentary():

    data = request.json

    connection = get_db_connection()
    cursor = connection.cursor()

    try:

        cursor.execute("""
            SELECT genre_name
            FROM genres
            WHERE genre_id = %s
        """, (data["genre_id"],))

        genre = cursor.fetchone()

        if genre is None:

            return jsonify({
                "error": "Invalid genre"
            }), 400

        genre_name = genre[0]


        cursor.execute("""
            INSERT INTO documentaries
            (
                platform_id,
                genre_id,
                genre_name,
                title,
                description,
                release_year,
                duration_minutes,
                language,
                rating,
                content_url
            )

            VALUES
            (
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s
            )
        """, (
            data["platform_id"],
            data["genre_id"],
            genre_name,
            data["title"],
            data["description"],
            data["release_year"],
            data["duration_minutes"],
            data["language"],
            data["rating"],
            data["content_url"]
        ))

        documentary_id = cursor.lastrowid


        cursor.execute("""
            INSERT INTO documentary_genres
            (
                documentary_id,
                genre_id
            )

            VALUES
            (%s, %s)
        """, (
            documentary_id,
            data["genre_id"]
        ))


        connection.commit()

        return jsonify({
            "message": "Documentary added successfully",
            "id": documentary_id
        })


    except Exception as e:

        connection.rollback()

        return jsonify({
            "error": str(e)
        }), 500


    finally:

        cursor.close()
        connection.close()


# =========================================================
# DELETE MOVIE
# =========================================================

@app.route("/api/movies/<int:movie_id>", methods=["DELETE"])
def delete_movie(movie_id):

    connection = get_db_connection()
    cursor = connection.cursor()

    try:

        cursor.execute("""
            DELETE FROM movies
            WHERE movie_id = %s
        """, (movie_id,))

        connection.commit()

        return jsonify({
            "message": "Movie deleted successfully"
        })

    except Exception as e:

        connection.rollback()

        return jsonify({
            "error": str(e)
        }), 500

    finally:

        cursor.close()
        connection.close()


# =========================================================
# DELETE SERIES
# =========================================================

@app.route("/api/series/<int:series_id>", methods=["DELETE"])
def delete_series(series_id):

    connection = get_db_connection()
    cursor = connection.cursor()

    try:

        cursor.execute("""
            DELETE FROM series
            WHERE series_id = %s
        """, (series_id,))

        connection.commit()

        return jsonify({
            "message": "Series deleted successfully"
        })

    except Exception as e:

        connection.rollback()

        return jsonify({
            "error": str(e)
        }), 500

    finally:

        cursor.close()
        connection.close()


# =========================================================
# DELETE DOCUMENTARY
# =========================================================

@app.route("/api/documentaries/<int:documentary_id>",
           methods=["DELETE"])
def delete_documentary(documentary_id):

    connection = get_db_connection()
    cursor = connection.cursor()

    try:

        cursor.execute("""
            DELETE FROM documentaries
            WHERE documentary_id = %s
        """, (documentary_id,))

        connection.commit()

        return jsonify({
            "message": "Documentary deleted successfully"
        })

    except Exception as e:

        connection.rollback()

        return jsonify({
            "error": str(e)
        }), 500

    finally:

        cursor.close()
        connection.close()


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )