# Slack Bot Project for Scheduled Messaging

## Description

This project implements a Slack bot that automatically sends messages to specific Slack channels based on a predefined schedule. The bot can mention users in shift messages and send periodic reminders. Configuration is managed through environment variables to ensure security and flexibility.

## Features

- **Send Slack Messages**: Sends messages to specified Slack channels.
- **Hydration Reminders**: Sends hydration reminders on weekdays from 9 AM to 11 PM (Argentina time).
- **Monthly Payroll Reminders**: Sends payroll reminders on the 29th of each month.
- **Inbox Shift Alerts**: Reads data from Google Sheets via Google API to send daily inbox shift alerts based on the user schedule.

## Libraries

- `time`
- `os`
- `random`
- `schedule`
- `google.auth`
- `google.oauth2.service_account.Credentials`
- `googleapiclient.discovery.build`
- `dotenv.load_dotenv`
- `slack_sdk.WebClient`
- `slack_sdk.errors.SlackApiError`
- `datetime`
- `pytz.timezone`

## Usage

1. Install required libraries:
    ```bash
    pip install slack_sdk pytz google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client python-dotenv schedule
    ```

2. Configure Slack API tokens, Google API credentials, and channel IDs.

3. Use the functions `hydrate`, `payroll_monthly`, and `inbox` to automate notifications.

