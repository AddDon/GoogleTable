from clickhouse_driver import connect

class ClickHouseMgr():
    """Работа с БД ClickHouse"""

    def __init__(self):
        self.__errorMsg = ""
        self.__host = ""
        self.__username = ""
        self.__password = ""
        self.__dbname = ""
        self.__conn = None


    def getLastError(self):
        """Получить текст последней ошибки

            :return: Текст ошибки
        """

        return self.__errorMsg


    def setConnParams(self, host, username, password, dbname):
        """Задать параметры ддя подключения

            :param host: Хост для подключения к БД
            :param username: Логин для подключения к БД
            :param password: Пароль для подключения к БД
            :param dbname: Наименование БД для подключения
        """

        self.__host = str(host)
        self.__username = str(username)
        self.__password = str(password)
        self.__dbname = str(dbname)


    def connect(self):
        """Полюключиться к БД"""

        self.__conn = connect(
            host = self.__host,
            user = self.__username,
            password = self.__password,
            database = self.__dbname
        )

    def execQuery(self, query):
        """Выполнить запрос к БД

            :param query: Текст запроса
        """

        items = []

        try:
            clh_cursor = self.__conn.cursor()
            clh_cursor.execute(query)

            row = clh_cursor.fetchone()
            while row:
                items.append(row)
                row = clh_cursor.fetchone()

            clh_cursor.close()
        except Exception as ex:
            self.__errorMsg = "Ошибка при выполнении запроса [%s]: %s" % (
                query,
                str(ex)
            )

            return False

        return items

    def closeConnection(self):
        if self.__conn is not None:
            self.__conn.close()
