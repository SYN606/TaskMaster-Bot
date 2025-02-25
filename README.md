TaskMaster Bot
==============

Your all-in-one utility bot for Discord

Overview
--------

TaskMaster Bot is a simple utility bot built with Node.js and Discord.js. It helps you manage and automate tasks in your Discord server with ease. The bot includes features like pinging the bot, showing latency, displaying the current server prefix, and more.

Features
--------

*   Custom prefix for each server.
*   Bot latency and API ping information.
*   Dynamic help command to list available bot commands.
*   Developer info and bot status when mentioned.

Setup
-----

To run the bot locally, follow these steps:

1.  Clone this repository:

git clone https://github.com/SYN606/TaskMaster-Bot.git

3.  Navigate to the bot folder:

cd taskmaster-bot

5.  Install dependencies:

npm install

7.  Create a \`.env\` file and add your bot's token:

TOKEN=your-bot-token

9.  Run the bot:

node main.js

Commands
--------

Here is a list of available commands:

*   **!ping** - Returns the bot's latency and API ping.
*   **!help** - Lists all available commands and their descriptions.
*   **!setprefix \[new\_prefix\]** - Changes the prefix for your server.
*   **!botinfo** - Displays information about the bot including developer name and prefix.

Bot Info (When Mentioned)
-------------------------

When you mention the bot, it will respond with an embed containing the following information:

*   Developer: 606
*   Current server prefix
*   Bot latency
*   API latency

Contributing
------------

If you would like to contribute to this bot, feel free to submit a pull request with your changes. Make sure to follow the code style and write clear commit messages.

© 2025 TaskMaster Bot - Developed by 606