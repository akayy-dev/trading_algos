import { Bar, LiveStockData, Trade } from "./live.js";

export class LiveStockDataFactory {
    constructor() {

    }
    public static parseStockData(data): LiveStockData {
        if (data.T == "b" || data.T == "d" || data.T == "u") {
            return new Bar(data);
        }
        else if (data.T == "t") {
            return new Trade(data);
            console.log(data)
        }
    }
}