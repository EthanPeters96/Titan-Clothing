// Auto-hiding footer functionality
$(document).ready(function () {
    const footer = $("footer");

    // Try to make the pseudo-element clickable
    $(document).on("click", function (e) {
        // Check if click is in the footer tab area
        const footerTop = footer.offset().top;
        if (e.pageY >= footerTop - 36 && e.pageY <= footerTop) {
            footer.toggleClass("active");
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

    // Allow clicking anywhere on the footer to toggle it
    footer.on("click", function (e) {
        // Only toggle if clicking directly on the footer background
        if ($(e.target).is(footer) || $(e.target).is("footer > .container")) {
            footer.toggleClass("active");
        }
    });

    // Initialize from localStorage
    if (localStorage.getItem("footerOpen") === "true") {
        footer.addClass("active");
    }

    // Save state to localStorage
    footer.on("transitionend", function () {
        localStorage.setItem("footerOpen", footer.hasClass("active"));
    });
});
