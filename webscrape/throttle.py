from rest_framework.throttling import SimpleRateThrottle
from datetime import date

class PlanBasedThrottle(SimpleRateThrottle):
    """
    Custom throttle class to enforce API limits based on user's subscription plan.
    """
    scope = 'plan_based'

    def get_cache_key(self, request, view):
        """
        Generate a cache key based on the user ID and current month.
        """
        if not request.user.is_authenticated:
            return None

        user = request.user
        current_month = date.today().strftime('%Y-%m')
        return f"throttle_{self.scope}_{user.id}_{current_month}"

    def get_rate(self):
        """
        Dynamically calculate the rate limit based on the user's plan.
        """
        if hasattr(self, 'request') and hasattr(self.request, 'user'):
            user = self.request.user
            if user.is_authenticated and hasattr(user, 'plan') and user.plan:
                return f"{user.plan.api_limit}/month"
        return super().get_rate()  # Default rate if no plan

    def allow_request(self, request, view):
        """
        Check and enforce plan-based limits.
        """
        self.request = request  # Ensure the request is accessible in `get_rate`

        if not request.user.is_authenticated:
            return True  # Allow unauthenticated users without throttling

        user = request.user

        # Handle missing plan gracefully
        if not user.plan:
            print(f"User {user.id} does not have an associated plan.")
            return super().allow_request(request, view)  # Fallback to default throttling

        today = date.today()

        # Reset usage if a new month has started
        if user.last_reset_date.month != today.month:
            user.api_usage = 0
            user.last_reset_date = today
            user.save()

        # Enforce API usage limits
        if user.api_usage >= user.plan.api_limit:
            return self.throttle_failure()

        # Increment API usage
        user.api_usage += 1
        user.save()

        return super().allow_request(request, view)
