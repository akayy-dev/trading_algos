export abstract class Strategy {
    private name: string;
    private balance: string;

    constructor() {

    }

    abstract onBar(bar): void;
    abstract onTrade(trade): void;
}