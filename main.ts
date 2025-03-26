import { createClient } from "@alpacahq/typescript-sdk";
import { Bar, LiveStockData } from "./types/data/live.js";
import { LiveStockDataFactory } from "./types/data/factory.ts";


const client = createClient({
    key: process.env["API_KEY"],
    secret: process.env["SECRET_KEY"]
})



const socket = new WebSocket("wss://stream.data.alpaca.markets/v2/iex")

socket.addEventListener("open", (event) => {

    socket.send(JSON.stringify(
        {
            "action": "auth",
            "key": process.env["API_KEY"],
            "secret": process.env["SECRET_KEY"]
        }
    ))
    console.log("sent auth")

    socket.send(JSON.stringify(
        {
            "action": "subscribe",
            "bars": ["AAPL"],
            "trades": ["AAPL"]
        }
    ))

});



socket.addEventListener("message", async (event) => {
    const data = JSON.parse(await event.data)
    data.forEach((barData) => {
        // avoid accidentally parsing log messages as bars
        if (barData.T.length == 1) {
            console.log(barData)
            console.log(LiveStockDataFactory.parseStockData(barData))
        }
        else {
            console.log(barData)
        }
    }
    )
}
)