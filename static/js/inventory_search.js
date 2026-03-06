document.addEventListener('DOMContentLoaded', function() {
    const searchForm = document.getElementById('searchForm');
    const productList = document.getElementById('productList');
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebar = document.getElementById('inventorySidebar');

    // Toggle sidebar (đã có)
    sidebarToggle.addEventListener('click', function() {
        sidebar.classList.toggle('hidden');
    });

    // Xử lý submit form tìm kiếm bằng AJAX
    searchForm.addEventListener('submit', async function(e) {
        e.preventDefault(); // Ngăn reload trang

        // Lấy dữ liệu form
        const formData = new FormData(searchForm);
        const params = new URLSearchParams(formData).toString();

        // Cập nhật URL (thay đổi thanh địa chỉ mà không reload)
        const newUrl = window.location.pathname + '?' + params;
        window.history.pushState({}, '', newUrl);

        // Gửi request AJAX
        try {
            const response = await fetch(newUrl, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest' // Đánh dấu là AJAX
                }
            });
            const data = await response.json();
            // Cập nhật nội dung danh sách sản phẩm
            productList.innerHTML = data.html;
        } catch (error) {
            console.error('Lỗi khi tìm kiếm:', error);
        }
    });

    // Khi tải trang, nếu có query params, tự động gửi tìm kiếm để hiển thị kết quả?
    // (Không cần vì Django đã render sẵn kết quả từ request.GET)
    // Tuy nhiên, nếu muốn đồng bộ hoàn toàn với AJAX, có thể gọi lại khi tải trang,
    // nhưng không cần thiết.
});