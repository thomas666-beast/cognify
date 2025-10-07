// Topic form enhancements
document.addEventListener('DOMContentLoaded', function() {
    // Real-time validation for title and description
    const titleInput = document.getElementById('id_title');
    const descriptionInput = document.getElementById('id_description');

    if (titleInput) {
        titleInput.addEventListener('input', function() {
            validateTitle(this);
        });
    }

    if (descriptionInput) {
        descriptionInput.addEventListener('input', function() {
            validateDescription(this);
        });
    }

    // About participant change handler
    const aboutSelect = document.getElementById('id_about');
    if (aboutSelect) {
        aboutSelect.addEventListener('change', function() {
            updateAvailableParticipants(this.value);
        });
    }

    function validateTitle(input) {
        const value = input.value.trim();
        const minLength = 5;

        if (value.length > 0 && value.length < minLength) {
            input.classList.add('is-invalid');
            input.classList.remove('is-valid');
        } else if (value.length >= minLength) {
            input.classList.add('is-valid');
            input.classList.remove('is-invalid');
        } else {
            input.classList.remove('is-valid', 'is-invalid');
        }
    }

    function validateDescription(input) {
        const value = input.value.trim();
        const minLength = 10;

        if (value.length > 0 && value.length < minLength) {
            input.classList.add('is-invalid');
            input.classList.remove('is-valid');
        } else if (value.length >= minLength) {
            input.classList.add('is-valid');
            input.classList.remove('is-invalid');
        } else {
            input.classList.remove('is-valid', 'is-invalid');
        }
    }

    function updateAvailableParticipants(aboutId) {
        // This would typically involve an AJAX call to update available participants
        // For now, we'll just show a message
        if (aboutId) {
            console.log('About participant changed to:', aboutId);
            // In a real implementation, you'd fetch updated participant lists
        }
    }

    // Add visual feedback for selected options
    const studyingSelect = document.querySelector('.studying-participants-select');
    const bossesSelect = document.querySelector('.bosses-select');

    if (studyingSelect) {
        studyingSelect.addEventListener('change', function() {
            updateSelectedCount(this, 'studying');
        });
        updateSelectedCount(studyingSelect, 'studying');
    }

    if (bossesSelect) {
        bossesSelect.addEventListener('change', function() {
            updateSelectedCount(this, 'bosses');
        });
        updateSelectedCount(bossesSelect, 'bosses');
    }

    function updateSelectedCount(selectElement, type) {
        const selectedCount = selectElement.selectedOptions.length;
        const label = document.querySelector(`label[for="${selectElement.id}"]`);

        if (label) {
            // Remove existing count badge
            const existingBadge = label.querySelector('.selected-count-badge');
            if (existingBadge) {
                existingBadge.remove();
            }

            // Add new count badge
            if (selectedCount > 0) {
                const badge = document.createElement('span');
                badge.className = 'selected-count-badge badge bg-primary ms-2';
                badge.textContent = selectedCount;
                label.appendChild(badge);
            }
        }
    }
});

// Silo Diagram Interactions
document.addEventListener('DOMContentLoaded', function() {
    const demoModal = document.getElementById('demoModal');

    if (demoModal) {
        demoModal.addEventListener('show.bs.modal', function() {
            // Add any initialization code for the demo here
            console.log('Demo modal opening');
        });

        // Add click handlers for interactive elements
        const participantAvatars = demoModal.querySelectorAll('.participant-avatar, .boss-avatar');
        participantAvatars.forEach(avatar => {
            avatar.addEventListener('click', function() {
                this.style.transform = 'scale(1.2)';
                setTimeout(() => {
                    this.style.transform = 'scale(1)';
                }, 300);
            });
        });

        // Add hover effects for cards
        const levelCards = demoModal.querySelectorAll('.level-card');
        levelCards.forEach(card => {
            card.addEventListener('mouseenter', function() {
                this.style.zIndex = '10';
            });

            card.addEventListener('mouseleave', function() {
                this.style.zIndex = '1';
            });
        });
    }

    // Print functionality enhancement
    const printButton = document.querySelector('button[onclick="window.print()"]');
    if (printButton) {
        printButton.addEventListener('click', function() {
            // Add any pre-print modifications here
            setTimeout(() => {
                alert('For best printing results, use landscape orientation and check "Background graphics" in print settings.');
            }, 100);
        });
    }
});
