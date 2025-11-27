// 開啟與關閉Modal
function open_input_table() {
    document.getElementById("addModal").style.display = "block";
}
function close_input_table() {
    document.getElementById("addModal").style.display = "none";
}

function delete_data(value) {
    // 發送 DELETE 請求到後端
    if (!confirm("確定要刪除這筆資料嗎？")) return;
    fetch(`/product?order_id=${value}`, {
        method: "DELETE",
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("伺服器回傳錯誤");
        }
        return response.json(); // 假設後端回傳 JSON 格式資料
    })
    .then(result => {
        console.log(result); // 在這裡處理成功的回應
        close_input_table(); // 關閉 modal
        location.assign('/'); // 重新載入頁面
    })
    .catch(error => {
        console.error("發生錯誤：", error);
    });
}

// 初始化表單欄位
function initForm() {
    document.getElementById("date").valueAsDate = new Date();
    document.getElementById("quantity").value = 1;
    document.getElementById("status").value = "未付款";
    document.getElementById("total").textContent = "小計：0 元";
}

// 1. 選取商品種類後的連動邏輯 (Fetch API)
function selectCategory() {
    const category = document.getElementById("category").value;
    fetch(`/product?category=${encodeURIComponent(category)}`)
        .then(res => res.json())
        .then(data => {
            const productSelect = document.getElementById("product");
            productSelect.innerHTML = "";
            data.product.forEach(name => {
                const option = document.createElement("option");
                option.value = name;
                option.textContent = name;
                productSelect.appendChild(option);
            });
            selectProduct(); // 預設選第一個商品並更新價格
        })
        .catch(err => console.error("商品列表取得失敗：", err));
}

// 2. 選取商品後的價格更新邏輯 (Fetch API)
function selectProduct() {
    const productName = document.getElementById("product").value;
    fetch(`/product?product=${encodeURIComponent(productName)}`)
        .then(res => res.json())
        .then(data => {
            document.getElementById("price").value = data.price;
            countTotal();
        })
        .catch(err => console.error("價格取得失敗：", err));
}

// 3. 計算小計邏輯
function countTotal() {
    const price = parseFloat(document.getElementById("price").value) || 0;
    const quantity = parseInt(document.getElementById("quantity").value) || 1;
    const total = price * quantity;
    document.getElementById("total").textContent = `小計：${total.toFixed(2)} 元`;
}

// 4. 表單送出邏輯
let submitting = false; // 全域旗標，防止重複送出
function submitForm() {
    if (submitting) return; // 如果正在送出，就跳過
    submitting = true;      // 鎖住送出

    const payload = {
        customer: document.getElementById("customer").value,
        note: document.getElementById("note").value,
        date: document.getElementById("date").value,
        quantity: parseInt(document.getElementById("quantity").value),
        status: document.getElementById("status").value,
        category: document.getElementById("category").value,
        product: document.getElementById("product").value,
        price: parseFloat(document.getElementById("price").value)
    };

    if (!payload.customer || !payload.product || payload.quantity <= 0) {
        alert("請填寫完整資料，且數量需大於 0");
        return;
    }

    fetch("/product", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    })
    .then(res => {
        if (!res.ok) throw new Error("新增失敗");
        return res.json();
    })
    .then(result => {
        alert("新增成功！");
        close_input_table();
        location.assign('/');
    })
    .catch(err => {
        console.error("送出失敗：", err);
        alert("送出失敗，請稍後再試");
    })
    .finally(() => {
        submitting = false; // 無論成功或失敗都要解鎖
    });
}