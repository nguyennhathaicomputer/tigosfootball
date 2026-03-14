// // product_detail.js

// document.addEventListener('DOMContentLoaded', function() {
//     // Xử lý chuyển ảnh khi click thumbnail
//     const mainImage = document.getElementById('mainImage');
//     const thumbnails = document.querySelectorAll('.thumbnail-item');

//     thumbnails.forEach(thumb => {
//         thumb.addEventListener('click', function() {
//             const imageUrl = this.dataset.imageUrl;
//             if (imageUrl) {
//                 mainImage.src = imageUrl;
//                 // Xóa class active khỏi tất cả thumbnail
//                 thumbnails.forEach(t => t.classList.remove('active'));
//                 // Thêm class active cho thumbnail được click
//                 this.classList.add('active');
//             }
//         });
//     });

//     // Đặt active cho thumbnail đầu tiên nếu có
//     if (thumbnails.length > 0) {
//         thumbnails[0].classList.add('active');
//     }

//     // Xử lý chọn size và tính tổng tiền nếu cần (ở đây chỉ đơn giản là lấy các size đã chọn)
//     const checkboxes = document.querySelectorAll('input[name="size"]');
//     const buyBtn = document.getElementById('buyNowBtn');
//     const addCartBtn = document.getElementById('addToCartBtn');

//     function getSelectedSizes() {
//         const selected = [];
//         checkboxes.forEach(cb => {
//             if (cb.checked) {
//                 selected.push({
//                     size: cb.value,
//                     stock: cb.parentElement.querySelector('.size-stock').textContent.replace(/[()]/g, '')
//                 });
//             }
//         });
//         return selected;
//     }

//     // Sự kiện cho nút "Đặt mua ngay"
//     buyBtn.addEventListener('click', function() {
//         const selected = getSelectedSizes();
//         if (selected.length === 0) {
//             alert('Vui lòng chọn ít nhất một size.');
//             return;
//         }
//         // TODO: chuyển hướng đến trang thanh toán với thông tin sản phẩm
//         alert('Bạn đã chọn: ' + selected.map(s => `Size ${s.size} (SL: ${s.stock})`).join(', '));
//     });

//     // Sự kiện cho nút "Thêm vào giỏ"
//     addCartBtn.addEventListener('click', function() {
//         const selected = getSelectedSizes();
//         if (selected.length === 0) {
//             alert('Vui lòng chọn ít nhất một size.');
//             return;
//         }
//         // TODO: gọi AJAX thêm vào giỏ hàng
//         alert('Đã thêm vào giỏ hàng: ' + selected.map(s => `Size ${s.size}`).join(', '));
//     });

//     // Có thể thêm validation: không cho chọn quá số lượng tồn (nhưng ở đây đã disable nếu stock = 0)
// });







// product_detail.js

