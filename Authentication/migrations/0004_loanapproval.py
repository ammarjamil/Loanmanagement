# Generated by Django 3.2.14 on 2023-06-21 18:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Authentication', '0003_user_is_manager'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoanApproval',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('approved', 'Approved'), ('rejected', 'Rejected')], max_length=10)),
                ('comment', models.TextField()),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('loan_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Authentication.loanrequest')),
                ('manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
