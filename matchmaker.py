"""A matchmaking service for GZM.

Uses an airtable list of interested people to create matches at random.
"""
import random
import os
from typing import List, Literal, TypedDict

import airtable
import discord

TOKEN = os.getenv("DISCORD_TOKEN")
AIRTABLE_BASE = os.getenv("AIRTABLE_BASE")
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")

client = discord.Client()
airtable = airtable.Airtable(AIRTABLE_BASE, "dumble", AIRTABLE_API_KEY)

copy = {
    "intro": "Welcome to Dumble! Are you open to matching in a romantic or friendly manner today?",
    "friendly": "😃",  # smiley face emoji
    "romantic": "💕",  # two hearts emoji
    "either": "😊",  # blushing emoji
}

romanticPool = set()  # {discord.User}, remove user when matched
friendlyPool = set()

UserFields = TypedDict(
    "UserFields",
    {
        "Email": str,
        "Twitter": str,
        "Name": str,
        "Phone": str,
        "Discord": str,
        "I am a": Literal["Man", "Woman", "Other"],
        "Looking for": List,
    },
)


class User(TypedDict):
    id: str
    fields: UserFields
    createdTime: str


class DiscordUserNotFound(Exception):
    pass


def list_available_users() -> List[User]:
    """List the available users in our airtable DB.

    Todo:
        - Only get the fields that I need:
    https://airtable-python-wrapper.readthedocs.io/en/master/params.html

    """
    return airtable.get_all(formula="AND(NOT({Email}=''), NOT({Looking for}=''))")


def find_match(user: User) -> User:
    """Find a match for a given user."""

    all_users = list_available_users()
    looking_for = user["fields"]["Looking for"]  # ['Man', 'Woman', ...]

    potential_matches = [
        user for user in all_users if user["fields"]["I am a:"] in looking_for
    ]

    return random.choice(potential_matches)


def find_match_by_discord_id(discord_id: str) -> (User, User):
    """Find match by discord id, so we can build a discord bot that matches people.

    discord_id should be of the form: "JaneDoe#1234"
    """
    users = airtable.search("Discord", discord_id)

    if len(users) == 0:
        raise DiscordUserNotFound("Could not find any users with that id.")
    user = users[0]  # if multiple users are returned, just grab the first one ¯\_(ツ)_/¯
    match = find_match(user)

    return user, match


# link to database: https://airtable.com/tbl6wkasPz9DHFdbp/viwMq7Xv2hRIzuZlb?blocks=hide


@client.event
async def on_ready():
    """on_ready is called when the discord bot first loads."""
    print(f"{client.user} has connected to Discord!")


async def addReactions(msg: discord.Message, emojis: List):
    for emoji in emojis:
        await msg.add_reaction(emoji)


async def userInterface(user: discord.Member, channel):
    introMsg = None
    try:
        introMsg = await user.send(copy["intro"])
    except discord.Forbidden:
        await channel.send(
            user.display_name
            + " please allow DM's from this bot and retype '!dumble' in order to proceed!"
        )
        return

    emojis = [copy["romantic"], copy["friendly"]]
    await addReactions(introMsg, emojis)


@client.event
async def on_reaction_add(reaction: discord.Reaction, user: discord.User):
    # Romantic Or Friendly
    if (
        user != client.user
        and reaction.message.author == client.user
        and reaction.message.content == copy["intro"]
    ):
        print("Reaction added to bot DM!", str(reaction))
        if str(reaction) == copy["romantic"]:
            romanticPool.add(user)
            print(romanticPool)
        elif str(reaction) == copy["friendly"]:
            friendlyPool.add(user)
            print(friendlyPool)
    # Match Or Don't Match
    elif ():
        pass

    # Base Case
    else:
        return


def getUserData(discord_id: str):
    """
    Find user in airtable else return None
    """
    users = airtable.search("Discord", discord_id)

    if len(users) == 0:
        return None
    return users[0]  # if multiple users are returned, just grab the first one ¯\_(ツ)_/¯


@client.event
async def on_message(msg: discord.Message):
    if msg.content.strip() == "!dumble":
        # get discord user from message
        author = msg.author
        print(author)

        user = getUserData(str(author))
        if user == None:
            await msg.channel.send(
                "Oh no! "
                + author.display_name
                + " isn't signed up for Dumble. "
                + "Sign up here: https://airtable.com/shrVpwd24p1353Ukk"
            )
        else:
            await msg.channel.send(
                author.display_name
                + " has joined the Dumble matchmaking pool! @"
                + author.display_name
                + " Please check your DM's from this bot to proceed!"
            )
            await userInterface(author, msg.channel)
        return

    elif msg.content.startswith("!dumble"):
        await msg.channel.send(
            "Sorry, I didn't get that. I don't have a help command either, so "
            + "go pester Eric or Andrew to build one."
        )
        return


client.run(TOKEN)
