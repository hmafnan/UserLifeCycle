from itertools import groupby

from django.db.models import Count
from django.db.models import Sum
from django.http import JsonResponse

from user_profile import models

ACTIVE = 'Active'
CHURNED = 'Churned'
LAPSED = 'Lapsed'
NEW = 'New'


def total_policy_count_for_user(request):
    """Count total policies for a given user

    Params:
        user_id: Required argument for whom policies should be counted

    Optional Params:
        month: Month number for which policies should be counted for given user
        underwriter: Underwriter for which polices should be counted
    """
    user_id = request.GET.get('user_id')
    assert user_id is not None, 'User id cannot be None'

    month = request.GET.get('month', None)
    underwriter = request.GET.get('underwriter', None)

    query = models.Policy.objects.filter(user_id=user_id)

    if underwriter is not None:
        query = query.filter(underwriter=underwriter)

    if month is not None:
        month = int(month)
        query = query.filter(policy_start_date__month=month)

    return JsonResponse({'policy_count': query.count()})


def total_days_active_for_user(request):
    """Count total days active for a given user

    Params:
        user_id: Required argument for whom days should be counted

    Optional Params:
        month: Month number for which results should be filtered
        underwriter: Underwriter for which results should be filtered
    """
    user_id = request.GET.get('user_id')
    assert user_id is not None, 'User id cannot be None'

    month = request.GET.get('month', None)
    underwriter = request.GET.get('underwriter', None)
    count = 0

    query = models.ViewUsersLifeCycleStatus.objects.filter(
        user_id=user_id,
        user_life_cycle_status=ACTIVE)

    if underwriter is not None:
        query = query.filter(underwriter=underwriter)

    if month is not None:
        month = int(month)
        query = query.filter(month_number=month)

    for status in query:
        count += models.Calendar.objects.filter(
            year_month=status.year_month).last().day_of_month
    return JsonResponse({'days_active': count})


def total_new_users_count_for_date(request):
    """Count new users for a given date

    Params:
        date: Required argument for which results should be counted

    Optional Params:
        underwriter: Underwriter for which results should be filtered

    ... Assumption:
        Already passing date so optional param for 'month' is not needed
    """
    date = request.GET.get('date')  # Expected format: "2020-03-29"
    assert date is not None, 'Date cannot be None'

    underwriter = request.GET.get('underwriter', None)
    count = 0
    query = models.ViewUsersLifeCycleStatus.objects

    if underwriter is not None:
        query = query.filter(underwriter=underwriter)

    query = query.filter(user_life_cycle_status=NEW)
    for user in query:
        policy_id = user.policy_id
        match = models.Policy.objects.filter(
            pk=policy_id,
            policy_start_date__lte=date,
            policy_end_date__gte=date).exists()
        if match:
            count += 1

    return JsonResponse({'new_users_count': count})


def total_lapsed_users_count_for_month(request):
    """Count total lapsed users for given month

    Params:
        month: Required argument for which results should be counted

    Optional Params:
        underwriter: Underwriter for which results should be filtered

    ... Assumption:
        Already passing required 'month' so optional param for 'month'
        is not needed

    """
    month = int(request.GET.get('month'))
    underwriter = request.GET.get('underwriter', None)

    query = models.ViewUsersLifeCycleStatus.objects
    if underwriter is not None:
        query = query.filter(underwriter=underwriter)

    query = query.filter(
        user_life_cycle_status=LAPSED,
        month_number=month).values('user_id').annotate(dcount=Count('user_id'))
    return JsonResponse({'lapsed_users_count': query.count()})


def total_new_users_premium_per_date_for_underwriter(request):
    """Get total premium for new users ordered by date for given underwriter

    Calculates the results in three steps
    1- Get all new users for given underwriter ordered by year month
    2- Aggregates premium for all policy of each user
    3- Generates final results as aggregated premium by year month

    Params:
        underwriter: Underwriter for which results should be filtered

    Optional Params:
        month: Required argument for which results should be counted

    ... Assumption:
        - For this solution it is assumed that 'per date' means {year month} and
         premium will be calculated with respect to this date
    """
    underwriter = request.GET.get('underwriter')
    assert underwriter is not None, 'Underwriter cannot be None'
    month = request.GET.get('month', None)
    data = []
    ordered_data = []
    query = models.ViewUsersLifeCycleStatus.objects

    if month is not None:
        month = int(month)
        query = query.filter(month_number=month)
    query = query.filter(
        user_life_cycle_status=NEW,
        underwriter=underwriter).annotate(dcount=Count('year_month')).order_by('year_month')

    for user in query:
        premium = models.Finance.objects.filter(policy_id=user.policy_id).aggregate(total=Sum('premium'))
        data.append({
            'premium': premium['total'],
            'year_month': user.year_month
        })

    for date, group in groupby(data, key=lambda item: item['year_month']):
        ordered_data.append({
            'date': date,
            'premium': sum(v['premium'] for v in group)
        })

    return JsonResponse(ordered_data, safe=False)


def get_policies(request):
    """Get all policies

    Optional Params:
        month: Filter policies by month number
        underwriter: Filter policies by underwriter
    """
    month = request.GET.get('month', None)
    underwriter = request.GET.get('underwriter', None)
    query = models.Policy.objects

    if underwriter is not None:
        query = query.filter(underwriter=underwriter)

    if month is not None:
        month = int(month)
        query = query.filter(policy_start_date__month=month)

    return JsonResponse(list(query.all().values()), safe=False)
