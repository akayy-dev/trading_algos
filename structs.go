package main

import (
	"time"
)

type AuthenticationMessage []struct {
	T   string `json:"T"`
	Msg string `json:"msg"`
}

type Subscriptions []struct {
	T            string        `json:"T"`
	Trades       []string      `json:"trades"`
	Quotes       []string      `json:"quotes"`
	Bars         []string      `json:"bars"`
	UpdatedBars  []interface{} `json:"updatedBars"`
	DailyBars    []string      `json:"dailyBars"`
	Statuses     []string      `json:"statuses"`
	Lulds        []interface{} `json:"lulds"`
	Corrections  []string      `json:"corrections"`
	CancelErrors []string      `json:"cancelErrors"`
}

type Trade struct {
	Type      string    `json:"T"`
	ID        int       `json:"i"`
	Symbol    string    `json:"S"`
	Exchange  string    `json:"x"`
	Price     float64   `json:"p"`
	Size      int       `json:"s"`
	Timestamp time.Time `json:"t"`
	Condition []string  `json:"c"`
	Tape      string    `json:"z"`
}

type Bar struct {
	Type   string    `json:"T"`
	Symbol string    `json:"S"`
	Open   float64   `json:"o"`
	High   float64   `json:"h"`
	Low    float64   `json:"l"`
	Close  float64   `json:"c"`
	Volume int       `json:"v"`
	Time   time.Time `json:"t"`
}
