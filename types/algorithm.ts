import { createClient, Client} from "@alpacahq/typescript-sdk";
import { AlpacaWebsocket } from "./websocket.ts";

export class Algorithm {
    client: Client

    socket: AlpacaWebsocket

    constructor() {
        this.client = createClient({
            key: process.env["API_KEY"],
            secret: process.env["SECRET_KEY"]
        })

        this.socket = AlpacaWebsocket.getInstance();
    }

    // TODO: Figure out how to parse websockets.
}