document.addEventListener('DOMContentLoaded', function() {
    // Lấy tất cả các checkbox filter
    const brandCheckboxes = document.querySelectorAll('.filter-brand input[type="checkbox"]');
    const sizeCheckboxes = document.querySelectorAll('.filter-size input[type="checkbox"]');
    const priceCheckboxes = document.querySelectorAll('.filter-price input[type="checkbox"]');
    const productGrid = document.getElementById('productGrid');
    const productCards = Array.from(document.querySelectorAll('.product-card'));

    // Hàm chuyển đổi giá trị price range thành [min, max]
    function parsePriceRange(value) {
        switch(value) {
            case 'under100': return [0, 100000];
            case '100-200': return [100000, 200000];
            case '200-500': return [200000, 500000];
            case 'above500': return [500000, Infinity];
            default: return null;
        }
    }

    // Hàm lấy tất cả giá trị đang được check từ một nhóm checkbox
    function getCheckedValues(checkboxes) {
        return Array.from(checkboxes)
            .filter(cb => cb.checked)
            .map(cb => cb.value);
    }

    // Hàm kiểm tra một sản phẩm có thỏa mãn filter không
    function matchesFilter(card) {
        const brand = card.dataset.brand;
        const price = parseFloat(card.dataset.price);
        const sizes = card.dataset.sizes.split(','); // mảng các size dạng string

        // Lọc brand
        const selectedBrands = getCheckedValues(brandCheckboxes);
        if (selectedBrands.length > 0 && !selectedBrands.includes(brand)) {
            return false;
        }

        // Lọc size: sản phẩm có ít nhất một size nằm trong danh sách size được chọn
        const selectedSizes = getCheckedValues(sizeCheckboxes);
        if (selectedSizes.length > 0) {
            const hasSize = sizes.some(s => selectedSizes.includes(s));
            if (!hasSize) return false;
        }

        // Lọc giá: kiểm tra từng khoảng giá được chọn, nếu không có khoảng nào được chọn thì bỏ qua
        const selectedPrices = getCheckedValues(priceCheckboxes);
        if (selectedPrices.length > 0) {
            let inRange = false;
            selectedPrices.forEach(range => {
                const [min, max] = parsePriceRange(range);
                if (price >= min && price < max) inRange = true;
            });
            if (!inRange) return false;
        }

        return true;
    }

    // Hàm cập nhật hiển thị
    function updateFilter() {
        productCards.forEach(card => {
            if (matchesFilter(card)) {
                card.style.display = 'block'; // hoặc 'flex' tùy vào card display
            } else {
                card.style.display = 'none';
            }
        });
    }

    // Gắn sự kiện change cho tất cả checkbox
    [...brandCheckboxes, ...sizeCheckboxes, ...priceCheckboxes].forEach(cb => {
        cb.addEventListener('change', updateFilter);
    });

    // Nếu có nút "Xóa filter", có thể thêm hàm reset
    // (không bắt buộc)
});