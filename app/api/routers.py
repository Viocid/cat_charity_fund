from fastapi import APIRouter

from app.api.endpoints import (charityproject_router, donation_router,
                               google_api_router, user_router)
from app.core.constants import (DONATION_PREFIX, DONATION_TAGS, GOOGLE_PREFIX,
                                GOOGLE_TAGS, PREFIX, TAGS)

main_router = APIRouter()

main_router.include_router(
    router=charityproject_router, prefix=PREFIX, tags=TAGS
)
main_router.include_router(
    router=donation_router, prefix=DONATION_PREFIX, tags=DONATION_TAGS
)
main_router.include_router(
    google_api_router, prefix=GOOGLE_PREFIX, tags=GOOGLE_TAGS
)
main_router.include_router(user_router)
