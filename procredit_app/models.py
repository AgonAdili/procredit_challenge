from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from datetime import date

class Client(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)


class NonClient(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)

class OutcomeCategory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job_title = models.CharField(null = True, blank = False, max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default = date.today())

class Outcome(models.Model):
    CATEGORY_CHOICES = [           
        ('bills', 'Bills'),
        ('needs', 'Needs'),
        ('wants', 'Wants'),
    ]
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    category = models.CharField(max_length = 50, choices = CATEGORY_CHOICES)
    amount = models.DecimalField(max_digits = 10, decimal_places = 2)
    date = models.DateField()


class Survey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    spending_areas = models.TextField()
    housing_status = models.CharField(max_length=255)
    debts = models.TextField()
    usual_spending = models.TextField()
    subscriptions = models.TextField()
    wants = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    sum = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.name

    def update_sum(self):
        self.sum = self.subcategories.aggregate(total_sum=Sum('sum'))['total_sum'] or 0
        self.save()

class SubCategory(models.Model):
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    sum = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.category.update_sum()


from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import User

@receiver(post_migrate)
def create_default_categories(sender, **kwargs):
    if sender.name == 'procredit_app':  # Replace 'procredit_app' with the actual name of your app
        default_user = User.objects.filter(is_superuser=True).first()  # Ensure you have a default user
        
        if not default_user:
            raise Exception("No superuser found. Create a superuser to associate default categories.")

        default_categories = {
            'Bills': [
                'Medical bills', 'Electricity', 'Gas and Fuel', 'Water', 'Garbage', 'Taxes', 'Insurance',
            ],
            'Needs': [
                'Groceries', 'Transportation', 'Healthcare', 'Clothing', 'Education', 'Savings'
            ],
            'Wants': [
                # Add subcategories as needed
            ]
        }

        for category_name, subcategories in default_categories.items():
            category, created = Category.objects.get_or_create(name=category_name, user=default_user)
            for subcategory_name in subcategories:
                SubCategory.objects.get_or_create(category=category, name=subcategory_name)
