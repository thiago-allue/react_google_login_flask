"""
This module provides functionalities to interact with Mock Database files storing quotes and user data.
It includes functions to load quotes, load user data, and save new quotes to the Mock Database file.
"""

import csv
import os
from flask import session


def load_all_quotes():
    """
    Load all quotes from the Mock Database file.

    Returns:
        list: A list of dictionaries containing author and quote information.
    """
    quotes = []

    with open('../db/table_id_quote_author.csv', 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for row in csv_reader:
            # Check for missing keys and log warnings
            missing_keys = [key for key in ['author', 'quote'] if key not in row]

            for key in missing_keys:
                print(f"Row missing '{key}' key: {row}")

            quotes.append({
                'author': row.get('author', 'Unknown Author'),
                'quote': row.get('quote', 'No quote available'),
            })

    return quotes


def load_user_data():
    """
    Load user data from the Mock Database file.

    Returns:
        dict: A dictionary containing email and password pairs.
    """
    users = {}

    with open('../db/table_email_password.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)

        for row in csv_reader:
            users[row[0]] = row[1]

    return users


def load_quotes_for_author(author):
    """
    Load quotes for a specific author from the Mock Database file.

    Args:
        author (str): The name of the author.

    Returns:
        list: A list of dictionaries containing quotes for the specified author.
    """
    quotes = []

    with open('../db/table_id_quote_author.csv', 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for row in csv_reader:
            # Check for missing keys and log warnings
            missing_keys = [key for key in ['title', 'email', 'author', 'quote'] if key not in row]

            for key in missing_keys:
                print(f"Row missing '{key}' key: {row}")

            if row['author'] == author:
                quotes.append({
                    'author': row.get('author', 'Unknown Author'),
                    'quote': row.get('quote', 'No quote available'),
                })

    return quotes


def load_quotes_for_email(email):
    """
    Load quotes for a specific email from the Mock Database file.

    Args:
        email (str): The email address.

    Returns:
        list: A list of dictionaries containing quotes for the specified email.
    """
    quotes = []

    with open('../db/table_id_quote_author.csv', 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for row in csv_reader:
            # Check for missing keys and log warnings
            missing_keys = [key for key in ['title', 'email', 'author', 'quote'] if key not in row]

            for key in missing_keys:
                print(f"Row missing '{key}' key: {row}")

            if row['email'] == email:
                quotes.append({
                    'title': row.get('title', 'Default Title'),
                    'author': row.get('author', 'Unknown Author'),
                    'quote': row.get('quote', 'No quote available'),
                })

    return quotes


def save_quote_to_csv(author, quote):
    """
    Save a new quote to the Mock Database file.

    Args:
        author (str): The name of the author.
        quote (str): The quote text.

    Returns:
        int: The ID of the saved quote or None if an error occurred.
    """
    # Check if the file is writable
    if not os.access('db/table_id_quote_author.csv', os.W_OK):
        print("Error: File 'db/table_id_quote_author.csv' is not writable.")
        return None

    # Determine the next available id_note
    max_id = 0

    try:
        with open('../db/table_id_quote_author.csv', 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)

            for row in csv_reader:
                max_id = max(max_id, int(row['id_note']))

        next_id = max_id + 1

        # Append the new quote to the Mock Database file
        with open('../db/table_id_quote_author.csv', 'a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([next_id, session['email'], author, True, quote])

        return next_id
    except Exception as e:
        print(f"Error writing to file 'db/table_id_quote_author.csv': {e}")
        return None
