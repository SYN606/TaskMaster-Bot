import { createData, updateData, readData, deleteData } from '../database'; // Import the DB functions
import { EmbedBuilder } from 'discord.js'; // Import EmbedBuilder for Discord v14 embeds

export const name = 'activity';
export const description = 'Start or stop a user activity';

export async function execute(message, args) {
    // If no activity command provided
    if (!args[0]) {
        return message.reply('Please specify an activity! Usage: `!activity <activity name>`');
    }

    const userId = message.author.id;
    const activityType = args[0]; // The activity type (e.g., "playing", "watching", etc.)
    const activityName = args.slice(1).join(' ') || 'Some activity'; // Activity name (rest of the args)

    // Check if the user already has an ongoing activity
    const currentActivity = readData('activities', userId);

    // If the user already has an activity, update it or stop it
    if (args[0].toLowerCase() === 'stop') {
        if (currentActivity) {
            // Stop the activity and remove it from the database
            deleteData('activities', userId);
            return message.reply('Your activity has been stopped!');
        } else {
            return message.reply('You do not have an activity to stop!');
        }
    }

    // If the user does not have an ongoing activity, start a new one
    if (currentActivity) {
        return message.reply('You already have an ongoing activity. Type `!activity stop` to stop it first.');
    }

    // Create activity data for the user
    const activityData = {
        activityType, // 'Playing', 'Watching', etc.
        activityName, // The name of the activity
        startTime: Date.now(), // The time the activity started
        elapsedTime: 0 // The time spent on the activity (will be updated as time passes)
    };

    // Create the activity in the DB
    createData('activities', userId, activityData);

    // Update bot's presence to reflect the user's activity
    message.client.user.setPresence({
        activities: [{
            name: `${activityType} ${activityName}`, // Set activity status
            type: activityType.toUpperCase() // Convert 'playing' or 'watching' to ActivityType
        }],
        status: 'online' // Bot status (you can change it to 'idle' or 'dnd' if needed)
    });

    // Send a message to confirm the activity has started
    const embed = new EmbedBuilder()  // Use EmbedBuilder instead of MessageEmbed
        .setColor('#0099ff')
        .setTitle('Activity Started')
        .setDescription(`**Activity**: ${activityType} ${activityName}`)
        .addFields({ name: 'Started at', value: `<t:${Math.floor(activityData.startTime / 1000)}:f>` })
        .setFooter({ text: 'TaskMaster Bot - Developer: 606', iconURL: 'https://cdn.discordapp.com/attachments/1046847428755734609/1343871216179744848/Purple_Aquamarine_Art_Pixel_Art_Discord_Profile_Banner.jpg' }) // Developer footer
        .setTimestamp();

    message.channel.send({ embeds: [embed] });
}
