import { createClient, Client} from "@alpacahq/typescript-sdk";

export class Algorithm {
    client: Client
    constructor() {
        this.client = createClient({
            key: process.env["API_KEY"],
            secret: process.env["SECRET_KEY"]
        })
    }

    // TODO: Figure out how to parse websockets.
}