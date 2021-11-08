import nextcord
from Systems.levelsys import levelling

async def backgroundUrl(id=None, guildID=None):
    if id is None:
        print("backgroundURL requires 'id'.")
        return
    
    if guildID is None:
        print("backgroundURL requires 'guildID'.")
        return
    
    else:
        try:
            stats = levelling.find_one({"guildid": guildID, "id": id})
            background = stats['background']
            if str(background) == "":
                return str(f"No Background!")
            return str(background)
        except Exception as e:
            print(f"backgroundURL ran into an error!\n\n{e}")

async def getXP(id=None, guildID=None):
    if id is None:
        print("getXP requires 'id'.")
        return
    if guildID is None:
        print("getXP requires 'guildID'.")
        return
    else:
        try:
            stats = levelling.find_one({"guildid": guildID, "id": id})
            xp = stats['xp']
            return str(xp)
        except Exception as e:
            print(f"getXP ran into an error!\n\n{e}")


async def getLevel(id=None, guildID=None):
    if id is None:
        print("getLevel requires 'id'.")
        return
    if guildID is None:
        print("getLevel requires 'guildID'.")
        return
    else:
        try:
            stats = levelling.find_one({"guildid": guildID, "id": id})
            rank = stats['rank']
            return str(rank)
        except Exception as e:
            print(f"getLevel ran into an error!\n\n{e}")


async def getXPColor(id=None, guildID=None):
    if id is None:
        print("getXPColor requires 'id'.")
        return
    if guildID is None:
        print("getXPColor requires 'guildID'.")
        return
    else:
        try:
            stats = levelling.find_one({"guildid": guildID, "id": id})
            xp_color = stats['xp_color']
            return str(xp_color)
        except Exception as e:
            print(f"getXPColor ran into an error!\n\n{e}")


async def getCirlce(id=None, guildID=None):
    if id is None:
        print("getCircle requires 'id'.")
        return
    if guildID is None:
        print("getCircle requires 'guildID'.")
        return
    else:
        try:
            stats = levelling.find_one({"guildid": guildID, "id": id})
            circle = stats['circle']
            return str(circle)
        except Exception as e:
            print(f"getCircle ran into an error!\n\n{e}")