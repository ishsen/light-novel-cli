import click
from src.chapters import ChapterRequester
from src.summary import SummaryGenerator
from src.popular import PopularRequester
from src.homepage import HomePageRequester
from src.epubconversion import TextConverter
from src.utils import getHomeOutput, getSummaryOutput, getChapterOutput, getPopularOutput


@click.group()
def messages():
    pass


@click.command()
@click.option('--amount', default=5, help='Number of popular books to retrieve', type=int)
@click.option('--genre', help='Genre to retrieve from', type=str)
@click.option('--site', help='Site to retrive popular books from', type=str)
def grab(amount, genre, site):

    p = PopularRequester(amount=amount)
    getPopularOutput(p)


@click.command()
@click.option('--site', help='Specific site to get homepage from', type=str)
@click.argument('title', type=str)
def info(site, title):

    h = HomePageRequester(title)
    getHomeOutput(h)

@click.command()
@click.option('--begin', help='Get epub of a specific number of chapter', type=int)
@click.option('--site', help='Specific site to get story from', type=str)
@click.argument('title', type=str)
@click.argument('chapter', type=int)
def save(begin, site, title, chapter):
    if begin:
        t = TextConverter(title=title, begin=begin, end=chapter)
    else:
        t = TextConverter(title=title, begin=chapter, end=chapter)


@click.command()
@click.option('--summary', help='Get a summary of specified number of chapters', type=int)
@click.option('--site', help='Specific site to get story from', type=str)
@click.argument('title', type=str)
@click.argument('chapter', type=int)
def read(summary, site, title, chapter):

    if (summary):

        s = SummaryGenerator(title=title, number=chapter, go_back=summary)

        getSummaryOutput(s, title, summary, chapter)
    else:

        req = ChapterRequester(title=title, number=chapter)

        getChapterOutput(req)


messages.add_command(read)
messages.add_command(grab)
messages.add_command(info)
messages.add_command(save)

if __name__ == '__main__':
    messages()

# python cli.py grab --amount 7
# python cli.py info "Battle Through The Heavens"
# python cli.py read " Dragon-Marked War God" 2914
# python cli.py read --summary 3 " Dragon-Marked War God" 2914
# python cli.py save " Dragon-Marked War God" 2914
