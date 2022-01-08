from django import template

register = template.Library()

@register.filter(name='censor')
def censor(text :str):
    offensives = ['девка', 'ублюдок']
    list_of_words = text.split()
    safe_list = []
    for word in list_of_words:
        if word in offensives:
            safe_list.append('*'*len(word))
        else:
            safe_list.append(word)
    return " ".join(safe_list)