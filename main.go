package main

import (
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
}

func subscribe(s Strategy, symbol string, interrupt chan os.Signal) {
	// channel will watch for Ctrl-c
	signal.Notify(interrupt, os.Interrupt)

	u := url.URL{Scheme: "wss", Host: "stream.data.sandbox.alpaca.markets", Path: "/v2/iex"}
	log.Infof("Connecting to %s", u.String())

	headers := http.Header{}
	headers.Add("Content-Type", "application/json")
	headers.Add("APCA-API-KEY-ID", os.Getenv("API_KEY"))
	headers.Add("APCA-API-SECRET-KEY", os.Getenv("SECRET_KEY"))
	c, _, err := websocket.DefaultDialer.Dial(u.String(), headers)

	if err != nil {
		log.Fatal("dial: ", err)
	}

	subscribePayload := map[string]interface{}{
		"action": "subscribe",
		"trades": []string{symbol},
	}

	err = c.WriteJSON(subscribePayload)
	if err != nil {
		log.Fatal("Error subscribing: ", err)
	}

	go func() {
		for {
			_, message, err := c.ReadMessage()
			if err != nil {
				log.Fatal("read goroutine: ", err)
				return
			}

			log.Printf("recv: %s", message)
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

	interrupt := make(chan os.Signal, 1)
	go subscribe(smaStrategy, "SPY", interrupt)
	log.Info(<-interrupt)

}
