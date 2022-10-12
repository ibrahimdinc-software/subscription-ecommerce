function popup_modal(proccess, action_href = "#") {
    $("#test_modal").modal('show');
    action_element = document.getElementById("modal-action");
    message_element = document.getElementById("modal-message");
    title_element = document.getElementById("modal-title");

    message = "";
    title = "";
    action = "";
    //Kullanıcı Bilgi Güncelleme
    if (proccess[0] == 0) {
        element = document.getElementById(proccess[1]);
        action_element.addEventListener("click", function () {
            element.submit()
        });
        message = "Güncellemek istediğinize emin misiniz?";
        title = "Güncelle";
        action = "Güncelle";
    }
    //Şifre Güncelleme
    else if (proccess[0] == 1) {
        element = document.getElementById(proccess[1]);
        action_element.addEventListener("click", function () {
            element.submit()
        });
        message = "Şifrenizi güncellemek istediğinize emin misiniz?";
        title = "Şifre Güncelle";
        action = "Güncelle";
    }
    //Kupon Kodu
    else if (proccess[0] == 2) {
        element = document.getElementById(proccess[1]);
        action_element.addEventListener("click", function () {
            element.submit();
        });
        message = "İndirim tutarı gelecek kutunuzun fiyatı ödenmedi ise o kutunuza uygulanır. Ödendi ise sonraki kutunuza uygulanır.";
        title = "Kuponu Uygula";
        action = "Uygula";
    }
    //Paket Yükseltme
    else if (proccess[0] == 3) {
        element = document.getElementById(proccess[1]);
        action_element.addEventListener("click", function () {
            element.submit();
        });
        message = "Adet artışı gelecek kutunuzun fiyatı ödenmedi ise o kutunuza uygulanır. Ödendi ise sonraki kutunuza uygulanır.";
        title = "Kuponu Uygula";
        action = "Uygula";
    }
    //Paket İptal
    else if (proccess[0] == 4) {
        element = document.getElementById(proccess[1]);
        action_element.addEventListener("click", function () {
            element.submit();
        });
        message = "Aboneliğinizi iptal etmek istediğinize emin misiniz?";
        title = "Aboneliği İptal Et";
        action = "İptal Et";
        //Paket İptal
    } else if (proccess[0] == 7) {
        element = document.getElementById(proccess[1]);
        action_element.addEventListener("click", function () {
            element.submit();
        });
        message = "Abonelikle birlikte siparişinizi de iptal etmek istediğinize emin misiniz?";
        title = "İptal Et";
        action = "İptal Et";
    } else if (proccess[0] == 8) {
        element = document.getElementById(proccess[1]);
        action_element.addEventListener("click", function () {
            element.submit();
        });
        message = "Siparişinizi iptal/iade etmek istediğinize emin misiniz?";
        title = "İptal/İade Et";
        action = "İptal/İade Et";
    } else if (proccess[0] == 5) {
        message = "Çıkış yapmak istediğinize emin misiniz?";
        title = "Çıkış Yap";
        action = "Çık";
    } else if (proccess[0] == 6) {
        message = "Silmek istediğinize emin misiniz?";
        title = "Sil";
        action = "Sil";
    }


    message_element.innerHTML = message;
    title_element.innerHTML = title;

    action_element.setAttribute("name", proccess[2]);
    action_element.innerHTML = action;
    action_element.setAttribute("href", action_href);

}