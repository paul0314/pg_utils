import matplotlib.pyplot as plt
import matplotlib.dates as dates
import matplotlib.patches as mpatches
import numpy as np
import csv
import datetime

FRIDAY = 4
FINISHED = "+"
INPROGRESS = "o"
# corresponds with excel format
TASKNUMBER = 0
TASKTITLE = 1
TASKDESCRIPTION = 2
TASKDIFFICULTY = 3
TASKRISK = 4
TASKSTART = 5
TASKEND = 6
TASKSTATUS = 7
TASKPERSON1 = 8


def generateBurnupChart(issues, start_dates_of_sprints, end_dates_of_sprints, save_plot=False):
    start_date = start_dates_of_sprints[0]
    end_date = end_dates_of_sprints[-1]

    number_of_days = (end_date - start_date).days + 1

    list_of_datetimes = [start_date + datetime.timedelta(days=x) for x in range(number_of_days)]

    summed_completed_story_points_daily_list = [0 for _ in range(number_of_days)]
    summed_scope_story_points_daily_list = [0 for _ in range(number_of_days)]

    for issue in issues:
        # monotonously increasing function representing completed points (taskdifficulty is the same as issue points)
        if issue[TASKSTATUS] == FINISHED:
            finish_date_of_issue = parseDate(issue[TASKEND])
            start_index_for_adding = max(0, (finish_date_of_issue - start_date).days)
            for i in range(start_index_for_adding, number_of_days):
                summed_completed_story_points_daily_list[i] += int(issue[TASKDIFFICULTY])

        # monotonously increasing function representing scope points (taskdifficulty is the same as issue points)
        if issue[TASKSTATUS] == FINISHED or issue[TASKSTATUS] == INPROGRESS:
            start_date_of_issue = parseDate(issue[TASKSTART])
            start_index_for_adding = max(0, (start_date_of_issue - start_date).days)
            for i in range(start_index_for_adding, number_of_days):
                summed_scope_story_points_daily_list[i] += int(issue[TASKDIFFICULTY])

    # don't plot any days in the future
    index_of_today = min(0, (datetime.date.today() - end_dates_of_sprints[-1]).days - 1)
    if index_of_today < 0:
        for i in range(index_of_today, 0, 1):
            summed_completed_story_points_daily_list[i] = None

    fig, ax = plt.subplots()

    # plot step functions
    for i in range(len(summed_completed_story_points_daily_list) - 1):
        # horizontal, connecting line between neighboring dates for completed story points
        ax.plot(
            (list_of_datetimes[i], list_of_datetimes[i + 1]),
            (summed_completed_story_points_daily_list[i], summed_completed_story_points_daily_list[i]),
            color='blue',
            linestyle='solid'
        )
        # vertical line segments between neighboring dates for completed story points
        if summed_completed_story_points_daily_list[i] != summed_completed_story_points_daily_list[i + 1]:
            ax.plot(
                (list_of_datetimes[i + 1], list_of_datetimes[i + 1]),
                (summed_completed_story_points_daily_list[i], summed_completed_story_points_daily_list[i + 1]),
                color='blue',
                linestyle='solid'
            )

    for i in range(len(summed_scope_story_points_daily_list) - 1):
        # horizontal, connecting line between neighboring dates for scope story points
        ax.plot(
            (list_of_datetimes[i], list_of_datetimes[i + 1]),
            (summed_scope_story_points_daily_list[i], summed_scope_story_points_daily_list[i]),
            color='orange',
            linestyle='solid'
        )
        # vertical line segments between neighboring dates for scope story points
        if summed_scope_story_points_daily_list[i] != summed_scope_story_points_daily_list[i + 1]:
            ax.plot(
                (list_of_datetimes[i + 1], list_of_datetimes[i + 1]),
                (summed_scope_story_points_daily_list[i], summed_scope_story_points_daily_list[i + 1]),
                color='orange',
                linestyle='solid'
            )

    # ideal sprint curve
    ax.plot((list_of_datetimes[0], list_of_datetimes[-1]),
            (0, summed_scope_story_points_daily_list[-1]),
            color='black',
            linestyle='solid',
            zorder=-1)

    # dotted horizontal lines for reference
    for i in range(5, summed_scope_story_points_daily_list[-1] + 9, 5):
        ax.axhline(y=i, color='grey', linestyle='dotted', zorder=-2)

    # dotted vertical lines for reference
    # ignore first and and last date
    for date in list_of_datetimes[1:-1]:
        if date.weekday() == FRIDAY:
            plt.axvline(date, linestyle="dotted", zorder=-2)

    plt.xticks(rotation=30)
    # display xticks as day-month
    plt.gca().xaxis.set_major_formatter(dates.DateFormatter('%d-%m'))
    # only display fridays as xticks
    plt.gca().xaxis.set_major_locator(dates.WeekdayLocator(byweekday=dates.FR))

    # yticks for every 5th point
    plt.yticks(
        np.arange(0, max(summed_scope_story_points_daily_list) + 9, 5)
    )

    plt.ylim(bottom=0)

    orange_patch = mpatches.Patch(color='orange', label='Scope')
    blue_patch = mpatches.Patch(color='blue', label='Completed')
    black_patch = mpatches.Patch(color='black', label='Ideal')
    plt.legend(handles=[orange_patch, blue_patch, black_patch], loc='center left', bbox_to_anchor=(1, 0.5))

    plt.title('Burnup Chart', fontsize=22, y=1.03)

    plt.margins(0)

    # needs to be at the end
    tick_labels = plt.xticks()[0]
    sprint_end_positions = []
    for i, tick in enumerate(tick_labels):
        if tick in dates.date2num(start_dates_of_sprints):
            sprint_end_positions.append(i)

    for end_position in sprint_end_positions:
        plt.gca().get_xticklabels()[end_position].set_color('red')

    if save_plot:
        plt.savefig('BurnupChart', dpi=300, bbox_inches='tight')

    plt.show()


