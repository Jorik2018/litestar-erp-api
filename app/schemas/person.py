from dataclasses import dataclass

@dataclass
class Person:
    id: int
    name: str
    age: int

@dataclass
class PersonCreate:
    id: int
    name: str
    age: int

@dataclass
class PersonUpdate:
    name: str | None = None
    age: int | None = None
