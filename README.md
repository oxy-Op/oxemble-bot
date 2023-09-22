# Oxemble

A versatile Discord bot packed with gambling, economy, fun, emotes, and utility features. 

## Features

- Economy bot, supports features such as balance, send, daily, topranks etc
- Utilites features such as botinfo, userinfo, serverinfo, etc
- Actions and emote gifs
- SQL and Redis Integrated
- Highly customizable

### Cons
 - Do not support every event logs and analytics
 - Do not support buy/sell feature

 Note that this is high-level overview, there are more features and information, please use `!help` or `/help` for more information about respective commands.



## Installation


```bash
$ git clone https://github.com/oxy-Op/oxemble-bot.git
$ cd oxemble-bot
$ pip install -r requirements.txt
$ python main.py
```

# Configuration Guide

To configure your bot, follow these steps:

## Step 1: Prerequisites

Before you start configuring your bot, make sure you have the following:

- [ ] Discord Bot Token
- [ ] Giphy API Key 
- [ ] MySQL Workbench
- [ ] Redis Server

## Step 2: JSON Configuration

Edit the `config.json` file with the following details:

```json
{
    "prefix": "!",
    "owner_id": 123,
    "giphy_api_key": "Your_Giphy_API_Key",
    "activity": [
        "Prefix: ! | Listening !help",
        "https://github.com/oxy-Op",
        "One xemble a day keeps sadness away"
    ],
    "token": "Your_Bot_Token",
    "balance": "your balance is ",
    "emoji": [
        "<:coin1:1115740536981164053>",
        "<:coin2:1115740556094603314>"
    ],
    "database": {
        "host": "localhost",
        "port": 3304,
        "user": "root",
        "pass": "Your_DB_Password",
        "database": "oxemble"
    },
    "redis": {
        "host": "localhost",
        "port": 6379,
        "pass": "Your_Redis_Password"
    }
}
```

## Step 3: Bot Token

To obtain a Discord bot token, follow these steps:

1. Visit the [Discord Developer Portal](https://discord.com/developers/applications).
2. Create a new application.
3. Navigate to the "Bot" section and click "Add Bot."
4. Under the "Token" section, click "Copy" to copy your bot token.
5. Paste the bot token into the `token` field in your `config.json` file.

## Step 4: Database Setup

If you're using a MySQL database, create a database named "oxemble" (default) and fill in the `database` section in your `config.json` with your database host, port, user, and password.

## Step 5: Redis Setup

If you're using Redis for caching or other purposes, provide your Redis host, port, and password in the `redis` section in your `config.json`.

## Step 6: Save Configuration

Save your `config.json` file with the updated settings.

## Step 7: Start the Bot

Now that your bot is configured, you can run it with the specified settings.
  You should get "ready as bot name" in your console. Now go to the discord and type `/help` for slash commands help or `!help` for general commands

