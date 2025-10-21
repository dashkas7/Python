from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy import select, text

from models import UserOrm, Model
from shemas import *

import os

BASE_DIR = os.path.dirname(__file__)
DB_DIR = os.path.join(BASE_DIR, 'db')

if not os.path.exists(DB_DIR):
    os.makedirs(DB_DIR)
    
DB_PATH = os.path.join(DB_DIR, 'fastapi.db')    

engine = create_async_engine(f"sqlite+aiosqlite:///{DB_PATH}")
new_session = async_sessionmaker(engine, expire_on_commit=False)








# class UserRepository:
#     @classmethod
#     async def add_user(cls, user:UserAdd) -> int:
#         data = user.model_dump() # в словарь 
#         print(data)
#         user = UserOrm(**data) #+пользователь  
#         session.add(user)
#         await session.flush()
#         await session.commit()
#         return user.id 

#     @classmethod
#     async def get_users(cls) -> list[UserOrm]:
#         async with new_session() as session:
#             query = select(UserOrm)
#             # query = text("SQL")
#             res = await session/execute(query)
#             users = res.scalars().all() 
#             return users
    
#     @classmethod
#     async def get_user(cls) -> UserOrm: #list[UserOrm]:
#         async with new_session() as session:
#             query = select(UserOrm)
#             # query = text("SQL")
#             res = await session/execute(query)
#             user = res.scalars().first() #all()
#             return user

class  DataRepository:
    @classmethod
    async def create_table(cls):
        async with engine.begin() as conn:
            await conn.run_sync(Model.metadata.create_all)
    
    @classmethod            
    async def delete_table(cls):
        async with engine.begin() as conn:
            await conn.run_sync(Model.metadata.drop_all)     

    @classmethod
    async def add_test_data(cls):
        async with new_session() as session:
            users = [
                UserOrm(name='user1', age=20),
                UserOrm(name='user2', age=30, phone='123456789'),
                UserOrm(name='user3', age=41, phone='11'),
                UserOrm(name='user4', age=42, phone='22'),
                UserOrm(name='user5', age=43, phone='33'),
                UserOrm(name='user6', age=44),
                UserOrm(name='user7', age=45)
            ]
            
            
            session.add_all(users)            
            
            # flush() - используется для синхронизации изменений с базой данных без завершения транзакции
            # проверяет, что операции (вставка, обновление) не вызывают ошибок
            # Если последующие действия в транзакции зависят от предыдущих изменений, 
            # flush() делает эти изменения видимыми в рамках текущей сессии
            await session.flush() 
            await session.commit()



class UserRepository:
        
    @classmethod
    async def add_user(cls, user: UserAdd) -> int:
        async with new_session() as session:
            data = user.model_dump() # в словарь
            # print(data)
            user = UserOrm(**data) #
            session.add(user)
            await session.flush()
            await session.commit()
            return user.id
    
    @classmethod        
    async def get_users(cls, limit, offset, user_filter) -> list[UserOrm]:
        async with new_session() as session:
            
            # select() - это новый стиль SQLAlchemy 2.0, который рекомендуется использовать.
            # при этом полная асинхронная поддержка: session.execute(select(...)) работает асинхронно.
            # query = select(UserOrm).limit(limit).offset(offset)
            # query = select(UserOrm)
            # print(query)
            
            query = select(UserOrm)
            query = user_filter.filter(query).limit(limit).offset(offset)
            query = user_filter.sort(query)
            
            res = await session.execute(query)
            users = res.scalars().all() # -> список
            return users
        
    @classmethod
    async def get_user(cls, id) -> UserOrm:
        async with new_session() as session:
            query = select(UserOrm).where(UserOrm.id==id)
            # query = text("SQL")            
            res = await session.execute(query)
            user = res.scalars().first()
            return user



# # CRUD 
# # С
# #     user = User(**user_data)
# #     session.add(user)
# #     # для bulk(множественных) операций
# #     stmt = insert(User).values(**user_data).returning(User.id)

# # R
# #     stmt = select(User)
# #     stmt = select(User).where(User.id == user_id)
# #     stmt = select(User).where(
# #             User.is_active == True,
# #             User.created_at >= datetime.now() - timedelta(days=30)
# #         )
# #     stmt = select(User).order_by(User.created_at.desc())        
# #     stmt = select(User).offset((page-1)*size).limit(size)
# #     stmt = select(User.name)
# #     stmt = select(User, Post).join(Post, User.id == Post.user_id)
# #     stmt = select(func.count(User.id))
# #     stmt = select(func.avg(User.age))
    
    
# #     # фильтрация
# #     # filter - старый стиль
# #     users = session.query(User).filter(User.name == 'John').filter(User.age > 25).all()    
# #     # where - новый стиль - предпочтительней
# #     stmt = select(User).where(User.name == 'John', User.age > 25)
    
# # U
# #     stmt = update(User).where(User.id == user_id).values(**update_data)  
# # D      
# #     stmt = delete(User).where(User.id == user_id)
            
    



# # .scalars().all() - список объектов
# # .scalar_one_or_none() - один объект или None
# # .scalar() - одно значение
# # .first() - первая запись
# # .one() - ровно одна запись (иначе исключение)
# # .all() - все записи как кортежи        