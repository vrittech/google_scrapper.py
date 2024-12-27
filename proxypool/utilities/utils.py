from ..models import ProxyPool, UserProxyAssignment

def assign_proxies_to_user(user):
    """
    Assign proxies to a user based on their subscription plan.
    """
    if not user.plan.dedicated_proxies:
        return None  # No proxy assignment for users without dedicated proxy access

    # Retrieve or create a UserProxyAssignment instance
    assignment, created = UserProxyAssignment.objects.get_or_create(user=user)

    # Fetch available proxies
    available_proxies = ProxyPool.objects.filter(is_active=True).exclude(assigned_users__in=[user])

    # Limit proxies based on the plan (e.g., 2 proxies for a Pro Plan)
    limit = user.plan.concurrent_scrapes
    assigned_proxies = available_proxies[:limit]

    if assigned_proxies:
        assignment.proxies.set(assigned_proxies)  # Assign proxies
        assignment.save()
        return assigned_proxies

    return None


# When a User Subscribes or Upgrades/Downgrades a Plan
# Add a signal to detect subscription changes and assign proxies if the new plan allows dedicated proxies.

# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import CustomUser, SubscriptionPlan
# from .utils import assign_proxies_to_user

# @receiver(post_save, sender=CustomUser)
# def handle_subscription_change(sender, instance, **kwargs):
#     """
#     Automatically assign proxies when a user subscribes or changes plans.
#     """
#     user = instance
#     if user.plan and user.plan.dedicated_proxies:
#         proxies = assign_proxies_to_user(user)
#         if proxies:
#             print(f"Assigned proxies to {user.username}: {[str(proxy) for proxy in proxies]}")
#         else:
#             print(f"No available proxies for {user.username}")
#     else:
#         # Clear proxies if the new plan doesn’t allow them
#         UserProxyAssignment.objects.filter(user=user).delete()
