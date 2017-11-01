from .models import Flag

def update_hacker_bucks_from_flag(session, userflag):
    '''
    Get flag points from the real database. This
    is actually done securely...no SQL injections
    here
    '''
    # Normalize input
    userflag = userflag.strip()
    hacker_bucks = 0
    matched_flag = None
    try:
        #pylint: disable=E1101
        for flagentry in Flag.objects.all():
            flag = flagentry.flag

            # Check if it's equal
            if userflag == flag:
                hacker_bucks = flagentry.value
                matched_flag = flag

            # If not, see if they just submitted the flag
            # value b/w curly braces
            pure_flag = flag.replace("flag{", '')
            pure_flag = pure_flag.replace("}", '')
            if userflag == pure_flag:
                hacker_bucks = flagentry.value
                matched_flag = flag
    except:
        pass

    if hacker_bucks and matched_flag:
        # If the flag hasn't already been claimed
        if matched_flag not in session.claimed_flags:
            session.claimed_flags.append(matched_flag)
            session.hacker_bucks += hacker_bucks
            session.lifetime_hacker_bucks += hacker_bucks
