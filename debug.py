from lib.database_utils import create_tables
from lib.author import Author
from lib.magazine import Magazine
from lib.article import Article

# Initialize database
create_tables()

# Quick manual test
if __name__ == "__main__":
    author = Author("NAssur Mohammed")
    author.save()

    mag = Magazine("Smart Tech Digest", "Technology")
    mag.save()

    article = Article(" Revolution", author, mag)
    article.save()

    print("Author's Magazines:", [m.name for m in author.magazines()])
    print("Magazine's Articles:", [a.title for a in mag.articles()])
