def conj_join(items, conjunction):
    if len(items) < 2:
        return ', '.join(items)
    else:
        return ', '.join(items[:-1] + [ conjunction + ' ' + items[-1] ])
