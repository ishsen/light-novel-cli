import click


def getPopularOutput(p):
    for book in p.books:
        click.echo()
        click.echo(click.style(book.title, fg="yellow", bold=True) + click.style(' | ', dim=True) + click.style(
            "(", dim=True) + click.style(book.link, dim=True, underline=True) + click.style(") ", dim=True))
        click.echo()
        click.echo(click.style(book.description, dim=True))
        click.echo()
        click.echo(click.style("Views: ") + click.style(book.views, dim=True, fg="yellow") + click.style(
            ' | ', dim=True) + click.style("Rating: ") + click.style(book.views, dim=True, fg="cyan"))


def getHomeOutput(h):
    click.echo()
    click.echo(click.style(h.homepage.title, fg="yellow", bold=True) + click.style(' | ', dim=True) +
               click.style("written by ", dim=True) + click.style(",".join(h.homepage.authors.keys()), fg="cyan"))
    click.echo(click.style("(", dim=True) + click.style(h.site +
               h.search_term, dim=True, underline=True) + click.style(") ", dim=True))
    click.echo(click.style("Status: ") + click.style(h.homepage.status, fg="cyan" if "complete" in h.homepage.status.lower()
               else "yellow", dim=True) + click.style(' | ') + click.style("Last updated: ") + click.style(h.homepage.updated, dim=True))
    click.echo()
    click.secho(h.homepage.description, dim=True)
    click.echo()
    click.echo(click.style("Tags: ") +
               click.style(", ".join(h.homepage.genres.keys()), dim=True))
    click.echo(click.style("Latest Chapters: ") +
               click.style(", ".join(h.homepage.latest_chapters.keys()), dim=True, fg="yellow"))

    click.echo()


def getSummaryOutput(s, title, summary, chapter):
    click.echo()
    click.echo(click.style('Summary for ') + click.style(str(title).strip(), fg="yellow", bold=True) + click.style(" from chapters ") +
               click.style(int(chapter) - int(summary), fg="cyan") + click.style(" to ") + click.style(int(chapter), fg="cyan"))

    click.echo()
    click.secho(s.summary, dim=True)
    click.echo()


def getChapterOutput(req):

    click.echo()
    click.echo(click.style(req.chapter.title, fg="yellow", bold=True) + click.style(' | ', dim=True)
               + click.style(req.chapter.author, fg="cyan"))
    click.echo(click.style("Previous: ") + click.style("(", dim=True) + click.style(
        req.chapter.prv, dim=True, underline=True) + click.style(") ", dim=True))
    click.echo(click.style("Next: ") + click.style("(", dim=True) + click.style(
        req.chapter.nxt, dim=True, underline=True) + click.style(") ", dim=True))
    click.echo()
    click.echo('Begin reading? [yn] ', nl=False)
    c = click.getchar()
    click.echo()
    if c == 'y':
        click.echo_via_pager(click.style(req.chapter.text_content, dim=True))
    elif c == 'n':
        click.echo('Abort!')
