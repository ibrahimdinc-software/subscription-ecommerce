class ProductSelector {
    constructor(element) {
        this.element = element
        this.pricing = element.parentElement.parentElement

        this.buttons = [] // ürün ekleme butonları
        this.standart_button = 3 // standart buton sayısı

        this.productList = $("#productList") // ürün listesi
        this.selectButtons = document.getElementsByName("selectButton") // ürün seçme butonları


        this.now_psb = "" // şu anki buton id

        this.price_text = document.getElementById("price-text") // fiyat yazısı
        this.price = 0.0 // fiyat

        this.cargo_text = document.getElementById("cargo-text") // kargo yazısı

        this.products = [] // ürünler listesi
        this.backend_products = document.getElementById("id_products") // backend için gereken seçili ürün bilgisi

        // standart buton sayısı kadar buton oluştur
        for (let i = 0; i < this.standart_button; i++) {
            this.createButton(null, "psb_" + i.toString())
        }
        this.createButton("add") // ekleme butonu oluştur

        // ürün seçme butonlarına fonksiyon ata
        for (let i = 0; i < this.selectButtons.length; i++) {
            this.selectButtons[i].addEventListener("click", () => {
                this.selectButton(this.selectButtons[i].getAttribute("find"))
            })
        }
    }

    // buton oluşturma fonksiyonu
    // add ekleme butonu veya silinebilir buton olup olmadığını belirtir.
    // psb_id buton id'si belirtir 'psb_X' şeklindedir.
    createButton(add = null, psb_id = null) {
        var e = document.createElement("div") // ana gövde
        var b = document.createElement("div") // buton gövdesi

        e.classList.add("col-md-4", "col-6", "my-auto") // gövde özellikleri
        b.classList.add("btn", "btn-block", "btn-outline-primary") // gövde özellikleri

        e.appendChild(b) // ana gövde içine buton eklemesi

        // ekleme butonu değilse veya silinebilir buton değilse çalışır 
        if (add == null || add == "deletable") {
            b.textContent = "Ürün Seç" // buton metni ataması
            b.setAttribute("name", "productSelectList") // buton ismi ataması
            b.setAttribute("id", psb_id) // buton id ataması
            b.addEventListener("click", () => { // buton tıklama fonksiyonu
                this.productSelectList(psb_id)
            })
            if (add == "deletable") { // silinebilir buton ataması
                var d = document.createElement("div") // silme butonu
                d.classList.add("top-delete", "d-flex") // silme butonu özellik ataması
                d.innerHTML = '<i class="fas fa-times mx-auto my-auto"></i>'
                d.addEventListener("click", (x) => { // silme butonu tıklama ataması
                    x.stopPropagation()
                    this.deleteElement(e, psb_id)
                })
                b.appendChild(d) // silinebilir butona silme butonu ataması
            }
            this.element.insertBefore(e, this.element.childNodes[this.element.childNodes.length - 1]) // butonu ana gövdeye ekleme 
            this.buttons.push(b) // butonu listeye ekleme
        } else {
            b.innerHTML = "<i class='fas fa-plus'></i>" // ekleme butonu oluştur
            b.setAttribute("name", "createButton") // isim ataması
            b.addEventListener("click", () => { // tıklama olayı atası
                console.log(parseInt(this.buttons[this.buttons.length - 1].getAttribute('id').split('_')[1]) + 1)
                console.log(this.buttons)
                this.createButton("deletable", "psb_" + (parseInt(this.buttons[this.buttons.length - 1].getAttribute('id').split('_')[1]) + 1).toString())
            })
            this.element.appendChild(e) // ana gövdeye buton ekleme
        }
    }


    productSelectList(psb_id) { // ürün seçme listesi açan fonksiyon
        this.productList.modal('toggle') // modal açma
        this.now_psb = psb_id // şimdiki buton id ataması 'psb_X'
    }

    // product element şeklinde gelir
    productSelectButtonView(product) { // ürün listesi butonu görünüm değişikliği
        var b = document.getElementById(this.now_psb) // buton çağrısı
        var p = product.children[0].cloneNode(true) // ürün kopyalama

        p.getElementsByTagName("button")[0].remove() // ürün içindeki butonu sil
        p.getElementsByTagName("img")[0].classList.replace("w-75", "w-100") // ürün resmini büyüt

        b.replaceChild(p, b.childNodes[0]) // butonun içindeki text ile yer değiştir
        b.classList.remove("btn", "btn-block", "btn-outline-primary") // buton özelliklerini sil

    }

    // ürün seçme butonu görünüm
    //id 'product_X' şeklinde
    selectButtonView(id) {
        var b = document.getElementById(id).getElementsByTagName("button")[0] // ürün kardında butonu bul
        b.classList.toggle("disabled") // devre dışı özelliğini toggle et
        if (b.classList.contains("disabled")) {
            b.innerText = "HER ÜRÜNDEN BİR ADET ALINABİLİR." // devre dışıysa metni değiştir
        } else {
            b.innerText = "SEÇ" // devre dıiı değilse değiştir
        }
    }

    // ürün ekle sil
    // operator '+' veya '-'
    // psb_id 'psb_X' şeklinde
    // operator '+' ise psb_id 'null', x ürün cardı olacak
    // operator '-' ise psb_id 'psb_X', x 'null' olacak 
    setProducts(operator, psb_id = null, x = null) {
        if (operator == "+") { // ürün ekleme

            for (let i = 0; i < this.products.length; i++) { // bütün ürünleri gez
                if (this.products[i]["psb_id"] == this.now_psb) { // şimdiki butonla eşit olan varsa 
                    psb_id = i // psb_id'yi 'X' şeklinde ayarla
                    break
                }
            }
            if (this.products[psb_id]) { // 'X' sıradaki ürün varsa daha önce ürün seçilmiş demektir. 
                console.log(x.getAttribute("id"))
                this.selectButtonView(this.products[psb_id]["id"]) // seçili ürünün id('product_X')'si ile buton metni değiştir.
                this.products[psb_id]["id"] = x.getAttribute("id") // yeni ürün id'si ekle
                this.products[psb_id]["price"] = x.getAttribute("price") // yeni ürün fiyatı ekle
            } else { // daha önce bu buton için ürün seçilmemiş
                this.products.push({ // ürünlerin arasına bunu ekle
                    "psb_id": this.now_psb, // psb_id şimdiki psb 'psb_X' şeklinde
                    "id": x.getAttribute("id"), // id 'product_X' şeklinde
                    "price": x.getAttribute("price") // fiyat metin şeklinde 
                })
            }
        } else if (operator == "-") { // silme varsa
            for (let i = 0; i < this.products.length; i++) { // bütün ürünleri gez
                console.log(this.products[i]["psb_id"])
                console.log(psb_id)
                if (this.products[i]["psb_id"] == psb_id) { // buton psb_id gelen psb_id'ye eşitse
                    this.selectButtonView(this.products[i]["id"])
                    this.products.splice(i, 1) // ürünü sil
                }
                console.log(this.products)

            }
        }
        this.changePrice() // fiyat değiştir
    }

    //find 'product_X' şeklinde
    selectButton(find) { // ürün seçme butonu 
        this.productList.modal('toggle') // listeyi kapat

        var p = document.getElementById(find) // ürün cardını bul

        this.productSelectButtonView(p) //ürün listesi butonu görünüm fonksiyonu

        this.selectButtonView(find) // ürün seçme butonu görünümü

        this.setProducts("+", null, p) // ürün ayarlama fonksiyonu
    }


    changePrice() {
        var p = 0 // fiyatı 0 yap
        for (let i = 0; i < this.products.length; i++) { // bütün ürünleri gez
            p += parseFloat(this.products[i]["price"].replace(',', '.')) // fiyatı ekle
        }
        this.price = p // asıl fiyatı ayarla
        this.price_text.innerText = this.price.toFixed(2).toString().replace('.', ',') + "₺" // fiyat metnini görselleştir

        this.setBackendProducts() // arka plan ürünlerini ayarla
        this.cargoTextSet() // kargo metnini ayarla

    }

    setBackendProducts() {
        var selects = Array.prototype.slice.call(this.backend_products.options) // seçilecek ürünlerin listesini al
        for (let i = 0; i < this.products.length; i++) { // bütün ürünleri dön

            for (let j = 0; j < selects.length; j++) { // bütün seçenekleri dön
                if (this.products[i]["id"].split("_")[1] == selects[j].value) { // 'product_X' içinden X'i alarak seçilebilecek ürünlerle kıyasla
                    selects[j].selected = true // eşit olan ürünü seç
                    selects.splice(j, 1) // bu seçimi sil
                    break

                }
            }
        }

        for (let i = 0; i < selects.length; i++) {
            selects[i].selected = false // kalan seçimleri seçilmemiş yap

        }

    }

    cargoTextSet() {
        console.log(this.products)
        if (this.buttons.length > this.standart_button) { // butonlar 3ten fazlaysa 
            this.cargo_text.children[0].classList.add("text-muted", "text-light", "strikethrough") // üstü çizili yap
        } else {
            this.cargo_text.children[0].classList.remove("text-muted", "text-light", "strikethrough") // üstü çizili sil
        }
    }

    // silme butonu 
    // e ana gövdeyle ürün butonu
    // psb_id 'psb_X' şeklinde
    deleteElement(e, psb_id) {


        var id = this.buttons.indexOf(document.getElementById(psb_id)) // ürün butonu nerede 
        this.buttons.splice(id, 1) // konuma göre sil
        e.remove()

        this.setProducts("-", psb_id) // ürünü sil


    }

}

var pselector = new ProductSelector(document.getElementById("psbs"))