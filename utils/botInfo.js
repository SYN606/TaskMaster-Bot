const { MessageEmbed } = require('discord.js');

module.exports = {
    name: 'botInfo',
    description: 'Send bot info with ping, latency, prefix, and bot name',
    async execute(message, client) {
        // Get latency
        const ping = Date.now() - message.createdTimestamp;
        const apiPing = Math.round(client.ws.ping); // WebSocket API latency

        // Create the embed message
        const embed = new MessageEmbed()
            .setColor('#0099ff')
            .setTitle('Bot Information')
            .setDescription('Here is the bot information:')
            .addFields(
                { name: '🏓 Latency', value: `${ping}ms`, inline: true },
                { name: '🌐 API Latency', value: `${apiPing}ms`, inline: true },
                { name: 'Prefix', value: `\`${client.prefix}\``, inline: true },
                { name: 'Bot Name', value: 'TaskMaster (created by 606)', inline: true }
            )
            .setTimestamp()
            .setFooter({ text: 'TaskMaster Bot' });

        // Send the embed in the current channel
        await message.channel.send({ embeds: [embed] });
    }
};
