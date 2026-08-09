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
