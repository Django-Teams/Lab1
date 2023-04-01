import tkinter as tk
import tkinter.font as tkFont
from tkinter import messagebox

from migrations import mysql_interface, postgresql_interface, sqlite_interface


class MigrationWindow:
    def __init__(self, root):
        root.title("Migrations")
        width = 810
        height = 580
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        title_text = tk.Label(root)
        ft = tkFont.Font(family='Times', size=26)
        title_text["font"] = ft
        title_text["fg"] = "#333333"
        title_text["justify"] = "center"
        title_text["text"] = "Migrations"
        title_text.place(x=280, y=10, width=277, height=52)

        # MYSQL FORM

        mysql_host_input = tk.Entry(root)
        mysql_host_input["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times', size=10)
        mysql_host_input["font"] = ft
        mysql_host_input["fg"] = "#333333"
        mysql_host_input["justify"] = "center"
        mysql_host_input.insert(0, "Host")
        mysql_host_input.place(x=50, y=100, width=180, height=30)
        self.mysql_host_input = mysql_host_input

        mysql_user_input = tk.Entry(root)
        mysql_user_input["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times', size=10)
        mysql_user_input["font"] = ft
        mysql_user_input["fg"] = "#333333"
        mysql_user_input["justify"] = "center"
        mysql_user_input.insert(0, "User name")
        mysql_user_input.place(x=50, y=140, width=181, height=30)
        self.mysql_user_input = mysql_user_input

        mysql_pass_input = tk.Entry(root)
        mysql_pass_input["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times', size=10)
        mysql_pass_input["font"] = ft
        mysql_pass_input["fg"] = "#333333"
        mysql_pass_input["justify"] = "center"
        mysql_pass_input.insert(0, "Password")
        mysql_pass_input.place(x=50, y=180, width=181, height=30)
        self.mysql_pass_input = mysql_pass_input

        mysql_db_input = tk.Entry(root)
        mysql_db_input["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times', size=10)
        mysql_db_input["font"] = ft
        mysql_db_input["fg"] = "#333333"
        mysql_db_input["justify"] = "center"
        mysql_db_input.insert(0, "Database Name")
        mysql_db_input.place(x=50, y=220, width=181, height=30)
        self.mysql_db_input = mysql_db_input

        text_mysql_title = tk.Label(root)
        ft = tkFont.Font(family='Times', size=14)
        text_mysql_title["font"] = ft
        text_mysql_title["fg"] = "#333333"
        text_mysql_title["justify"] = "center"
        text_mysql_title["text"] = "MYSQL"
        text_mysql_title.place(x=110, y=60, width=70, height=25)

        # POSTGRESQL FORM

        psql_host_input = tk.Entry(root)
        psql_host_input["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times', size=10)
        psql_host_input["font"] = ft
        psql_host_input["fg"] = "#333333"
        psql_host_input["justify"] = "center"
        psql_host_input.insert(0, "Host")
        psql_host_input.place(x=320, y=100, width=180, height=30)
        self.psql_host_input = psql_host_input

        psql_user_input = tk.Entry(root)
        psql_user_input["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times', size=10)
        psql_user_input["font"] = ft
        psql_user_input["fg"] = "#333333"
        psql_user_input["justify"] = "center"
        psql_user_input.insert(0, "User name")
        psql_user_input.place(x=320, y=140, width=181, height=30)
        self.psql_user_input = psql_user_input

        psql_pass_input = tk.Entry(root)
        psql_pass_input["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times', size=10)
        psql_pass_input["font"] = ft
        psql_pass_input["fg"] = "#333333"
        psql_pass_input["justify"] = "center"
        psql_pass_input.insert(0, "Password")
        psql_pass_input.place(x=320, y=180, width=181, height=30)
        self.psql_pass_input = psql_pass_input

        psql_db_input = tk.Entry(root)
        psql_db_input["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times', size=10)
        psql_db_input["font"] = ft
        psql_db_input["fg"] = "#333333"
        psql_db_input["justify"] = "center"
        psql_db_input["text"] = "Entry"
        psql_db_input.insert(0, "Database name")
        psql_db_input.place(x=320, y=220, width=181, height=30)
        self.psql_db_input = psql_db_input

        text_psql_title = tk.Label(root)
        ft = tkFont.Font(family='Times', size=14)
        text_psql_title["font"] = ft
        text_psql_title["fg"] = "#333333"
        text_psql_title["justify"] = "center"
        text_psql_title["text"] = "POSTGRESQL"
        text_psql_title.place(x=320, y=60, width=181, height=25)

        # SQLITE FORM

        sqlite_path_input = tk.Entry(root)
        sqlite_path_input["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times', size=10)
        sqlite_path_input["font"] = ft
        sqlite_path_input["fg"] = "#333333"
        sqlite_path_input["justify"] = "center"
        sqlite_path_input.insert(0, "Path to file")
        sqlite_path_input.place(x=590, y=100, width=180, height=30)
        self.sqlite_path_input = sqlite_path_input

        text_sqlite_title = tk.Label(root)
        ft = tkFont.Font(family='Times', size=14)
        text_sqlite_title["font"] = ft
        text_sqlite_title["fg"] = "#333333"
        text_sqlite_title["justify"] = "center"
        text_sqlite_title["text"] = "SQLITE"
        text_sqlite_title.place(x=590, y=60, width=181, height=25)

        migrate_first_button = tk.Button(root)
        migrate_first_button["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times', size=10)
        migrate_first_button["font"] = ft
        migrate_first_button["fg"] = "#000000"
        migrate_first_button["justify"] = "center"
        migrate_first_button["text"] = "Migrate 1"
        migrate_first_button.place(x=210, y=290, width=143, height=43)
        migrate_first_button["command"] = self.migrate_first_button_command

        migrate_second_button = tk.Button(root)
        migrate_second_button["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times', size=10)
        migrate_second_button["font"] = ft
        migrate_second_button["fg"] = "#000000"
        migrate_second_button["justify"] = "center"
        migrate_second_button["text"] = "Migrate 2"
        migrate_second_button.place(x=470, y=290, width=138, height=43)
        migrate_second_button["command"] = self.migrate_second_button_command

    def migrate_first_button_command(self):
        """
        Process button click to make a migration
        Mysql to postgresql
        :return:
        """
        try:
            # Get mysql credentials
            m_host = self.mysql_host_input.get()
            m_user = self.mysql_user_input.get()
            m_pass = self.mysql_pass_input.get()
            m_db = self.mysql_db_input.get()

            # Get postgresql credentials
            p_host = self.psql_host_input.get()
            p_user = self.psql_user_input.get()
            p_pass = self.psql_pass_input.get()
            p_db = self.psql_db_input.get()

            # Try to make a mysql connection
            try:
                mysql_db = mysql_interface.MySQL(m_host, 3306, m_user, m_pass, m_db)
            except:
                messagebox.showerror("Error", "MySQL connection error")
                return
            # Try to make a postgresql connection
            try:
                pg_db = postgresql_interface.PostgreSQL(p_host, 5432, p_user, p_pass, p_db)
            except:
                messagebox.showerror("Error", "PostgreSQL connection error")
                return

            # Get mysql tables
            mysql_tables = mysql_db.export_tables()
            for table in mysql_tables:
                # Import tables to postgresql
                pg_db.import_tables(table)
                # Import data
                pg_db.import_data(table, mysql_db.export_data(table["name"]))

            # Close connections
            mysql_db.close_conn()
            pg_db.close_conn()
        except Exception as ex:
            messagebox.showerror("Error", str(ex))

    def migrate_second_button_command(self):
        """
        Process button click to make a migration
        Postgresql to sqlite
        :return:
        """
        try:
            # Get postgresql credentials
            p_host = self.psql_host_input.get()
            p_user = self.psql_user_input.get()
            p_pass = self.psql_pass_input.get()
            p_db = self.psql_db_input.get()

            # Get sqlite file path
            s_path = self.sqlite_path_input.get()

            # Try to make a postgresql connection
            try:
                pg_db = postgresql_interface.PostgreSQL(p_host, 5432, p_user, p_pass, p_db)
            except:
                messagebox.showerror("Error", "PostgreSQL connection error")
                return
            # Try to make a sqlite connection
            try:
                sqlite_db = sqlite_interface.SQLite(s_path)
            except:
                messagebox.showerror("Error", "SQLite connection error")
                return

            # Get postgresql tables
            pg_tables = pg_db.export_tables()
            for table in pg_tables:
                # Import tables to sqlite
                sqlite_db.import_tables(table)
                # Import data
                sqlite_db.import_data(table, pg_db.export_data(table["name"]))

            # Close connections
            pg_db.close_conn()
            sqlite_db.close_conn()
        except Exception as ex:
            messagebox.showerror("Error", str(ex))
