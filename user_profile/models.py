from django.db import models


class Policy(models.Model):
    policy_id = models.CharField(max_length=100, blank=False, primary_key=True)
    user_id = models.CharField(max_length=100, blank=False)
    subscription_id = models.CharField(max_length=100, blank=False)
    policy_start_date = models.DateTimeField(blank=True)
    policy_end_date = models.DateTimeField(blank=True)
    underwriter = models.TextField(max_length=30, blank=True, default='')

    def __repr__(self):
        return self.policy_id + ' | ' + self.user_id


class Calendar(models.Model):
    date = models.DateTimeField(primary_key=True, blank=False)
    year = models.IntegerField()
    month_number = models.IntegerField()
    month_name = models.CharField(max_length=30)
    day_of_month = models.IntegerField()
    day_of_week = models.IntegerField()
    year_month = models.TextField(max_length=30)

    def __repr__(self):
        return self.year_month + ' | ' + self.month_name


class Finance(models.Model):
    finance_transaction_id = models.CharField(max_length=100, blank=False, primary_key=True)
    created_at = models.DateTimeField(blank=True)
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE)
    reason = models.CharField(max_length=30)
    premium = models.IntegerField()
    ipt = models.IntegerField()

    def __repr__(self):
        return self.reason + ' | ' + str(self.policy.id)


class ViewUsersLifeCycleStatus(models.Model):
    id = models.AutoField(primary_key=True)
    year_month = models.CharField(max_length=100, blank=False)
    user_id = models.CharField(max_length=100, blank=False)
    active_from = models.CharField(max_length=50)
    user_life_cycle_status = models.CharField(max_length=50)
    lapsed_months = models.IntegerField()
    policy_id = models.CharField(max_length=50, blank=True, null=True)
    month_number = models.IntegerField()
    underwriter = models.TextField(max_length=30, blank=True, default='')

    def __repr__(self):
        return self.user_id + ' | ' + self.user_life_cycle_status + ' | ' + self.year_month


