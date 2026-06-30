from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='email',
            field=models.EmailField(default='unknown@ai-solutions.com', max_length=254),
            preserve_default=False,
        ),
    ]
