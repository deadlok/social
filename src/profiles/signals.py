from django.db.models.signals import post_save, pre_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile, Relationship

@receiver(post_save, sender=User)
def post_save_create_profile(sender, instance, created, **kwarg):
    print("sender", sender)
    print("instance", instance)
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=Relationship)
def post_save_add_to_friends(sender, instance, created, **kwarg):
    sender_ = instance.sender
    receiver_ = instance.receiver
    if instance.status == 'accepted':
        if receiver_.user not in sender_.friends.all():
            print(f"{sender_.user} add {receiver_.user} as friends")
            sender_.friends.add(receiver_.user)
            sender_.save()

        if sender_.user not in receiver_.friends.all():
            print(f"{receiver_.user} add {sender_.user} as friends")
            receiver_.friends.add(sender_.user)
            receiver_.save()
        

@receiver(pre_delete, sender=Relationship)
def pre_delete_remove_from_freinds(sender, instance, **kwarg):
    sender_ = instance.sender
    receiver_ = instance.receiver

    if receiver_.user in sender_.friends.all():
        print(f"{sender_.user} remove {receiver_.user} as friends")
        sender_.friends.remove(receiver_.user)
        sender_.save()

    if sender_.user in receiver_.friends.all():
        print(f"{receiver_.user} remove {sender_.user} as friends")
        receiver_.friends.remove(sender_.user)
        receiver_.save()