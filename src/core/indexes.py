# This code was made obsolete by Django 2.2
# It has to stay there for now because it is still imported by migrations
# It will be deleted as soon as existing migrations are squashed.

from django.contrib.postgres.indexes import GinIndex, GistIndex


class GinTrigramIndex(GinIndex):
    """A Gin index with the Trigram operator class.

    Trigram matching is an awesome Postsresql tool to speed up alphanum
    similarity.

    Postsqresql offers Trigram indexes that offer good performance on
    naive text search queries like this one:

    SELECT * FROM tags where name LIKE '%query%'

    Unfortunately, Django does not offer a quick access to this index type, so
    this class offers an easy way to access it.

    Please note that starting with Django 2.2, the `django.db.models.Index`
    class will provide a `opclasses` parameter, rendering this class obsolete.

    References:
    https://niallburkley.com/blog/index-columns-for-like-in-postgres/
    https://about.gitlab.com/2016/03/18/fast-search-using-postgresql-trigram-indexes/
    https://stackoverflow.com/a/51880653/665797
    https://www.postgresql.org/docs/9.6/pgtrgm.html
    """

    def create_sql(self, model, schema_editor, using=""):
        statement = super().create_sql(model, schema_editor, using=using)
        statement.template = """
            CREATE INDEX %(name)s
            ON %(table)s%(using)s (%(columns)s gin_trgm_ops)%(extra)s
        """
        return statement


class GistTrigramIndex(GistIndex):
    """A Gist index with the Trigram operator class.

    See above for details
    """

    def create_sql(self, model, schema_editor, using=""):
        statement = super().create_sql(model, schema_editor, using=using)
        statement.template = """
            CREATE INDEX %(name)s
            ON %(table)s%(using)s (%(columns)s gist_trgm_ops)%(extra)s
        """
        return statement
