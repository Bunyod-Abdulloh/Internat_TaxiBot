from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config


class Database:

    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME
        )

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False
                      ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    async def create_table_drivers(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Drivers (
        id SERIAL PRIMARY KEY,
        full_name VARCHAR(255) NOT NULL,
        birth_date TEXT NULL,
        phone_number TEXT NULL,
        passport_one TEXT NULL,
        passport_two TEXT NULL,
        driver_photo TEXT NULL,
        car_photo TEXT NULL,
        car_number TEXT NULL,        
        telegram_id BIGINT NOT NULL UNIQUE 
        );
        """
        await self.execute(sql, execute=True)

    async def add_drivers(self, full_name, birth_date, phone_number, passport_one, passport_two, driver_photo,
                          car_photo,
                          car_number, telegram_id):
        sql = "INSERT INTO Drivers (full_name, birth_date, phone_number, passport_one, passport_two, driver_photo, " \
              "car_photo, car_number, telegram_id) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9) returning*"
        return await self.execute(sql, full_name, birth_date, phone_number, passport_one, passport_two, driver_photo,
                                  car_photo, car_number, telegram_id, fetchrow=True)

    async def select_all_drivers(self):
        sql = "SELECT * FROM Drivers"
        return await self.execute(sql, fetch=True)

    async def select_driver(self, telegram_id):
        sql = "SELECT * FROM Drivers WHERE telegram_id=$1"
        return await self.execute(sql, telegram_id, fetchrow=True)

    async def count_drivers(self):
        sql = "SELECT COUNT(*) FROM Drivers"
        return await self.execute(sql, fetchval=True)

    async def delete_drivers(self, telegram_id):
        await self.execute("DELETE FROM Drivers WHERE telegram_id=$1", telegram_id, execute=True)

    async def create_table_pupils(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Pupils (
        id SERIAL PRIMARY KEY,
        class_number TEXT NOT NULL,
        full_name TEXT NOT NULL,
        birth_date TEXT NULL,
        pupil_photo TEXT NULL,        
        phone_number_of_parents TEXT NULL,
        phone_number_of_teacher TEXT NULL,
        home_latitude FLOAT8 NULL,
        home_longitude FLOAT8 NULL,
        work_latitude FLOAT8 NULL,
        work_longitude FLOAT8 NULL,
        other_latitude FLOAT8 NULL,
        other_longitude FLOAT8 NULL,
        telegram_id BIGINT NOT NULL UNIQUE 
        );
        """
        await self.execute(sql, execute=True)

    async def add_pupil(self, class_number, full_name, birth_date, pupil_photo, phone_number_of_parents,
                        phone_number_of_teacher, home_latitude, home_longitude, telegram_id):
        sql = ("INSERT INTO Pupils (class_number, full_name, birth_date, pupil_photo, phone_number_of_parents, "
               "phone_number_of_teacher, home_latitude, home_longitude, telegram_id) VALUES ($1, $2, $3, $4, $5, $6, "
               "$7, $8, $9) returning *")
        return await self.execute(sql, class_number, full_name, birth_date, pupil_photo, phone_number_of_parents,
                                  phone_number_of_teacher, home_latitude, home_longitude, telegram_id, fetchrow=True)

    async def select_classes(self, class_number):
        sql = "SELECT * FROM Pupils WHERE class_number=$1"
        return await self.execute(sql, class_number, fetchrow=True)

    async def select_pupil(self, telegram_id):
        sql = "SELECT * FROM Pupils WHERE telegram_id=$1"
        return await self.execute(sql, telegram_id, fetchrow=True)

    async def count_pupils(self):
        sql = "SELECT COUNT(*) FROM Pupils"
        return await self.execute(sql, fetchval=True)

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
        id SERIAL PRIMARY KEY,
        full_name VARCHAR(255) NOT NULL,
        username varchar(255) NULL,
        telegram_id BIGINT NOT NULL UNIQUE 
        );
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())

    async def add_user(self, full_name, username, telegram_id):
        sql = "INSERT INTO users (full_name, username, telegram_id) VALUES($1, $2, $3) returning *"
        return await self.execute(sql, full_name, username, telegram_id, fetchrow=True)

    async def select_all_users(self):
        sql = "SELECT * FROM Users"
        return await self.execute(sql, fetch=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM Users"
        return await self.execute(sql, fetchval=True)

    async def update_user_username(self, username, telegram_id):
        sql = "UPDATE Users SET username=$1 WHERE telegram_id=$2"
        return await self.execute(sql, username, telegram_id, execute=True)

    async def delete_users(self):
        await self.execute("DELETE FROM Users WHERE TRUE", execute=True)

    async def drop_users(self):
        await self.execute("DROP TABLE Users", execute=True)
