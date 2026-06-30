from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0003_content_images'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(upload_to='content/events/gallery/')),
                ('caption', models.CharField(blank=True, max_length=200)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gallery_images', to='content.event')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
    ]
