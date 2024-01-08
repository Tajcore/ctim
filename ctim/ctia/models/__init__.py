# import the models modules in the Django way
from ctim.ctia.models.ransomware import Group, Location, Post, Profile
from ctim.ctia.models.telegram import Adjacency, Channel, ChannelPost, Media, Message, UserProfile

__all__ = [
    "Group",
    "Location",
    "Post",
    "Profile",
    "Adjacency",
    "Channel",
    "Media",
    "Message",
    "UserProfile",
    "ChannelPost",
]