def generateBurnupChartForSprint(issues, sprint_start, sprint_end, chart_title='Burnup Chart', save_plot=False):
    start_date = sprint_start
    end_date = sprint_end

    number_of_days = (end_date - start_date).days + 1

    list_of_datetimes = [start_date + datetime.timedelta(days=x) for x in range(number_of_days)]

    summed_completed_story_points_daily_list = [0 for _ in range(number_of_days)]
    summed_scope_story_points_daily_list = [0 for _ in range(number_of_days)]

    for issue in issues:
        if not issue[TASKSTART]:
            continue

        start_date_of_issue = parseDate(issue[TASKSTART])

        finish_date_of_issue = None
        if issue[TASKEND]:
            finish_date_of_issue = parseDate(issue[TASKEND])

        if start_date_of_issue == end_date:
            continue

        # unfinished task must only be added to scope
        if finish_date_of_issue is None:
            if issue[TASKSTATUS] == FINISHED or issue[TASKSTATUS] == INPROGRESS:
                start_index_for_adding = max(0, (start_date_of_issue - start_date).days)
                for i in range(start_index_for_adding, number_of_days):
                    summed_scope_story_points_daily_list[i] += int(issue[TASKDIFFICULTY])

        # if task is within sprint scope, add to scope and if completed also to completed
        elif not (finish_date_of_issue < start_date or start_date_of_issue > end_date):
            # add to completed if completed
            if issue[TASKSTATUS] == FINISHED:
                start_index_for_adding = max(0, (finish_date_of_issue - start_date).days)
                for i in range(start_index_for_adding, number_of_days):
                    summed_completed_story_points_daily_list[i] += int(issue[TASKDIFFICULTY])

            # add to scope
            if issue[TASKSTATUS] == INPROGRESS or issue[TASKSTATUS] == FINISHED:
                start_index_for_adding = max(0, (start_date_of_issue - start_date).days)
                for i in range(start_index_for_adding, number_of_days):
                    summed_scope_story_points_daily_list[i] += int(issue[TASKDIFFICULTY])

    # don't plot any days in the future
    index_of_today = min(0, (datetime.date.today() - end_date).days - 1)
    if index_of_today < 0:
        for i in range(index_of_today, 0, 1):
            summed_completed_story_points_daily_list[i] = None

    fig, ax = plt.subplots()

    # plot step functions
    for i in range(len(summed_completed_story_points_daily_list) - 1):
        # horizontal, connecting line between neighboring dates for completed story points
        ax.plot(
            (list_of_datetimes[i], list_of_datetimes[i + 1]),
            (summed_completed_story_points_daily_list[i], summed_completed_story_points_daily_list[i]),
            color='blue',
            linestyle='solid'
        )
        # vertical line segments between neighboring dates for completed story points
        if summed_completed_story_points_daily_list[i] != summed_completed_story_points_daily_list[i + 1]:
            ax.plot(
                (list_of_datetimes[i + 1], list_of_datetimes[i + 1]),
                (summed_completed_story_points_daily_list[i], summed_completed_story_points_daily_list[i + 1]),
                color='blue',
                linestyle='solid'
            )

    for i in range(len(summed_scope_story_points_daily_list) - 1):
        # horizontal, connecting line between neighboring dates for scope story points
        ax.plot(
            (list_of_datetimes[i], list_of_datetimes[i + 1]),
            (summed_scope_story_points_daily_list[i], summed_scope_story_points_daily_list[i]),
            color='orange',
            linestyle='solid'
        )
        # vertical line segments between neighboring dates for scope story points
        if summed_scope_story_points_daily_list[i] != summed_scope_story_points_daily_list[i + 1]:
            ax.plot(
                (list_of_datetimes[i + 1], list_of_datetimes[i + 1]),
                (summed_scope_story_points_daily_list[i], summed_scope_story_points_daily_list[i + 1]),
                color='orange',
                linestyle='solid'
            )

    # ideal sprint curve
    ax.plot((list_of_datetimes[0], list_of_datetimes[-1]),
            (0, summed_scope_story_points_daily_list[-1]),
            color='black',
            linestyle='solid',
            zorder=-1)

    # dotted horizontal lines for reference
    for i in range(5, summed_scope_story_points_daily_list[-1] + 9, 5):
        ax.axhline(y=i, color='grey', linestyle='dotted', zorder=-2)

    # dotted vertical lines for reference
    # ignore first and and last date
    for date in list_of_datetimes[1:-1]:
        if date.weekday() == FRIDAY:
            plt.axvline(date, linestyle="dotted", zorder=-2)

    plt.xticks(rotation=30)
    # display xticks as day-month
    plt.gca().xaxis.set_major_formatter(dates.DateFormatter('%d-%m'))
    # only display fridays as xticks
    plt.gca().xaxis.set_major_locator(dates.WeekdayLocator(byweekday=dates.FR))

    # yticks for every 5th point
    plt.yticks(
        np.arange(0, max(summed_scope_story_points_daily_list) + 9, 5)
    )

    plt.ylim(bottom=0)

    # define legend
    orange_patch = mpatches.Patch(color='orange', label='Scope')
    blue_patch = mpatches.Patch(color='blue', label='Completed')
    black_patch = mpatches.Patch(color='black', label='Ideal')
    plt.legend(handles=[orange_patch, blue_patch, black_patch], loc='center left', bbox_to_anchor=(1, 0.5))

    plt.title(chart_title, fontsize=22, y=1.03)

    plt.margins(0)

    if save_plot:
        plt.savefig(chart_title, dpi=300, bbox_inches='tight')

    plt.show()


