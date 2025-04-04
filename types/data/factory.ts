import { Bar, LiveStockData, Trade } from "./live.ts";

export class LiveStockDataFactory {
    constructor() {

    }
    public static parseStockData(data): LiveStockData {
        if (data.T == "b" || data.T == "d" || data.T == "u") {
            const bar = new Bar(data);
            return bar
        }
        else if (data.T == "t") {
            const trade = new Trade(data)
            return trade;
        } else {
            return null;
        }
    }
}