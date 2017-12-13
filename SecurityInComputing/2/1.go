package main

import (
	"crypto/aes"
	"crypto/cipher"
	"crypto/rand"
	"encoding/hex"
	"fmt"
	"hash/fnv"
	"io"
	"io/ioutil"
)

func AesCBCEncrypt(key_ string, plaintext_ string) string {
	key := []byte(key_)
	plaintext := []byte(plaintext_)

	if len(plaintext)%aes.BlockSize != 0 {
		panic("plaintext is not a multiple of the block size")
	}

	block, err := aes.NewCipher(key)
	if err != nil {
		panic(err)
	}

	ciphertext := make([]byte, aes.BlockSize+len(plaintext))
	iv := ciphertext[:aes.BlockSize]
	if _, err := io.ReadFull(rand.Reader, iv); err != nil {
		panic(err)
	}

	mode := cipher.NewCBCEncrypter(block, iv)
	mode.CryptBlocks(ciphertext[aes.BlockSize:], plaintext)

	return fmt.Sprintf("%x", ciphertext)
}

func AesCBCDecrypter(key_ string, cipher_ string) string {
	key := []byte(key_)
	ciphertext, _ := hex.DecodeString(cipher_)

	block, err := aes.NewCipher(key)
	if err != nil {
		panic(err)
	}

	if len(ciphertext) < aes.BlockSize {
		panic("ciphertext too short")
	}
	iv := ciphertext[:aes.BlockSize]
	ciphertext = ciphertext[aes.BlockSize:]

	if len(ciphertext)%aes.BlockSize != 0 {
		panic("ciphertext is not a multiple of the block size")
	}

	mode := cipher.NewCBCDecrypter(block, iv)
	mode.CryptBlocks(ciphertext, ciphertext)

	return fmt.Sprintf("%s", ciphertext)
}

var P int64 = 23
var G int64 = 5

func publicKey(G int64, P int64, a uint64) int64 {
	tempG := G
	var i uint64 = 0
	for ; i < a; i++ {
		tempG = (tempG * G) % P
	}
	return tempG
}

func hashValueOf(key string) uint64 {
	h := fnv.New64a()
	h.Write([]byte(key))
	return h.Sum64()
}

func main() {

	//key := "example key 1234example key 1234"
	//a := hashValueOf(key)
	//var a uint64 = 4010
	//key_i := publicKey(G, P, a)
	//key := strconv.FormatInt(key_i, 10)

	plainText := "exampleplaintext"
	text, _ := ioutil.ReadFile("secret1.bin")
	key1 := string(text[0:32])
	//fmt.Println("Key1 : ", key1)

	c := AesCBCEncrypt(key1, plainText)
	fmt.Println("Cipher Text :", c)

	text, _ = ioutil.ReadFile("secret2.bin")
	key2 := string(text[0:32])
	t := AesCBCDecrypter(key2, c)
	fmt.Println("Plain Text : ", t)

}
