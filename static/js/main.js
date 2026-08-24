/* 
=====================================================================
LuxeCraft Interior Studio - Core Frontend JavaScript
Interactivity & Dynamic Behaviors
=====================================================================
*/

document.addEventListener('DOMContentLoaded', () => {
    
    // 1. Mobile Navigation Toggle
    const mobileToggle = document.querySelector('.mobile-toggle');
    const navLinks = document.querySelector('.nav-links');

    if (mobileToggle && navLinks) {
        mobileToggle.addEventListener('click', () => {
            navLinks.classList.toggle('active');
            const isOpen = navLinks.classList.contains('active');
            mobileToggle.innerHTML = isOpen ? '✕' : '☰';
        });
    }

    // 2. Auto-Dismiss Flash Alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            alert.style.transition = 'opacity 0.5s ease';
            setTimeout(() => alert.remove(), 500);
        }, 5000);
    });

    // 3. Dynamic Image File Upload Preview
    const fileInputs = document.querySelectorAll('input[type="file"][data-preview]');
    fileInputs.forEach(input => {
        input.addEventListener('change', function(e) {
            const previewId = this.getAttribute('data-preview');
            const previewImage = document.getElementById(previewId);
            
            if (previewImage && this.files && this.files[0]) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    previewImage.src = e.target.result;
                    previewImage.style.display = 'block';
                }
                reader.readAsDataURL(this.files[0]);
            }
        });
    });

    // 4. Modal Toggles for Admin CRUD forms
    window.openModal = function(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) modal.style.display = 'flex';
    };

    window.closeModal = function(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) modal.style.display = 'none';
    };

    // 5. Smooth Scroll for internal anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            if (targetId && targetId !== '#') {
                const targetElement = document.querySelector(targetId);
                if (targetElement) {
                    e.preventDefault();
                    targetElement.scrollIntoView({ behavior: 'smooth' });
                }
            }
        });
    });

    // 6. Interactive Spatial Project Budget Estimator
    const estPropType = document.getElementById('est_prop_type');
    const estSqft = document.getElementById('est_sqft');
    const estSqftVal = document.getElementById('est_sqft_val');
    const estTotalPrice = document.getElementById('est_total_price');
    const estAddons = document.querySelectorAll('.est_addon');

    function calculateEstimate() {
        if (!estPropType || !estSqft || !estTotalPrice) return;

        const rate = parseFloat(estPropType.value) || 1.5;
        const sqft = parseInt(estSqft.value) || 2500;
        
        if (estSqftVal) {
            estSqftVal.textContent = `${sqft.toLocaleString()} sq ft`;
        }

        let baseCost = sqft * rate;
        let addonsTotal = 0;

        estAddons.forEach(cb => {
            if (cb.checked) {
                addonsTotal += parseFloat(cb.value) || 0;
            }
        });

        const grandTotal = baseCost + addonsTotal;
        estTotalPrice.textContent = `$${grandTotal.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
    }

    if (estPropType && estSqft) {
        estPropType.addEventListener('change', calculateEstimate);
        estSqft.addEventListener('input', calculateEstimate);
        estAddons.forEach(cb => cb.addEventListener('change', calculateEstimate));
        calculateEstimate();
    }

    console.log("⚡ LuxeCraft Interactive Engine Initialized.");
});
