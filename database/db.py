import sqlite3


def get_connection():

    return sqlite3.connect(
        "database/candidates.db"
    )


def create_table():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS candidates(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT,

            ats REAL,

            cgpa REAL,

            projects REAL,

            internship REAL,

            summary TEXT,

            shortlisted INTEGER DEFAULT 0

        )
        """
    )

    conn.commit()

    conn.close()

def toggle_shortlist(name):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE candidates
        SET shortlisted =
            CASE
                WHEN shortlisted = 1 THEN 0
                ELSE 1
            END
        WHERE name = ?
        """,
        (name,)
    )

    conn.commit()

    conn.close()


def save_candidate(candidate):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """

        INSERT INTO candidates(

        name,
        ats,
        cgpa,
        projects,
        internship,
        summary

        )

        VALUES(

        ?,
        ?,
        ?,
        ?,
        ?,
        ?

        )

        """,

        (

        candidate["name"],

        candidate["ats"],

        candidate["cgpa"],

        candidate["projects"],

        candidate["internship"],

        candidate["summary"]

        )

    )

    conn.commit()

    conn.close()

def get_candidates():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(

        """
        SELECT

        name,
        ats,
        cgpa,
        projects,
        internship,
        summary,
        shortlisted

        FROM candidates
        """

    )

    rows = cursor.fetchall()

    conn.close()

    return rows

def get_shortlisted():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
        name,
        ats,
        cgpa,
        projects,
        internship,
        summary

        FROM candidates

        WHERE shortlisted = 1
        """
    )

    rows = cursor.fetchall()

    conn.close()

    return rows

def clear_candidates():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(

        "DELETE FROM candidates"

    )

    conn.commit()

    conn.close()

#temporarily
#def insert_dummy():