def readExcel(number_of_people):
    filename = './TaskVerwaltung.csv'

    issues = []

    with open(filename, 'r') as csvfile:
        datareader = csv.reader(csvfile)
        for row in datareader:
            issues.append(row)

        people = issues[:1][0][TASKPERSON1:TASKPERSON1 + number_of_people]
        # issues start at second row
        issues = issues[1:]

    return issues, people


def generateBurnupCharts(issues, start_date_of_sprints, end_date_of_sprints, save_plots=False):
    sprint_ranges = [list(sprint) for sprint in zip(start_date_of_sprints, end_date_of_sprints)]

    # generates the burnup chart for all sprints
    generateBurnupChart(issues, start_date_of_sprints, end_date_of_sprints, save_plots)

    # generates individual sprint charts
    for sprint_count, sprint_range in enumerate(sprint_ranges, start=1):
        generateBurnupChartForSprint(issues, *sprint_range, "Sprint " + str(sprint_count), save_plots)


def parseDate(date):
    return datetime.datetime.strptime(date, "%d/%m/%Y").date()


def workedTimePerPersonChart(issues, people, save_plot=False):
    x = [person for person in people]
    y = [0 for _ in people]
    # sum up hours spent from all issues for all persons
    for issue in issues:
        for i in range(len(people)):
            if issue[TASKPERSON1 + i]:
                y[i] += float(issue[TASKPERSON1 + i])
    plt.bar(x, y)
    plt.ylabel("Hours spent")
    plt.title("Total hours spent on all issues", y=1.03, fontsize=22)
    if save_plot:
        plt.savefig('HoursSpent', dpi=300, bbox_inches='tight')
    plt.show()


def main():
    # Define Inputs
    NUMBEROFPEOPLE = 4
    start_dates_of_sprints = [datetime.date(2021, 4, 9), datetime.date(2021, 5, 7), datetime.date(2021, 6, 11)]
    end_dates_of_sprints = [datetime.date(2021, 5, 6), datetime.date(2021, 6, 10), datetime.date(2021, 7, 1)]
    tasks, team = readExcel(NUMBEROFPEOPLE)

    # Specify whether or not to save the created plots in your project folder as png files
    save_plot = True

    # Generate Outputs
    generateBurnupCharts(tasks, start_dates_of_sprints, end_dates_of_sprints, save_plot)
    workedTimePerPersonChart(tasks, team, save_plot)


if __name__ == '__main__':
    main()
