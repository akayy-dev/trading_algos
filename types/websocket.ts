import { resolve } from "path"
import { LiveStockDataFactory } from "./data/factory.ts"
import { Bar, LiveStockData, Trade } from "./data/live.ts"


// define the structure of a method
type StockCallback = (a: LiveStockData) => any

class CallbackManager {
    private callbacks: { [key: string]: StockCallback[] } = {};

    add(symbol: string, callback: StockCallback) {
        if (!this.callbacks[symbol]) {
            this.callbacks[symbol] = [];
        }
        this.callbacks[symbol].push(callback);
    }

    execute(symbol: string, data: LiveStockData) {
        const callbacks = this.callbacks[symbol] || [];
        callbacks.forEach(callback => callback(data));
    }
}

export class AlpacaWebsocket {
    private socket: WebSocket;
    private static instance: AlpacaWebsocket;
    private connectionPromise: Promise<void>;

    private tradeCallbacks: CallbackManager;
    private barCallbacks: CallbackManager;

    private constructor() {
        this.socket = new WebSocket("wss://stream.data.alpaca.markets/v2/test");
        this.tradeCallbacks = new CallbackManager();
        this.barCallbacks = new CallbackManager();

        this.connectionPromise = new Promise((resolve, reject) => {
            this.socket.addEventListener("open", () => {
                this.socket.send(JSON.stringify({
                    "action": "auth",
                    "key": process.env["API_KEY"],
                    "secret": process.env["SECRET_KEY"]
                }));
                console.log("AlpacaWebsocket Opened Connection")
                resolve();
            });

            this.socket.addEventListener("error", (error) => {
                reject(error);
            });

            this.socket.addEventListener("close", (event) => {
                console.log("AlpacaWebSocket connection closed: ", event.code, event.reason)
            })
        });

        this.socket.addEventListener("message", async (event) => {
            try {
                const data = await JSON.parse(event.data);
                data.forEach(d => {
                    if (d.T == "t") {
                        console.log("trade");
                        console.log(d);
                        const stockData = LiveStockDataFactory.parseStockData(d);
                        this.tradeCallbacks.execute(d.S, stockData);
                    }
                    if (d.T == "b" || d.T == "d" || d.T == "u") {
                        console.log("bar");
                        console.log(d);
                        const stockData = LiveStockDataFactory.parseStockData(d);
                        this.barCallbacks.execute(d.S, stockData);
                    }
                });
            } catch (error) {
                console.error('Error processing message:', error);
            }
        });
    }

    public async subscribeTrades(symbol: string, callback: (a: LiveStockData) => any) {
        try {
            // Wait for connection before subscribing
            await this.connectionPromise;

            this.tradeCallbacks.add(symbol, callback)

            this.socket.send(JSON.stringify({
                "action": "subscribe",
                "trades": [symbol]
            }));

            console.log(`Subscribing to ${symbol} trades`)

        } catch (error) {
            console.error('Error subscribing:', error);
            throw error; // Re-throw if you want to handle it at a higher level
        }
    }


    public async subscribeBars(symbol: string, callback: (a: LiveStockData) => any) {
        try {
            // Wait for connection before subscribing
            await this.connectionPromise;

            this.barCallbacks.add(symbol, callback)

            this.socket.send(JSON.stringify({
                "action": "subscribe",
                "bars": [symbol],
            }));

            console.log(`Subscribing to ${symbol} bars`)

        } catch (error) {
            console.error('Error subscribing:', error);
            throw error; // Re-throw if you want to handle it at a higher level
        }
    }



    public static getInstance() {
        if (!this.instance) {
            this.instance = new AlpacaWebsocket()
        }
        return this.instance;
    }
}

const i = AlpacaWebsocket.getInstance()
// i.subscribeTrades("FAKEPACA", async (data: Trade) => { console.log(`Trade: ${typeof (data)}`) })
// i.subscribeBars("FAKEPACA", async (data: Bar) => { console.log(`Bar: ${typeof (data)}`) })