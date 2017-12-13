package main

import (
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
	"os/exec"
	"path"
	"strings"
)

var serverFolder = ".//ServerFiles"
var publicParam = "dhparam.pem"

var privateKey = "dhpvtkey.pem"
var publicKey = "dhpubkey.pem"
var peerPublicKey = "peerpubkey.pem"
var secretKey = "secret.bin"

var pubparam = path.Join(serverFolder, publicParam)

func Handler(writer http.ResponseWriter, request *http.Request) {
	//receive shareable public key
	//generate secret key
	//Start Communication

	userIP := strings.Split(request.RemoteAddr, ":")[0]
	userFolder := path.Join(serverFolder, userIP)

	if _, err := os.Stat(userFolder); os.IsNotExist(err) {
		os.MkdirAll(userFolder, os.ModeDir)
	}

	pvtkey := path.Join(userFolder, privateKey)
	pubkey := path.Join(userFolder, publicKey)
	peerpubkey := path.Join(userFolder, peerPublicKey)
	secretkey := path.Join(userFolder, secretKey)

	if _, err := os.Stat(pvtkey); os.IsNotExist(err) {
		GeneratePrivateKey(pubparam, pvtkey)
	}
	if _, err := os.Stat(pubkey); os.IsNotExist(err) {
		ExtractPublickey(pvtkey, pubkey)
	}

	file, err := os.OpenFile(peerpubkey, os.O_CREATE|os.O_TRUNC|os.O_WRONLY, 0600)
	data, _ := ioutil.ReadAll(request.Body)
	file.Write(data)

	if _, err := os.Stat(); os.IsNotExist(err) {

	}

	//RECEIVE PUBLICKEY FILE FROM PEER and
	//Generate Secret
	GenerateSecret(pvtkey, peerpubkey, secretkey)
}

func getDHparam(writer http.ResponseWriter, request *http.Request) {
	// If public parameter is not generated, generate one
	if _, err := os.Stat(publicParam); os.IsNotExist(err) {
		GeneratePublicParam(pubparam)
	}
	data, err := ioutil.ReadFile(publicParam)
	if err != nil {
		fmt.Println(err)
	}
	writer.Write(data)
}

func GeneratePublicParam(fileAbsPath string) {
	os.MkdirAll(serverFolder, os.ModeDir)
	cmd := exec.Command("openssl", "genpkey", "-genparam", "-algorithm", "DH", "-out", fileAbsPath)
	_, err := cmd.Output()
	if err != nil {
		panic(err)
	} else {
		fmt.Println("New Public Parameters File is Created at", fileAbsPath)
	}
}

func GeneratePrivateKey(publicparamfile string, privatekeyfile string) {
	cmd := exec.Command("openssl", "genpkey", "-paramfile", publicparamfile, "-out", privatekeyfile)
	_, err := cmd.Output()
	if err != nil {
		panic(err)
	} else {
		fmt.Println("New Private Key File is Created at", privatekeyfile)
	}
}

func ExtractPublickey(privatekeyfile string, publickeyfile string) {
	cmd := exec.Command("openssl", "pkey", "-in", privatekeyfile, "-pubout", "-out", publickeyfile)
	_, err := cmd.Output()
	if err != nil {
		panic(err)
	} else {
		fmt.Println("New Public Key File is Created at", publickeyfile)
	}
}

func GenerateSecret(inkey string, peerpublikeyfile string, secretfile string) {
	cmd := exec.Command("openssl", "pkeyutl", "-derive", "-inkey", inkey, "-peerkey", peerpublikeyfile, "-out", secretfile)
	_, err := cmd.Output()
	if err != nil {
		panic(err)
	} else {
		fmt.Println("New Secret Key File is Created at", secretfile)
	}
}

func main() {

	//generate public key
	//GeneratePublicParam(pubparam)

	//http.HandleFunc("/dhparam", getDHparam)

	fmt.Println("REM", strings.Split("127.0.0.1:51610", ":")[0])

	//http.HandleFunc("/", Handler)
	//http.ListenAndServe(":9000", nil)
}
