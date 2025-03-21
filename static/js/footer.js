// Auto-hiding footer functionality
$(document).ready(function () {
    const footer = $("footer");

    // Always reset footer state on page load - start with footer hidden
    footer.removeClass("active");
    localStorage.removeItem("footerOpen");

    // Try to make the pseudo-element clickable
    $(document).on("click", function (e) {
        // Check if click is in the footer tab area
        const footerTop = footer.offset().top;
        if (e.pageY >= footerTop - 36 && e.pageY <= footerTop) {
            footer.toggleClass("active");
        } else if (
            footer.hasClass("active") &&
            !footer.is(e.target) &&
            footer.has(e.target).length === 0
        ) {
            // Close the footer when clicking outside of it (if it's open)
            footer.removeClass("active");
        }
    });

    // Show footer when scrolling to bottom of page
    $(window).scroll(function () {
        if ($(window).scrollTop() + $(window).height() > $(document).height() - 100) {
            footer.addClass("active");
        } else if (!footer.is(":hover")) {
            footer.removeClass("active");
        }
    });

    // Add keyboard support for closing the footer with Escape key
    $(document).on("keydown", function (e) {
        if (e.key === "Escape" && footer.hasClass("active")) {
            footer.removeClass("active");
        }
    });

    // Allow clicking anywhere on the footer to toggle it
    footer.on("click", function (e) {
        // Only toggle if clicking directly on the footer background
        if ($(e.target).is(footer) || $(e.target).is("footer > .container")) {
            footer.toggleClass("active");
        }
    });

    // Add an event listener for page navigation
    $(window).on("beforeunload", function () {
        // Reset footer state before navigating away
        localStorage.removeItem("footerOpen");
    });
});
