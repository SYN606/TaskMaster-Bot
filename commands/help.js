module.exports = {
    name: 'help',
    description: 'Lists all available commands and their descriptions.',
    async execute(message, args) {
        const client = message.client;

        // Fetch all commands dynamically
        const commands = client.commands;
        let helpMessage = '**Here are the available commands:**\n\n';

        // Loop through each command and add its name, description, and usage
        for (const [commandName, command] of Object.entries(commands)) {
            helpMessage += `**${commandName}**: ${command.description}\n`;

            // If a usage example exists for the command, include it
            if (command.usage) {
                helpMessage += `Usage: \`${client.prefix}${commandName} ${command.usage}\`\n\n`;
            } else {
                helpMessage += '\n';
            }
        }

        // Send the help message
        message.channel.send(helpMessage);
    }
};
