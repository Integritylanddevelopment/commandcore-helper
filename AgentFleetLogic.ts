export class AgentFleetBot {
    id: string;
    status: string;
    tasks: string[];

    constructor(id: string) {
        this.id = id;
        this.status = 'idle';
        this.tasks = [];
    }

    assignTask(task: string) {
        if (this.status === 'idle') {
            this.tasks.push(task);
            this.status = 'busy';
            console.log(`Task "${task}" assigned to bot ${this.id}.`);
        } else {
            console.log(`Bot ${this.id} is currently busy.`);
        }
    }

    completeTask() {
        if (this.tasks.length > 0) {
            const completedTask = this.tasks.shift();
            console.log(`Bot ${this.id} completed task "${completedTask}".`);
            this.status = this.tasks.length > 0 ? 'busy' : 'idle';
            this.upgradeBot(); // Upgrade bot after task completion
            AgentCore.upgradeCore(); // Upgrade agent core after task completion
        } else {
            console.log(`Bot ${this.id} has no tasks to complete.`);
        }
    }

    communicate(message: string) {
        console.log(`Bot ${this.id} says: ${message}`);
    }

    handleError(error: string) {
        console.error(`Bot ${this.id} encountered an error: ${error}`);
        this.status = 'error';
    }

    reportToAgentCorps() {
        console.log(`Bot ${this.id} reporting to agent corps. Status: ${this.status}, Tasks: ${this.tasks.join(', ')}`);
    }

    trainBot() {
        console.log(`Bot ${this.id} is being trained.`);
        // Simulate training logic
        console.log(`Bot ${this.id} training complete.`);
    }

    upgradeBot() {
        console.log(`Bot ${this.id} is being upgraded.`);
        // Simulate upgrade logic
        console.log(`Bot ${this.id} upgrade complete.`);
    }
}

export class AgentCore {
    static upgradeCore() {
        console.log('Agent core is being upgraded.');
        // Simulate core upgrade logic
        console.log('Agent core upgrade complete.');
    }

    static trainAllAgents(agents: AgentFleetBot[]) {
        console.log('Training all agents in the fleet.');
        agents.forEach(agent => agent.trainBot());
        console.log('All agents training complete.');
    }
}
