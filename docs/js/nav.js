function hamburgerNav() {
    // Get the navigation list from the page
    let nav_list = document.getElementById('nav-list');
    // Get the hamburger from the page (to change the shape)
    let hamburger = document.getElementById('hamburger');

    // Add or remove the active class from the navigation list
    if (nav_list.classList.contains('active')) {
        nav_list.classList.remove('active');
    } else {
        nav_list.classList.add('active');
    }
    // Add or remove the active class from the hamburger
    if (hamburger.classList.contains('active')) {
        hamburger.classList.remove('active');
    } else {
        hamburger.classList.add('active');
    }
}