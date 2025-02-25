
import { Client, GatewayIntentBits } from 'discord.js';
require('dotenv').config();

const client = new Client({
    intents: [
        GatewayIntentBits.Guilds,
        GatewayIntentBits.GuildMessages,
        GatewayIntentBits.MessageContent
    ]
});

client.once('ready', () => {
    console.log('TaskMaster bot is online!');
});

client.on('messageCreate', message => {
    if (message.author.bot) return;

    if (message.content === '!ping') {
        message.channel.send('Pong!');
    }
});

// Log in to Discord with your app's token
client.login(process.env.TOKEN);
