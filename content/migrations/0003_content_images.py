from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0002_chatbotresponse_display_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='aiservice',
            name='image',
            field=models.FileField(blank=True, upload_to='content/services/'),
        ),
        migrations.AddField(
            model_name='article',
            name='image',
            field=models.FileField(blank=True, upload_to='content/articles/'),
        ),
        migrations.AddField(
            model_name='event',
            name='image',
            field=models.FileField(blank=True, upload_to='content/events/'),
        ),
    ]
