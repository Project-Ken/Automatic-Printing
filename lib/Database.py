class Info:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

class Base:
    def __init__(self, info:Info):
        self.info = info
        self.connection = None

    def __new__(cls, *args, **kwargs):
        if cls is Base:
            raise TypeError('Base Class Cannot be Instantiated Directly')
        return super().__new__(cls)

    def Connect(self):
        raise NotImplementedError('Base Class Function [ Connect ] Not For Use')

    def Disconnect(self):
        if self.connection:
            self.connection.close()
            self.connection = None
            print(' - Database Disconnected')

    def Rollback(self):
        if self.connection:
            self.connection.rollback()

    def Commit(self):
        if self.connection:
            self.connection.commit()

    def Execute(self, sql:str, *args):
        connection = self.Connect()
        cursor = None
        try:
            cursor = connection.cursor()
            cursor.execute(sql, args)

            return cursor.fetchall()
        except Exception as e:
            print(f'SQL: {sql}\n - SQL Error\n{str(e)}')
            self.Rollback()
            return None
        finally:
            if cursor:
                cursor.close()

    def ExecuteCommit(self, sql:str, *args):
        connection = self.Connect()
        cursor = None
        try:
            cursor = connection.cursor()
            cursor.execute(sql, args)
            self.Commit()
        except Exception as e:
            print(f'SQL: {sql}\n- SQL Error\n{str(e)}')
            self.Rollback()
        finally:
            if cursor:
                cursor.close()





from . import MySQL_Connector

class MySQL_Database(Base):
    def __new__(cls, info:Info):
        missing = [key for key in ['host', 'port', 'database', 'user', 'password'] if not hasattr(info, key)]
        if missing:
            raise ValueError(f"Missing Required Info: {', '.join(missing)}")
        return super().__new__(cls)

    def __init__(self, info:Info):
        super().__init__(info)

    def Connect(self):
        if not self.connection:
            try:
                self.connection = MySQL_Connector.connect(
                    host = self.info.host,
                    port = self.info.port,
                    database = self.info.database,
                    user = self.info.user,
                    password = self.info.password
                )
                print(f' - Database [ {self.info.database}@{self.info.host}:{self.info.port} ] Connected Successful')
            except MySQL_Connector.Error as e:
                print(f' - Database [ {self.info.database}@{self.info.host}:{self.info.port} ] Connection Error\n{e}')
        return self.connection



from . import OracleSQL

class Oracle_Database(Base):
    def __new__(cls, info:Info):
        missing = [key for key in ['host', 'port', 'service', 'user', 'password'] if not hasattr(info, key)]
        if missing:
            raise ValueError(f"Missing Required Info: {', '.join(missing)}")
        return super().__new__(cls)

    def __init__(self, info:Info):
        super().__init__(info)

    def Connect(self):
        if not self.connection:
            try:
                self.connection = OracleSQL.connect(
                    user = self.info.user,
                    password = self.info.password,
                    dsn = OracleSQL.makedsn(
                        self.info.host,
                        self.info.port,
                        service_name = self.info.service
                    )
                )
                print(f' - Database [ {self.info.service}@{self.info.host}:{self.info.port} ] Connected Successful')
            except OracleSQL.DatabaseError as e:
                print(f' - Database [ {self.info.service}@{self.info.host}:{self.info.port} ] Connection Error\n{e}')
        return self.connection

    def Procedure(self, name:str, *args):
        connection = self.Connect()
        cursor = None
        try:
            cursor = connection.cursor()
            cursor.callproc(name, args)
            print(f" - Procedure [ {name} ] Called Successfully")
        except OracleSQL.DatabaseError as e:
            error, = e.args
            print(f" - Procedure [ {name} ] Error ({error.code})\n{error.message}")
        finally:
            if cursor:
                cursor.close()



from . import PostgreSQL

class PostgreSQL_Database(Base):
    def __new__(cls, info:Info):
        missing = [key for key in ['host', 'port', 'database', 'user', 'password'] if not hasattr(info, key)]
        if missing:
            raise ValueError(f"Missing Required Info: {', '.join(missing)}")
        return super().__new__(cls)

    def __init__(self, info:Info):
        super().__init__(info)

    def Connect(self):
        if not self.connection:
            try:
                self.connection = PostgreSQL.connect(
                    host = self.info.host,
                    port = self.info.port,
                    database = self.info.database,
                    user = self.info.user,
                    password = self.info.password
                )
                print(f" Database [ {self.info.database}@{self.info.host}:{self.info.port} ] Connected Successful")
            except PostgreSQL.Error as e:
                print(f" - Database [ {self.info.database}@{self.info.host}:{self.info.port} ] Connection Error\n{e}")
        return self.connection
