from django import template
register = template.Library()

@register.filter
def index(sequence, i):
    try:
        return sequence[int(i) - 1]  # 如果 periods 是從 1 開始
    except:
        return ""
@register.filter
def get_course(day_dict, i):
    try:
        return day_dict[int(i) - 1]
    except:
        return ""

@register.filter
def get_course_data(data, key):
    try:
        return data.get(key, [])
    except:
        return []
