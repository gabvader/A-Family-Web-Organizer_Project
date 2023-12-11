import os
from datetime import date, timedelta


def generate_weekly_days(day):
    first_day = day

    # Calculate the start of the week (Monday)
    # start_of_week = today - timedelta(days=current_weekday)

    weekly_days = []
    for i in range(7):
        current_day = first_day + timedelta(days=i)
        weekly_days.append({
            'date': current_day,
            'weekday': current_day.strftime('%A'),  # Get the weekday name (e.g., 'Monday')
        })

    return weekly_days


def eur(value):
    """Format value as EUR."""
    return f"${value:,.2f}"