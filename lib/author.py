from .database_utils import get_connection

class Author:
    def __init__(self, name, id=None):
        self._name = name
        self.id = id

    @property
    def name(self):
        if not isinstance(self._name, str) or len(self._name.strip()) == 0:
            raise ValueError("Author name must be a non-empty string.")
        return self._name

    @classmethod
    def new_from_db(cls, row):
        return cls(name=row[1], id=row[0])

    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM authors WHERE id = ?", (id,))
        row = cur.fetchone()
        conn.close()
        return cls.new_from_db(row) if row else None

    def save(self):
        conn = get_connection()
        cur = conn.cursor()
        if self.id is None:
            cur.execute("INSERT INTO authors (name) VALUES (?)", (self.name,))
            self.id = cur.lastrowid
        else:
            cur.execute("UPDATE authors SET name=? WHERE id=?", (self.name, self.id))
        conn.commit()
        conn.close()

    def articles(self):
        from .article import Article  # 🔁 delayed import to avoid circular import
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM articles WHERE author_id = ?", (self.id,))
        rows = cur.fetchall()
        conn.close()
        return [Article.new_from_db(row) for row in rows]

    def magazines(self):
        from .magazine import Magazine
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT DISTINCT m.* FROM magazines m
            JOIN articles a ON a.magazine_id = m.id
            WHERE a.author_id = ?
        """, (self.id,))
        rows = cur.fetchall()
        conn.close()
        return [Magazine.new_from_db(row) for row in rows]

    def add_article(self, magazine, title):
        from .article import Article
        article = Article(title=title, author=self, magazine=magazine)
        article.save()
        return article

    def topic_areas(self):
        return list({mag.category for mag in self.magazines()})
