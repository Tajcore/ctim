# import the models modules in the Django way
from ctim.ctia.models.ransomware import Group, Location, Post, Profile
from ctim.ctia.models.telegram import Adjacency, Channel, ChannelPost, Media, Message, UserProfile
from ctim.ctia.models.threat_actor import CVE, Mitigation, RelatedThreatGroup, Risk, ThreatActor

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
    "ThreatActor",
    "Mitigation",
    "RelatedThreatGroup",
    "CVE",
    "Risk",
]
