

def clean_profile_deletion(sender, instance=None, **kwargs):
    email = instance.email
    print('e', email)
    reserve_email = instance.reserve_email
    print('r_e', reserve_email)
    user = instance.user
    if email:
        email.delete()
    if reserve_email:
        reserve_email.delete()
    if user:
        user.delete()