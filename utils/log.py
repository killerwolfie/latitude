from ev import search_channel, logger, settings

INFOCHANNEL = search_channel(settings.CHANNEL_MUDINFO[0])[0]
NEWSCHANNELS = search_channel('News')

def log_info(message):
    """
    Log a message to the info channel
    """
    INFOCHANNEL.msg('{Y[ {g%s{Y | {n%s{Y ]' % (INFOCHANNEL.key, message))
    logger.log_infomsg("log_info: %s" % (message))

def log_news(message):
    """
    Log a message to the news channel (To announce to everyone who hasn't left the channel)
    """
    if NEWSCHANNELS:
        for chan in NEWSCHANNELS:
            chan.msg('{Y[ {g%s{Y | {n%s{Y ]' % (chan.key, message))
