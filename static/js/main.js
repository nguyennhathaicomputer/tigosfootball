document.addEventListener('DOMContentLoaded', function() {
    const sidebar = document.querySelector('.sidebar');
    const toggleBtn = document.getElementById('sidebarToggle');
    const overlay = document.getElementById('sidebarOverlay');

    if (!sidebar || !toggleBtn) return;

    function openSidebar() {
        sidebar.classList.add('sidebar-visible');
        if (overlay) overlay.classList.add('active');
        toggleBtn.innerHTML = '<i class="fas fa-chevron-left"></i>';
    }

    function closeSidebar() {
        sidebar.classList.remove('sidebar-visible');
        if (overlay) overlay.classList.remove('active');
        toggleBtn.innerHTML = '<i class="fas fa-chevron-right"></i>';
    }

    toggleBtn.addEventListener('click', function(e) {
        e.stopPropagation();
        if (sidebar.classList.contains('sidebar-visible')) {
            closeSidebar();
        } else {
            openSidebar();
        }
    });

    // Click overlay để đóng sidebar
    if (overlay) {
        overlay.addEventListener('click', closeSidebar);
    }

    // Đóng sidebar khi resize lên desktop (nếu cần)
    window.addEventListener('resize', function() {
        if (window.innerWidth > 768) {
            // Nếu đang ở chế độ desktop, loại bỏ class visible và ẩn nút
            sidebar.classList.remove('sidebar-visible');
            if (overlay) overlay.classList.remove('active');
            toggleBtn.style.display = 'none'; // Ẩn nút trên desktop
        } else {
            toggleBtn.style.display = 'flex'; // Hiện nút trên mobile
            // Đảm bảo sidebar ẩn khi load lại trang ở mobile
            closeSidebar();
        }
    }).trigger('resize'); // Gọi ngay khi load để set đúng trạng thái
});
