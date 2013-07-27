from ev import search_channel, logger, settings

INFOCHANNEL = search_channel(settings.CHANNEL_MUDINFO[0])[0]

def log_info(message):
    """
    Log a message to the info channel
    """
    try:
        INFOCHANNEL.msg('{Y[ {g%s{Y | {n%s{Y ]' % (INFOCHANNEL.key, message))
    except AttributeError:
        logger.log_infomsg("log_info: %s" % (message))

