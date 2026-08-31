document.addEventListener('DOMContentLoaded', function () {

  // 1. Debounced Live Universal Search (300ms)
  const searchInput = document.getElementById('orient-search-input');
  const searchCategory = document.getElementById('orient-search-category');
  const searchResults = document.getElementById('search-results-dropdown');
  let searchDebounceTimer = null;

  if (searchInput && searchResults) {
    searchInput.addEventListener('input', function () {
      clearTimeout(searchDebounceTimer);
      const query = this.value.trim();
      const category = searchCategory ? searchCategory.value : 'all';

      if (query.length < 2) {
        searchResults.style.display = 'none';
        searchResults.innerHTML = '';
        return;
      }

      searchDebounceTimer = setTimeout(() => {
        fetch(`/api/search/?q=${encodeURIComponent(query)}&category=${encodeURIComponent(category)}`)
          .then(res => res.json())
          .then(data => {
            if (data.results && data.results.length > 0) {
              let html = '';
              data.results.forEach(item => {
                const priceFormatted = `৳ ${parseInt(item.discount_price > 0 ? item.discount_price : item.price).toLocaleString()}`;
                html += `
                  <a href="${item.url}" class="search-item">
                    <img src="${item.image_url}" alt="${item.name}" style="width: 44px; height: 44px; object-fit: contain; margin-right: 12px; background: #f8fafc; border-radius: 4px; padding: 2px;">
                    <div class="flex-grow-1 overflow-hidden">
                      <div class="fw-semibold text-truncate small">${item.name}</div>
                      <div class="text-muted d-flex justify-content-between" style="font-size: 0.75rem;">
                        <span>${item.brand} &bull; ${item.category}</span>
                        <strong class="text-primary">${priceFormatted}</strong>
                      </div>
                    </div>
                  </a>
                `;
              });
              searchResults.innerHTML = html;
              searchResults.style.display = 'block';
            } else {
              searchResults.innerHTML = '<div class="p-3 text-muted text-center small">No matching hardware components found.</div>';
              searchResults.style.display = 'block';
            }
          })
          .catch(() => {
            searchResults.style.display = 'none';
          });
      }, 300);
    });

    document.addEventListener('click', function (e) {
      if (!searchInput.contains(e.target) && !searchResults.contains(e.target)) {
        searchResults.style.display = 'none';
      }
    });
  }

  // 2. Flash Deal Countdown Timer (HH:MM:SS)
  const countdownContainer = document.getElementById('flash-deal-countdown');
  if (countdownContainer) {
    const targetDateStr = countdownContainer.dataset.target;
    const targetDate = targetDateStr ? new Date(targetDateStr).getTime() : (new Date().getTime() + 24 * 60 * 60 * 1000);

    function updateCountdown() {
      const now = new Date().getTime();
      const distance = targetDate - now;

      if (distance < 0) {
        countdownContainer.innerHTML = '<span class="badge bg-danger">Offer Expired</span>';
        return;
      }

      const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
      const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
      const seconds = Math.floor((distance % (1000 * 60)) / 1000);

      const hElem = document.getElementById('cd-hours');
      const mElem = document.getElementById('cd-mins');
      const sElem = document.getElementById('cd-secs');

      if (hElem) hElem.textContent = String(hours).padStart(2, '0');
      if (mElem) mElem.textContent = String(minutes).padStart(2, '0');
      if (sElem) sElem.textContent = String(seconds).padStart(2, '0');
    }

    updateCountdown();
    setInterval(updateCountdown, 1000);
  }

  // 3. Bangladesh Division -> District Cascade (REQ-F-CHK-02)
  const divisionSelect = document.getElementById('id_division');
  const districtSelect = document.getElementById('id_district');

  if (divisionSelect && districtSelect) {
    const currentDistrict = districtSelect.dataset.current || '';

    function loadDistricts(division, selected) {
      if (!division) {
        districtSelect.innerHTML = '<option value="">Select Division first</option>';
        return;
      }

      fetch(`/api/districts/?division=${encodeURIComponent(division)}`)
        .then(res => res.json())
        .then(data => {
          let html = '<option value="">Select District</option>';
          data.districts.forEach(d => {
            const isSel = (d === selected) ? 'selected' : '';
            html += `<option value="${d}" ${isSel}>${d}</option>`;
          });
          districtSelect.innerHTML = html;
        });
    }

    divisionSelect.addEventListener('change', function () {
      loadDistricts(this.value, '');
    });

    if (divisionSelect.value) {
      loadDistricts(divisionSelect.value, currentDistrict);
    }
  }

  // 4. Wishlist AJAX Toggle
  document.querySelectorAll('.wishlist-toggle-btn').forEach(btn => {
    btn.addEventListener('click', function (e) {
      e.preventDefault();
      const productId = this.dataset.productId;
      const csrfToken = document.querySelector('meta[name="csrf-token"]')?.content || getCookie('csrftoken');

      fetch('/cart/wishlist/toggle/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'X-CSRFToken': csrfToken,
          'X-Requested-With': 'XMLHttpRequest'
        },
        body: `product_id=${productId}`
      })
      .then(res => res.json())
      .then(data => {
        if (data.success) {
          if (data.action === 'added') {
            this.classList.add('active', 'text-danger');
            this.innerHTML = '<i class="bi bi-heart-fill"></i>';
            showToast('Wishlist', 'Product added to your wishlist.');
          } else {
            this.classList.remove('active', 'text-danger');
            this.innerHTML = '<i class="bi bi-heart"></i>';
            showToast('Wishlist', 'Product removed from your wishlist.');
          }
          const badge = document.getElementById('wishlist-badge');
          if (badge) badge.textContent = data.wishlist_count;
        }
      });
    });
  });

  // 5. Checkout Shipping Method Real-Time Calculation (REQ-F-CHK-03)
  const shippingRadios = document.querySelectorAll('input[name="shipping_method"]');
  const summaryBox = document.getElementById('order-summary-box');
  const shippingFeeDisplay = document.getElementById('summary-shipping-fee');
  const grandTotalDisplay = document.getElementById('summary-grand-total');

  if (shippingRadios.length > 0 && summaryBox && shippingFeeDisplay && grandTotalDisplay) {
    const subtotal = parseFloat(summaryBox.dataset.subtotal || 0);
    const discount = parseFloat(summaryBox.dataset.discount || 0);

    const shippingPrices = {
      'inside_dhaka': (subtotal >= 50000) ? 0 : 100,
      'outside_dhaka': 200,
      'express': 300,
      'pickup': 0
    };

    function updateShippingAndTotal() {
      const selectedMethod = document.querySelector('input[name="shipping_method"]:checked')?.value || 'inside_dhaka';
      const shippingCost = shippingPrices[selectedMethod] !== undefined ? shippingPrices[selectedMethod] : 100;
      const grandTotal = Math.max(0, subtotal - discount + shippingCost);

      if (shippingCost === 0) {
        shippingFeeDisplay.textContent = 'FREE';
        shippingFeeDisplay.className = 'font-monospace fw-bold text-success';
      } else {
        shippingFeeDisplay.textContent = `৳ ${shippingCost.toLocaleString()}`;
        shippingFeeDisplay.className = 'font-monospace text-dark';
      }

      grandTotalDisplay.textContent = `৳ ${Math.round(grandTotal).toLocaleString()}`;
    }

    shippingRadios.forEach(r => r.addEventListener('change', updateShippingAndTotal));
    updateShippingAndTotal();
  }

  // 6. Checkout Payment Method Toggle (bKash/Nagad & Credit Card / Online Bank)
  const paymentRadios = document.querySelectorAll('input[name="payment_method"]');
  const mfsBox = document.getElementById('mfs-details-section');
  const cardBox = document.getElementById('card-details-section');

  if (paymentRadios.length > 0) {
    function togglePaymentFields() {
      const selected = document.querySelector('input[name="payment_method"]:checked')?.value;
      if (mfsBox) {
        if (selected === 'bkash' || selected === 'nagad') {
          mfsBox.style.display = 'block';
          const brandLabel = document.getElementById('mfs-brand-label');
          const brandLabel2 = document.getElementById('mfs-brand-label-2');
          const brandName = selected === 'bkash' ? 'bKash' : 'Nagad';
          if (brandLabel) brandLabel.textContent = brandName;
          if (brandLabel2) brandLabel2.textContent = brandName;
        } else {
          mfsBox.style.display = 'none';
        }
      }

      if (cardBox) {
        if (selected === 'card') {
          cardBox.style.display = 'block';
        } else {
          cardBox.style.display = 'none';
        }
      }
    }

    paymentRadios.forEach(r => r.addEventListener('change', togglePaymentFields));
    togglePaymentFields();

    // Optional: Format Card input as XXXX XXXX XXXX XXXX
    const cardInput = document.getElementById('id_card_number');
    if (cardInput) {
      cardInput.addEventListener('input', function (e) {
        let value = this.value.replace(/\D/g, '').substring(0, 16);
        let formatted = value.match(/.{1,4}/g)?.join(' ') || value;
        this.value = formatted;
      });
    }

    // Optional: Format Expiry input as MM/YY
    const expiryInput = document.getElementById('id_card_expiry');
    if (expiryInput) {
      expiryInput.addEventListener('input', function (e) {
        let value = this.value.replace(/\D/g, '').substring(0, 4);
        if (value.length >= 3) {
          this.value = value.substring(0, 2) + '/' + value.substring(2, 4);
        } else {
          this.value = value;
        }
      });
    }
  }

});

// Helper: Toast Notifications
function showToast(title, message) {
  const toastEl = document.getElementById('orient-global-toast');
  if (toastEl && window.bootstrap) {
    document.getElementById('toast-title').textContent = title;
    document.getElementById('toast-body').textContent = message;
    const toast = new bootstrap.Toast(toastEl);
    toast.show();
  }
}

// Helper: CSRF Cookie Fetcher
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
