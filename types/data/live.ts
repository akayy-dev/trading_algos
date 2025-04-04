export abstract class LiveStockData {
    private symbol: string;
    private timestamp: Date;

    constructor(data: {
        S: string;    // Symbol
        t: string;    // Timestamp
    }) {
        this.symbol = data.S;
        this.timestamp = new Date(data.t);
    }


    public getSymbol(): string {
        return this.symbol;
    }
    public getTimestamp(): Date {
        return this.timestamp;
    }
}

export class Bar extends LiveStockData {
    readonly open: number;
    readonly high: number;
    readonly low: number;
    readonly close: number;
    readonly volume: number;

    constructor(data: any) {
        super(data);
        this.open = data.o;
        this.high = data.h;
        this.low = data.l;
        this.close = data.c;
        this.volume = data.v;
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
}

export class Trade extends LiveStockData {
    private id: number;
    private size: number;
    private condition: string[];
    private price: number;

    constructor(data: any) {
        super(data);
        this.id = data.i;
        this.size = data.s;
        this.price = data.p;
        this.condition = data.c;
    }


    public getId(): number {
        return this.id;
    }

    public getSize(): number {
        return this.size;
    }

    public getPrice(): number {
        return this.price;
    }

    public getCondition(): string[] {
        return this.condition;
    }
}