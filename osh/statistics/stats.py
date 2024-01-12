from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    # abort
)

from osh.database.database import get_groups_for_month, get_all_groups
from osh.statistics.stats_utility import get_current_month, translate_month_name

stats_bp = Blueprint('stats', __name__,
                     static_folder='static',
                     template_folder='templates'
                     )


@stats_bp.route('/', methods=['GET'])
def stats():
    # все группы
    groups = get_all_groups()

    # текущий месяц
    current_month = get_current_month()

    # выбранный месяц из параметра запроса
    selected_month = request.args.get('selected_month')
    selected_month = selected_month or current_month

    translated_month = translate_month_name(selected_month)

    # фильтруем группы для выбранного месяца
    groups_for_month = sorted(
        [group for group in groups if group['month'] == selected_month],
        key=lambda x: x['date']
    )

    total_groups = len(groups_for_month)
    total_payment = total_groups * 3250

    return render_template('stats.html',
                           groups_for_month=groups_for_month,
                           current_month=translated_month,
                           groups=groups,
                           total_groups=total_groups,
                           total_payment=total_payment
                           )