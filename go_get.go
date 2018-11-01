package main

import (
	"database/sql"
	"fmt"
	"github.com/antchfx/htmlquery"
	_ "github.com/go-sql-driver/mysql"
	"golang.org/x/net/html"
	"golang.org/x/net/html/charset"
	"io/ioutil"
	"log"
	. "net/http"
	"strconv"
	"strings"
	"sync"
	"time"
)

type Items struct {
	index   int
	sub_url string
	name    string
}

type Worker struct {
	id        int
	urlChan   chan string
	itemsChan chan Items
	wg        *sync.WaitGroup
}

func (w Worker) Run() {
	log.Println("create worker id:", w.id)
	go fetchByQuery(w.id, w.urlChan, w.itemsChan)
	go saver(w.id, w.wg, w.itemsChan)
}

var urlTags = [][2]string{
	{"B", "25"},
	{"C", "25"},
	{"D", "25"},
	{"E", "25"},

}

func httpGet(url string) (*html.Node, error) {

	client := &Client{}
	req, _ := NewRequest("GET", url, strings.NewReader("name=cjb"))

	req.Header.Set("Content-Type", "text/html;charset=utf-8")
	req.Header.Set("User-Agent", "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) "+
		"AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1")
	req.Header.Set("Connection", " keep-alive")

	resp, err := client.Do(req)
	if err != nil {
		panic(err)
	}
	defer resp.Body.Close()

	r, err := charset.NewReader(resp.Body, "text/html;charset=utf-8")
	if err != nil {
		panic(err)
	}
	return htmlquery.Parse(r)
}



func IoUtil(name string) string {
	if contents, err := ioutil.ReadFile(name); err == nil {
		result := strings.Replace(string(contents), "\n", "", 1)
		//fmt.Println(result)
		return result
	}
	return ""

}

func main() {
	t1 := time.Now()
	const workerNum = 50
	urlChan := make(chan string, 20)
	var wg sync.WaitGroup
	for i := 0; i < workerNum; i++ {
		worker := Worker{
			i, urlChan,
			make(chan Items, 100),
			&wg,
		}
		wg.Add(1)
		worker.Run()
	}

	//go func() {
	for i := 0; i < len(urlTags); i++ {
		num, _ := strconv.Atoi(urlTags[i][1])
		var lastUrl string
		for j := 1; j < num+1; j++ {
			url := fmt.Sprintf("http://shop.99114.com/list/pinyin/%s_%d", urlTags[i][0], j)
			urlChan <- url
			lastUrl =url
		}
		log.Println(lastUrl)
		//println(url)
	}

	close(urlChan)
	wg.Wait()
	elapsed := time.Since(t1)
	fmt.Println("App elapsed: ", elapsed)

}

func fetchByQuery(id int, urls chan string, r chan Items) {
	for url := range urls {
		//fmt.Printf("work:%d-url:%s done.\n",id,url)

		doc, err := httpGet(url)
		if err != nil {
			panic(err)
		}
		for _, n := range htmlquery.Find(doc, "//*[@id=\"footerTop\"]/ul/li/a") {
			sub_url := htmlquery.InnerText(htmlquery.FindOne(n, "@href"))
			name := htmlquery.InnerText(htmlquery.FindOne(n, "b/text()"))
			splits := strings.Split(sub_url, "/")
			index, err := strconv.Atoi(splits[len(splits)-1])
			if err == nil {
				r <- Items{index, sub_url, name}
			} else {
				return
			}
		}

	}
	log.Println("close worker items chan: ", id)
	close(r)
}

func saver(id int, wg *sync.WaitGroup, items chan Items) {
	dbline := IoUtil("dbline.txt")
	db, err := sql.Open("mysql", dbline+"@tcp(127.0.0.1:3306)/trnet?parseTime=true")
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()
	for i := range items {
		cmd := fmt.Sprintf("INSERT INTO company_test (id, content, sub) VALUES (%d,'%s','%s')", i.index, i.name, i.sub_url)
		_, err := db.Exec(cmd)
		if err != nil {
			log.Println(err)
		}

	}
	wg.Add(-1)
}
