// inventory_modal.js
document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('productModal');
    const closeBtn = document.querySelector('.close');
    const cancelBtn = document.getElementById('modal-cancel');
    const updateBtn = document.getElementById('modal-update');
    const modalImage = document.getElementById('modal-image');
    const modalName = document.getElementById('modal-name');
    const modalPrice = document.getElementById('modal-price');
    const modalSizes = document.getElementById('modal-sizes');

    // Biến lưu dữ liệu hiện tại của sản phẩm
    let currentProductId = null;
    let originalData = null; // để so sánh khi cập nhật

    // Đóng modal
    function closeModal() {
        modal.style.display = 'none';
    }

    closeBtn.onclick = closeModal;
    cancelBtn.onclick = closeModal;

    // Click bên ngoài modal cũng đóng
    window.onclick = function(event) {
        if (event.target == modal) {
            closeModal();
        }
    };

    // Lắng nghe click trên các card (dùng event delegation vì card có thể load lại qua AJAX)
    document.getElementById('productList').addEventListener('click', function(e) {
        const card = e.target.closest('.product-card');
        if (!card) return;

        const productId = card.dataset.productId;
        if (!productId) return;
        console.log("truoc khi goi api product")

        e.preventDefault();
        openModal(productId);
    });

    // Hàm mở modal và fetch dữ liệu
    async function openModal(productId) {
        try {
            // Fetch chi tiết sản phẩm từ API (thay URL phù hợp)
            // const url = `{% url 'product-detail' pk=${productId}%}`;
            console.log("truoc khi request openmodal");
            const response = await fetch(`/admin_user/api/product/${productId}/`, {
                method: 'GET',
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken')
                    }
                    });

            if (!response.ok) throw new Error('Lỗi tải dữ liệu');
            const data = await response.json();

            // Lưu lại dữ liệu gốc
            currentProductId = productId;
            originalData = JSON.parse(JSON.stringify(data)); // clone

            // Hiển thị thông tin cơ bản
            modalImage.src = data.image_url;
            modalName.textContent = data.name;
            modalPrice.value = data.price;

            // Render các size
            // renderSizes(data.sizes);
            renderVariants(data.variants);

            // Hiển thị modal
            modal.style.display = 'block';
        } catch (error) {
            alert('Không thể tải thông tin sản phẩm: ' + error.message);
        }
    }

    // // Render danh sách size
    // function renderSizes(sizes) {
    //     modalSizes.innerHTML = '';
    //     sizes.forEach(sizeInfo => {
    //         const row = document.createElement('div');
    //         row.className = 'size-row';
    //         row.dataset.size = sizeInfo.size;

    //         row.innerHTML = `
    //             <span>Size ${sizeInfo.size}</span>
    //             <div class="size-controls">
    //                 <button class="size-decrease" ${sizeInfo.stock <= 0 ? 'disabled' : ''}>-</button>
    //                 <input type="text" class="size-quantity" value="${sizeInfo.stock}" readonly>
    //                 <button class="size-increase">+</button>
    //             </div>
    //         `;

    //         // Gán sự kiện cho nút + và -
    //         const decreaseBtn = row.querySelector('.size-decrease');
    //         const increaseBtn = row.querySelector('.size-increase');
    //         const quantityInput = row.querySelector('.size-quantity');

    //         decreaseBtn.addEventListener('click', function() {
    //             let current = parseInt(quantityInput.value);
    //             if (current > 0) {
    //                 quantityInput.value = current - 1;
    //             }
    //             // Cập nhật disabled cho nút -
    //             decreaseBtn.disabled = (parseInt(quantityInput.value) <= 0);
    //         });

    //         increaseBtn.addEventListener('click', function() {
    //             let current = parseInt(quantityInput.value);
    //             quantityInput.value = current + 1;
    //             decreaseBtn.disabled = false;
    //         });

    //         modalSizes.appendChild(row);
    //     });
    // }

    // // Xử lý nút Cập nhật
    // updateBtn.addEventListener('click', async function() {
    //     if (!currentProductId) return;

    //     // Thu thập dữ liệu từ modal
    //     const updatedSizes = [];
    //     document.querySelectorAll('.size-row').forEach(row => {
    //         const size = row.dataset.size;
    //         const quantity = parseInt(row.querySelector('.size-quantity').value);
    //         updatedSizes.push({ size: size, stock: quantity });
    //     });

    //     const updatedData = {
    //         product_id: currentProductId,
    //         price: modalPrice.value.replace(/[^0-9]/g, ''), // loại bỏ ký tự không phải số
    //         sizes: updatedSizes
    //     };

    //     try {
    //         // Gửi dữ liệu lên server (PUT hoặc POST)
    //         const response = await fetch('/admin_user/api/update-product/', {
    //             method: 'POST',
    //             headers: {
    //                 'Content-Type': 'application/json',
    //                 'X-CSRFToken': getCookie('csrftoken') // nếu dùng CSRF
    //             },
    //             body: JSON.stringify(updatedData)
    //         });

    //         if (!response.ok) throw new Error('Cập nhật thất bại');
    //         const result = await response.json();
    //         alert('Cập nhật thành công!');
    //         closeModal();
    //         // Có thể reload lại danh sách sản phẩm hoặc cập nhật card tương ứng
    //         location.reload(); // tạm thời reload
    //     } catch (error) {
    //         alert('Lỗi: ' + error.message);
    //     }
    // });



    // Render variants (nhóm theo size)
