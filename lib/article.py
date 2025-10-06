from .database_utils import get_connection

class Article:
    def __init__(self, title, author, magazine, id=None):
        self._title = title
        self.author = author
        self.magazine = magazine
        self.id = id

    @property
    def title(self):
        if not isinstance(self._title, str) or len(self._title.strip()) == 0:
            raise ValueError("Article title must be a non-empty string.")
        return self._title

    @classmethod
    def new_from_db(cls, row):
        from .author import Author
        from .magazine import Magazine
        author = Author.find_by_id(row[2])
        magazine = Magazine.find_by_id(row[3])
        return cls(title=row[1], author=author, magazine=magazine, id=row[0])

    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM articles WHERE id = ?", (id,))
        row = cur.fetchone()
        conn.close()
        return cls.new_from_db(row) if row else None

    def save(self):
        conn = get_connection()
        cur = conn.cursor()
        if self.id is None:
            cur.execute(
                "INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)",
                (self.title, self.author.id, self.magazine.id)
            )
            self.id = cur.lastrowid
        else:
            cur.execute(
                "UPDATE articles SET title=?, author_id=?, magazine_id=? WHERE id=?",
                (self.title, self.author.id, self.magazine.id, self.id)
            )
        conn.commit()
        conn.close()
