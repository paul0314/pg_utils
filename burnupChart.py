import matplotlib.pyplot as plt
import matplotlib.dates as dates
import numpy as np
import csv
import datetime

FRIDAY = 4
TASKNUMBER = 0
TASKTITLE = 1
TASKDESCRIPTION = 2
TASKDIFFICULTY = 3
TASKRISK = 4
TASKSTART = 5
TASKEND = 6
TASKSTATUS = 7
TASKPERSON1HOURS = 8
TASKPERSON2HOURS = 9
TASKPERSON3HOURS = 10
TASKPERSON4HOURS = 11
TASKTOTALHOURS = 12
TASKHOURSPERPOINTS = 13


def generateBurnupChart(issues):

    start_date = datetime.date(2021, 4, 9)
    end_date = datetime.date(2021, 7, 2)

    number_of_days = (end_date - start_date).days + 1

    list_of_datetimes = [start_date + datetime.timedelta(days=x) for x in range(number_of_days)]

    summed_completed_story_points_daily_list = [0 for _ in range(number_of_days)]
    summed_scope_story_points_daily_list = [0 for _ in range(number_of_days)]

    for issue in issues:
        if issue[TASKSTATUS] == "+":
            finish_date_of_issue = parseDate(issue[TASKEND])
            start_index_for_adding = (finish_date_of_issue - start_date).days
            for i in range(start_index_for_adding, number_of_days):
                summed_completed_story_points_daily_list[i] += int(issue[TASKDIFFICULTY])

        if issue[TASKSTATUS] == "o" or issue[TASKSTATUS] == "+":
            start_date_of_issue = parseDate(issue[TASKSTART])
            start_index_for_adding = (start_date_of_issue - start_date).days
            for i in range(start_index_for_adding, number_of_days):
                summed_scope_story_points_daily_list[i] += int(issue[TASKDIFFICULTY])

    fig, ax = plt.subplots()

    ax.plot_date(list_of_datetimes, summed_completed_story_points_daily_list, linestyle='solid', markersize=0, label='Completed')
    ax.plot_date(list_of_datetimes, summed_scope_story_points_daily_list, linestyle='solid', markersize=0, label='Scope')

    for i in range(5, summed_scope_story_points_daily_list[-1] + 9, 5):
        ax.axhline(y=i, color='grey', linestyle='dotted')

    # ignore first and and last date
    for date in list_of_datetimes[1:-1]:
        if date.weekday() == FRIDAY:
            plt.axvline(date, linestyle="dotted")

    plt.xticks(rotation=30)
    plt.gca().xaxis.set_major_formatter(dates.DateFormatter('%d-%m'))
    plt.gca().xaxis.set_major_locator(dates.WeekdayLocator(byweekday=dates.FR))

    plt.yticks(
        np.arange(0, max(summed_scope_story_points_daily_list) + 9, 5)
    )

    plt.ylim(bottom=0)

    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.title('Burnup Chart', fontsize=22, y=1.03)

    plt.margins(0)

    plt.show()


def generateBurnupChartForSprint(issues, sprint_start, sprint_end, chart_title='Burnup Chart'):

    start_date = sprint_start
    end_date = sprint_end

    number_of_days = (end_date - start_date).days + 1

    list_of_datetimes = [start_date + datetime.timedelta(days=x) for x in range(number_of_days)]

    summed_completed_story_points_daily_list = [0 for _ in range(number_of_days)]
    summed_scope_story_points_daily_list = [0 for _ in range(number_of_days)]

    for issue in issues:
        if not issue[TASKEND]:
            continue

        if not issue[TASKSTART]:
            continue

        start_date_of_issue = parseDate(issue[TASKSTART])
        finish_date_of_issue = parseDate(issue[TASKEND])

        if start_date_of_issue == end_date:
            continue

        if not finish_date_of_issue < start_date:
            if issue[TASKSTATUS] == "+":
                start_index_for_adding = (finish_date_of_issue - start_date).days
                for i in range(start_index_for_adding, number_of_days):
                    summed_completed_story_points_daily_list[i] += int(issue[TASKDIFFICULTY])

            if issue[TASKSTATUS] == "o" or issue[TASKSTATUS] == "+":
                start_index_for_adding = (start_date_of_issue - start_date).days
                for i in range(start_index_for_adding, number_of_days):
                    summed_scope_story_points_daily_list[i] += int(issue[TASKDIFFICULTY])

    fig, ax = plt.subplots()

    ax.plot_date(list_of_datetimes, summed_completed_story_points_daily_list, linestyle='solid', markersize=0, label='Completed')
    ax.plot_date(list_of_datetimes, summed_scope_story_points_daily_list, linestyle='solid', markersize=0, label='Scope')

    for i in range(5, summed_scope_story_points_daily_list[-1] + 9, 5):
        ax.axhline(y=i, color='grey', linestyle='dotted')

    # ignore first and and last date
    for date in list_of_datetimes[1:-1]:
        if date.weekday() == FRIDAY:
            plt.axvline(date, linestyle="dotted")

    plt.xticks(rotation=30)
    plt.gca().xaxis.set_major_formatter(dates.DateFormatter('%d-%m'))
    plt.gca().xaxis.set_major_locator(dates.WeekdayLocator(byweekday=dates.FR))

    plt.yticks(
        np.arange(0, max(summed_scope_story_points_daily_list) + 9, 5)
    )

    plt.ylim(bottom=0)

    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.title(chart_title, fontsize=22, y=1.03)

    plt.margins(0)

    plt.show()


def readExcel():
    filename = './TaskVerwaltung.csv'

    issues = []

    with open(filename, 'r') as csvfile:
        datareader = csv.reader(csvfile)
        for row in datareader:
            issues.append(row)

        issues = issues[1:]

    return issues


def parseDate(date):
    return datetime.datetime.strptime(date, "%d/%m/%Y").date()


start_date_of_sprints = [datetime.date(2021, 4, 9), datetime.date(2021, 5, 7), datetime.date(2021, 6, 11)]

# generateBurnupChart(readExcel())

generateBurnupChartForSprint(readExcel(), datetime.date(2021, 4, 16), datetime.date(2021, 5, 7), "Sprint 1")
