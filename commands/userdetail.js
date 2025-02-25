import { EmbedBuilder } from 'discord.js';

export const name = 'userdetail';
export const description = 'Fetch detailed user information using their user ID';

export async function execute(message, args) {
    // Make sure user ID is provided
    if (!args[0]) {
        return message.reply('Please provide a valid user ID!');
    }

    const userId = args[0];

    try {
        // First, try to fetch the user from the server if they are in the server
        const member = await message.guild.members.fetch(userId);

        // Create an embed for the detailed user info
        const embed = new EmbedBuilder()
            .setColor('#0099ff')
            .setTitle(`${member.user.tag}'s Info`)
            .setThumbnail(member.user.avatarURL())
            .addFields(
                { name: 'Username', value: member.user.username, inline: true },
                { name: 'Discriminator', value: `#${member.user.discriminator}`, inline: true },
                { name: 'Joined Server', value: `<t:${Math.floor(member.joinedTimestamp / 1000)}:f>`, inline: true },
                { name: 'Roles', value: member.roles.cache.map(role => role.name).join(', ') || 'No roles', inline: false }
            )
            .setFooter({ text: `Requested by: ${message.author.username}`, iconURL: message.author.avatarURL() })
            .setTimestamp();

        message.channel.send({ embeds: [embed] });

    } catch (err) {
        // If the user is not in the server, fetch basic public information
        try {
            const user = await message.client.users.fetch(userId);

            // Embed for public user info
            const embed = new EmbedBuilder()
                .setColor('#ff0000')
                .setTitle(`${user.tag}'s Basic Info`)
                .setThumbnail(user.avatarURL())
                .addFields(
                    { name: 'Username', value: user.username, inline: true },
                    { name: 'Discriminator', value: `#${user.discriminator}`, inline: true },
                    { name: 'User ID', value: user.id, inline: true }
                )
                .setFooter({ text: `Requested by: ${message.author.username}`, iconURL: message.author.avatarURL() })
                .setTimestamp();

            message.channel.send({ embeds: [embed] });

        } catch (error) {
            console.error(error);
            message.reply('Could not fetch the user. Please make sure the user ID is valid!');
        }
    }
}
