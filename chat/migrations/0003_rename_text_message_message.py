# Generated by Django 5.0.6 on 2024-10-10 15:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_remove_message_chat_rename_sender_message_user_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='text',
            new_name='message',
        ),
    ]
