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
    return airtable.get_all(formula="NOT({Email}='')")


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


@client.event
async def on_message(msg: discord.Message):
    if msg.content == "!dumble":
        # get discord user from message
        author = msg.author
        print(author)
        discord_id = "{}#{}".format(author.name, author.discriminator)
        print(discord_id)
        try:
            user, match = find_match_by_discord_id(discord_id)
        except DiscordUserNotFound:
            await msg.channel.send(
                "That person isn't signed up for the matchmaking service. "
                "Sign up here: https://airtable.com/tbl8bNs3vfb5gMm5V"
            )
            return

        # format message
        response = "Congrats! {} and {} just matched.".format(
            user["fields"]["Name"],
            match["fields"]["Name"],
        )

        await msg.channel.send(response)

    elif msg.content.startswith("!dumble") and len(msg.mentions) == 1:
        matchee = msg.mentions[0]
        discord_id = "{}#{}".format(matchee.name, matchee.discriminator)
        try:
            user, match = find_match_by_discord_id(discord_id)
        except DiscordUserNotFound:
            await msg.channel.send(
                "That person isn't signed up for the matchmaking service. "
                "Sign up here: https://airtable.com/shrVpwd24p1353Ukk"
            )
            return

        # format message
        response = "Congrats! {} and {} just matched.".format(
            user["fields"]["Name"],
            match["fields"]["Name"],
        )

        await msg.channel.send(response)

    elif msg.content.startswith("!dumble"):
        await msg.channel.send(
            "Sorry, I didn't get that. I don't have a help command either"
            "go pester Andrew to build one."
        )


client.run(TOKEN)
