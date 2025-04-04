import { Bar, LiveStockData, Trade } from "./types/data/live.ts";
import { Instrument, Strategy } from "./types/strategy.ts";


class TestStrategy extends Strategy {
    constructor() {
        super("TestStrategy", new Instrument("FAKEPACA"), 1000)
    }
    protected async init(): Promise<void> {
        // await this.subscribe(["FAKEPACA"])
        console.log("Initialized strategy")
    }
    protected async onBar(bar: Bar): Promise<void> {
        console.log("Bar: ", bar)
    }
    protected async onTrade(trade: Trade): Promise<void> {
        console.log("Trade: ", trade)
    }
}

const test = new TestStrategy();
test.run()