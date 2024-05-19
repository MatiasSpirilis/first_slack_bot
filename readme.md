# Slack Bot Project for Scheduled Messaging

## Description

This project implements a Slack bot that automatically sends messages to specific Slack channels based on a predefined schedule. The bot can mention users in shift messages and send periodic reminders. Configuration is managed through environment variables to ensure security and flexibility.

## Features

- **Scheduled Messages**: Sends messages to Slack channels at specific times from Monday to Friday.
- **User Mentions**: Mentions users in messages based on a daily schedule.
- **Periodic Reminders**: Sends reminder messages at regular intervals.
- **Time Zone Handling**: Adjusts sending times to the Argentina time zone.

## Requirements

### Dependencies

- Python 3.x
- Python packages:
  - `python-dotenv`: For managing environment variables.
  - `slack-sdk`: For interacting with the Slack API.
  - `schedule`: For scheduling tasks.
  - `pytz`: For handling time zones.

### Environment Variables

The following variables must be defined in a `.env` file:

- `BOT_KEY`: Slack bot token.
- `CHANNEL_ID_1`: ID of the first Slack channel for periodic reminders.
- `CHANNEL_ID_2`: ID of the second Slack channel for shift messages.
- `MENTION_USERS`: List of users to mention in periodic reminders, separated by spaces.
- `TIME_INTERVAL`: Time interval (in seconds) between each reminder message.
- `MONDAY_USERS`, `TUESDAY_USERS`, `WEDNESDAY_USERS`, `THURSDAY_USERS`, `FRIDAY_USERS`: Lists of users to mention each day of the week, separated by spaces.

## Code Structure

### Imports

Imports necessary libraries and modules such as `time`, `os`, `schedule`, `dotenv`, `slack_sdk`, `datetime`, and `pytz`.

### Environment Variable Configuration

Loads environment variables from a `.env` file located in the same directory as the script.

### Slack Client Initialization

Initializes the Slack client using the bot token from the environment variables.

### Function to Send Slack Messages

Defines a function to send messages to a specified Slack channel and handles potential errors.

### Scheduled Task

Defines a task that runs on weekdays at 4:00 PM (Argentina time), sending a shift message to a specific channel.

### Task Scheduling

Schedules the defined task to run at 4:00 PM from Monday to Friday.

### Main Loop

Implements the main loop of the bot, which periodically sends reminder messages and checks for scheduled tasks to run. The loop can handle interruptions gracefully.

## Usage Instructions

1. **Install Dependencies**: Ensure all dependencies listed in the requirements section are installed.
2. **Configure Environment Variables**: Create a `.env` file in the script directory and define all necessary environment variables.
3. **Run the Script**: Execute the script to start the bot. The bot will automatically send messages according to the defined schedule and environment configurations.