from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatbotresponse',
            name='display_order',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterModelOptions(
            name='chatbotresponse',
            options={'ordering': ['display_order', 'question']},
        ),
    ]
