import re

from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.contrib.syndication.views import Feed
from django.core.cache import cache
from django.utils import timezone
from django.utils.feedgenerator import Atom1Feed

from judge.jinja2.markdown import markdown
from judge.models import BlogPost, Comment, Problem


TEX_REPLACEMENTS = {
    r'\le': '≤', r'\leq': '≤', r'\ge': '≥', r'\geq': '≥',
    r'\times': '×', r'\cdot': '·', r'\ldots': '…', r'\dots': '…',
    r'\rightarrow': '→', r'\to': '→', r'\infty': '∞', r'\pm': '±',
}


def strip_math(text):
    """Feeds have no MathJax, so render TeX as readable plain text instead."""
    text = re.sub(r'\$\$(.+?)\$\$', r'\1', text, flags=re.S)
    text = re.sub(r'(?<!\$)\$(?!\$)([^$\n]+?)(?<!\$)\$(?!\$)', r'\1', text)
    text = re.sub(r'(?<!~)~([^~\n]+?)~(?!~)', r'\1', text)
    for tex, replacement in TEX_REPLACEMENTS.items():
        text = text.replace(tex, replacement)
    return text


class ProblemFeed(Feed):
    title = 'Recently Added %s Problems' % settings.SITE_NAME
    link = '/'
    description = 'The latest problems added on the %s website' % settings.SITE_LONG_NAME

    def items(self):
        return Problem.get_public_problems().order_by('-date', '-id')[:25]

    def item_title(self, problem):
        return problem.name

    def item_description(self, problem):
        key = 'problem_feed:%d' % problem.id
        desc = cache.get(key)
        if desc is None:
            desc = str(markdown(strip_math(problem.description), 'problem'))[:500] + '...'
            cache.set(key, desc, 86400)
        return desc

    def item_pubdate(self, problem):
        return problem.date

    item_updateddate = item_pubdate


class AtomProblemFeed(ProblemFeed):
    feed_type = Atom1Feed
    subtitle = ProblemFeed.description


class CommentFeed(Feed):
    title = 'Latest %s Comments' % settings.SITE_NAME
    link = '/'
    description = 'The latest comments on the %s website' % settings.SITE_LONG_NAME

    def items(self):
        return Comment.most_recent(AnonymousUser(), 25)

    def item_title(self, comment):
        return '%s -> %s' % (comment.author.user.username, comment.page_title)

    def item_description(self, comment):
        key = 'comment_feed:%d' % comment.id
        desc = cache.get(key)
        if desc is None:
            desc = str(markdown(strip_math(comment.body), 'comment'))
            cache.set(key, desc, 86400)
        return desc

    def item_pubdate(self, comment):
        return comment.time

    item_updateddate = item_pubdate


class AtomCommentFeed(CommentFeed):
    feed_type = Atom1Feed
    subtitle = CommentFeed.description


class BlogFeed(Feed):
    title = 'Latest %s Blog Posts' % settings.SITE_NAME
    link = '/'
    description = 'The latest blog posts from the %s' % settings.SITE_LONG_NAME

    def items(self):
        return BlogPost.objects.filter(visible=True, publish_on__lte=timezone.now()).order_by('-sticky', '-publish_on')

    def item_title(self, post):
        return post.title

    def item_description(self, post):
        key = 'blog_feed:%d' % post.id
        summary = cache.get(key)
        if summary is None:
            summary = str(markdown(strip_math(post.summary or post.content), 'blog'))
            cache.set(key, summary, 86400)
        return summary

    def item_pubdate(self, post):
        return post.publish_on

    item_updateddate = item_pubdate


class AtomBlogFeed(BlogFeed):
    feed_type = Atom1Feed
    subtitle = BlogFeed.description
