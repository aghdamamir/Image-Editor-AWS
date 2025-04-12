document.addEventListener('DOMContentLoaded', function() {
    // Image preview functionality with enhanced animation
    const imageInput = document.getElementById('id_image');
    const imagePreview = document.getElementById('imagePreview');
    const imagePreviewContainer = document.getElementById('imagePreviewContainer');
    
    if (imageInput) {
        imageInput.addEventListener('change', function(e) {
            if (e.target.files && e.target.files[0]) {
                const reader = new FileReader();
                
                reader.onload = function(event) {
                    // Remove previous animation classes
                    imagePreviewContainer.classList.remove('d-none', 'fadeIn', 'fadeInUp');
                    
                    // Set source and add animation
                    imagePreview.src = event.target.result;
                    
                    // Add classes after a small delay to ensure transition
                    setTimeout(() => {
                        imagePreviewContainer.classList.add('fadeInUp');
                        imagePreviewContainer.style.display = 'block';
                    }, 50);
                }
                
                reader.readAsDataURL(e.target.files[0]);
            } else {
                imagePreviewContainer.classList.add('d-none');
            }
        });
    }
    
    // Filter selection with improved interaction
    const filterInputs = document.querySelectorAll('.filter-option input[type="radio"]');
    
    filterInputs.forEach(input => {
        // Initial setup - apply selected class to the checked input
        if (input.checked) {
            const label = input.nextElementSibling;
            label.classList.add('selected');
        }
        
        input.addEventListener('change', function() {
            // Update UI for all options
            filterInputs.forEach(inp => {
                const label = inp.nextElementSibling;
                
                if (inp.checked) {
                    // Smoothly add the selected class
                    label.classList.add('selected');
                    
                    // Create ripple effect
                    const icon = label.querySelector('.filter-icon');
                    icon.style.animation = 'none';
                    setTimeout(() => {
                        icon.style.animation = 'pulse 0.5s';
                    }, 10);
                } else {
                    // Remove the selected class
                    label.classList.remove('selected');
                }
            });
        });
    });
    
    // Interactive hover effects for filter options
    const filterOptions = document.querySelectorAll('.filter-option label');
    filterOptions.forEach(option => {
        option.addEventListener('mouseenter', function() {
            if (!this.classList.contains('selected')) {
                this.style.transform = 'translateY(-5px)';
                this.style.boxShadow = 'var(--shadow-md)';
            }
        });
        
        option.addEventListener('mouseleave', function() {
            if (!this.classList.contains('selected')) {
                this.style.transform = '';
                this.style.boxShadow = '';
            }
        });
    });
    
    // Form validation with improved feedback
    const form = document.getElementById('uploadForm');
    if (form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
                
                // Highlight invalid fields with animation
                const invalidFields = form.querySelectorAll(':invalid');
                invalidFields.forEach(field => {
                    field.classList.add('shake');
                    setTimeout(() => {
                        field.classList.remove('shake');
                    }, 600);
                });
            } else {
                // Add loading state when form is valid
                const submitBtn = form.querySelector('button[type="submit"]');
                if (submitBtn) {
                    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
                    submitBtn.disabled = true;
                }
            }
            
            form.classList.add('was-validated');
        });
    }
    
    // Add loading animation
    document.querySelectorAll('.btn').forEach(btn => {
        btn.addEventListener('click', function() {
            // Create ripple effect on button click
            const ripple = document.createElement('span');
            ripple.classList.add('ripple-effect');
            
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            
            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = (event.clientX - rect.left - size/2) + 'px';
            ripple.style.top = (event.clientY - rect.top - size/2) + 'px';
            
            this.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });
    
    // Add soft scroll animation for page loads
    document.body.classList.add('fade-in');
    
    // Add animation to card on page load
    document.querySelectorAll('.card').forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            card.style.opacity = '1';
            card.style.transform = '';
        }, 100 + (index * 100));
    });
});

// Add CSS for new animations
const style = document.createElement('style');
style.textContent = `
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        20%, 60% { transform: translateX(-5px); }
        40%, 80% { transform: translateX(5px); }
    }
    
    .shake {
        animation: shake 0.6s ease-in-out;
    }
    
    .ripple-effect {
        position: absolute;
        border-radius: 50%;
        background-color: rgba(255, 255, 255, 0.3);
        transform: scale(0);
        animation: ripple-animation 0.6s linear;
        pointer-events: none;
    }
    
    @keyframes ripple-animation {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
    
    .fade-in {
        animation: fade-in 0.5s ease-out;
    }
    
    @keyframes fade-in {
        from { opacity: 0; }
        to { opacity: 1; }
    }
`;
document.head.appendChild(style);