function renderVariants(variants) {
    modalSizes.innerHTML = ''; // vẫn dùng modalSizes container

    // Nhóm variants theo size
    const sizeMap = {};
    variants.forEach(v => {
        if (!sizeMap[v.size]) sizeMap[v.size] = [];
        sizeMap[v.size].push(v);
    });

    // Sắp xếp size (nếu là số)
    const sortedSizes = Object.keys(sizeMap).sort((a, b) => {
        const numA = parseFloat(a);
        const numB = parseFloat(b);
        if (!isNaN(numA) && !isNaN(numB)) return numA - numB;
        return a.localeCompare(b);
    });

    sortedSizes.forEach(size => {
        const sizeGroup = document.createElement('div');
        sizeGroup.className = 'size-group';
        sizeGroup.dataset.size = size;

        // Tiêu đề size
        const sizeTitle = document.createElement('div');
        sizeTitle.className = 'size-title';
        sizeTitle.textContent = `Size ${size}`;
        sizeGroup.appendChild(sizeTitle);

        // Các dòng loại đế
        sizeMap[size].forEach(v => {
            const soleRow = document.createElement('div');
            soleRow.className = 'sole-row';
            soleRow.dataset.sole = v.sole;

            soleRow.innerHTML = `
                <span class="sole-name">${v.sole}</span>
                <div class="size-controls">
                    <button class="size-decrease">-</button>
                    <input type="text" class="size-quantity" value="${v.stock}" readonly>
                    <button class="size-increase">+</button>
                </div>
            `;

            const decreaseBtn = soleRow.querySelector('.size-decrease');
            const increaseBtn = soleRow.querySelector('.size-increase');
            const quantityInput = soleRow.querySelector('.size-quantity');

            decreaseBtn.addEventListener('click', function() {
                let current = parseInt(quantityInput.value);
                if (current > 0) {
                    quantityInput.value = current - 1;
                }
            });

            increaseBtn.addEventListener('click', function() {
                let current = parseInt(quantityInput.value);
                quantityInput.value = current + 1;
            });

            sizeGroup.appendChild(soleRow);
        });

        modalSizes.appendChild(sizeGroup);
    });
}

// Xử lý nút Cập nhật
updateBtn.addEventListener('click', async function() {
    if (!currentProductId) return;

    // Thu thập dữ liệu từ các dòng
    const updatedVariants = [];
    document.querySelectorAll('.size-group').forEach(group => {
        const size = group.dataset.size;
        group.querySelectorAll('.sole-row').forEach(row => {
            const sole = row.dataset.sole;
            const quantity = parseInt(row.querySelector('.size-quantity').value);
            updatedVariants.push({
                size: size,
                sole: sole,
                stock: quantity
            });
        });
    });

    const updatedData = {
        product_id: currentProductId,
        price: modalPrice.value.replace(/[^0-9.]/g, ''), // giữ số thập phân nếu có
        variants: updatedVariants
    };

    try {
        const response = await fetch('/admin_user/api/update-product/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(updatedData)
        });

        if (!response.ok) throw new Error('Cập nhật thất bại');
        const result = await response.json();
        alert('Cập nhật thành công!');
        closeModal();
        location.reload();
    } catch (error) {
        alert('Lỗi: ' + error.message);
    }
});


    // Hàm lấy CSRF token (nếu Django dùng cookie)
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});