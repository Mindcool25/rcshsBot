# Using cogs makes life a lot easier!
import discord
from discord.ext import commands
from datetime import datetime as d
import urllib, requests, html2text, re
from markdown import Markdown
from io import StringIO


# Takes a string and removes whitespace and makes it lowercase. This is useful in comparisions that need to happen later on.
def normalize_key(key): # TODO: Make this more powerful in the future, maybe with some sort of globbing.
    return key.strip().lower()

# This function return a python dictionary structure that contains computer terms as keys and links to their definitions as values.
def fetch_dictionary():
    url = 'https://www.techopedia.com/dictionary'
    # This is needed to trick sites into thinking this is an actual browser.
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    req = urllib.request.Request(url, headers=headers) 
    il = list(filter(lambda s: '/definition' in s, str(urllib.request.urlopen(req).read()).split('\\n')))
    final_dict = {}
    for e in il:
        [value, key] = e.split('>', 1)
        final_dict[normalize_key(key.rstrip('</a>'))] = value.lstrip('<a href="/definition/').rstrip('"')
    return final_dict


def fetch_page(key, dict):
    url = 'https://www.techopedia.com/definition/' + dict[key]
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    return str(urllib.request.urlopen(urllib.request.Request(url, headers=headers)).read())

# Removes formatting characters from a single text element
def unmark_element(element, stream=None):
    if stream is None:
        stream = StringIO()
    if element.text:
        stream.write(element.text)
    for sub in element:
        unmark_element(sub, stream)
    if element.tail:
        stream.write(element.tail)
    return stream.getvalue()

# Patching the Markdown class to support plaintext (i.e. not marked-up) output
Markdown.output_formats["plain"] = unmark_element
__md = Markdown(output_format="plain")
__md.stripTopLevelTags = False

# Removes formatting from multiple text elements
def unmark(text):
    return __md.convert(text)

# Combines the the patching, unmark, and unmark_element into one easy to use html-to-plaintext converter
def html_to_plain(s):
    return unmark(html2text.html2text(s))

#COMMMANDS!
class BasicCog(commands.Cog):
    # Initializing cog into the bot
    def __init__(self, bot):
        self.bot = bot
        # Fetching and caching the dictionary of terms from online. This is stored in a python dictionary structure, as you might expect.
        self.dict = fetch_dictionary()

    # Returns out a short definition of whatever term is given.
    @commands.command(
        name="define",  # The name of the command, what you will type to invoke the command
        description="Command to define computer terms.",  # Description for help command
        aliases = ['def']
    )
    # Function for `define` command
    async def define_command(self, ctx):
        userInput = ctx.message.content[len(ctx.prefix) + len(ctx.invoked_with):][1:]
        msg = ""
        try:
            normkey = normalize_key(userInput)
            page_lines = html_to_plain(fetch_page(normkey, self.dict)).split("\\n")
            for i in range(0, len(page_lines)):
                e = page_lines[i].lower()
                if 'what does' in e and normkey in e:
                    line = page_lines[i+1].strip().replace("\n", " ")
                    if len(line) >= 2000:
                        msg = "The definition is too long to send. Read it here: " + 'https://www.techopedia.com/definition/' + self.dict[normkey] + "."
                    else:
                        msg = line
        except:
            msg = "No definition found."
        await ctx.send(content=msg)
    # Return a longer explantion/definition of whatever term is given.
    @commands.command(
        name = "explain",
        description = "Command to explain terms more in depth than .define does.",
    )
    # Function for `explain` command
    async def explain_command(self, ctx):
        userInput = ctx.message.content[len(ctx.prefix) + len(ctx.invoked_with):][1:]
        msg = ""
        try:
            normkey = normalize_key(userInput)
            page_lines = html_to_plain(fetch_page(normkey, self.dict)).split("\\n")
            for i in range(0, len(page_lines)):
                e = page_lines[i].lower()
                if 'techopedia explains' in e and normkey in e:
                    line = page_lines[i+1].strip().replace("\n", " ")
                    if len(line) >= 2000:
                        msg = "The explantion is too long to send. Read it here: " + 'https://www.techopedia.com/definition/' + self.dict[normkey] + "."
                    else:
                        msg = line

        except:
            msg = "No explanation found."
        await ctx.send(content=msg)

#ALWAYS KEEP THIS HERE
# This needs to be at the bottom of all cog files for the cog to be added to the main bot
def setup(bot):
    bot.add_cog(BasicCog(bot))
