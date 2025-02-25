import { Client, GatewayIntentBits, EmbedBuilder } from 'discord.js';
import { readDB } from './database';  // Import the readDB function
import dotenv from 'dotenv';  // Import dotenv for environment variables
dotenv.config();  // Load environment variables

// Import commands dynamically (make sure you're importing from the correct location)
import commands from './commands'; // Ensure this imports all command files, including help
import utilities from './utils';   // Import utilities

const client = new Client({
    intents: [
        GatewayIntentBits.Guilds,
        GatewayIntentBits.GuildMessages,
        GatewayIntentBits.MessageContent
    ]
});

// Set the bot prefix from the database, default to '!' if not found
const data = readDB();
client.prefix = data?.prefix || '!'; // Use optional chaining for cleaner code

// Attach commands and utilities to the client
client.commands = commands;
client.utils = utilities;

client.once('ready', () => {
    console.log('TaskMaster bot is online!');
});

// Listen for messages
client.on('messageCreate', async (message) => {
    if (message.author.bot) return; // Ignore bot's own messages

    // Check if the bot is mentioned in the message
    if (message.mentions.has(client.user)) {
        // Fetch latency
        const latency = Date.now() - message.createdTimestamp;
        const apiLatency = Math.round(message.client.ws.ping);

        // Get the current prefix
        const currentPrefix = client.prefix;

        // Create the embed message
        const embed = new EmbedBuilder()
            .setColor('#0099ff')
            .setTitle('👋 Hello, I am TaskMaster Bot!')
            .setDescription('Here is some information about me:')
            .addFields(
                { name: 'Developer', value: '606', inline: true },
                { name: 'Prefix', value: currentPrefix, inline: true },
                { name: 'Latency', value: `${latency}ms`, inline: true },
                { name: 'API Latency', value: `${apiLatency}ms`, inline: true }
            )
            .setTimestamp()
            .setFooter({ text: 'TaskMaster Bot', iconURL: message.client.user.avatarURL() });

        // Send the embed message
        await message.channel.send({ embeds: [embed] });
    }

    // If the message starts with the prefix, process commands
    if (!message.content.startsWith(client.prefix)) return;

    const args = message.content.slice(client.prefix.length).trim().split(/ +/); 
    const commandName = args.shift().toLowerCase(); // Get the command name

    // If the command exists, execute it
    const command = client.commands[commandName];
    if (!command) return;

    try {
        // Execute the command
        await command.execute(message, args);
    } catch (error) {
        console.error(error);
        message.reply('There was an error trying to execute that command!');
    }
});

// Log in to Discord with your app's token
client.login(process.env.TOKEN);
