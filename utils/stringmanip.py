def conj_join(items, conjunction):
    items = [str(item) for item in items]
    if len(items) < 2:
        return ', '.join(items)
    else:
        return ', '.join(items[:-1] + [ conjunction + ' ' + items[-1] ])
