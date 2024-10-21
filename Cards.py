from typing import Any, Union
from sqlalchemy import Integer, Unicode, UnicodeText, String, URL, ForeignKey
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, declarative_base

Base = declarative_base()

class Clan(Base):
    __tablename__ = 'clans'
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    name = mapped_column(Unicode(100), nullable=False)
    def __init__(self, name: str, id = None):
        self.name = name
        if id is not None:
            self.id = id
    def __repr__(self):
        return f"<Clan(name={self.name})>"

class CardClan(Base):
    __tablename__ = 'card_clan'
    card = mapped_column(Integer, ForeignKey('cards.id'), primary_key=True)
    clan = mapped_column(Integer, ForeignKey('clans.id'), primary_key=True)
    def __init__(self, card: int, clan: int):
        self.card = card
        self.clan = clan
    def __repr__(self):
        return f"<CardClan(card={self.card}, clan={self.clan})>"

class Race(Base):
    __tablename__ = 'races'
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    name = mapped_column(Unicode(100), nullable=False)
    def __init__(self, name: str, id = None):
        self.name = name
        if id is not None:
            self.id = id
    def __repr__(self):
        return f"<Race(name={self.name})>"

class CardRace(Base):
    __tablename__ = 'card_race'
    card = mapped_column(Integer, ForeignKey('cards.id'), primary_key=True)
    race = mapped_column(Integer, ForeignKey('races.id'), primary_key=True)
    def __init__(self, card: int, race: int):
        self.card = card
        self.race = race
    def __repr__(self):
        return f"<CardRace(card={self.card}, race={self.race})>"

class Nation(Base):
    __tablename__ = 'nations'
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    name = mapped_column(Unicode(100), nullable=False)
    def __init__(self, name: str, id = None):
        self.name = name
        if id is not None:
            self.id = id
    def __repr__(self):
        return f"<Nation(name={self.name})>"

class CardNation(Base):
    __tablename__ = 'card_nation'
    card = mapped_column(Integer, ForeignKey('cards.id'), primary_key=True)
    nation = mapped_column(Integer, ForeignKey('nations.id'), primary_key=True)
    def __init__(self, card: int, nation: int):
        self.card = card
        self.nation = nation
    def __repr__(self):
        return f"<CardNation(card={self.card}, nation={self.nation})>"

class Type(Base):
    __tablename__ = 'types'
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    name = mapped_column(Unicode(100), nullable=False)
    def __init__(self, name: str, id = None):
        self.name = name
        if id is not None:
            self.id = id
    def __repr__(self):
        return f"<Type(name={self.name})>"
    

class Set(Base):
    __tablename__ = 'sets'
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    code = mapped_column(Unicode(100), nullable=False)
    name = mapped_column(Unicode(100), nullable=True)
    def __init__(self, code: str, name: str = None, id = None):
        self.code = code
        if name is not None:
            self.name = name
        if id is not None:
            self.id = id
    def __repr__(self):
        return f"<Set(name={self.name}, code={self.code})>"
    
class Rarity(Base):
    __tablename__ = 'rarities'
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    name = mapped_column(Unicode(100), nullable=False)
    def __init__(self, name: str, id = None):
        self.name = name
        if id is not None:
            self.id = id
    def __repr__(self):
        return f"<Rarity(name={self.name})>"
    
class CardSetRarity(Base):
    __tablename__ = 'card_set_rarity'
    card = mapped_column(Integer, ForeignKey('cards.id'), primary_key=True)
    set = mapped_column(Integer, ForeignKey('sets.id'), primary_key=True)
    rarity = mapped_column(Integer, ForeignKey('rarities.id'), primary_key=True)
    def __init__(self, card: int, set: int, rarity: int):
        self.card = card
        self.set = set
        self.rarity = rarity
    def __repr__(self):
        return f"<CardSetRarity(card={self.card}, set={self.set}, rarity={self.rarity})>"
    
    
class Trigger(Base):
    __tablename__ = 'triggers'
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    name = mapped_column(Unicode(100), nullable=False)
    power = mapped_column(Integer, nullable=False)
    def __init__(self, name: str, power: int, id = None):
        self.name = name
        self.power = power
        if id is not None:
            self.id = id
    def __repr__(self):
        return f"<Trigger(name={self.name}, power={self.power})>"
            

class Card(Base):
    __tablename__ = 'cards'
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    name = mapped_column(Unicode(100), nullable=False)
    url = mapped_column(Unicode, nullable=False)
    image = mapped_column(Unicode, nullable=True)
    skills = mapped_column(UnicodeText, nullable=True)
    grade = mapped_column(Integer, nullable=False)
    ability = mapped_column(UnicodeText, nullable=True)
    power = mapped_column(Unicode, nullable=False)
    shield = mapped_column(Unicode, nullable=False)
    critical = mapped_column(Integer, nullable=False)
    type = mapped_column(Integer, ForeignKey('types.id'), nullable=False)
    trigger = mapped_column(Integer, ForeignKey('triggers.id'), nullable=True)
    format = mapped_column(Unicode(100), nullable=True)
    icon = mapped_column(Unicode, nullable=True)
    
    def __init__(self, name: str, url: str, image: str, skills: str, grade: int, ability: str, power: int, shield: int, critical: int, type: int, trigger: int, format: str, icon: str, id = None):
        self.name = name
        self.url = url
        self.image = image
        self.skills = skills
        self.grade = grade
        self.ability = ability
        self.power = power
        self.shield = shield
        self.critical = critical
        self.type = type
        self.trigger = trigger
        self.format = format
        self.icon = icon
        if id is not None:
            self.id = id
    def __repr__(self):
        return f"<Card(name={self.name}, url={self.url}, image={self.image}, grade={self.grade}, ability={self.ability}, power={self.power}, shield={self.shield}, critical={self.critical}, type={self.type}, trigger={self.trigger}, format={self.format}, icon={self.icon})>"

class DiscordUser(Base):
    __tablename__ = 'discord_users'
    discordID = mapped_column(Integer, primary_key=True)
    name = mapped_column(Unicode(100), nullable=False)
    def __init__(self, name: str, discordID: int):
        self.name = name
        self.discordID = discordID
    def __repr__(self):
        return f"<DiscordUser(name={self.name}, discordID={self.discordID})>"

class CardList(Base):
    __tablename__ = 'card_lists'
    discordID = mapped_column(Integer, ForeignKey('discord_users.discordID'), primary_key=True)
    cardID = mapped_column(Integer, ForeignKey('cards.id'), primary_key=True)
    quantity = mapped_column(Integer, nullable=False)
    rarity = mapped_column(Integer, ForeignKey('rarities.id'), primary_key=True)
    def __init__(self, discordID: int, cardID: int, rarity: int, quantity: int = 1):
        self.discordID = discordID
        self.cardID = cardID
        self.quantity = quantity
        self.rarity = rarity
    def __repr__(self):
        return f"<CardList(discordID={self.discordID}, cardID={self.cardID}, rarity={self.rarity}, quantity={self.quantity})>"
    