from app.representations.user_response import UserProfileResponse
from app.storages.sqlite import get_connection, init_db


class UserProfileRepository:
    """Read user profiles from the SQLite source-of-truth store."""

    def find_by_id(self, user_id: int) -> UserProfileResponse | None:
        """Find a user profile by id.

        Args:
            user_id: User identifier.

        Returns:
            User profile when the row exists, otherwise None.
        """
        init_db()
        with get_connection() as conn:
            row = conn.execute(
                """
                SELECT name, age
                FROM user_profiles
                WHERE user_id = ?
                """,
                (user_id,),
            ).fetchone()

        if row is None:
            return None

        return UserProfileResponse(name=row["name"], age=row["age"])

    def save(self, user_id: int, profile: UserProfileResponse) -> None:
        """Insert or replace a user profile row.

        Args:
            user_id: User identifier.
            profile: User profile payload to store.

        Returns:
            None.
        """
        init_db()
        with get_connection() as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO user_profiles (user_id, name, age)
                VALUES (?, ?, ?)
                """,
                (user_id, profile.name, profile.age),
            )