document.addEventListener('DOMContentLoaded', function() {
    // Xử lý chuyển ảnh khi click thumbnail
    const mainImage = document.getElementById('mainImage');
    const thumbnails = document.querySelectorAll('.thumbnail-item');

    thumbnails.forEach(thumb => {
        thumb.addEventListener('click', function() {
            const imageUrl = this.dataset.imageUrl;
            if (imageUrl) {
                mainImage.src = imageUrl;
                thumbnails.forEach(t => t.classList.remove('active'));
                this.classList.add('active');
            }
        });
    });

    if (thumbnails.length > 0) {
        thumbnails[0].classList.add('active');
    }

    // Số điện thoại Zalo cố định (định dạng quốc tế, bỏ số 0 đầu)
    const ZALO_PHONE = '0396691067'; // Thay bằng số thật

    // Hàm lấy danh sách các variant đã chọn
    function getSelectedVariants() {
        const variantCheckboxes = document.querySelectorAll('input[name="variant"]:checked');
        const selected = [];
        variantCheckboxes.forEach(cb => {
            const sizeGroup = cb.closest('.size-group');
            const sizeName = sizeGroup ? sizeGroup.querySelector('h4').textContent.replace('Size ', '') : 'Không rõ';
            const parentLabel = cb.closest('label');
            const soleName = parentLabel ? parentLabel.querySelector('.sole-name').textContent : 'Không rõ';
            const stockSpan = parentLabel ? parentLabel.querySelector('.sole-stock') : null;
            let stock = '';
            if (stockSpan) {
                const match = stockSpan.textContent.match(/\((\d+)\)/);
                stock = match ? match[1] : '0';
            }
            selected.push({
                size: sizeName,
                sole: soleName,
                stock: stock
            });
        });
        return selected;
    }

    // Lấy thông tin sản phẩm
    function getProductInfo() {
        const name = document.querySelector('.product-title').textContent;
        const imageUrl = mainImage.src;
        return { name, imageUrl };
    }

    // // Sự kiện cho nút "Đặt mua ngay"
    // const buyBtn = document.getElementById('buyNowBtn');
    // buyBtn.addEventListener('click', function() {
    //     const selectedVariants = getSelectedVariants();
    //     if (selectedVariants.length === 0) {
    //         alert('Vui lòng chọn ít nhất một size và loại đế.');
    //         return;
    //     }

    //     const product = getProductInfo();

    //     let message = `Tôi muốn đặt mua giày: ${product.name}\n`;
    //     message += `Chi tiết:\n`;
    //     selectedVariants.forEach((v, index) => {
    //         message += `  - Size ${v.size}, loại đế: ${v.sole}, số lượng còn: ${v.stock}\n`;
    //     });
    //     message += `Hình ảnh sản phẩm: ${product.imageUrl}`;

    //     const encodedMessage = encodeURIComponent(message);
    //     const zaloLink = `https://zalo.me/${ZALO_PHONE}?text=${encodedMessage}`;
    //     window.location.href = zaloLink;
    // });


        // Hàm tạo nội dung tin nhắn
    function buildMessage() {
        const selectedVariants = getSelectedVariants();
        const product = getProductInfo();

        let message = `Tôi muốn đặt mua giày: ${product.name}\n`;
        message += `Chi tiết:\n`;
        selectedVariants.forEach(v => {
            message += `- Size ${v.size}, loại đế: ${v.sole}, số lượng còn: ${v.stock}\n`;
        });
        message += `Hình ảnh: ${product.imageUrl}`;
        return message;
    }

    // Sự kiện nút "Đặt mua ngay" - cải tiến
    const buyBtn = document.getElementById('buyNowBtn');
    buyBtn.addEventListener('click', function() {
        const selectedVariants = getSelectedVariants();
        if (selectedVariants.length === 0) {
            alert('Vui lòng chọn ít nhất một size và loại đế.');
            return;
        }

        const message = buildMessage();

        // Tạo một textarea ẩn để copy nội dung vào clipboard
        const textarea = document.createElement('textarea');
        textarea.value = message;
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy'); // Sao chép vào clipboard
        document.body.removeChild(textarea);

        // Thông báo đã copy
        alert('Đã sao chép nội dung đặt hàng vào bộ nhớ tạm.\nVui lòng dán (Ctrl+V) vào Zalo.');

        // Mở Zalo chat (không có text, chỉ mở số điện thoại)
        window.open(`https://zalo.me/${ZALO_PHONE}`, '_blank');
    });

    // Sự kiện cho nút "Thêm vào giỏ"
    const addCartBtn = document.getElementById('addToCartBtn');
    addCartBtn.addEventListener('click', function() {
        const selectedVariants = getSelectedVariants();
        if (selectedVariants.length === 0) {
            alert('Vui lòng chọn ít nhất một size và loại đế.');
            return;
        }
        const variantIds = Array.from(document.querySelectorAll('input[name="variant"]:checked')).map(cb => cb.value);
        alert('Đã thêm vào giỏ hàng các variant: ' + variantIds.join(', '));
    });
});