
## simple example of typical rhombus viewer

from genaf_snp.views import *

def index( request ):
    pass

@roles( PUBLIC )
def edit( request ):
    pass

@roles( PUBLIC )
def add( request ):
    pass

@roles( PUBLIC )
def action(request):
    pass


def list_posts( request ):

    dbh = get_dbhandler()

    posts = dbh.get_post()

    body = tbody()

    for post in posts:
        tbody.add(
            tr(
                td( a(post.title, href=request.route_url('post-view', id=post.id)) ),
            )
        )

    table_posts = table(
        thead(
            tr(
                th('Title')
            )
        )
    )

    table_posts.add( body )

    return table_posts