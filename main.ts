import { createClient } from "@alpacahq/typescript-sdk";


const client = createClient({
    key: process.env["API_KEY"],
    secret: process.env["SECRET_KEY"]
})


// client.getAsset({
//     symbol_or_asset_id: "NVDA"
// }).then(console.log)


const socket = new WebSocket("wss://paper-api.alpaca.markets/stream")

socket.addEventListener("open", (event) => {
    socket.send(JSON.stringify(
        {
            "action": "auth",
            "key": process.env["API_KEY"],
            "secret": process.env["SECRET_KEY"]
        }
    ))

    socket.send(JSON.stringify(
        {
            "action": "listen",
            "data": {
                "streams": ["trade_updates"]
            }
        }
    ))

});


console.log("sent listen signal")

socket.addEventListener("message", async (event) => {
    console.log(await event.data.text())
})