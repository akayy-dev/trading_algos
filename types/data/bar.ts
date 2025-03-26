export class LiveStockData {
    private symbol: string;
    private open: number;
    private high: number;
    private low: number;
    private close: number;
    private volume: number;
    private timestamp: Date;

    constructor(data: {
        S: string;    // Symbol
        o: number;    // Open
        h: number;    // High
        l: number;    // Low
        c: number;    // Close
        v: number;    // Volume
        t: string;    // Timestamp
    }) {
        this.symbol = data.S;
        this.open = data.o;
        this.high = data.h;
        this.low = data.l;
        this.close = data.c;
        this.volume = data.v;
        this.timestamp = new Date(data.t);
    }

    public getSymbol(): string {
        return this.symbol;
    }

    public getOpen(): number {
        return this.open;
    }

    public getHigh(): number {
        return this.high;
    }

    public getLow(): number {
        return this.low;
    }

    public getClose(): number {
        return this.close;
    }

    public getVolume(): number {
        return this.volume;
    }

    public getTimestamp(): Date {
        return this.timestamp;
    }
}

export class Bar extends LiveStockData {
}
