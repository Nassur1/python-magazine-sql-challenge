from .database_utils import get_connection

class Magazine:
    def __init__(self, name, category, id=None):
        self._name = name
        self._category = category
        self.id = id

    @property
    def name(self):
        if not isinstance(self._name, str) or len(self._name.strip()) == 0:
            raise ValueError("Magazine name must be a non-empty string.")
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or len(value.strip()) == 0:
            raise ValueError("Magazine name must be a non-empty string.")
        self._name = value

    @property
    def category(self):
        if not isinstance(self._category, str) or len(self._category.strip()) == 0:
            raise ValueError("Magazine category must be a non-empty string.")
        return self._category

    @category.setter
    def category(self, value):
        if not isinstance(value, str) or len(value.strip()) == 0:
            raise ValueError("Magazine category must be a non-empty string.")
        self._category = value

    @classmethod
    def new_from_db(cls, row):
        return cls(name=row[1], category=row[2], id=row[0])

    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM magazines WHERE id = ?", (id,))
        row = cur.fetchone()
        conn.close()
        return cls.new_from_db(row) if row else None

    def save(self):
        conn = get_connection()
        cur = conn.cursor()
        if self.id is None:
            cur.execute("INSERT INTO magazines (name, category) VALUES (?, ?)", (self.name, self.category))
            self.id = cur.lastrowid
        else:
            cur.execute("UPDATE magazines SET name=?, category=? WHERE id=?", (self.name, self.category, self.id))
        conn.commit()
        conn.close()

    def articles(self):
        from .article import Article
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM articles WHERE magazine_id = ?", (self.id,))
        rows = cur.fetchall()
        conn.close()
        return [Article.new_from_db(row) for row in rows]

    def contributors(self):
        from .author import Author
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT DISTINCT au.* FROM authors au
            JOIN articles a ON a.author_id = au.id
            WHERE a.magazine_id = ?
        """, (self.id,))
        rows = cur.fetchall()
        conn.close()
        return [Author.new_from_db(row) for row in rows]

    def article_titles(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT title FROM articles WHERE magazine_id = ?", (self.id,))
        titles = [r[0] for r in cur.fetchall()]
        conn.close()
        return titles

    def contributing_authors(self):
        from .author import Author
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT author_id FROM articles
            WHERE magazine_id = ?
            GROUP BY author_id
            HAVING COUNT(id) > 2;
        """, (self.id,))
        author_ids = [r[0] for r in cur.fetchall()]
        conn.close()
        return [Author.find_by_id(aid) for aid in author_ids if aid]
