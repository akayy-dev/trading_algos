import { Bar, LiveStockData, Trade } from "./data/live.ts";
import { AlpacaWebsocket } from "./websocket.ts";

export abstract class Strategy {
    private name: string;
    private balance: string;
    readonly instrument: Instrument;
    private cash: number;

    private socket: AlpacaWebsocket

    constructor(name: string, instrument: Instrument, cash: number) {
        this.name = name
        this.instrument = instrument
        this.cash = cash
        this.socket = AlpacaWebsocket.getInstance()

        this.init().then(() => { console.log("Initialized Strategy") })
    }

    /**
     * Runs before the algorithm starts
     */
    protected async init() { }

    /**
     * Subscribe to a symbols trades and bars.
     * @param symbols a list of symbols to subscribe to
     */
    protected async subscribe(symbols: string[]) {
        for (let i = 0; i < symbols.length; i++) {
            console.log(`Subscribing to ${symbols[i]}`)
            this.socket.subscribeBars(symbols[i], (bar: LiveStockData) => { this.onBar(bar) })
            this.socket.subscribeTrades(symbols[i], (trade: LiveStockData) => { this.onTrade(trade) })
        }
    }

    protected async onBar(bar: Bar) { }
    protected async onTrade(trade: Trade) { }

    public async run() {
        await this.subscribe([this.instrument.symbol])
        console.log("Running strategy")
    }
}

export class Instrument {
    readonly symbol: string
    constructor(symbol: string) {
        this.symbol = symbol
    }
}

export class Group {
    readonly name: string

    constructor(name) {
        this.name = name;
    }
}