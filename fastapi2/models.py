from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from  sqlalchemy import ForeignKey, String, Table, Column, func

class Model(DeclarativeBase):
    pass

 # можно тут добавить тогда эти столбцы будут во всех таблицах
   # т.к. мы наследуемся от этого класса
    
    id: Mapped[int] = mapped_column(primary_key=True)
    
    # будет вписывать дататайм при создании записи
    dateCreate: Mapped[datetime] = mapped_column(        
                                        server_default=func.now(),
                                        nullable=False)
    
    # будет вписывать дататайм при обновлении записи
    dateUpdate: Mapped[datetime] = mapped_column(        
                                        server_default=func.now(),
                                        server_onupdate=func.now(),
                                        nullable=False)
    
class UserOrm(Model):
    __tablename__ = 'user'
    
    # уже не нужен так как наследуется
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    age: Mapped[int]
    phone: Mapped[str|None]
    # quiz = relationship('QuizOrm', backref='user')



class UserFilter(Filter):
    name: str | None = None
    name__like: str | None = None
    name__startswith: str | None = None
    phone__in: list[str] | None = None
    
    # # ?order_by=-age,name
    order_by: list[str] = ['age']
    
    class Constants(Filter.Constants):
        model = UserOrm



'''
добавляются к названию поля через два "_"

Сравнительные операторы :
    eq: равно
    neq(или ): не равно not
    gt: больше
    lt: меньше
    gte: больше или равно
    lte: меньше или равно
Операторы для работы с коллекциями :
    in: принадлежит множеству
    not_in: не принадлежит множеству
Операторы для строковых данных :
    like: соответствует шаблону 
    ilike: регистронезависимый поиск по шаблону
    startswith: начинается с
    endswith:кончается на
    contains:содержит подстроку
    not_like: не соответствует шаблону
Специальные операторы :
    isnull: проверка на NULL
    not_isnull:проверка на NOT NULL

'''
