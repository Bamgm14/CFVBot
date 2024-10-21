
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from Cards import *
import random as r
from PIL import Image
import requests 
import io
import numpy as np
import discord

engine = create_engine(r"sqlite:///cards.db")
Base.metadata.create_all(engine)

def pullCards(interaction: discord.Interaction, setid: str, pulls: int = 7):
    #print(c["BT01"])
    #print(interaction.id)
    print(setid)
    setid = setid.upper()
    with Session(engine) as session:
        sets = session.query(CardSetRarity.card).filter(CardSetRarity.set.in_(session.query(Set.id).filter(Set.code == (f"{setid}")))).all()
        cards = session.query(Card, Rarity).filter(Card.id == CardSetRarity.card).filter(Rarity.id == CardSetRarity.rarity).filter(Card.id.in_([x[0] for x in sets])).all()
    if len(cards) == 0:
        return "Set not found"
    #print(cards[0])
    with Session(engine) as session:
        user = session.query(DiscordUser).filter(DiscordUser.discordID == interaction.user.id).all()
        if len(user) == 0:
            user = DiscordUser(discordID = interaction.user.id, name=interaction.user.name)
            session.add(user)
        else:
            user = user[0]
        user = user.discordID
        session.commit()
    lst = [r.choice(cards) for _ in range(pulls)]
    embeds = []
    color = discord.Color.from_rgb(r.randint(0, 255), r.randint(0, 255), r.randint(0, 255))
    names = {}
    for index, a in enumerate(lst):
        names[(a[0].id, a[1].id)] = names.get((a[0].id, a[1].id), 0) + 1 if (a[0].id, a[1].id) in names.keys() else 1
        embed = discord.Embed(title = f"[#{index + 1}] " + a[0].name + f" ({a[1].name})", color = color, url = a[0].url + "#"*(names[(a[0].id, a[1].id)] - 1))
        embed.set_image(url = a[0].image)
        embeds.append(embed)
    return embeds, names, user
    #print(a)

def allCard(interaction: discord.Interaction):
    with Session(engine) as session:
        cards: list[tuple[Card, int, str]] = session.query(Card, CardList.quantity, Rarity.name).filter(Rarity.id == CardList.rarity).filter(Card.id == CardList.cardID).filter(CardList.discordID == interaction.user.id).all()
    color = discord.Color.from_rgb(r.randint(0, 255), r.randint(0, 255), r.randint(0, 255))
    embeds = []
    for card, quantity, rarity in cards:
        embed = discord.Embed(title = f"[ID: {card.id}] " + card.name + f" x{quantity} " + f"({rarity})", color = color, url = card.url)
        embed.set_image(url = card.image)
        embeds.append(embed)
    return embeds

def verifyCard(user: discord.User, cardID: int, rarity: str, quantity: int):
    
    with Session(engine) as session:
        card = session.query(
            CardList.cardID
        ).filter(
            CardList.discordID == user.id
        ).filter(
            CardList.cardID == cardID
        ).filter(
            CardList.rarity == rarity
        ).filter(
            CardList.quantity >= quantity
        ).all()
        print(card)
        if len(card) == 0:
            return False
        else:
            return True
        

def tradingCard(sender: dict, reciever: dict):
    with Session(engine) as session:
        send: CardList = session.query(
            CardList
        ).filter(
            CardList.discordID == sender["User"].id
        ).filter(
            CardList.cardID == sender["cardID"]
        ).filter(
            CardList.rarity == sender["rarity"]
        ).first()
        send.quantity -= sender["quantity"]
        recv: CardList = session.query(
            CardList
        ).filter(
            CardList.discordID == reciever["User"].id
        ).filter(
            CardList.cardID == reciever["cardID"]
        ).filter(
            CardList.rarity == reciever["rarity"]
        ).first()
        recv.quantity -= reciever["quantity"]
        card: list[CardList] = session.query(CardList).filter(CardList.discordID == sender["User"].id).filter(CardList.cardID == reciever["cardID"]).filter(CardList.rarity == reciever["rarity"]).all()
        if len(card) == 0:
            card = CardList(discordID = sender["User"].id, cardID = reciever["cardID"], rarity = reciever["rarity"], quantity = reciever["quantity"])
            session.add(card)
        else:
            card[0].quantity += reciever["quantity"]
        card = session.query(CardList).filter(CardList.discordID == reciever["User"].id).filter(CardList.cardID == sender["cardID"]).filter(CardList.rarity == sender["rarity"]).all()
        if len(card) == 0:
            card = CardList(discordID = reciever["User"].id, cardID = sender["cardID"], rarity = sender["rarity"], quantity = sender["quantity"])
            session.add(card)
        else:
            card[0].quantity += sender["quantity"]
        session.commit()
    return True