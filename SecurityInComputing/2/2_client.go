package main

import (
	"fmt"
	"net/http"
)

func main() {
	client := http.Client{}
	req, err := http.NewRequest("GET", "http://127.0.0.1:9000", nil)
	if err != nil {
		fmt.Println(err)
	}
	resp, err := client.Do(req)
	if err != nil {
		fmt.Println(err)
	}

}
