import threading
import psycopg2


def query_thread_manager(db_con, query, params=None):
    # TODO long timeout
    timeout = 30.0  # * 1.0  # [seconds]

    query_thread = threading.Thread(target=db_con.execute_query, args=(query, params))
    query_thread.start()
    query_thread.join(timeout)

    while query_thread.is_alive():
        print "Query still running..."
        query_thread.join(timeout)

        try:
            new_cur = db_con.con.cursor()
            new_cur.execute('SELECT \'Pinging data base... \'')
            new_cur.close()
        except psycopg2.ProgrammingError:
            print "Pinged database..."
    else:
        return db_con
