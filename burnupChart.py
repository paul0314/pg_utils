import matplotlib.pyplot as plt
import matplotlib.dates as dates
import numpy as np
import datetime

FRIDAY = 4


def generateBurnupChart():
    start_date = datetime.date(2021, 6, 11)
    end_date = datetime.date(2021, 7, 2)

    xTicks = 7

    number_of_days = (end_date - start_date).days + 1

    print(number_of_days)

    list_of_datetimes = [start_date + datetime.timedelta(days=x) for x in range(number_of_days)]
    print(list_of_datetimes)

    summed_completed_story_points_daily_list = [x for x in range(22)]

    fig, ax = plt.subplots()

    ax.plot_date(list_of_datetimes, summed_completed_story_points_daily_list)

    for i in range(5, summed_completed_story_points_daily_list[-1] + 4, 5):
        ax.axhline(y=i, color='grey', linestyle='dotted')

    # ignore first and and last date
    for date in list_of_datetimes[1:-1]:
        if date.weekday() == FRIDAY:
            plt.axvline(date, linestyle="dotted")

    plt.gcf().autofmt_xdate()
    plt.gca().xaxis.set_major_formatter(dates.DateFormatter('%d-%m'))
    plt.gca().xaxis.set_major_locator(dates.WeekdayLocator(byweekday=dates.FR))

    plt.yticks(
        np.arange(min(summed_completed_story_points_daily_list), max(summed_completed_story_points_daily_list) + 1, 5)
    )

    plt.margins(0)

    plt.show()


generateBurnupChart()
