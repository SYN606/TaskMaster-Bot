import { Client, GatewayIntentBits } from 'discord.js';
import { readDB } from './utils';  
import fs from 'fs';
import path from 'path';
require('dotenv').config();

const client = new Client({
    intents: [
        GatewayIntentBits.Guilds,
        GatewayIntentBits.GuildMessages,
        GatewayIntentBits.MessageContent
    ]
});

// Set a default prefix (fallback to '!' if db is empty or unavailable)
let data = readDB();
client.prefix = data ? data.prefix : '!';

// Load commands dynamically from the commands folder
client.commands = {};
const commandFiles = fs.readdirSync(path.join(__dirname, 'commands')).filter(file => file.endsWith('.js'));

for (const file of commandFiles) {
    const command = require(`./commands/${file}`);
    client.commands[command.name] = command;
}

client.once('ready', () => {
    console.log('TaskMaster bot is online!');
});

// Listen for messages
client.on('messageCreate', async (message) => {
    if (message.author.bot) return; // Ignore bot's own messages

    // Check if the message starts with the prefix
    if (!message.content.startsWith(client.prefix)) return;

    const args = message.content.slice(client.prefix.length).trim().split(/ +/); // Split arguments
    const commandName = args.shift().toLowerCase(); // Get the command name

    // Check if the command exists
    if (!client.commands[commandName]) return;

    try {
        // Execute the command
        await client.commands[commandName].execute(message, args);
    } catch (error) {
        console.error(error);
        message.reply('There was an error trying to execute that command!');
    }
});

// Log in to Discord with your app's token
client.login(process.env.TOKEN);
