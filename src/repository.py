from src.db import get_connection


class RequestRepository:
    def list(self, status_id=None, category_id=None, q=None):
        sql = "SELECT * FROM Requests WHERE 1=1"
        params = []
        if status_id:
            sql += " AND StatusId = ?"
            params.append(status_id)
        if category_id:
            sql += " AND CategoryId = ?"
            params.append(category_id)
        if q:
            sql += " AND LOWER(Title) LIKE LOWER(?)"
            params.append(f"%{q}%")
        sql += " ORDER BY Id DESC"
        with get_connection() as conn:
            return [dict(r) for r in conn.execute(sql, params).fetchall()]

    def get(self, request_id: int):
        with get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM Requests WHERE Id = ?", (request_id,)
            ).fetchone()
            return dict(row) if row else None

    def create(self, data: dict) -> int:
        with get_connection() as conn:
            cur = conn.execute(
                "INSERT INTO Requests (Title, Description, AuthorId, StatusId, CategoryId) "
                "VALUES (?, ?, ?, 1, ?)",
                (data["title"], data.get("description"), data["author_id"], data["category_id"]),
            )
            conn.commit()
            return cur.lastrowid

    def update(self, request_id: int, data: dict) -> bool:
        fields = []
        values = []
        for k in ("title", "description", "category_id", "status_id", "assignee_id"):
            if k in data and data[k] is not None:
                col = {
                    "title": "Title",
                    "description": "Description",
                    "category_id": "CategoryId",
                    "status_id": "StatusId",
                    "assignee_id": "AssigneeId",
                }[k]
                fields.append(f"{col} = ?")
                values.append(data[k])
        if not fields:
            return False
        values.append(request_id)
        with get_connection() as conn:
            conn.execute(f"UPDATE Requests SET {', '.join(fields)} WHERE Id = ?", values)
            conn.commit()
            return True

    def delete(self, request_id: int) -> bool:
        with get_connection() as conn:
            cur = conn.execute("DELETE FROM Requests WHERE Id = ?", (request_id,))
            conn.commit()
            return cur.rowcount > 0

    # --- вспомогательные методы для проверки FK ---

    def get_category(self, category_id: int):
        with get_connection() as conn:
            return conn.execute(
                "SELECT * FROM Categories WHERE Id = ?", (category_id,)
            ).fetchone()

    def get_user(self, user_id: int):
        with get_connection() as conn:
            return conn.execute(
                "SELECT * FROM Users WHERE Id = ?", (user_id,)
            ).fetchone()

    def get_status(self, status_id: int):
        with get_connection() as conn:
            return conn.execute(
                "SELECT * FROM Statuses WHERE Id = ?", (status_id,)
            ).fetchone()


class UserRepository:
    def list(self):
        with get_connection() as conn:
            return [
                dict(r) for r in conn.execute(
                    "SELECT Id, Login, FullName, RoleId FROM Users"
                ).fetchall()
            ]


class StatusRepository:
    def list(self):
        with get_connection() as conn:
            return [dict(r) for r in conn.execute("SELECT * FROM Statuses").fetchall()]


class CategoryRepository:
    def list(self):
        with get_connection() as conn:
            return [dict(r) for r in conn.execute("SELECT * FROM Categories").fetchall()]