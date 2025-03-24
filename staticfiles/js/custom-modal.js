// Custom confirmation modal functionality
document.addEventListener("DOMContentLoaded", function () {
    // Create modal HTML structure and add to body
    const modalHtml = `
        <div class="custom-confirm-modal" id="deleteConfirmModal" style="display: none;">
            <div class="custom-confirm-backdrop"></div>
            <div class="custom-confirm-dialog">
                <div class="custom-confirm-content">
                    <div class="custom-confirm-header">
                        <h5 class="custom-confirm-title">Confirm Deletion</h5>
                        <button type="button" class="close custom-confirm-close" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                    <div class="custom-confirm-body">
                        <p id="deleteConfirmMessage">Are you sure you want to delete this item?</p>
                    </div>
                    <div class="custom-confirm-footer">
                        <button type="button" class="btn btn-outline-black" id="cancelDeleteBtn">Cancel</button>
                        <button type="button" class="btn btn-danger" id="confirmDeleteBtn">Delete</button>
                    </div>
                </div>
            </div>
        </div>
    `;
    document.body.insertAdjacentHTML("beforeend", modalHtml);

    // Get modal elements
    const modal = document.getElementById("deleteConfirmModal");
    const cancelBtn = document.getElementById("cancelDeleteBtn");
    const confirmBtn = document.getElementById("confirmDeleteBtn");
    const closeBtn = document.querySelector(".custom-confirm-close");
    const backdrop = document.querySelector(".custom-confirm-backdrop");

    // Add event listeners to close modal
    cancelBtn.addEventListener("click", closeModal);
    closeBtn.addEventListener("click", closeModal);
    backdrop.addEventListener("click", closeModal);

    // Function to open modal
    window.openDeleteConfirmModal = function (message, confirmCallback) {
        document.getElementById("deleteConfirmMessage").textContent =
            message || "Are you sure you want to delete this item?";
        modal.style.display = "block";
        document.body.classList.add("modal-open");

        // Store the confirm callback
        confirmBtn.onclick = function () {
            closeModal();
            if (typeof confirmCallback === "function") {
                confirmCallback();
            }
        };
    };

    // Function to close modal
    function closeModal() {
        modal.style.display = "none";
        document.body.classList.remove("modal-open");
    }

    // Update all delete buttons to use our custom modal
    document.querySelectorAll('a[onclick*="confirm(\'Are you sure"]').forEach(function (btn) {
        const href = btn.getAttribute("href");
        const originalOnClick = btn.getAttribute("onclick");

        // Extract the confirmation message
        let message = "Are you sure you want to delete this item?";
        if (originalOnClick) {
            const match = originalOnClick.match(/confirm\('([^']+)'\)/);
            if (match && match[1]) {
                message = match[1];
            }
        }

        // Replace the onclick handler
        btn.removeAttribute("onclick");
        btn.addEventListener("click", function (e) {
            e.preventDefault();
            openDeleteConfirmModal(message, function () {
                window.location.href = href;
            });
        });
    });
});
