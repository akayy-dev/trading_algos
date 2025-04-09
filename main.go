package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"net/url"
	"os"
	"os/signal"

	"github.com/alpacahq/alpaca-trade-api-go/v3/alpaca"
	"github.com/charmbracelet/log"
	"github.com/gorilla/websocket"
)

type Strategy interface {
	onTrade(t Trade)
}

type SMA struct {
	balance float64
	client  alpaca.Client
}

func (s SMA) onTrade(t Trade) {
	for _, trade := range t {
		log.Infof("Trade executed on %s for %.2f", trade.Symbol, trade.Price)

	}
}

func subscribe(s Strategy, symbols []string, interrupt chan os.Signal) {
	// channel will watch for Ctrl-c
	signal.Notify(interrupt, os.Interrupt)

	// Get API Keys
	API_KEY := os.Getenv("API_KEY")
	SECRET := os.Getenv("SECRET_KEY")

	u := url.URL{Scheme: "wss", Host: "stream.data.alpaca.markets", Path: "/v2/iex"}
	log.Infof("Connecting to %s", u.String())

	headers := http.Header{}
	headers.Add("Content-Type", "application/json")
	headers.Add("APCA-API-KEY-ID", API_KEY)
	headers.Add("APCA-API-SECRET-KEY", SECRET)
	c, _, err := websocket.DefaultDialer.Dial(u.String(), headers)

	if err != nil {
		log.Fatal("Error attempting to connect to websocket: ", err)
	}

	for _, symbol := range symbols {
		subscribepayload := map[string]interface{}{
			"action": "subscribe",
			"trades": []string{symbol},
		}

		err = c.WriteJSON(subscribepayload)

		if err != nil {
			log.Fatal("error subscribing: ", err)
		} else {
			log.Infof("Successfully subscribed to $%v", symbol)
		}

	}

	// Responsible for handling different messages
	go func() {
		for {
			_, message, err := c.ReadMessage()

			if err != nil {
				log.Fatal("Error reading websocket message: ", err)
				return
			}

			// Parse the raw message into a list of maps
			var msgMap []map[string]interface{}
			if err := json.Unmarshal(message, &msgMap); err != nil {
				log.Error("Error unmarshalling JSON to list of maps:", err)
				return
			}

			for _, rawMsg := range msgMap {
				msgType := rawMsg["T"]
				switch msgType {
				case "t":
					var trade Trade
					if err := json.Unmarshal(message, &trade); err != nil {
						log.Error("Error occured while Unmarshaling trade data")
						fmt.Println(string(message))
					}
					s.onTrade(trade)
				}
			}

		}
	}()

}

func main() {
	client := alpaca.NewClient(alpaca.ClientOpts{
		APIKey:    os.Getenv("API_KEY"),
		APISecret: os.Getenv("SECRET_KEY"),
		BaseURL:   "https://paper-api.alpaca.markets",
	})

	acct, err := client.GetAccount()
	if err != nil {
		// shut down if we can't get the account
		panic(err)
	}
	fmt.Printf("%+v\n", *acct)
	log.Info("Retrieved account")

	balance := 500.4
	smaStrategy := SMA{
		balance: balance,
		client:  *client,
	}
	log.Infof("Creating SMA strategy with a balance of $%.2f", balance)

	symbols := []string{"SPY", "SH"}

	interrupt := make(chan os.Signal, 1)
	go subscribe(smaStrategy, symbols, interrupt)
	log.Info(<-interrupt)

}
