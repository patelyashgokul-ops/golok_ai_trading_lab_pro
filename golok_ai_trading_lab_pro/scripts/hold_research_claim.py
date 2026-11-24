"""Disposable test worker holding an uncommitted database claim."""

import sys
from time import sleep

import psycopg2


def run(database, port, job_id):
    if not database.startswith("golok_p08_fresh_") or not port.isdecimal() or not job_id.isdecimal():
        raise ValueError("Use a disposable P08 test database.")
    with psycopg2.connect(host="127.0.0.1", port=port, dbname=database, user="golok_test") as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id FROM golok_lab_research_job WHERE id=%s AND state='queued' FOR UPDATE",
                           (int(job_id),))
            if not cursor.fetchone():
                raise RuntimeError("No queued job.")
            cursor.execute("UPDATE golok_lab_research_job SET state='failed' WHERE id=%s", (int(job_id),))
            print("CLAIMED", flush=True)
            sleep(45)
            raise RuntimeError("The test must interrupt this process.")


if __name__ == "__main__":
    run(*sys.argv[1:])
