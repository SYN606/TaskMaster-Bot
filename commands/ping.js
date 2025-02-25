import { EmbedBuilder } from 'discord.js'; // Use require instead of import

export const name = 'ping';
export const description = 'Ping the bot to get its latency!';
export async function execute(message) {
    // Get the latency
    const latency = Date.now() - message.createdTimestamp;
    const apiLatency = Math.round(message.client.ws.ping); // WebSocket API latency


    // Create the embed message
    const embed = new EmbedBuilder() // Use EmbedBuilder instead of MessageEmbed
        .setColor('#0099ff') // Set embed color (blue)
        .setTitle('🏓 Pong!')
        .setDescription('Here is the bot\'s ping and latency details:')
        .addFields(
            { name: 'Latency', value: `${latency}ms`, inline: true },
            { name: 'API Latency', value: `${apiLatency}ms`, inline: true },
            { name: 'Developer', value: '606', inline: true }
        )
        .setTimestamp()
        .setFooter({ text: 'TaskMaster Bot', iconURL: message.client.user.avatarURL() });

    // Send the embed message
    await message.channel.send({ embeds: [embed] });
}
