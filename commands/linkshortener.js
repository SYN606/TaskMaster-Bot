import shortid from 'shortid';
import { readDB, writeDB } from '../database'; // Import read/write DB functions
import { EmbedBuilder } from 'discord.js';

export const name = 'linkshortener';
export const description = 'Shortens a provided URL and handles user URL limits';

const getUserData = (userId) => {
    const data = readDB();
    if (!data.users) data.users = {};  // Initialize the users data if not present
    return data.users[userId] || { shortenedLinks: [], lastReset: Date.now() };  // Default to empty object if no user data exists
};

const updateUserData = (userId, userData) => {
    const data = readDB();
    data.users[userId] = userData;
    writeDB(data);
};

// Utility function to check and reset limits
const checkAndResetLimits = (userId) => {
    const userData = getUserData(userId);
    const now = Date.now();
    const timeDiff = now - userData.lastReset;

    // If more than 24 hours have passed, reset the user limit and shorten links
    if (timeDiff >= 24 * 60 * 60 * 1000) {
        userData.shortenedLinks = [];  // Reset the list of shortened links
        userData.lastReset = now;  // Update the last reset time
        updateUserData(userId, userData);
    }
};

export async function execute(message, args) {
    const userId = message.author.id;
    checkAndResetLimits(userId);  // Ensure user limit is up to date

    // Handle "list" command to show all shortened links
    if (args[0] === 'list') {
        const userData = getUserData(userId);
        if (userData.shortenedLinks.length === 0) {
            return message.reply('You have no shortened links.');
        }

        // Create an embed to display shortened links
        const embed = new EmbedBuilder()
            .setColor('#0099ff')
            .setTitle('Your Shortened Links')
            .setDescription('Here are the links you have shortened:')
            .addFields(userData.shortenedLinks.map((linkData, index) => ({
                name: `Link ${index + 1}`,
                value: `[${linkData.originalUrl}](https://yourdomain.com/${linkData.shortId}) - Expires in <t:${Math.floor(linkData.expiry / 1000)}:R>`
            })));

        return message.channel.send({ embeds: [embed] });
    }

    // Handle "remove" command to remove a shortened link
    if (args[0] === 'remove' && args[1]) {
        const shortId = args[1];
        const userData = getUserData(userId);

        const linkIndex = userData.shortenedLinks.findIndex(link => link.shortId === shortId);
        if (linkIndex === -1) {
            return message.reply('No shortened link found with that ID.');
        }

        // Remove the link and update the DB
        userData.shortenedLinks.splice(linkIndex, 1);
        updateUserData(userId, userData);

        return message.reply('The shortened link has been removed.');
    }

    // Handle "shorten" or default case
    if (!args[0] || !args[0].startsWith('http')) {
        return message.reply('Please provide a valid URL to shorten!');
    }

    // Handle URL shortening
    const userData = getUserData(userId);
    const url = args.join(' ');

    // Check the user’s URL limit
    const limit = message.member.permissions.has('ADMINISTRATOR') ? 15 : 10;  // 15 for admins, 10 for normal users
    if (userData.shortenedLinks.length >= limit) {
        return message.reply(`You have reached your limit of ${limit} shortened URLs. Please wait until your limit is reset (24 hours).`);
    }

    // Create the shortened link
    const shortId = shortid.generate();
    const expiryTime = Date.now() + 24 * 60 * 60 * 1000; // Link expires in 24 hours

    // Store the shortened link
    const newLink = {
        shortId,
        originalUrl: url,
        expiry: expiryTime
    };

    userData.shortenedLinks.push(newLink);
    updateUserData(userId, userData);

    // Send a confirmation message
    const embed = new EmbedBuilder()
        .setColor('#0099ff')
        .setTitle('Your Shortened Link')
        .setDescription(`**Shortened Link**: [https://yourdomain.com/${shortId}](https://yourdomain.com/${shortId})`)
        .addFields(
            { name: 'Original URL', value: url },
            { name: 'Expires In', value: `<t:${Math.floor(expiryTime / 1000)}:R>` }
        )
        .setFooter({ text: 'TaskMaster Bot - Developer: 606' })
        .setTimestamp();

    message.channel.send({ embeds: [embed] });
}
