from sqlmodel import Field, Relationship, SQLModel


class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str | None
    is_active: bool = Field(default=True)
    items: list["Item"] = Relationship(back_populates="owner")


class UserRead(UserBase):
    id: int
    is_active: bool
    items: list["Item"]


class UserCreate(UserBase):
    password: str


class ItemBase(SQLModel):
    title: str = Field(index=True)
    description: str = Field(index=True)
    owner_id: int | None = Field(default=None, foreign_key="user.id")


class Item(ItemBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    owner: User | None = Relationship(back_populates="items")


class ItemCreate(ItemBase):
    pass


UserRead.update_forward_refs()
