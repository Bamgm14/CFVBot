import discord
from discord import app_commands, Member

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from Cards import *
import random as r
from PIL import Image
import requests 
import io
import numpy as np
from CardfightFunctions import *
token = ""
engine = create_engine(r"sqlite:///cards.db")
Base.metadata.create_all(engine)

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

class pullMenu(discord.ui.View):
    def __init__(self, interaction: discord.Interaction, pulls: int, setid: str):
        super().__init__()
        self.index = 0
        self.pulls = pulls
        self.setid = setid
        self.embeds, self.names, self.user = pullCards(interaction, setid, pulls)
        #print(self.embeds)
    
    @discord.ui.button(label="Previous", style=discord.ButtonStyle.primary, disabled=True)
    async def previous(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.index -= 1
        for child in self.children:
            if isinstance(child, discord.ui.Button) and child.label == "Next":
                print(child.disabled)
                child.disabled = False
        if self.index == 0:
            button.disabled = True
        else:
            button.disabled = False
        print(button.disabled)
        await interaction.response.edit_message(embed=self.embeds[self.index], view=self)
    
    @discord.ui.button(label="Next", style=discord.ButtonStyle.primary)
    async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.index += 1
        for child in self.children:
            if isinstance(child, discord.ui.Button) and child.label == "Previous":
                print(child.disabled)
                child.disabled = False
        if self.index == len(self.embeds) - 1:
            button.disabled = True
        else:
            button.disabled = False
        print(button.disabled)
        #print(self.embeds[self.index].to_dict())    
        await interaction.response.edit_message(embed=self.embeds[self.index], view=self)
    
    @discord.ui.button(label="Add Cards to List (Exit)", style=discord.ButtonStyle.red)
    async def exit(self, interaction: discord.Interaction, button: discord.ui.Button):
        with Session(engine) as session:
            for cardID, rarity in self.names.keys():
                usercard = session.query(CardList).filter(CardList.discordID == self.user).filter(CardList.cardID == cardID).filter(CardList.rarity == rarity).all()
                if len(usercard) == 0:
                    usercard = CardList(discordID = self.user, cardID = cardID, rarity = rarity, quantity = self.names[(cardID, rarity)])
                    session.add(usercard)
                else:
                    usercard: CardList = usercard[0]
                    usercard.quantity += self.names[(cardID, rarity)]
                session.flush()
            session.commit()
        await interaction.response.edit_message(content="Cards Added", embed=None, view=None, delete_after=5)
        self.stop()
    
class allCardsMenu(discord.ui.View):
    def __init__(self, interaction: discord.Interaction):
        super().__init__()
        self.index = 0
        self.embeds = allCard(interaction)
        
    
    @discord.ui.button(label="Previous", style=discord.ButtonStyle.primary, disabled=True)
    async def previous(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.index -= 1
        for child in self.children:
            if isinstance(child, discord.ui.Button) and child.label == "Next":
                print(child.disabled)
                child.disabled = False
        if self.index == 0:
            button.disabled = True
        else:
            button.disabled = False
        print(button.disabled)
        await interaction.response.edit_message(embed=self.embeds[self.index], view=self)
    
    @discord.ui.button(label="Next", style=discord.ButtonStyle.primary)
    async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.index += 1
        for child in self.children:
            if isinstance(child, discord.ui.Button) and child.label == "Previous":
                print(child.disabled)
                child.disabled = False
        if self.index == len(self.embeds) - 1:
            button.disabled = True
        else:
            button.disabled = False
        print(button.disabled)
        #print(self.embeds[self.index].to_dict())    
        await interaction.response.edit_message(embed=self.embeds[self.index], view=self)
    
    @discord.ui.button(label="Exit", style=discord.ButtonStyle.red)
    async def exit(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content="Exiting", embed=None, view=None, delete_after=5)
        self.stop()

class tradeCard(discord.ui.View):
    def __init__(self, interaction: discord.Interaction, user: discord.User,
                 recvCardID: int, recvRarity: str, recvQuantity: int, 
                 sendCardID: int, sendRarity: str, sendQuantity: int):
        super().__init__()
        self.sender = {"User": interaction.user, "cardID": sendCardID, "rarity": sendRarity, "quantity": sendQuantity}
        self.recvier = {"User": user, "cardID": recvCardID, "rarity": recvRarity, "quantity": recvQuantity}
    
    @discord.ui.button(label="Accept", style=discord.ButtonStyle.primary)
    async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id == self.recvier["User"].id:
            if tradingCard(self.sender, self.recvier):
                await interaction.response.edit_message(content="Trade Completed", view=None, delete_after=5)
        else:
            pass
    
    @discord.ui.button(label="Decline", style=discord.ButtonStyle.danger)
    async def decline(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id == self.recvier["User"].id:
            await interaction.response.edit_message(content="Trade Declined", view=None, delete_after=5)
        else:
            pass
    

@tree.command(
    name="pullcards",
    description="Full Random Cards"
)

async def pullcards(interaction: discord.Interaction, setid: str, pulls: int = 7):
    view = pullMenu(interaction, pulls, setid)
    await interaction.response.send_message(embed = view.embeds[0], view=view, delete_after=1800)

@tree.command(
    name="tradecards",
    description="Trade Cards",
    guild=discord.Object(id=1205815943247175712)
)

async def trade(interaction: discord.Interaction, user: Member, 
                recvcardid: int, recvquantity: int, recvrarity: str,
                sendcardid: int, sendquantity: int, sendrarity: str):
    print(user, interaction.user)
    recvCardID, recvRarity, recvQuantity = recvcardid, recvrarity, recvquantity
    print(recvCardID, recvRarity, recvQuantity)
    sendCardID, sendRarity, sendQuantity = sendcardid, sendrarity, sendquantity
    print(sendCardID, sendRarity, sendQuantity)
    if not (verifyCard(interaction.user, recvCardID, recvRarity, recvQuantity) and verifyCard(user, sendCardID, sendRarity, sendQuantity)):
        await interaction.response.send_message(content="Invalid Trade", delete_after=5)
        return None
    view = tradeCard(interaction, user, recvCardID, recvRarity, recvQuantity, sendCardID, sendRarity, sendQuantity)
    await interaction.response.send_message(content=f"Trade Request Sent to {user.mention}", view=view, delete_after=1800)


@tree.command(
    name="findcard",
    description="Find a Card"
)

async def findCard(interaction: discord.Interaction, cardname: str, setid: str = None):
    with Session(engine) as session:
        card = session.query(Card).filter(Card.name.like(f"{cardname}"))
        #print([x for x in card.all()])
        if setid is not None:
            setcard = session.query(CardSetRarity).filter(CardSetRarity.card.in_([x.id for x in card])).filter(CardSetRarity.set.in_(session.query(Set.id).filter(Set.code.like(f"{setid.upper()}")))).all()
            card = card.filter(Card.id.in_([x.card for x in setcard]))
        if card.count() == 0:
            await interaction.response.send_message("Card not found", ephemeral=True)
            return None
        
        embeds = [discord.Embed(title = a.name, color = discord.Color.from_rgb(r.randint(0, 256), r.randint(0, 256), r.randint(0, 256)), url = a.url) for a in card]
        for embed, choice in zip(embeds, card):
            embed.set_image(url = choice.image)
        #print([x.to_dict() for x in embeds])
        if len(embeds) > 10:
            await interaction.response.send_message("Too many results", ephemeral=True)
        else:
            await interaction.response.send_message(content="Multiple Found" if card.count() > 1 else None, embeds=embeds, ephemeral=True)


@tree.command(
    name="allcards",
    description="Full Random Cards"
)

async def allcards(interaction: discord.Interaction):
    view = allCardsMenu(interaction)
    await interaction.response.send_message(embed = view.embeds[0], view=view, ephemeral=True, delete_after=1800)
    

@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=1205815943247175712))
    print("Ready!")



client.run(token)