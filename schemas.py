from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, EmailStr




class UserBase(BaseModel):
    username: str = Field(min_length=1, max_length=50)
    email: EmailStr = Field(max_length=120)


class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    image_file: str | None
    image_path: str

class UserUpdate(BaseModel):
    username: str | None = Field(default=None, min_length=1, max_length=50)
    email: EmailStr | None = Field(default=None, max_length=120)
    image_file: str | None = Field(default=None, min_length=1, max_length=200)





#it looks like data classes, but pydantic uses these type hints to validate data at runtime.
class PostBase(BaseModel):
    title: str = Field(default=None, min_length=1, max_length=100)
    content: str = Field(default=None, min_length=1)
# without default values, it means that these fields are mandatory.


class PostCreate(PostBase):
    user_id: int # Temperary

class PostUpdate(PostBase):
    title: str | None = Field(default=None, min_length=1, max_length=100)
    content: str | None = Field(default=None, min_length=1)



#
class PostResponse(PostBase):
    model_config = ConfigDict(from_attributes=True) # pydantic v2 -> imp when we add database
    # right now our posts are dicts. we access data with bracket notation []. when we add a database
    # our data is going to be accessed through "." notation.
    # by default pydantic knows how to read dictionaries
    # the above configuration allows it to read from objects using . notation

    id: int # for database models and api responses, using id is basically the standard convension, this id is scope to the class, won't conflict with the global
    user_id: int
    date_posted: datetime # in memory data, when database it would be datetime
    author: UserResponse