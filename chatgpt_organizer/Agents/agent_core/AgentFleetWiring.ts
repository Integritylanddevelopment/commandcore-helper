import { AgentFleetBot } from './AgentFleetLogic';

export class AgentFleetManager {
    bots: AgentFleetBot[];

    constructor(botIds: string[]) {
        this.bots = botIds.map(id => new AgentFleetBot(id));
    }

    assignTaskToBot(botId: string, task: string) {
        const bot = this.bots.find(b => b.id === botId);
        if (bot) {
            bot.assignTask(task);
        } else {
            console.error(`Bot with ID ${botId} not found.`);
        }
    }

    broadcastMessage(message: string) {
        this.bots.forEach(bot => bot.communicate(message));
    }

    handleBotError(botId: string, error: string) {
        const bot = this.bots.find(b => b.id === botId);
        if (bot) {
            bot.handleError(error);
        } else {
            console.error(`Bot with ID ${botId} not found.`);
        }
    }
}
