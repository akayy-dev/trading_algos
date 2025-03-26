import { Bar, LiveStockData } from "./bar.ts";

export class LiveStockDataFactory {
    constructor() {

    }
    public static parseStockData(data): LiveStockData {
        if (data.T == "b" || data.T == "d" || data.T == "u") {
            return new Bar(data);
        }
        return null;
    }
}