from app.repositories.user_profile_repository import UserProfileRepository
from app.services.user_profile_cache import UserProfileCache
from app.services.user_profile_service import UserProfileService


def get_user_profile_service() -> UserProfileService:
    """Build the user profile service for FastAPI route injection.

    Returns:
        UserProfileService wired with SQLite as origin and Redis as cache.
    """
    return UserProfileService(
        repository=UserProfileRepository(),
        cache=UserProfileCache(),
    )
