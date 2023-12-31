from .models import Profile, Relationship

def profile_pic(request):
    if request.user.is_authenticated:
        profile_obj = Profile.objects.get(user=request.user)
        pic = profile_obj.avatar
        return {'picture':pic}
    return {}

def invitation_received_no(request):
    if request.user.is_authenticated:
        profile_obj = Profile.objects.get(user=request.user)
        qs_count = Relationship.objects.invitations_received(profile_obj).count()
        # print(f"invite count: {qs_count}")
        return {'invites_num':qs_count}
    return {}

def invitation_send_no(request):
    if request.user.is_authenticated:
        profile_obj = Profile.objects.get(user=request.user)
        qs_count = Relationship.objects.invitations_send(profile_obj).count()
        # print(f"sent count: {qs_count}")
        return {'send_num':qs_count}
    return {}