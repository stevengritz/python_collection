import json
import os
import getpass

import psycopg2


# Container for data base profile info
class DbConnectionHandler:
    user = str()
    db_name = str()
    host = str()
    port = str()
    schema = str()
    table_prefix_ids = list()
    filter_out = dict()

    user_choice = {'Y': True, 'N': False}
    con = None
    cur = None

    def __init__(self):
        pass

    def load_profile(self, profile_name, directory, **optional):
        if 'fp' in optional:
            j_file = optional['fp']
        else:
            j_path = directory + '/' + "db_profile.json"
            if os.path.isfile(j_path):
                j_file = open(directory + '/' + "db_profile.json", "r")
            else:
                j_file = open(directory + '/' + "db_profile.json", "w+")
                j_file.write('{\"profiles\":{}}')
                j_file.seek(0)
        profiles = json.load(j_file)
        if profile_name in profiles['profiles']:
            profile = profiles['profiles'][profile_name]
            self.user = profile['user']
            self.db_name = profile['db_name']
            self.host = profile['host']
            self.port = profile['port']

        else:
            create_new_profile = raw_input('Profile not found. '
                                           'Create new Redshift connection profile called %s? (Y/[N])  ' % profile_name)
            if self.user_choice.get(create_new_profile, False):
                new_profile = dict()
                new_profile['user'] = raw_input('Enter the username: ')
                new_profile['db_name'] = raw_input('Enter the database name (e.g. cidw): ')
                new_profile['host'] = raw_input('Enter the host/IP address: ')
                new_profile['port'] = raw_input('Enter the port number: ')
                new_profile['schema'] = raw_input('Enter the schema name: ')
                prefix_string = raw_input('Enter the filter prefixes, single space'
                                          ' between multiple (leave blank for none): ')
                new_profile['table_prefix_ids'] = prefix_string.split()
                # filter_string = raw_input('Enter the key/value pairs to be filtered out'
                #                           ' (leave blank for none): ')
                new_profile['filter_out'] = ''  # filter_string.split()

                profiles['profiles'][profile_name] = new_profile
                j_file.close()

                j_file = open(directory + '/' + "db_profile.json", "w+")
                json.dump(profiles, j_file)
                j_file.close()

                self.load_profile(profile_name, directory)
            else:
                quit(10)

    def establish_connection(self, user=None, passw=None):
        if passw is None:
            print 'Enter password for user: %s on db: %s ...' % (self.user, self.db_name)
            pw = getpass.getpass()
        else:
            pw = passw

        if user is None:
            uname = self.user
        else:
            uname = user

        self.con = psycopg2.connect(dbname=self.db_name, host=self.host,
                                    port=self.port, user=uname, password=str(pw))
        self.con.set_session(autocommit=True)
        self.cur = self.con.cursor()
        print 'Connected to database name ', self.db_name

    def close_connection(self):
        self.cur.close()
        self.con.close()

    def execute_query(self, query, query_params):
        self.cur.execute(query, query_params)

